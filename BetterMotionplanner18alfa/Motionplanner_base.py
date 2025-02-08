import pyglet
import math
import json
import random
import sys
from Renderer import Renderer
from pyglet.window import key, mouse
from MotionplannerAstar import Astar
from MotionplannerMath import createVector
from MotionplannerPointAndLine import inObstacle, neighbor2, whichSquare, neighbors

class MotionPlanner(pyglet.window.Window):
    #Rörelseplanneraren har tidskomplexiteten O(nm), oavsett om man trycker för att lägga till en ny punkt eller inte.
    #Koden för att slumpa alla punkter så att de inte hamnar inuti något hinder är O(nm). Koden för att lägga till alla linjesegment är O(nm). A-star är O(nm).
    #Om dessa delar vore inuti varandras for-loopar (alltså att det är en for loop inuti en for loop inuti en for loop...) då skulle tidskomplexiteten vara O((nm)^3).
    #I detta fall är dock tidskomplexiteten O(3nm), och då det bara är nm som kvittar för väldigt stora n-värden (nm är den dominanta faktorn) så är tidskomplexiteten för hela rörelseplanneraren egentligen O(nm).

    #Setup-delen av rörelseplanneraren har tidskomplexiteten O(h) där h står för alla hinder i "obstacles1.json"-filen.
    def __init__(self):
        #Öppnar json-filen
        with open('obstacles1.json') as json_file:
            data = json.load(json_file) #Laddar in json-filen. "data" blir då till en hierarchy då inladdade json-filer blir till hierarchys.
            #width och height bestämmer bredden och höjden på fönstret som "renderer"-objektet ska rita på.
            #width och height tar från värdena från json-filen (som nu är en hierarchy) genom att ta värdet från nyckeln "width" som är en del av värdet av nyckeln "setup".
            width = data["setup"]["width"] #data["setup"]["width"] ger alltid värdet 800
            height = data["setup"]["height"] 
            super(MotionPlanner, self).__init__(height=height, width=width, resizable=True) #Super skapar konstruktorn för parent:en.
            self.renderer = Renderer(width, height) #skapar mitt renderer-objekt
            self.set_minimum_size(100, 100)
            self.K = data["setup"]["K"]  #K bestämmer antalet närmsta grannar man ska koppla ihop (varje punkt ska koppla till de 5 närmsta punkterna)
            self.num_samples = data["setup"]["numSamples"] #numsamples är hur många gånger man ska slumpa punkter/hur många punkter som finns totalt i 2D-planet.
            self.obstacleList = [] #Skapar en lista med all nödvändig information för varje hinder.

            #O(h) där h är antalet hinder i "obstacles1.json"
            #När json-filen läses in görs json-filen om till en dictionary. 
            #När man skriver "data["obstacles"].keys()" refererar man till alla hinder i "obstacles" i json-filen, och "i" refererar då i detta fall först till det första hindret, sedan till nästa hinder, sedan till nästa hinder....
            for i in data["obstacles"].keys():
                obstacle = data["obstacles"][i] #"obstacle" tar sig an datan för först det första hindret, sedan nästa hinder, sedan nästa... "obstacle" beror av "i".
                #Om hindrets typ är "Circle", då bara läggs hindret in i renderer och obstacleList. Om hindrets typ är "Triangle", då skapas först triangelns 3 sidor innan man kan lägga in den i obstacleList.
                if obstacle["type"] == "Circle":
                    self.renderer.add_render_object("Circle", [obstacle["center"], obstacle["radius"]], obstacle["id"], [0.5, 0.5, 0.5])
                    self.obstacleList.append(("Circle", obstacle["center"][0], obstacle["center"][1], obstacle["radius"]))
                elif obstacle["type"] == "Triangle":
                    self.renderer.add_render_object("Triangle", obstacle["vertices"], obstacle["id"], [0.5, 0.5, 0.5])
                    side1 = createVector(obstacle["vertices"][0], obstacle["vertices"][1]) #gör en vektor mellan punkt 1 och punkt 2 i triangeln
                    side2 = createVector(obstacle["vertices"][1], obstacle["vertices"][2]) #gör en vektor mellan punkt 2 och punkt 3 i triangeln
                    side3 = createVector(obstacle["vertices"][2], obstacle["vertices"][0]) #gör en vektor mellan punkt 3 och punkt 1 i triangeln
                    self.obstacleList.append(("Triangle", side1, side2, side3, obstacle["vertices"][0], obstacle["vertices"][1], obstacle["vertices"][2]))


        #    PUNKTER
        self.pointList = [] #Skapar en tom lista där alla punkter som har placerats ut på talplanet ligger (alltså inte de som skulle vara i kollision med ett hinder).
        self.squareDict = {} #Skapar en dictionary som ska innehålla vilka punkter som ligger i vilken ruta. 
        numColumns = 100#int(input("How many columns should the grid have?"))
        numRows = 100#int(input("How many rows should the grid have?"))
        for i in range(numColumns*numRows):
            self.squareDict[i] = []

        #O(z) där z är lika med vad som än numSamples har som värde. Man kan säga att loopen har tidskomplexiteten O(1) då värdet på numSamples aldrig ändras om man inte manuellt ändrar det i koden, men då vissa värden på numSamples gör att algoritmen inte alls fungerar så kan man ändå säga att loopen har tidskomplexiteten O(p).
        for z in range(self.num_samples):
            #Slumpar ett x- och y-värde för en punkt. 
            x = random.randint(0, width)
            y = random.randint(0, height)
            #Ser om den slumpade punkten ligger inuti något objekt.
            #O(m) då inObstacle-funktionen är O(m) m står för alla objekt i obstacleList.
            if (inObstacle((x,y), self.obstacleList) == False):
                self.pointList.append((x,y))
                square = whichSquare((x,y), width, height, numColumns, numRows) #square är en variabel som säger vilken ruta en punkt ska vara i. Om man vill ha ett rutnät som är 4x4 stort då kommer den första rutan att heta "0" och den sista rutan kommer heta "15". I det fallet skulle då square kunna vara ett heltal mellan 0 och 15.
                self.squareDict[square].append(len(self.pointList)-1) #Här delas alltså alla punkter in i varsin ruta i rutnätet. Punktens index i pointList sparas.

        self.renderer.add_render_object("Point", self.pointList, "point1", [0, 0, 0])
        self.lineSegmentDict, verticesList = neighbors(self.pointList, self.obstacleList, self.squareDict, width, height, numColumns, numRows) #"neighbors"-funktionen har ordo-notationen O(np) där n står för mängden punkter i pointList och p står för mängden punkter i en ruta.
        self.renderer.add_render_object("Line", verticesList, "lineSegment1", [0,191,255])

    def on_draw(self): 
        self.renderer.draw()

    def on_mouse_press(self, x, y, button, modifiers): #O(ng) där n står för alla punkter i pointList och g står för en punkts alla grannar.
        #O(ng) där n står för alla punkter i pointList och g står för en punkts alla grannar (brukar vara mellan 4 till 6 grannar).
        if button == mouse.LEFT:
            #Punkten ritas ut och läggs till i pointlist.
            point = (x,y) #Den punkt som just skapades
            if inObstacle(point, self.obstacleList) == False: #Punkten får inte placeras inuti ett hinder.
                self.pointList.append(point)
                self.renderer.add_render_object("Point", [point], "point", [0, 0, 0])

                #Härnäst hittas punktens 5 närmsta grannar, som då läggs till i verticesList så att man kan rita ut grannarna.
                verticesList = [] #En lista som används för att renderaren ska kunna rita ut alla linjer
                pointIndex = len(self.pointList)-1
                nearestNeighbors = neighbor2(pointIndex, self.pointList, self.obstacleList) #neighbor2-funktionen är O(n)
                for i in range(len(nearestNeighbors)): #O(g) där g är antalet grannar till punkten 'point'.
                    self.lineSegmentDict[nearestNeighbors[i]].append(pointIndex) #När jag lägger till en ny punkt så känner bara den punkten till alla sina grannar. Punktens grannar vet dock inte att den nya punkten finns, vilket gör att det är helt och håller omöjligt att komma till den punkten från någon annan punkt.
                    verticesList.append(self.pointList[pointIndex]) #Just nu är den nya punkten den allra sista punkten i pointList. Punkten och de punkter som har blivit dess grannar läggs till i verticesList så att linjerna kan ritas ut.
                    verticesList.append(self.pointList[nearestNeighbors[i]])
                self.lineSegmentDict[pointIndex] = nearestNeighbors #Nu läggs det till en ny nyckel i lineSegmentDict dictionaryn, där nyckeln är indexet av den nuvarande punkten och att värdet är en lista på den nuvarande punktens 5 närmsta punkter
                self.renderer.add_render_object("Line", verticesList, ("lineSegment" + str(pointIndex-1)), [0,191,255])
            else: #Specialfall: Om punkten man försöker sätta ut ligger inuti ett hinder, då läggs inte punkten ner.
                print("Point is in an obstacle")
        

    def on_key_press(self, symbol, modifiers): #O(nm) där n står för alla punkter A*-algoritmen går igenom och m står för alla punkter n's närmsta grannar
        if symbol == key.SPACE:
            start = len(self.pointList)-2 #Startpunkten för Astar
            goal = len(self.pointList)-1 #Slutpunkten för Astar
            Astar(start, goal, self.pointList, self.lineSegmentDict, self.renderer) #O(ng) där n står för alla punkter algoritmen går igenom och g står för alla punkter n's närmsta grannar

if __name__ == "__main__":
    app = MotionPlanner()
    pyglet.app.run()