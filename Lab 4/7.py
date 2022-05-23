import time
import random
import sys

# Algo for Ant Colony

class Ant_Colony_Algo(object):

    def __init__(ANT, DistBtwCities, Ant_count, α, β, ρ, Q):

        # Declarations
        ANT.DistBtwCities = DistBtwCities
        ANT.Ant_count = Ant_count
        # Parameters
        ANT.Q = Q
        ANT.β = β
        ANT.ρ = ρ
        ANT.α = α

       # Parameters assignment
        ANT.pheromones = [
            [0.15 for city in range(city_count)] for selectedcity in range(city_count)]
        ANT.bestCost = float('Inf')
        ANT.bestTour = range(city_count)

    # Function for Optimization
    def Path_Length(ANT):

        # Loop initialization
        while time.time()-start < 299.999999999:

            ants = []

            pheromonesDelta = [
                [0 for x in range(city_count)] for y in range(city_count)]

            for j in range(ANT.Ant_count):
                ant = Ant_(ANT.DistBtwCities,
                           ANT.pheromones,
                           ANT.α, ANT.β)

                ants.append(ant)

                if ant.pathCost(ANT.DistBtwCities) < ANT.bestCost:
                    ANT.bestCost = ant.pathCost(ANT.DistBtwCities)
                    ANT.bestTour = ant.crnt_Path
                    ANT.lastChange = time.time()
                    print("Tour Length =", ANT.bestCost, sep=' ')
                    print(*ANT.bestTour, sep=" ")
                    print(
                        "\n**************************************************************************************************************************\n")

            ants.sort(key=lambda city: city.pathCost(ANT.DistBtwCities))

            for mungi in ants[:int(city_count/20)]:
                for x, y in enumerate(mungi.crnt_Path):
                    nextOne = mungi.crnt_Path[(x+1) % city_count]
                    pheromonesDelta[y][nextOne] += ANT.Q / \
                        DistBtwCities[y][nextOne]

            for i in range(city_count):
                for j in range(city_count):
                    ANT.pheromones[i][j] = (
                        (1-ANT.ρ)**0.5)*ANT.pheromones[i][j] + pheromonesDelta[i][j]

            if time.time()-ANT.lastChange > 300:
                break


# Ant class structure defined

class Ant_(object):

    def __init__(ANT, DistBtwCities, pheromones, α, β):
        ANT.crnt_Path = []
        ANT.getPath(DistBtwCities, pheromones, α, β)

# Creating Path for 
    def getPath(ANT, DistBtwCities, pheromones, α, β):

        start_city = random.randint(0, city_count-1)
        next_valid_Cities = list(range(0, city_count))
        next_valid_Cities.remove(start_city)

        ANT.crnt_Path.append(start_city)
        while(len(ANT.crnt_Path) < city_count):

            lastCity = ANT.crnt_Path[-1]

            probability = [(pheromones[lastCity][nextPossibleCity]**α * (
                1/DistBtwCities[lastCity][nextPossibleCity])**β) for nextPossibleCity in next_valid_Cities]

            prop_list = [x/sum(probability) for x in probability]

            upcoming_next_city = random.choices(next_valid_Cities, weights=prop_list)[0]
            ANT.crnt_Path.append(upcoming_next_city)
            next_valid_Cities.remove(upcoming_next_city)

# Path cost function
    def pathCost(ANT, DistBtwCities):
        way = 0
        for i in range(len(ANT.crnt_Path)):
            way += DistBtwCities[ANT.crnt_Path[i]
                                  ][ANT.crnt_Path[(i+1) % city_count]]
        return way


if __name__ == '__main__':

    start = time.time()

    # input_data = open("noneuc_100", "r").readlines()
    input_data = open(sys.argv[1], "r").readlines()

    Euclidean_check = 0

    if(input_data[0] == "euclidean"):
        Euclidean_check = 1
    else:
        Euclidean_check = 0

    city_count = int(input_data[1])

    Co_ordinates = []
    DistBtwCities = []

    for z in range(city_count):
        coor = [float(i) for i in input_data[z+2].strip().split(' ')]
        Co_ordinates.append(coor)
        dist = [float(i)
                for i in input_data[city_count+2+z].strip().split(' ')]
        DistBtwCities.append(dist)

# Euclidean Distance init
    if Euclidean_check == 1:
        Ant_Colony_Optimization_Path = Ant_Colony_Algo(
            DistBtwCities, Ant_count=int(city_count), α=1.5, β=1.5, ρ=0.1, Q=0.1)
    else:
        Ant_Colony_Optimization_Path = Ant_Colony_Algo(DistBtwCities, Ant_count=int(city_count),
                                                       α=5, β=5, ρ=0.05, Q=0.05)

    Ant_Colony_Optimization_Path.Path_Length()
