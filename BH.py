import random
import math
import sys

range_d = 200.0
left = -100.0

dim = 10

#rosenbrock's function
def fun(star, flag):
    res = 0.0
    if flag == "rosenbrock":
        for i in range(0, dim - 1):
            res += (100 * (star.pos[i] ** 2 - star.pos[i + 1]) ** 2 + (star.pos[i] - 1) ** 2)
        return res
    elif flag == "bent_cigar":
        for i in range(1, dim):
            res += star.pos[i] ** 2
        res *= 10 ** 6
        res += star.pos[0] ** 2
        return res
    elif flag == "zakharov":
        part_1 = 0.
        part_2 = 0.
        part_3 = 0.
        for i in range(0, dim):
            part_1 += star.pos[i] ** 2
            part_2 += star.pos[i] * .5
            part_3 += star.pos[i] * .5
        part_2 = part_2 ** 2
        part_3 = part_3 ** 4
        res = part_1 + part_2 + part_3
        return res
    elif flag == "rastrigin":
        for i in range(0, dim):
            res += (star.pos[i] ** 2 - 10. * math.cos(2 * math.pi * star.pos[i]) + 10.)
        return res

class Star:
    def __init__(self):
        self.pos = [random.random() * range_d + left for i in range(dim)]
        self.isBH = False
        self.fitness = 0.0

    #wybor funkcji do analizy
    def updateFitness(self):
        #self.fitness = fun(self, "zakharov")
        #self.fitness = fun(self, "rosenbrock")
        self.fitness = fun(self, "bent_cigar")
        #self.fitness = fun(self, "rastrigin")

    def updateLocation(self, BH):
        for i in range(len(self.pos)):
            self.pos[i] += random.random() * (BH.pos[i] - self.pos[i])

    def __str__(self):
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
pop_number = 100
pop = []
for i in range(0, pop_number):
    pop.append(Star())

max_iter = 1e8
it = 0
BH = Star()

while it < max_iter:
    #For each star, evaluate the objective function
    for i in range(0, pop_number):
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
        print (BH)

    it += 1

    if BH.fitness < 1e-8:
        break

print (BH)

