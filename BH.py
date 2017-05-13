import random
import math
import sys

range_x, range_y = 10.0, 10.0
left_x, left_y = -5.0, -5.0

def fun(star):
    return pow(star.x,2) + pow(star.y,2) + 1000

class Star:
    def __init__(self):
        self.x = random.random() * range_x + left_x
        self.y = random.random() * range_y + left_y
        self.isBH = False
        self.fitness = 0.0

    def updateFitness(self):
        self.fitness = fun(self)

    def updateLocation(self, BH):
        self.x += random.random() * (BH.x - self.x)
        self.y += random.random() * (BH.y - self.y)

    def __str__(self):
        return "Is Bh: " + str(self.isBH) + " fitness: " + str(self.fitness)


def selectBH(stars):
    """Returns index of star which became black hole (to avoid references ambiguous)"""
    tmp = Star()
    tmp.fitness = sys.maxint
    it = 0
    bhNum = 0
    for star in stars:
        if star.fitness < tmp.fitness:
            tmp = star
            bhNum = it
        it += 1
    return bhNum

def calcEvetHorizon(BH, stars):
    tmp = 0
    for star in stars:
        tmp += star.fitness
    return BH.fitness / tmp

def isCrossingEventHorizon(BH, star, horizon):
    x = pow(abs(BH.x - star.x), 2)
    y = pow(abs(BH.y - star.y), 2)
    if math.sqrt(x + y) <= horizon:
        return True
    return False

#initializing population
pop_number = 100
pop = []
for i in range(pop_number):
    pop.append(Star())

max_iter = 1000
it = 0
BH = Star()

while it < max_iter:
    #For each star, evaluate the objective function
    for i in range(pop_number):
        pop[i].updateFitness()
        pop[i].isBH = False
    #Select the best star that has the best fitness value as the black hole
    #this is equal to If a star reaches a location with lower cost than the black hole, exchange their locations
    BH = pop[selectBH(pop)]
    BH.isBH = True
    #Change the location of each star
    for i in range(pop_number):
        pop[i].updateLocation(BH)

    eventHorizon = calcEvetHorizon(BH, pop)

    #If a star crosses the event horizon of the black hole,
    # replace it with a new star in a random location in the search space
    for i in range(pop_number):
        if isCrossingEventHorizon(BH, pop[i], eventHorizon) == True and pop[i].isBH == False:
            pop[i].x = random.random() * range_x + left_x
            pop[i].y = random.random() * range_y + left_y


    # do wypisywania
    # for i in range(pop_number):
    #     print str(pop[i]) + " " + str(pop[i].x) + " " + str(pop[i].y)
    # print eventHorizon
    # print

    it += 1

print BH

