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

sizeSwarm = 100
globalBestAdaptation = math.inf
globalBestCoord = np.array([0.0, 0.0])
theBestIter = 0
x = []
y = []
iterChart = 0
amountIter = 50


class Particle(object):
    def __init__(self, x, y):
        self.coord = np.array([x, y], dtype=np.float64)
        self.velocity = 0
        self.actualAdaptation = math.inf
        self.bestCoord = np.array([0, 0])
        self.bestAdaptation = math.inf
        self.updateAdaptation(0)

    def updateAdaptation(self, i):
        global globalBestAdaptation
        global globalBestCoord
        global theBestIter
        self.actualAdaptation = adaptation(self.coord[0], self.coord[1])
        if (self.bestAdaptation > self.actualAdaptation):
            self.bestAdaptation = self.actualAdaptation
            self.bestCoord = np.copy(self.coord)
        if (globalBestAdaptation > self.actualAdaptation):
            globalBestAdaptation = self.actualAdaptation
            globalBestCoord = np.copy(self.coord)
            theBestIter = i

    def getInerita(self):
        return inerita * self.velocity

    def getCognitiveCoefficient(self):
        return cognitiveCoefficient * random.uniform(0, 1) * (self.bestCoord - self.coord)


    def getSocialFactor(self):
        global globalBestCoord
        return socialFactor * random.uniform(0, 1) * (globalBestCoord - self.coord)

    def updateVelocity(self):
        global x
        global y
        self.velocity = self.getInerita() + self.getCognitiveCoefficient() + self.getSocialFactor()
        self.coord += self.velocity
        x.append(self.coord[0])
        y.append(self.coord[1])


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
    chart.set_xdata(x[iterChart:iterChart + 100])
    chart.set_ydata(y[iterChart:iterChart + 100])
    ax.set_title(i)
    iterChart += 100
    return chart


if __name__ == '__main__':
    for z in range(10):
        k=random.uniform(-4,4)
        k2 = random.uniform(-4, 4)
        arr = [k, k2]
        print("--------------------------------")
        swarm = []
        globalBestAdaptation = math.inf
        globalBestCoord = np.array([0, 0])
        theBestIter = 0
        fx = []
        fy = []
        x = [0]*sizeSwarm
        y = [0]*sizeSwarm
        iterChart = 0
        generateSwarm(sizeSwarm)
        for particle in swarm:
            fx.append(particle.coord[0])
            fy.append(particle.coord[1])
            x.append(particle.coord[0])
            y.append(particle.coord[1])
        fiqa, az = plt.subplots()
        az.set_xlim(minX, maxX)
        az.set_ylim(minY, maxY)
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
