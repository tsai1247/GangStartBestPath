from Constant import *
from Board import *

def getPathLength(board: list[list[bool]]):
    path_cnt = 0
    for i in range(ROW):
        for j in range(COLUMN):
            if board[i][j]:
                path_cnt += 1
    return path_cnt

def getCombo(board: list[list[str]], selected: list[list[bool]] = None):
    def BFS(row, column, hex):
        if row < 0 or row >= ROW or column < 0 or column >= COLUMN:
            return 0
        cur_hex = board[row][column]
        if selected != None and selected[row][column]:
            cur_hex = BoardColor.NextName(cur_hex, 2)
            
        if isTraveled_to_Circle_Region[row][column] or cur_hex != hex:
            return 0
        
        # self
        isTraveled_to_Circle_Region[row][column] = True
        isTraveled_to_Check_Combo[row][column] = True
        cnt = 1

        # up
        cnt += BFS(row-1, column, hex)
        # down
        cnt += BFS(row+1, column, hex)
        # left
        cnt += BFS(row, column-1, hex)
        # right
        cnt += BFS(row, column+1, hex)

        return cnt
    def is_3_inLine():
        for row in range(ROW-2):
            for column in range(COLUMN):
                if not isTraveled_to_Check_Combo[row][column]:
                    continue
                if isTraveled_to_Check_Combo[row+1][column] and isTraveled_to_Check_Combo[row+2][column]:
                    return True
                    
        for row in range(ROW):
            for column in range(COLUMN-2):
                if not isTraveled_to_Check_Combo[row][column]:
                    continue
                if isTraveled_to_Check_Combo[row][column+1] and isTraveled_to_Check_Combo[row][column+2]:
                    return True
        return False
                    
    # score = 0
    combolist = [0 for _ in range(4)]
    isTraveled_to_Circle_Region = [[False for _ in range(COLUMN)] for __ in range(ROW)]
    for i in range(ROW):
        for j in range(COLUMN):
            name = board[i][j]
            isTraveled_to_Check_Combo = [[False for _ in range(COLUMN)] for __ in range(ROW)]
            BFS(i, j, name)
            isvalidRegion = is_3_inLine()
            if isvalidRegion:
                index = BoardColor.GetIndex(name)
                combolist[index] += 1
    return combolist

def getMatchedNum(board: list[list[str]], selected: list[list[bool]] = None):
    def BFS(row, column, hex):
        if row < 0 or row >= ROW or column < 0 or column >= COLUMN:
            return 0
        cur_hex = board[row][column]
        if selected != None and selected[row][column]:
            cur_hex = BoardColor.NextName(cur_hex, 2)

        if isTraveled_to_Circle_Region[row][column] or cur_hex != hex:
            return 0
        
        # self
        isTraveled_to_Circle_Region[row][column] = True
        isTraveled_to_Check_Combo[row][column] = True
        cnt = 1

        # up
        cnt += BFS(row-1, column, hex)
        # down
        cnt += BFS(row+1, column, hex)
        # left
        cnt += BFS(row, column-1, hex)
        # right
        cnt += BFS(row, column+1, hex)

        return cnt
    def is_3_inLine():
        for row in range(ROW-2):
            for column in range(COLUMN):
                if not isTraveled_to_Check_Combo[row][column]:
                    continue
                if isTraveled_to_Check_Combo[row+1][column] and isTraveled_to_Check_Combo[row+2][column]:
                    return True
                    
        for row in range(ROW):
            for column in range(COLUMN-2):
                if not isTraveled_to_Check_Combo[row][column]:
                    continue
                if isTraveled_to_Check_Combo[row][column+1] and isTraveled_to_Check_Combo[row][column+2]:
                    return True
        return False
                    
    # score = 0
    cntnumlist = [0 for _ in range(4)]
    isTraveled_to_Circle_Region = [[False for _ in range(COLUMN)] for __ in range(ROW)]
    for i in range(ROW):
        for j in range(COLUMN):
            name = board[i][j]
            isTraveled_to_Check_Combo = [[False for _ in range(COLUMN)] for __ in range(ROW)]
            num = BFS(i, j, name)
            isvalidRegion = is_3_inLine()
            if isvalidRegion:
                index = BoardColor.GetIndex(name)
                cntnumlist[index] += num

    return cntnumlist

#################################################################3
BOARD: list[list[str]]
# about EA



def f(selected: Path):
    global BOARD
    
    length = getPathLength(selected.getBoard())
    combo = getCombo(BOARD, selected.getBoard())
    num = getMatchedNum(BOARD, selected.getBoard())
    return sum(num)*10000 + sum(combo)* 100 + length

def getIndividual():
    ret = Path.random()
    return ret

def getResult(board: list[list[str]], termination_criterion = 3000, population_size = 5, termination_score = 15) -> list[list[bool]]:
    def parent_selection():
        total_score = sum(parent_fitness)
        num = random.randint(0, total_score)
        front_score = 0
        for i in range(population_size):
            front_score += parent_fitness[i]
            if front_score >= num:
                return i

        return i
    def mutation(index):
        selected_parent: list[Path] = []
        for i in range(4):
            selected_parent.append(copy(parent[index]))
        returnList: list[Path] = []
        
        mutationtype = random.random()
        if mutationtype < 0.5:
            if parent[index].length() < 15:
                for i in range(4):
                    startP = selected_parent[i].path[0]
                    try:
                        newstartP = startP.walk(i)
                    except:
                        continue
                    if not selected_parent[i].isPointOnPath(newstartP):
                        selected_parent[i].board.set(newstartP)
                        selected_parent[i].path.insert(0, newstartP)
                        returnList.append(selected_parent[i])

            back_parent: Path = copy(parent[index])
            if back_parent.length() > 1:
                startP = back_parent.path[0]
                back_parent.board.set(startP, False)
                back_parent.path.pop(0)
                returnList.append(back_parent)

        else:
            if parent[index].length() < 15:
                for i in range(4):
                    endP = selected_parent[i].path[-1]
                    try:
                        newEndP = endP.walk(i)
                    except:
                        continue
                    if not selected_parent[i].isPointOnPath(newEndP):
                        selected_parent[i].board.set(newEndP)
                        selected_parent[i].path.append(newEndP)
                        returnList.append(selected_parent[i])

            back_parent: Path = copy(parent[index])
            if back_parent.length() > 1:
                endP = back_parent.path[-1]
                back_parent.board.set(endP, False)
                back_parent.path.pop()
                returnList.append(back_parent)

        return returnList
    def getBest(individuals, fitnesses, probabilities = [80, 60, 20, 6, 2]):
        assert(len(individuals) == len(fitnesses))
        compete = [(fitnesses[i], individuals[i]) for i in range(len(individuals))]
        sorted(compete, reverse = True)
        probabilities = probabilities[:len(individuals)]
        target = random.randint(0, sum(probabilities))
        score = 0
        for i in range(population_size):
            score += probabilities[i]
            if score >= target:
                return individuals[i], fitnesses[i]
        return individuals[i], fitnesses[i]



    def recombination():
        selected_parents = copy([parent[parent_selection()], parent[parent_selection()]])
        
        # hybrid
        # pos1 = random.randint(0, chromosome_size)

        # swap index from pos1 to pos2
        # tmp = selected_parents[0][pos1:]
        # selected_parents[0][pos1:] = selected_parents[1][pos1:]
        # selected_parents[1][pos1:] = tmp

        # mutate
        ''' no mutation'''

        selected_parents_fits = [f(selected_parents[i]) for i in range(len(selected_parents))]

        children.extend(selected_parents)
        children_fitness.extend(selected_parents_fits)

    global BOARD
    BOARD = board
    goal_fitness = 28
    mutation_probability = 0.5

    # init
    parent: list[Path] = []
    parent_fitness = []
    children = []
    children_fitness = []
    for _ in range(population_size):
        individual = getIndividual()
        fit_score = f(individual)
        parent_fitness.append(fit_score)
        parent.append(individual)

    generation_count = 0
    current_max_score = -1
    record_best_fitness_value_list = []
    while generation_count != termination_criterion:
        if generation_count % 100 == 0:
            print(generation_count, parent_fitness, [i.length() for i in parent])
        # record_best_fitness_value()
        generation_count += 1

        # hybriddization
        # for _ in range(population_size // 2):
        #     recombination()

        # mutation
        for i in range(population_size):
            children.append(mutation(i))
            fitnessList = []
            for child in children[i]:
                fitnessList.append(f(child))
            children_fitness.append(fitnessList)

        # children grow up
        base = 1.6
        for i in range(len(parent)):
            competeList = children[i] + [parent[i]]
            competefitnessList = children_fitness[i] + [parent_fitness[i]]
            bestone, bestonefitness = getBest(competeList, competefitnessList)

            parent[i] = bestone
            parent_fitness[i] = bestonefitness

        children = []
        children_fitness = []

        for i in range(len(parent)):
            if parent_fitness[i] >= termination_score:
                return parent[i].getBoard()
            if parent_fitness[i] > current_max_score:
                current_max_score = parent_fitness[i]
                bestofall = parent[i]
                print('\tnew score:', current_max_score)
    if generation_count % 100 == 0:
        print(generation_count, parent_fitness)
    bestindex = 0
    for i in range(len(parent)):
        if parent_fitness[i] > parent_fitness[bestindex]:
            bestindex = i
    # return parent[bestindex].getBoard()
    return bestofall.getBoard()