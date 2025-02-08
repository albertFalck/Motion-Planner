from math import sqrt

def createVector(point1, point2): #Skapar en vektor mellan 2 punkter. O(1)
        x = point2[0] - point1[0]
        y = point2[1] - point1[1]
        return [x,y]

def createNormalVector(vector): #Tar fram normalvektorn av en vektor. O(1)
        normalvektor = [vector[1], vector[0]*(-1)]
        return normalvektor

def distanceBetweenPoints(point1, point2): #Tar fram avståndet mellan två punkter. O(1)
        a2 = (point2[0] - point1[0])**2 #Använder a^2 + b^2 = c^2, där c är längden mellan de två punkterna.
        b2 = (point2[1] - point1[1])**2
        c = sqrt(a2 + b2) #Tar kvadratroten ur c^2 för att få fram c.
        return c

def scalar(normalvector, vector): #Tar fram skalärprodukten mellan en normalvektor och en vektor. O(1)
        dotProduct = (normalvector[0] * vector[0]) + (normalvector[1] * vector[1])
        return dotProduct
        #Om man har en punkt [3,2] och en annan punkt [4,7] som ska multipliceras ihop, då tar man (3 * 4) + (2 * 7) = nånting

def createProjection(vectorToGetProjected, vectorToGetProjection): #Tar fram projektionsvektorn mellan två vektorer. O(1)
        vectorLength = distanceBetweenPoints([0,0], vectorToGetProjection) 
        uTimesV = scalar(vectorToGetProjection, vectorToGetProjected)
        vectorProj = multiplyNumberToVector((uTimesV/vectorLength**2), vectorToGetProjection)
        return vectorProj
        #u_proj = (vektor u * vektor v) / (längden av vektor v)^2, och sedan allting multiplicerat med vektor v igen

def multiplyNumberToVector(number, vector): #Multiplicerar ett nummer med en vektors x- och y-värden. O(1)
        newVector = ((vector[0] * number), (vector[1] * number))
        return newVector