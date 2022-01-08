import random
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import warnings

warnings.filterwarnings('error')

inerita = 0.2
cognitiveCoefficient = 1.0
socialFactor = 1.0
swarm = []

minX = -4.5
maxX = 4.5
minY = -4.5
maxY = 4.5

# minX = -1.5
# maxX = 4.0
# minY = -3.0
# maxY = 4.0

sizeSwarm = 50
globalBestAdaptation = math.inf
globalBestCoord = [0.0, 0.0]
theBestIter = 0
xChart = []
yChart = []
iterChart = 0
amountIter = 50


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


def adaptation(x, y):
    return ((1.5 - x + x * y) ** 2) + ((2.25 - x + x * (y ** 2)) ** 2) + ((2.625 - x + x * (y ** 3)) ** 2)

# def adaptation(x, y):
#     return np.sin(x + y) + (x - y)**2 - 1.5 * x + 2.5 * y + 1


def animation_frame(i):
    global iterChart
    chart.set_xdata(xChart[iterChart:iterChart + sizeSwarm])
    chart.set_ydata(yChart[iterChart:iterChart + sizeSwarm])
    ax.set_title(i)
    iterChart += sizeSwarm
    return chart


if __name__ == '__main__':
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
        fiqa, az = plt.subplots()
        az.set_xlim(minX, maxX)
        az.set_ylim(minY, maxY)
        az.set_title(z)
        chart2, = az.plot(fx, fy, 'o')
        plt.show()
        plt.close(fiqa)
        for i in range(amountIter):
            for particle in swarm:
                particle.updateVelocity()
            for particle in swarm:
                particle.updateAdaptation(i)

        fig = plt.figure(figsize=(8, 8))
        ax = fig.add_subplot(111, projection='3d')
        lastX = []
        lastY = []
        lastAdapt = []
        for particle in swarm:
            lastX.append(particle.coord[0])
            lastY.append(particle.coord[1])
            lastAdapt.append(particle.actualAdaptation)
        ax.scatter(lastX, lastY, lastAdapt)
        ax.set_title(z)
        plt.show()
        plt.close(fig)
        fig, ax = plt.subplots()
        ax.set_xlim(minX, maxX)
        ax.set_ylim(minY, maxY)
        chart, = ax.plot(0, 0, 'o')
        animation = FuncAnimation(fig, func=animation_frame, frames=amountIter, interval=500 )
        animation.save('coil' + str(z) + '.gif')
        plt.close(fig)
        print(globalBestAdaptation)
        print(globalBestCoord)
        print(theBestIter)
