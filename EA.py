from Constant import *
from Board import *

def getPathLength(board: list[list[bool]]):
    path_cnt = 0
    for i in range(ROW):
        for j in range(COLUMN):
            if board[i][j]:
                path_cnt += 1
    return path_cnt

def getCombo(board: list[list[str]]):
    def BFS(row, column, hex):
        if row < 0 or row >= ROW or column < 0 or column >= COLUMN:
            return 0
        cur_hex = board[row][column]
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

def getMatchedNum(board: list[list[str]]):
    def BFS(row, column, hex):
        if row < 0 or row >= ROW or column < 0 or column >= COLUMN:
            return 0
        cur_hex = board[row][column]
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
    combo = getCombo(BOARD)
    num = getMatchedNum(BOARD)
    return sum(num)

def getIndividual():
    ret = Path.random()
    return ret

def getResult(board: list[list[str]], termination_criterion = 3000, population_size = 5) -> list[list[bool]]:
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
        selected_parent = copy(parent[index])
        
        mutationtype = random.random()
        if mutationtype < 0.3:
            startP = selected_parent.path[0]
            newstartP = startP.randomwalk()
            if not selected_parent.isPointOnPath(newstartP):
                selected_parent.board.set(newstartP)
                selected_parent.path.insert(0, newstartP)

        elif mutationtype < 0.6:
            endP = selected_parent.path[-1]
            newEndP = endP.randomwalk()
            if not selected_parent.isPointOnPath(newEndP):
                selected_parent.board.set(newEndP)
                selected_parent.path.append(newEndP)

        elif mutationtype < 0.8:
            if selected_parent.length() > 1:
                startP = selected_parent.path[0]
                newstartP = selected_parent.path[1]
                selected_parent.board.set(startP, False)
                selected_parent.path.pop(0)

        elif mutationtype < 1:
            if selected_parent.length() > 1:
                endP = selected_parent.path[-1]
                newendP = selected_parent.path[-2]
                selected_parent.board.set(endP, False)
                selected_parent.path.pop()

        return selected_parent

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
    termination_score = 15
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
            print(generation_count, parent_fitness)
        # record_best_fitness_value()
        generation_count += 1

        # hybriddization
        # for _ in range(population_size // 2):
        #     recombination()

        # mutation
        for i in range(population_size):
            children.append(mutation(i))
            children_fitness.append(f(children[i]))

        # children grow up
        base = 1.6
        for i in range(len(parent)):
            chil = children_fitness[i]
            pare = parent_fitness[i]
            if random.random() < pow(base, chil) / (pow(base, chil) + pow(base, pare)):
                parent[i] = children[i]
                parent_fitness[i] = children_fitness[i]
        # parent[0:population_size] = children[0:population_size]
        # parent_fitness[0:population_size] = children_fitness[0:population_size]
        children = []
        children_fitness = []

        for i in range(len(parent)):
            if parent_fitness[i] > termination_score:
                return parent[i].getBoard()
            if parent_fitness[i] > current_max_score:
                current_max_score = parent_fitness[i]
                print('\tnew score:', current_max_score)
    if generation_count % 100 == 0:
        print(generation_count, parent_fitness)
    bestindex = 0
    for i in range(len(parent)):
        if parent_fitness[i] > parent_fitness[bestindex]:
            bestindex = i
    return parent[bestindex].getBoard()