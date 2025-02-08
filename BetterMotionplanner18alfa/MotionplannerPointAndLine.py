from MotionplannerMath import createVector, createNormalVector, distanceBetweenPoints, scalar, createProjection
import math

def inObstacle(point, obstacleList): #Säger om en punkt ligger inuti någon av hindrena i "obstacleList". O(h) där h står för alla hinder i obstacleList
        inObstacle = False #En bool-variabel som säger om punkten ligger inuti ett hinder eller inte.
        #O(h) där h står för alla hinder i obstacleList
        for i in range(len(obstacleList)):
                if (obstacleList[i][0] == "Circle"): #Om hindret är av typen "Circle"
                    circleMiddle = (obstacleList[i][1], obstacleList[i][2]) #Koordinaterna för mittpunkten av cirkeln.
                    distance = distanceBetweenPoints(circleMiddle, point) #Avståndet från punkten man angav till cirkelns mittpunkt.
                    if distance > obstacleList[i][3]: #Om avståndet är större än cirkelns radie, då ligger inte punkten inuti cirkeln. Annars ligger punkten inuti cirkeln.
                        inObstacle = False
                    else:
                        inObstacle = True
                        break

                elif(obstacleList[i][0] == "Triangle"):
                    count = 1   #Används för for-loopen. 
                    inObstacle = True
                    #O(1) då loopen körs samma antal gånger varje gång
                    while count <= 3:
                        normalVector = createNormalVector(obstacleList[i][count])  #Skapar en normalvektor till varje sida, en efter en. I första loopen får den första sidan en normalvektor, i andra loopen får den andra sidan en normalvektor etc...
                        vector = createVector(obstacleList[i][3+count], point)  #Varje sida i triangeln har en startpunkt och en slutpunkt. Här skapas en vektor mellan den nuvarande sidans startpunkt och punkten som antingen är innanför eller utanför triangeln. 
                        dotProduct = scalar(normalVector, vector) #Använder skalärprodukten mellan normalvektorn och den nya vektorn vi tog fram. Om skalärprodukten är negativ, då är vinkeln mellan normalvektorn och den nya vektorn högre än 90 grader. Om den är positiv, då är vinkeln mindre än 90 grader.
                        
                        if (dotProduct < 0): #Om skalärprodukten bara en enda gång är negativ, då vet vi att punkten ligger utanför triangeln. Därför stannas loopen och vi går över till nästa hinder/nästa punkt.
                            inObstacle = False
                            break
                        count = count+1
                    #obstacleList[i][1 till 3] är triangeln sidor.
        return inObstacle

def inObstacleLine(point1, point2, obstacleList): #Säger om en linje korsar/kolliderar med någon av hindrena i "obstacleList". O(h) där h står för alla hinder i obstacleList
        lineIsColliding = False #Ett bool-värde som säger om en linje kolliderar med ett hinder eller inte
        shortList = [point1, point2] #En kort lista som används bara för senare i koden (rad 55 och neråt) för att spara på plats i koden.
        vectorLineSegment = createVector(point1, point2) #skapar en vektor mellan den nuvarande punkten och den närmsta punkten man ser på nu.

        #O(h) där h står för alla hinder i obstacleList.
        for obstacleNum in range(len(obstacleList)): #Tittar igenom alla hinder.
            if (obstacleList[obstacleNum][0] == "Circle"):
                #Två vektorer skapas: normalVector1 går från linjesegmentets första punkt till linjesegmentets andra punkt, och normalVector2 går istället från den andra punkten till den första punkten.
                #Dessa vektorer ska agera som normalvektorer, så att man kan avgränsa en region där man kan bestämma om man borde använda en ortogonal projektionsvektor eller om man bara kan dra en vektor från en av linjesegmentets punkter till alla cirklarnas mittpunkter.

                normalVector1 = vectorLineSegment #Går från linjesegmentets första punkt till linjesegmentets andra punkt
                normalVector2 = createVector(point2, point1) #Går från linjesegmentets andra punkten till linjesegmentets första punkt."
                shortList2 = [normalVector1, normalVector2] #En kort lista som används vara för sneare i koden (rad 55 och neråt) för att spara på plats i koden.
                circleRadius = (obstacleList[obstacleNum][1], obstacleList[obstacleNum][2]) #Radien på cirkeln man ser på just nu
                inRegion = True #En bool som säger om cirkelns mittpunkt är innanför eller utanför regionen.

                for x in range(2): #O(1) då loopen alltid bara körs igenom 2 gånger
                    vectorToCircle = createVector(shortList[x], circleRadius)
                    dotProduct = scalar(shortList2[x], vectorToCircle)

                    
                    
                    if dotProduct <= 0: #Bara om dotProduct blir positiv för båda normalvektorer vet vi att cirkeln ligger inuti regionen. EXTRA KOMMENTAR: Om en punkt kunde vara inne i cirkeln, då skulle jag se om avståndet från linjesegmentets punkter skulle kunna vara mindre än radien av cirkeln (då korsar linjesegmentet cirkeln) (if dotProduct < 0: if vectorToCircle > obstacleList[obstacleNum][3]: lineIsColliding = True --> break)
                        lineIsColliding = False
                        inRegion = False
                        break

                #Om cirkelns mittpunkt ligger inom regionen, då projicerar man vektorn som går till cirkeln på linjesegmentets vektor: Detta ger den punkt på linjesegmentet som ger det minsta avståndet från linjesegmentet till cirkeln.
                #För att sedan få fram den allra minsta möjliga vektorn från cirkelns mittpunkt till linjesegmentet, då kan man subtrahera vectorToCircle med vectorProjection. Efter det kan man ta fram längden på den vektorn och sedan se om vektorn är mer eller mindre än cirkelns radie.
                if inRegion == True:
                    vectorProjection = createProjection(vectorToCircle, normalVector2)
                    shortestVector = [(vectorToCircle[0] - vectorProjection[0]), (vectorToCircle[1] - vectorProjection[1])] #Representerar det kortaste avståndet från linjen till cirkelns mittpunkt.
                    shortestVectorLength = distanceBetweenPoints([0,0], shortestVector)
                    if shortestVectorLength < obstacleList[obstacleNum][3]:
                        lineIsColliding = True
                        break

            elif (obstacleList[obstacleNum][0] == "Triangle"):
                #1. Kolla linjesegmentets normalvektor med triangelns punkter (är triangelns punkter på samma sida av linjesegmentet? Om de är, då kan inte linjesegmentet inte korsa triangeln. Om de inte är det, kolla kondition 2)
                normalVector = createNormalVector(vectorLineSegment) #Skapar normalvektor till den nya vektorn.
                count = 0
                #O(1) då loopen alltid körs 3 gånger
                for trianglePointNum in range(3): #Går igenom triangelns 3 punkter
                    vectorTrianglePoint = createVector(point1, obstacleList[obstacleNum][4+trianglePointNum]) #Skapar en vektor mellan den nuvarande punktens närmsta punkt och en av triangelns punkter.
                    dotProduct = scalar(normalVector, vectorTrianglePoint)

                    #Om skalärprodukten mellan linjesegmentets normalvektor och vektorn mellan den närmsta punkten och en av triangelns punkter är positiv, då tar man +1 på "count". Annars tar man -1 på "count". Detta är för att....
                    if (dotProduct > 0):
                        count = count+1
                    elif (dotProduct < 0):
                        count = count-1
                        
                #.... Om "count" är 3 eller -3, då är alla triangelns punkter åt en sida av linjesegmentet då dotproduct har varit antingen positiv för alla triangelns punkter eller negativ för alla triangelns punkter.
                if (count == 3 or count == -3):
                    #Linjesegmentet korsar inte triangeln. Programmet går vidare, då "lineIsColliding" redan är False
                    pass
                            
                else:
                    #2. Jämför triangelns sidors normalvektorer med linjesegmentets punkter. Om linjesegmentets punkter har samma skalärprodukter med triangelns sidor, då kan inte linjesegmentet korsa triangeln. Annars korsar linjesegmentet triangeln.
                    #Nu jämför programmet linjesegmentets två punkter med alla triangelns punkter för att se om linjesegmentets två punkter har samma skalärprodukt (linjen korsar ej triangeln) eller om punkterna har olika skalärprodukter (linjen korsar triangeln)
                    #O(1) då loopen alltid körs 3 gånger
                    for pointCompare in range(3):
                        normalVector = createNormalVector(obstacleList[obstacleNum][1+pointCompare])
                        vectorPoint1 = createVector(obstacleList[obstacleNum][4+pointCompare], point1)  
                        vectorPoint2 = createVector(obstacleList[obstacleNum][4+pointCompare], point2)
                        dotProductPoint1 = scalar(normalVector, vectorPoint1)
                        dotProductPoint2 = scalar(normalVector, vectorPoint2)
                        if (dotProductPoint1 < 0 and dotProductPoint2 > 0) or (dotProductPoint1 > 0 and dotProductPoint2 < 0):
                            lineIsColliding = True
                            break
        return lineIsColliding

def neighbor2(point, pointList, obstacleList): #Tar fram en punkts (som max 5) närmsta grannar och ser till att det inte bildas någon koppling som korsar ett hinder. Tidskomplexitet av O(n + h) där n står för alla punkter i pointList och h står för alla hinder i "obstacleList".
        distanceList = [] #En tom lista som sedan ska innehålla avståndet från en punkt till alla andra punkter
        #O(n) där n står för alla punkter i pointList
        for i in range(len(pointList)): #Först läggs alla punkter till i distanceList.
            currentDistance = distanceBetweenPoints(pointList[point], pointList[i]) #Ser avståndet mellan den nuvarande punkten och alla andra punkter. Funktionen "distanceBetweenPoints" har tidskomplexiteten O(1).
                    
            if (currentDistance != 0): #Om det nuvarande avståndet är lika med 0, då jämför ju punkten bara med sig själv.
                distanceList.append((currentDistance, i)) #Lägger till en tuple i distanceList som ger indexet på den punkten som jämförs och avståndet mellan den nuvarande punkten och punkten som jämförs.

        distanceList.sort() #Sedan sorteras distanceList så att de närmsta punkterna hamnar längst fram. En möjlig förbättring är ju att göra så att bara de 5 närmsta punkterna hamnar längst fram istället för att sortera hela pointList

        nearestPoints = [] #En tom lista som sedan ska innehålla en punkts som max 5 närmsta grannar.
        for i in range(5): #Ser om de 5 närmsta punkterna kan läggas till som linjesegment i lineSegmentDict. O(1) då loopen alltid körs igenom 5 gånger
            neighbor = distanceList[i][1] #Tar fram indexet i pointlist för de 5 närmsta punkterna
            if (inObstacleLine(pointList[point], pointList[neighbor], obstacleList) == False): #Om linjen inte kolliderar med något hinder, då läggs linjesegmentet till. Funktionen "inObstacleLine" har tidskomplexiteten O(h).
                nearestPoints.append(neighbor) #Lägger till indexet av de 5 närmsta punkterna i listan "nearestPoints"
        return nearestPoints

def neighbors(pointList, obstacleList, squareDict, widthOfWindow, heightOfWindow, numColumns, numRows): #Komplexiteten för steg 1 och steg 2 blir tillsammans O(np + rp) där n står för antalet punkter i pointList, p står för antalet punkter i en ruta och r står för antalet rutor i rutfältet.
                                                                                                        #Då antalet rutor 'r' är helt separat från både antalet punkter i pointlist 'n' och antalet punkter i en ruta 'p' så finns det vissa fall då värdet på rp är större än np och tvärtemot.
                                                                                                        #Oftast är dock antalet punkter 'n' i pointList större än antalet rutor 'r' i rutfältet, då det inte finns så mycket poäng i att ha till exempel 90 punkter i ett 10x10 rutfält. Därför är, allra oftast, np den dominanta faktorn.
                                                                                                        #Den slutgiltiga komplexiteten för den förbättrade "neighbors"-algoritmen är alltså O(np). Om det finns fler rutor än 1 i hela fönstret är alltså denna algoritm snabbare än den förra "närmsta granne"-algoritmen, som är O(n^2).
    

    #Steg 1. Den fulla komplexiteten för steg 1 är O(np + ngh + ng^2 + ng^2) där n står för alla punkter i pointList, p står för mängden punkter i en ruta, g står för mängden närmsta grannar till punkten 'p' och h står för alla hinder i obstacleList.
    #Antalet hinder 'h' i obstacleList, om man inte manuellt lägger till eller tar bort hinder i koden, är 3. Antalet närmsta grannar till en punkt brukar vara 5 men kan vara mellan mellan 7 och 0 eller högre i vissa fall. Antalet punkter i en ruta brukar variera väldigt stort för varje ruta, men om n är 1500 och det är ett 4x4 rutnät, då vore p i genomsnitt lika med 94.
    #I komplexitetsanalyser bortser man från konstanter, vilket betyder att man inte har med 2ng^2 utan bara ng^2. Då p beror väldigt mycket på n medans g inte beror lika mycket på n (om n = 1500 i ett 4x4 rutnät så skulle p vara i genomsnitt lika med 94, medans g i största sannolikhet vore mellan 7 och 0 även om n vore 500 eller 10000) betyder det att np är större än ng^2 för stora värden på n. np är alltså den dominanta faktorn.
    #Den slutgiltiga komplexiteten för steg 1 blir alltså O(np).

    distanceList = [] #En tom lista som sedan ska innehålla avståndet från en punkt till alla andra punkter i samma ruta.
    lineSegmentDict = {} #En dictionary där alla nycklar är indexen för alla punkter i pointList och alla värden är indexen för alla punkter i pointList som är närmsta granne till nyckeln.
    verticesList = [] #Lista som endast är till för att renderaren ska kunna rita ut alla linjer.

    #Alla punkter i pointList jämförs med de andra punkterna i samma ruta som punkten.
    for point in range(len(pointList)): #O(n) där n är alla punkter i pointList. Varje punkt i pointList jämförs med de andra punkterna som är i samma ruta som denna punkt. point är indexet för varje punkter i pointList. 
        square = whichSquare(pointList[point], widthOfWindow, heightOfWindow, numColumns, numRows) #Tar fram vilken ruta denna punkt ligger i.

        for i in squareDict[square]: #O(p) där p är alla punkter i en rutan "square". "i" är alla punkter i samma ruta som "point"
            currentDistance = distanceBetweenPoints(pointList[point], pointList[i]) #Ser avståndet mellan den nuvarande punkten och alla andra punkter. Funktionen "distanceBetweenPoints" har tidskomplexiteten O(1).
                    
            if (currentDistance != 0): #Om det nuvarande avståndet är lika med 0, då jämför ju punkten bara med sig själv.
                distanceList.append((currentDistance, i)) #Lägger till en tuple i distanceList som ger indexet på den punkten som jämförs och avståndet mellan den nuvarande punkten och punkten som jämförs.

        distanceList.sort() #Sedan sorteras distanceList så att de närmsta punkterna hamnar längst fram. En möjlig förbättring är ju att göra så att bara de 5 närmsta punkterna hamnar längst fram istället för att sortera hela pointList

        nearestPoints = [] #En tom lista som sedan ska innehålla en punkts som max 5 närmsta grannar.
        if (len(distanceList) > 4):
            for i in range(5): #Ser om de 5 närmsta punkterna kan läggas till som linjesegment i lineSegmentDict. O(g) där g står för antalet närmsta grannar en punkt har. Är inte O(1) då, om distanceList har färre än 5 index så körs denna loop ett mindre antal gånger.
                neighbor = distanceList[i][1] #Tar fram indexet i pointlist för de 5 närmsta punkterna
                if (inObstacleLine(pointList[point], pointList[neighbor], obstacleList) == False): #Om linjen inte kolliderar med något hinder, då läggs linjesegmentet till. Funktionen "inObstacleLine" har tidskomplexiteten O(h).
                    nearestPoints.append(neighbor) #Lägger till indexet av de 5 närmsta punkterna i listan "nearestPoints"
        else: #Specialfall: Om det inte finns 5 punkter eller mer i rutan, då körs denna kod.
            for i in range(len(distanceList)): #O(g) där g står för antalet närmsta grannar en punkt har. Man går här alltså igenom vilka 5 eller färre punkter som ligger närmast punkten 'p'. 
                neighbor = distanceList[i][1] #Tar fram indexet i pointlist för de 5 närmsta punkterna
                if (inObstacleLine(pointList[point], pointList[neighbor], obstacleList) == False): #Om linjen inte kolliderar med något hinder, då läggs linjesegmentet till. Funktionen "inObstacleLine" har tidskomplexiteten O(h).
                    nearestPoints.append(neighbor) #Lägger till indexet av de 5 närmsta punkterna i listan "nearestPoints"
        distanceList = []

        
        #Punkten och alla dess 5 närmsta grannar läggs först till i verticesList. Sedan läggs punkten till i lineSegmentDict tillsammans med dess närmsta grannar. Till sist läggs punkten till som ett av värdena hos alla grannarna i lineSegmentDict.
        for i in range(len(nearestPoints)): #O(g) där g står för en punkts alla närmsta grannar. Mellan 5 och 0 i detta fall.
            verticesList.append(pointList[point]) #Denna del...
            verticesList.append(pointList[nearestPoints[i]]) #...och denna del är bara för att renderer:n ska kunna rita ut alla linjer.

            #Om punkt A har punkt B som granne så är det inte säkert att punkt B har punkt A som granne. Detta kan göra algoritmen lite konstig.
            if lineSegmentDict.get(nearestPoints[i]) == None: #Om punkt B inte ännu finns i lineSegmentDict, då läggs den till. O(1) då man helt enkelt ser om "lineSegmentDict[point]" ens finns snarare än att kolla igenom alla 'lineSegmentDict's nycklar, så vitt jag vet.
                lineSegmentDict[nearestPoints[i]] = [point]
            elif point not in lineSegmentDict[nearestPoints[i]]: #Om punkt B redan finns men att punkt A inte finns med i punkt Bs grannar, då läggs punkt A till. O(g) där g står för antalet grannar till punkten 'nearestPoint[i]'.
                lineSegmentDict[nearestPoints[i]].append(point)


        if lineSegmentDict.get(point) == None: #Om point inte finns med i lineSegmentDict, då läggs point till. O(1) då man helt enkelt ser om "lineSegmentDict[point]" ens finns snarare än att kolla igenom alla 'lineSegmentDict's nycklar, så vitt jag vet.
            lineSegmentDict[point] = nearestPoints #Nu läggs det till en ny nyckel i lineSegmentDict dictionaryn, där nyckeln är indexet av den nuvarande punkten och att värdet är en lista på den nuvarande punktens 5 närmsta punkter
        else: #Om currentpoint redan finns som en nyckel i lineSegmentDict så har den redan ett värde. Då läggs bara alla nearestNeighbors till på värdet för nyckeln.
            i = 0
            while i < len(nearestPoints): #O(g) där g står för en punkts alla närmsta grannar.
                if (nearestPoints[i] in lineSegmentDict[point]): #SPECIALFALL: Det finns en chans att det värde som nyckeln har är en av grannarna i nearestNeighbor. Då tas den grannen bort från nearestNeighbor så att man inte får två av samma granne i värdet för nyckeln. O(g) där g är antalet grannar till punkten 'point'. Värdena för nyckeln 'point' i lineSegmentDict är en lista på vilka punkter som är närmsta granne med 'point'.
                    nearestPoints.remove(nearestPoints[i])
                else:
                    lineSegmentDict[point].append(nearestPoints[i])
                i = i+1


    #Steg 2. Den fulla komplexiteten för steg 2 är O(rp + rh) där r är alla rutor i rutfältet, p är alla punkter i en ruta och h är alla hinder i obstacleList. 
    #Mängden hinder i obstacleList just nu, om man inte lägger till eller tar bort några hinder manuellt i koden, är 3. Om n är säg 1500 så skulle i genomsnitt, på ett 4x4 rutfält, vara runt 94. I det fallet skulle rp vara den dominanta faktorn.
    #I vissa fall, om n är ett mycket mindre nummer som till exempel 40 eller om det vore ett till exempel 25x25 rutfält, då vore rh antagligen större än rp. I det flesta fall är dock rp större än rh.
    #Den slutgiltiga komplexiteten för steg 2 i algoritmen är alltså O(rp).

    for currentSquare in squareDict.keys(): #O(r) där r står för alla rutor i rutfältet. "currentSquare" är alltså den ruta algoritmen ser på just nu och representerar alla rutor i rutfältet. Först är currentSquare lika med 0, då den första rutan i rutfältet heter "0". Nästa ruta heter "1" så 'currentSquare' kommer vara lika med 1 etc.
        middleList = [] #middleList är en lista som innehåller "currentSquare"s mittpunkt och de närliggande rutornas mittpunkter. I "steg 2" drar man en vektor mellan en rutas alla närliggande rutor för att man ska se vilken punkt som ligger närmast den andra rutan. 
        x = widthOfWindow/(numColumns*2) + (widthOfWindow/numColumns)*(currentSquare%numColumns) #Denna beräkning bör få fram x-koordinaten för mittpunkten på varje ruta. 
        y = heightOfWindow/(numRows*2) + (heightOfWindow/numRows)*(math.floor(currentSquare/numRows)) #Denna beräkning bör få fram y-koordinaten för mittpunkten på varje ruta.
        middlePointCurrentSquare = ((x, y)) #"currenSquare"s mittpunkt, som alla mittpunkter i middleList ska jämföras med.

        middleList.append(((x - widthOfWindow/numColumns), (y + heightOfWindow/numRows))) #Detta är mittpunkten för rutan som ska vara precis uppåt åt vänster om "currentSquare", om det finns en ruta där.
        middleList.append((x, (y + heightOfWindow/numRows))) #Detta är mittpunkten för rutan som ska vara precis ovanför "currentSquare", om det finns en ruta där.
        middleList.append(((x + widthOfWindow/numColumns), (y + heightOfWindow/numRows))) #Detta är mittpunkten för rutan som ska vara precis uppåt åt höger om "currentSquare", om det finns en ruta där.
        middleList.append(((x + widthOfWindow/numColumns), y)) #Detta är mittpuntken för rutan som ska vara precis åt höger om "currentSquare", om det finns någon där.

        for i in range(4): #O(1) då denna loop alltid körs 4 gånger. Det finns ju alltid bara 4 index i middleList.
            nearestSquare = whichSquare(middleList[i], widthOfWindow, heightOfWindow, numColumns, numRows) #"whichSquare"-funktionen är O(1). Ser i vilken ruta de 4 mittenpunkterna i "middleList" ska vara i.

            if nearestSquare != -1: #Specialfall: Om nearestSquare är -1 så ligger inte punkten inuti någon ruta i rutfältet.
                normalVector = createVector(middlePointCurrentSquare, middleList[i]) #Skapar först en vektor från "currentSquare"s mittpunkt till den närliggande rutans mittpunkt.
                highestScalar1 = -100000 #Lagrar den högsta skalärprodukten som har hittats i "currentSquare".
                nearestPoint1 = -1 #NearestPoint1 är den punkt inuti "currentSquare" som är närmast den närliggande rutan.
                highestScalar2 = -100000 #Lagrar den högsta skalärprodukten som har hittats i den närliggande rutan.
                nearestPoint2 = -1 #NearestPoint2 är den punkt inuti den närliggande rutan som är närmast "currentSquare"
                for a in squareDict[currentSquare]: # O(p) där p står för alla punkter i "currentSquare". i är alla punkter i "currentSquare"
                    vector = createVector(middlePointCurrentSquare, pointList[a]) #Man ritar sedan en vektor var till alla punkter i "currentSquare"... 
                    scalarProduct = scalar(normalVector, vector) #...och tar sedan fram skalärprodukten mellan normalvektorn och alla de andra punkternas vektorer. 
                    if scalarProduct > highestScalar1: #Den punkt som ligger allra närmast den närliggande rutan har då störst skalärprodukt.
                        highestScalar1 = scalarProduct #Den nya skalärprodukten är den högsta skalärprodukten.
                        nearestPoint1 = a #Punkten 'pointList[a]' är den punkt närmast den andra rutan som man hittills har hittat.

                #Samma process upprepas sedan fast åt andra hållet, för att få fram vilken punkt i "currentSquare" som ligger närmast den närliggande rutan och vilken punkt i den närliggande rutan som ligger närmast "currentSquare".
                normalVector = createVector(middleList[i], middlePointCurrentSquare) 
                for b in squareDict[nearestSquare]: #O(p) där p står för alla punkter i "nearestSquare". 'i' är alla punkter i den närliggande rutan.
                    vector = createVector(middleList[i], pointList[b])
                    scalarProduct = scalar(normalVector, vector)
                    if scalarProduct > highestScalar2:
                        highestScalar2 = scalarProduct
                        nearestPoint2 = b
                        
                #Till sist läggs den nya kopplingen in i verticesList. Den närmsta punkten i "currentSquare" får även den närmsta punkten i den närliggande rutan som närmsta granne och tvärtom.
                if nearestPoint1 != -1 and nearestPoint2 != -1 and inObstacleLine(pointList[nearestPoint1], pointList[nearestPoint2], obstacleList) == False: #Om man faktiskt har hittat någon närmsta punkt i båda rutorna (alltså om ingen av rutorna är tomma) så ser man om linjen mellan de två skulle kollidera med något hinder. "inObstacleLine"-funktionen är O(h) där h står för alla hinder i obstacleList.
                    verticesList.append(pointList[nearestPoint1]) #Om det finns någon punkt i båda rutorna och om en linje mellan de två närmsta punkterna inte skulle kollidera med ett hinder, då läggs kopplingen till både i verticesList...
                    verticesList.append(pointList[nearestPoint2])
                    lineSegmentDict[nearestPoint1].append(nearestPoint2) #... och i lineSegmentDict.
                    lineSegmentDict[nearestPoint2].append(nearestPoint1)

    return lineSegmentDict, verticesList #Till slut returneras lineSegmentDict och verticesList. verticesList används av renderaren och lineSegmentDict används av Astar.

    #Förklaring för hur man hittar de närmsta rutorna för alla rutor i denna kod (förklaring med lite mer visuell förklaring finns i PDF jag har skickat in också)
    #I ett 4x4 rutfält går man igenom alla rutor då man börjar med ruta 0 och slutar med ruta 15. 
    #För varje ruta, ta fram rutans mittpunkt. Hur man räknar ut koordinaten för mittpunkten: X = B/(numColumn*2) + (B/numColumn)*(square%numColumn).  Y = H/(numRows*2) + (H/numRows)(math.floor(square/numRows))
    #Sedan tar man den mittpunkten och skapar 4 andra punkter. Den nuvarande rutans mittpunkt säger vi är (x,y). Punkt 1 ska ha koordinaterna (x-B/numColumns, y+H/numRows), punkt 2 är vid (x, y+H/numRows), punkt 3 är vid (x+B/numColumns, y+H/numRows) och punkt 4 är vid (x+B/numColumns, y). numRows är antalet rader i rutfältet och numColumns är antalet kolumner i rutfältet. B är bredden på fönstret, H är höjden på fönstret.
    #Man ser sedan vilka av dessa 4 punkter som ligger inuti en ruta, med hjälp av "whichSquare"-funktionen. De punkter som faktiskt ligger i en ruta är, för alla rutor i rutfältet, mittpunkterna för alla de närliggande rutorna som inte redan är kopplade till den nuvarande rutan. Detta gäller oavsett hur stort eller litet rutfältet eller fönstret är.
    #Det skapas då vektorer mellan den nuvarande mittpunkten och de andra mittpunkterna, då man sedan ritar en vektor till alla punkter i båda rutorna och använder skalärprodukten mellan de vektorerna och vektorn mellan mittpunkterna för att se vilka punkter som ligger närmast den andra rutan (de med högst skalärprodukt är närmast, så ha bara en variabel och säg "if (skalärprodukt > variabel): variabel = skalärprodukt, närmsta punkt = nuvarande punkt")

def whichSquare(point, widthOfWindow, heightOfWindow, numColumns, numRows): #Tar emot en punkts koordinater, höjden och bredden på fönstret och antalet kolumner och rader det ska vara i rutnätet. Ruta 1 är alltid i nedersta vänstra hörn. Kolumn 1 är alltid längst åt vänster och rad 1 är alltid raden längst ner i rutfältet. O(1).
    if point[0] < 0 or point[1] < 0: #Specialfall: Om punktens x- eller y-värde är negativt, då finns inte punkten i fönstret och därmed inte inuti någon ruta.
        return -1
    elif point[0] > widthOfWindow or point[1] > heightOfWindow: #Specialfall: Om punktens x-värde är högre än fönstrets bredd eller om punktens y-värde är högre än fönstrets höjd, då finns inte punkten i fönstret och därmed inte inuti någon ruta.
        return -1
    else:
        column = math.floor(point[0] / (widthOfWindow/numColumns)) #Hashar fram vilken kolumn punkten ligger i. Man får ett heltal från 0 till värdet på numColumns.
        row = math.floor(point[1] / (heightOfWindow/numRows)) #Hashar fram vilken rad punkten ligger. Man får ett heltal från 0 till värdet på numRows.
        if (column == numColumns): #Specialfall om punktens x-koordinat är exakt samma som bredden på fönstret.
            column = column -1
        if (row == numRows): #Specialfall om punktens y-koordinat är exakt samma som höjden på fönstret.
            row = row -1
        whichSquare = column + numRows* row #Då rutorna namnges "0", "1", "2" etc så kommer denna del beräkna vilken ruta som punkten hamnar i. Om punkten ligger i kolumn 1 så kommer "column" ha ett värde på 0.
        return whichSquare #Kommer ge ett värde mellan 0 och numColumns * numRows -1. numColumns * numRows är mängden rutor i rutfältet men då ruta 1 heter "0" så kommer den sista rutan att ha värdet numColumns * numRows - 1.