import random
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import warnings

warnings.filterwarnings('error')
#Piotr Chłapiński 229853, Maciej Urbański 230030

inerita = 0.3
cognitiveCoefficient = 0.5
socialFactor = 0.8
swarm = []




sizeSwarm = 50
globalBestAdaptation = math.inf
globalBestCoord = [0.0, 0.0]
theBestIter = 0
xChart = []
yChart = []
iterChart = 0
amountIter = 100


class Particle(object):
    def __init__(self, x, y):
        self.coord = [x,y]
        self.velocity = [0.0,0.0]
        self.actualAdaptation = math.inf
        self.bestCoord = [0.0,0.0]
        self.bestAdaptation = math.inf
        self.updateAdaptation(0)

    def updateAdaptation(self, i):
        global globalBestAdaptation
        global globalBestCoord
        global theBestIter
        self.actualAdaptation = adaptation(self.coord[0], self.coord[1])
        if (self.bestAdaptation > self.actualAdaptation):
            self.bestAdaptation = self.actualAdaptation
            self.bestCoord = self.coord.copy()
        if (globalBestAdaptation > self.actualAdaptation):
            globalBestAdaptation = self.actualAdaptation
            globalBestCoord = self.coord.copy()
            theBestIter = i

    def getInerita(self):
        return [inerita * self.velocity[0],inerita * self.velocity[1] ]

    def getCognitiveCoefficient(self):
        x=cognitiveCoefficient * random.uniform(0, 1) * (self.bestCoord[0] - self.coord[0])
        y=cognitiveCoefficient * random.uniform(0, 1) * (self.bestCoord[1] - self.coord[1])
        return [x,y]


    def getSocialFactor(self):
        global globalBestCoord
        x= socialFactor * random.uniform(0, 1) * (globalBestCoord[0] - self.coord[0])
        y= socialFactor * random.uniform(0, 1) * (globalBestCoord[1] - self.coord[1])
        return [x,y]

    def updateVelocity(self):
        global xChart
        global yChart
        compInerita = self.getInerita()
        compCC = self.getCognitiveCoefficient()
        compSF = self.getSocialFactor()
        self.velocity = [compInerita[0]+compSF[0]+compCC[0],compInerita[1]+compSF[1]+compCC[1]]
        self.coord[0] += self.velocity[0]
        self.coord[1] += self.velocity[1]
        xChart.append(self.coord[0])
        yChart.append(self.coord[1])


def generateSwarm(n):
    global swarm
    for i in range(n):
        swarm.append(Particle(random.uniform(minX, maxX), random.uniform(minY, maxY)))

#funkcja 1
def adaptation1(x, y):
    return ((1.5 - x + x * y) ** 2) + ((2.25 - x + x * (y ** 2)) ** 2) + ((2.625 - x + x * (y ** 3)) ** 2)
#funkcja 2
def adaptation2(x, y):
    return np.sin(x + y) + (x - y)**2 - 1.5 * x + 2.5 * y + 1


def animation_frame(i):
    global iterChart
    chart.set_xdata(xChart[iterChart:iterChart + sizeSwarm])
    chart.set_ydata(yChart[iterChart:iterChart + sizeSwarm])
    ax.set_title(i)
    iterChart += sizeSwarm
    return chart


if __name__ == '__main__':
    f=0
    while(f!= 1 and f!=2):
        f = input("Wybierz funkcję\n1.((1.5 - x + x * y) ** 2) + ((2.25 - x + x * (y ** 2)) ** 2) + ((2.625 - x + x * (y ** 3)) ** 2)\n2. np.sin(x + y) + (x - y)**2 - 1.5 * x + 2.5 * y + 1:\n")
        try:
            f = int(f)
        except:
            f=0
            print("Niepoprawny numer funkcji!")
    if(f==1):
        adaptation = adaptation1
        minX = -4.5
        maxX = 4.5
        minY = -4.5
        maxY = 4.5
    else:
        adaptation = adaptation2
        minX = -1.5
        maxX = 4.0
        minY = -3.0
        maxY = 4.0

    for z in range(5):
        k=random.uniform(-4,4)
        k2 = random.uniform(-4, 4)
        arr = [k, k2]
        print("--------------------------------")
        swarm = []
        globalBestAdaptation = math.inf
        globalBestCoord = [0.0,0.0]
        theBestIter = 0
        fx = []
        fy = []
        xChart = [0] * sizeSwarm
        yChart = [0] * sizeSwarm
        iterChart = 0
        generateSwarm(sizeSwarm)
        for particle in swarm:
            fx.append(particle.coord[0])
            fy.append(particle.coord[1])
            xChart.append(particle.coord[0])
            yChart.append(particle.coord[1])
        #Rysowanie wykresu początkowego
        fiqa, az = plt.subplots()
        az.set_xlim(minX, maxX)
        az.set_ylim(minY, maxY)
        az.set_xlabel('x', fontsize=16)
        az.set_ylabel('y', fontsize=16)
        az.set_title(z+1)
        chart2, = az.plot(fx, fy, 'o')
        plt.show()
        plt.close(fiqa)
        for i in range(amountIter):
            for particle in swarm:
                particle.updateVelocity()
            for particle in swarm:
                particle.updateAdaptation(i)
        lastX = []
        lastY = []
        lastAdapt = []
        for particle in swarm:
            lastX.append(particle.coord[0])
            lastY.append(particle.coord[1])
            lastAdapt.append(particle.actualAdaptation)
        # Rysowanie wykresu 3d
        fig2 = plt.figure(figsize=(8, 8))
        ax2 = fig2.add_subplot(projection='3d')
        ax2.scatter(lastX, lastY, lastAdapt)
        ax2.set_xlim(minX, maxX)
        ax2.set_ylim(minY, maxY)
        ax2.set_xlabel('x', fontsize=16)
        ax2.set_ylabel('y', fontsize=16)
        ax2.set_zlabel('f(x,y)', fontsize=16)
        ax2.set_title(z+1)
        plt.show()
        plt.close(fig2)
        #Rysowanie wykresu 3
        fiqa, az = plt.subplots()
        az.set_xlim(minX, maxX)
        az.set_ylim(minY, maxY)
        az.set_xlabel('x', fontsize=16)
        az.set_ylabel('y', fontsize=16)
        az.set_title(z + 1)
        chart2, = az.plot(lastX, lastY, 'o')
        plt.show()
        plt.close(fiqa)
        fig, ax = plt.subplots()
        ax.set_xlim(minX, maxX)
        ax.set_ylim(minY, maxY)
        ax.set_xlabel('x', fontsize=16)
        ax.set_ylabel('y', fontsize=16)
        chart, = ax.plot(0, 0, 'o')
        animation = FuncAnimation(fig, func=animation_frame, frames=amountIter, interval=500 )
        animation.save('coil' + str(z) + '.gif')
        plt.close(fig)
        print(globalBestAdaptation)
        print(globalBestCoord)
        print(theBestIter)
