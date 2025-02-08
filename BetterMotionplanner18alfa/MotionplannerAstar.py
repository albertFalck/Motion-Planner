from MotionplannerMath import distanceBetweenPoints

def Astar(start, goal, pointList, neighborDict, renderer): #Tar fram den kortaste vägen från en punkt till en annan och ritar sedan ut det. O(ng) där n står för alla punkter algoritmen går igenom och g står för alla punkter n's närmsta grannar
        #Funktionens fullständiga tidskomplexitet är O(ng + v) där n står för alla punkter algoritmen går igenom, g står för alla punkter n's närmsta grannar och v står för alla punkter som man åker till på vägen från startpunkten till målet. Då v inte betyder mycket för stora värden på n, g och v kan man säga att funktionens tidskomplexitet är O(ng). 
        #Koden går först igenom alla punkter och går sedan igenom alla linjesegment som kanske kan leda till en väg till målet, och när man har nått målet körs "pathToGoal"-funktionen en gång.

        foundNodes = [start] #I början vet vi bara start-noden
        cameFrom = {} #En dictionary där varje nyckel är alla punkter som algoritmen går igenom och värdet av varje nyckel är den punkt man var på precis innan man kom till punkten som är nyckeln (t.ex {punkt A: punkt B} betyder att algoritmen kom till punkt A från punkt B)
        current = start #Den nod algoritmen är på just nu
        gScore = {start: 0} #gScore är ett värde som säger hur långt man har färdats hittills sammanlagt. T.ex kanske man är på punkt A och man ska till punkt B och sedan punkt C. Om det är ett avstånd på 4 mellan punkt A och punkt B och sedan ett avstånd på 5 mellan punkt B och punkt C kommer man att ha en gScore på 9 för att komma till punkt C från punkt A om man tar den vägen.
        fScore = {start: distanceBetweenPoints(pointList[start], pointList[goal])} #fScore är bara gScore fast att man lägger till hur långt det är från den punkt man är på till den punkt man i slutändan vill nå (goal). Startpunktens g-score är 0. Därför är startpunktens f-score lika med 0 + längden från startpunkten till slutpunkten.
        
        #O(n) där n står för alla noder man går igenom fram tills att
        while foundNodes: #Om vi har någon nod i foundNodes, då kör koden på.
            current = min(fScore, key=fScore.get) #Tar fram nyckeln för noden med lägst f-score

            if current == goal: #Om den nuvarande noden är målpunkten, då avslutas funktionen.
                goalPath = pathToGoal(cameFrom, current, pointList) #Funktionen "pathToGoal" är O(v) där v är alla punkter som man åker till på vägen från startpunkten till målet
                if "pathLine" in renderer.render_objects: #Om det redan ritats ut en väg från en punkt till en annan i programmet då tas först den vägen bort, så att man sedan kan rita ut vägen från den nuvarande startpunkten till det nuvarande målet.
                    renderer.remove_render_object("pathLine")
                renderer.add_render_object("Line", goalPath, "pathLine", [255,0,0])
                return

            foundNodes.remove(current) #Den nuvarande noden behövs inte längre i foundNodes
            del fScore[current] #Vi behöver inte denna fScore längre.

            for nearest in neighborDict[current]: #Går igen den nuvarande punktens alla grannar. O(g) egentligen då en punkt ibland har 4 grannar, ibland 3 grannar, ibland 5 grannar etc.
                new_gScore = gScore[current] + distanceBetweenPoints(pointList[current], pointList[nearest]) #Skapar ett nytt g-score från den nuvarande punkten till alla de andra grannarna.
                if (nearest not in gScore.keys()) or (new_gScore < gScore[nearest]): #Om grannen antingen inte finns i gScore ännu eller om grannens förra g-score var större än nu, då läggs grannen till i gScore eller så ändras dess g-score och f-score värde.
                    cameFrom[nearest] = current
                    gScore[nearest] = new_gScore
                    fScore[nearest] = (new_gScore + distanceBetweenPoints(pointList[nearest], pointList[goal]))
                    if nearest not in foundNodes: #Om grannen inte finns med i foundNodes, då läggs den till.
                        foundNodes.append(nearest)
        print("failed")
        return

def pathToGoal(cameFrom, currentNode, pointList): #Tar fram vägen från startpunkten till målet (är en del av Astar-algoritmen). O(v) där v är alla punkter som man åker till på vägen från startpunkten till målet
    #Loopen börjar vid målet. cameFrom är en dictionary där varje nod som man har rest till finns med som en nyckel, där nyckelns värde är den nod som man reste från. 
    #Loopen går sedan till den nod som man reste till innan målet. Och sedan noden innan den. Och sedan noden innan den, tills man kommer till startpunkten. 
    #Då startpunkten inte har någon nod innan den finns startpunkten inte med som en nyckel i cameFrom och loopen avslutas. 
    #Så även om programmet, säg, först åkte från punkt A till punkt B till punkt C men sedan såg att punkt B har en mindre fScore än alla punkt Cs grannar och att programmet istället går från punkt B till punkt F, då kommer inte nod C vara med i path. 
    #Nod C är inte med i path då den nod som kom innan nod F är ju nod B, och den nod som kom innan nod B är nod A. Nod C är inte med.
        path = [] #En tom lista som ska innehålla alla punkter man åker till på vägen från målet till startpunkten (och därmed vägen från startpunkten till målet)
        while currentNode in cameFrom.keys(): 
            path.append(pointList[currentNode])
            currentNode = cameFrom[currentNode]
            path.append(pointList[currentNode])
        return path