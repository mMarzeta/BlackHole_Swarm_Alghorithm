import random
import math
import sys

range_d = 200.0
left = -100.0

dim = 10

#rosenbrock's function
def fun(star):
    res = 0.0
    for i in range(1, dim-1):
        res += (100 * (star.pos[i] ** 2 - star.pos[i+1]) ** 2 + (star.pos[i] - 1) ** 2)
    return res

class Star:
    def __init__(self):
        self.pos = [random.random() * range_d + left for i in range(dim)]
        self.isBH = False
        self.fitness = 0.0

    def updateFitness(self):
        self.fitness = fun(self)

    def updateLocation(self, BH):
        for i in range(len(self.pos)):
            self.pos[i] += random.random() * (BH.pos[i] - self.pos[i])

    def __str__(self):
        for i in range(dim):
            print self.pos
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
    r = 0.0
    #euclidian norm
    for i in range(len(star.pos)):
        r += pow(star.pos[i] - BH.pos[i], 2)
    if math.sqrt(r) <= horizon:
        return True
    return False

#initializing population
pop_number = 1000
pop = []
for i in range(pop_number):
    pop.append(Star())

max_iter = 1e8
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
            for j in range(dim):
                pop[i].pos[j] = random.random() * range_d + left


    # do wypisywania
    # for i in range(pop_number):
    #     print str(pop[i]) + " " + str(pop[i].x) + " " + str(pop[i].y)
    # print eventHorizon
    # print
    if it % 1000 == 0:
        print BH

    it += 1

print BH

