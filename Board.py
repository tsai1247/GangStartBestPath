import logging
import random
from copy import deepcopy as copy
from Constant import *
from typing import List, Tuple

class Direction():
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    @staticmethod
    def random():
        return random.randint(0, 3)

class Point():
    def __init__(self, X = 0, Y = 0, row = ROW, column = COLUMN) -> None:
        self.X = X
        self.Y = Y
        self.row = row
        self.column = column

    @staticmethod
    def random(row = ROW, column = COLUMN):
        return Point(random.randint(0, column-1), random.randint(0, row-1), row, column)

    def walk(self, direction):
        nextPoint = copy(self)

        match direction:
            case Direction.UP:
                if nextPoint.Y == 0:
                    raise Exception("Unreachable road")
                nextPoint.Y -= 1
            case Direction.DOWN:
                if nextPoint.Y +1 == nextPoint.row:
                    raise Exception("Unreachable road")
                nextPoint.Y += 1
            case Direction.LEFT:
                if nextPoint.X == 0:
                    raise Exception("Unreachable road")
                nextPoint.X -= 1
            case Direction.RIGHT:
                if nextPoint.X +1 == nextPoint.column:
                    raise Exception("Unreachable road")
                nextPoint.X += 1
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
        return f'({self.X}, {self.Y})'

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
        x, y = point.X, point.Y
        row, column = self.row, self.column
        return 0 <= x and x < column and 0 <= y and y < row

    def set(self, point: Point, value = True):
        if self.isPointinBoard(point):
            self.board[point.Y][point.X] = value
        else:
            raise Exception(f"point {point.tostring()} is not in board")
    def get(self, point: Point):
        return self.board[point.Y][point.X]
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
        self.length = len(self.path)
        self.board = Board.Empty()
        for point in self.path:
            self.board.set(point)

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
                path.append(Point(targetcol, i))
                
        else:                       # ─
            targetrow = random.randint(0, row-1)
            a, b = random.randint(0, column-1), random.randint(0, column-1)
            while a == b:
                b = random.randint(0, column-1)
            a, b = min(a, b), max(a, b)
            
            for i in range(a, b+1):
                path.append(Point(i, targetrow))

        return Path(path)

    def show(self):
        return self.board.show(self.path)

a = Path.random().show()
print(a)