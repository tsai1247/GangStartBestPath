import logging
import random
from copy import deepcopy as copy
from Constant import *
from typing import List, Tuple

class BoardColor():
    color_to_hex = {
        'RED': '#d6456e', 
        'GREEN': '#92e69b', 
        'BLUE': '#18c1e0', 
        'YELLOW': '#f0ea94', 
    }
    
    name_list = list(color_to_hex.keys())
    hex_list = list(color_to_hex.values())
    hex_to_color = {v: k for k, v in color_to_hex.items()}
    
    @staticmethod
    def toHex(colorname):
        return BoardColor.color_to_hex[colorname]
        
    @staticmethod
    def toName(colorvalue):
        return BoardColor.hex_to_color[colorvalue]
    
    @staticmethod
    def NextName(colorname, offset = 1):
        index = BoardColor.name_list.index(colorname) + offset
        return BoardColor.name_list[index % len(BoardColor.name_list)]
        
    @staticmethod
    def NextHex(colorname, offset = 1):
        index = BoardColor.hex_list.index(colorname) + offset
        return BoardColor.hex_list[index % len(BoardColor.hex_list)]

    @staticmethod
    def GetName(index):
        return BoardColor.name_list[index]
        
    @staticmethod
    def GetHex(index):
        return BoardColor.hex_list[index]

    @staticmethod
    def GetIndex(name):
        try:
            return BoardColor.name_list.index(name)
        except ValueError:
            return BoardColor.hex_list.index(name)

class Direction():
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    @staticmethod
    def random():
        return random.randint(0, 3)

class Point():
    def __init__(self, row = 0, column = 0, maxrow = ROW, maxcolumn = COLUMN) -> None:
        self.row = row
        self.column = column
        self.maxrow = maxrow
        self.maxcolumn = maxcolumn
    def __lt__(self, other):
        return self.row < other.row or self.row == other.row and self.column < other.column
        
    @staticmethod
    def random(maxrow = ROW, maxcolumn = COLUMN):
        return Point(random.randint(0, maxrow-1), random.randint(0, maxcolumn-1), maxrow, maxcolumn)

    def walk(self, direction):
        nextPoint = copy(self)

        match direction:
            case Direction.UP:
                if nextPoint.row == 0:
                    raise Exception("Unreachable road")
                nextPoint.row -= 1
            case Direction.DOWN:
                if nextPoint.row +1 == nextPoint.maxrow:
                    raise Exception("Unreachable road")
                nextPoint.row += 1
            
            case Direction.LEFT:
                if nextPoint.column == 0:
                    raise Exception("Unreachable road")
                nextPoint.column -= 1
            case Direction.RIGHT:
                if nextPoint.column +1 == nextPoint.maxcolumn:
                    raise Exception("Unreachable road")
                nextPoint.column += 1
        return nextPoint

    def randomwalk(self):
        power = 20
        while power:
            try:
                return self.walk(Direction.random())
            except:
                power -= 1

        if not power:
            raise Exception("no direction available.")

    def tostring(self):
        return f'({self.row}, {self.column})'

class Board():
    def __init__(self, board: List[List[bool]]) -> None:
            if len(board) > 0 and len(board[0]) > 0:
                self.row = len(board)
                self.column = len(board[0])
                self.board = board
            else:
                raise Exception("the board size is wrong")
    @staticmethod
    def Empty(row = ROW, column = COLUMN):
        return Board([[False for i in range(column)] for j in range(row)])

    def isPointinBoard(self, point: Point):
        x, y = point.row, point.column
        row, column = self.row, self.column
        return 0 <= x and x < row and 0 <= y and y < column

    def set(self, point: Point, value = True):
        if self.isPointinBoard(point):
            self.board[point.row][point.column] = value
        else:
            raise Exception(f"point {point.tostring()} is not in board")
    
    def get(self, point: Point):
        return self.board[point.row][point.column]

    def isDeadEnd(self, point: Point):
        for i in range(4):
            try:
                if not self.get(point.walk(i)):
                    return False
            except:
                continue
        return True

    def show(self, path: List[Point]):
        if path is None:
            ret = '-'* (len(self.board[0]) + 2) + '\n'
            for row in self.board:
                ret += '|'
                for e in row:
                    ret += '■' if e else '□'

                ret += '|\n'
            
            ret += '-'* (len(self.board[0]) + 2)
            return ret
        else:
            board = copy(self)
            for i in range(len(path)):
                board.set(path[i], i)
            
            ret = '-'* (len(board.board[0]) + 2) + '\n'
            for row in board.board:
                ret += '|'
                for e in row:
                    if type(e) is int:
                        ret += str(e)
                    else:
                        ret += '■' if e else '□'

                ret += '|\n'
            
            ret += '-'* (len(board.board[0]) + 2)
            return ret
    
class Path():
    def __init__(self, path: List[Point]) -> None:
        self.path: List[Point] = path
        self.board = Board.Empty()
        for point in self.path:
            self.board.set(point)

    def __lt__(self, other):
        for i in range(len(self.path)):
            if i >= len(other.path):
                return False
            if self.path[i] < other.path[i]:
                return True
            elif other.path[i] < self.path[i]:
                return False
        return False


    def length(self):
        return len(self.path)

    @staticmethod
    def random(row = ROW, column = COLUMN):
        path: List[Point] = []

        if random.random() > 0.5:   # |
            targetcol = random.randint(0, column-1)
            a, b = random.randint(0, row-1), random.randint(0, row-1)
            while a == b:
                b = random.randint(0, row-1)
            a, b = min(a, b), max(a, b)
            
            for i in range(a, b+1):
                path.append(Point(i, targetcol))

        else:                       # ─
            targetrow = random.randint(0, row-1)
            a, b = random.randint(0, column-1), random.randint(0, column-1)
            while a == b:
                b = random.randint(0, column-1)
            a, b = min(a, b), max(a, b)
            
            for i in range(a, b+1):
                path.append(Point(targetrow, i))

        return Path(path)
    
    def isPointOnPath(self, point: Point):
        return self.board.get(point)

    def getBoard(self):
        return [[self.board.get(Point(i, j)) for j in range(self.board.column)] for i in range(self.board.row)]
    
    def show(self):
        return self.board.show(self.path)
        
# a = Path.random().show()