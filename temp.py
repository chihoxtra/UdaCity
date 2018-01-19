
""" manh distance + wall denstiy + block wall cost"""
    dCost = 0.0
    wCost = 0.0
    bCost = 0.0
    dCostArray = []
    wCostArray = []
    bCostArray = []
    if bool(foodGrid.asList()):
        for f in foodGrid.asList():
            #distance component
            manhdist = util.manhattanDistance(currPos, f)
            manhdist_mean = float(1.*manhdist/(w.height-2 + w.width-2))
            dCostArray.append(manhdist_mean)
            #wall component
            wallDensity = gridDensity(w, currPos, f)
            wCostArray.append(wallDensity)

            #blocking wall
            bWallCount = 0
            bWallCost = blockingWall(w, currPos, f)
            if bWallCost > 0:
                bWallCount += 1
            bCostArray.append(bWallCost)
            #if f[0] == 1:
            #    print(f, currPos, wallDensity, manhdist_mean)
            #print(f, currPos,manhdist_mean,wallDensity,bWallCost)

        dCost = min(dCostArray)
        wCost = min(wCostArray)
        bCost = min(bCostArray)

        if bWallCount != 0:
            bCost = 1.*sum(bCostArray)/bWallCount
        else:
            bCost = 0

        dCost + wCost: 16456
        dCost + wCost + bCost(min): 16006
        dCost + bCost(average): cannot pass
        dCost + bCost(min): 16099


""" actual cost to shorest food + points """
    currPos, foodGrid = state
    w = p.walls
    #WAKA


    #step 1: find closest food
    closestFood = findClosestFood(currPos, foodGrid, w)

    #step 2: find the actual distance
    dCost1 = 0.0
    points = 0.0
    if bool(closestFood):
        dCost1 = mazeDistance(currPos, closestFood, p.startingGameState)

    #step 3: add points to rest of foods

        for f in foodGrid.asList():
            if f != closestFood and f[0] != currPos[0] and f[1] != currPos[1]:
                points += 1

    hCost = dCost1 + points


""" CROSS REGION """
def foodHeuristic(state, p):

    currPos, foodGrid = state
    w = p.walls

    TotalFcost = 0.0

    # part 1 identify the cross region for foods
    # done for first time only
    if 'fCrossRegionList' not in p.heuristicInfo:
        p.heuristicInfo['fCrossRegionList'] = {}
        p.heuristicInfo['hCost'] = {}
        for f in foodGrid.asList():
            fCrossRegion = getCrossRegion(f, w)

            p.heuristicInfo['fCrossRegionList'][f] = fCrossRegion

    # part II: get pacman cross region
    pacRegion = getCrossRegion(currPos, w)

    for f in foodGrid.asList():
        fcost = 0.0
        fCrossRegion = p.heuristicInfo['fCrossRegionList'][f]

        intersacts = [x for x in fCrossRegion if x in pacRegion]

        if len(intersacts) > 0:
            print(f, currPos, (intersacts))
            for interact in intersacts:
                if f == (1,5):
                    a1 = util.manhattanDistance(f, interact)
                    b1 = util.manhattanDistance(currPos, interact)
                    print(currPos, a1, b1)
                fcost += util.manhattanDistance(f, interact)

        if f in p.heuristicInfo['hCost']:
            p.heuristicInfo['hCost'][f].append(fcost)
            costHistory = p.heuristicInfo['hCost'][f]
            Fcost = float(sum(costHistory))/float(len(costHistory))

        else:
            p.heuristicInfo['hCost'][f] = []
            p.heuristicInfo['hCost'][f].append(fcost)
            Fcost = fcost

        TotalFcost += Fcost

    return TotalFcost
