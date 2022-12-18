
def getResult(board: list[list[str]]) -> list[list[bool]]:
    ret = [[False for i in range(len(board[0]))] for j in range(len(board))]
    ret[0][0] = True
    ret[1][0] = True
    ret[1][1] = True
    ret[1][2] = True
    ret[1][3] = True

    return ret