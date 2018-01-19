def foodHeuristic(state, p):
    """
    Your heuristic for the FoodSearchProblem goes here.

    This heuristic must be consistent to ensure correctness.  First, try to come
    up with an admissible heuristic; almost all admissible heuristics will be
    consistent as well.

    If using A* ever finds a solution that is worse uniform cost search finds,
    your heuristic is *not* consistent, and probably not admissible!  On the
    other hand, inadmissible or inconsistent heuristics may find optimal
    solutions, so be careful.

    The state is a tuple ( pacmanPosition, foodGrid ) where foodGrid is a Grid
    (see game.py) of either True or False. You can call foodGrid.asList() to get
    a list of food coordinates instead.

    If you want access to info like walls, capsules, etc., you can query the
    problem.  For example, problem.walls gives you a Grid of where the walls
    are.

    If you want to *store* information to be reused in other calls to the
    heuristic, there is a dictionary called problem.heuristicInfo that you can
    use. For example, if you only want to count the walls once and store that
    value, try: problem.heuristicInfo['wallCount'] = problem.walls.count()
    Subsequent calls to this heuristic can access
    problem.heuristicInfo['wallCount']
    """
    c, foodGrid = state
    hCost = 0.0
    ep = 1e-10

    wCost = 0.0
    dCost = 0.0
    fCost = 0.0
    for f in foodGrid.asList():
        #identify horizontal wall
        for py in range(min(f[1],c[1]),max(f[1],c[1])+1):
            h = []
            hDensity = 0.0
            for px in range(min(f[0],c[0]),max(f[0],c[0])+1):
                h.append(p.walls[px][py])
            hDensity = max(float(sum(h))/(float(len(h)) + ep), hDensity)

        #identify vertial wall
        for px in range(min(f[0],c[0]),max(f[0],c[0])+1):
            v = []
            vDensity = 0.0
            for py in range(min(f[1],c[1]),max(f[1],c[1])+1):
                v.append(p.walls[px][py])
            vDensity = max(float(sum(v))/(float(len(v)) + ep), vDensity)

            wCost += hDensity+hDensity

        dCost += util.manhattanDistance(c, f)
        wCost += GridDensity(p.walls, c, f)
        fCost += GridDensity(foodGrid, c, f)

    hCost = 0.2*wCost + 0.8*dCost + 1/(fCost+ep)
    return hCost


"""""""""""""""""""""""


    fcost = 0.0
    # part 1 identify the gold region
    goldenRegion = []
    for cx in reversed(range(1, c[0])):
        if not w[cx][c[1]]:
            goldenRegion.append((cx, c[1]))
        else:
            break
    for cx in range(c[0]+1, w.width):
        if not w[cx][c[1]]:
            goldenRegion.append((cx,c[1]))
        else:
            break
    for cy in reversed(range(1, c[1])):
        if not w[c[0]][cy]:
            goldenRegion.append((c[0], cy))
        else:
            break
    for cy in range(c[1]+1, w.height):
        if not w[c[0]][cy]:
            goldenRegion.append((c[0],cy))
        else:
            break

    # part II find the overlapping:
    masterFoodCostList = []
    for f in foodGrid.asList():
        foodcost = 0.0
        overlapFound = False
        foodMaxRegion = []
        for fx in reversed(range(1, f[0])):
            if not w[fx][f[1]]:
                if (fx,f[1])  in goldenRegion:
                    foodcost += abs(f[0]-fx)
                    overlapFound = True
                    break
            else:
                break
        foodMaxRegion.append(abs(f[0]-1))

        for fx in range(f[0]+1, w.width):
            if not w[fx][f[1]]:
                if (fx,f[1]) in goldenRegion:
                    foodcost += abs(fx-f[0])
                    overlapFound = True
                    break
            else:
                break
        foodMaxRegion.append(w.width-f[0]+1)

        for fy in reversed(range(1, f[1])):
            if not w[f[0]][fy]:
                if (f[0],fy) in goldenRegion:
                    foodcost += abs(f[1]-fy)
                    overlapFound = True
                    break
            else:
                break
        foodMaxRegion.append(abs(f[1]-1))

        for fy in range(f[1]+1, w.height):
            if not w[f[0]][fy]:
                if (f[0],fy) in goldenRegion:
                    foodcost += abs(fy-f[1])
                    overlapFound = True
                    break
            else:
                break
        foodMaxRegion.append(abs(w.height-f[1]+1))

        if overlapFound == False:
            foodcost = max(foodMaxRegion)

        masterFoodCostList.append(foodcost)

    fcost = float(sum(masterFoodCostList))


    """
    if 'firstVisit' not in p.heuristicInfo:
        print(c)
        print(goldenRegion)
        print(w)
        p.heuristicInfo['firstVisit'] = True
    """

"""""""""""""""""""""""
