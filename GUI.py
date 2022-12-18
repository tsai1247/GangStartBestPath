from typing import List
from EA import getResult
from Font import *
from Constant import *
import tkinter as tk
import tkinter.font as tkFont
import random


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

class Window():
    modeList = ['排版', '轉珠']
    def __init__(self) -> None:
        self.window = tk.Tk()
        self.window.title(str_window_title)

        self.frame_setting = tk.Frame(self.window)
        self.frame_setting.grid(row=0, column=0, sticky='W', padx = 10, pady=10)

        self.frame_result = tk.Frame(self.window)
        self.frame_result.grid(row=1, column=0, sticky='W', padx = 10, pady=10)

        self.frame_board = tk.Frame(self.window)
        self.frame_board.grid(row=2, column=0, padx=10, pady=10)
                
        # set board
        self.boardList: List[List[tk.Button]] = []
        button_size = 7
        for i in range(ROW):
            curlist = []
            for j in range(COLUMN):
                item = tk.Button(
                    self.frame_board, 
                    name=f'item {i} {j}', text=f'({i}, {j})', 
                    width=button_size, height=button_size//2,
                    font=font_board_index,
                    borderwidth=0.5,
                    command=lambda row=i, column = j: self.change_item_color(row, column)
                )

                item.grid(row=i, column=j)

                curlist.append(item)
            self.boardList.append(curlist)

        # mode
        self.label_mode_title = tk.Label(
            self.frame_setting, text='目前模式：', 
            font=font_setting_title
        )
        self.label_mode_title.grid(row=0, column=0)

        self.button_switchmode = tk.Button(
            self.frame_setting, text=self.modeList[0],
            font=font_setting_button, 
            command = self.switch_mode
        )
        self.button_switchmode.grid(row=0, column=1)

        # shuffle
        self.button_shuffleboard = tk.Button(
            self.frame_setting, text='隨機版面',
            font=font_setting_button, 
            command = self.shuffle
        )
        self.button_shuffleboard.grid(row=0, column=2, padx=5)

        # train
        self.button_train = tk.Button(
            self.frame_setting, text='計算好的解',
            font=font_setting_button,
            state='disabled', 
            command = self.train
        )
        self.button_train.grid(row=0, column=3, padx=5)



        # score
        ## 總分
        self.label_score_title = tk.Label(
            self.frame_result, text='版面總分：', 
            font=font_setting_title
        )
        self.label_score_title.grid(row=0, column=0, sticky='W')
        
        self.label_totalscore = tk.Label(
            self.frame_result, text='0', 
            font=font_setting_content
        )
        self.label_totalscore.grid(row=0, column=1)

        self.button_calculatescore = tk.Button(
            self.frame_result, text='重新計算', 
            font=font_setting_button,
            command=self.calculate
        )
        self.button_calculatescore.grid(row=0, column=2, columnspan=4, padx=5, sticky='W')

        ## Combo
        self.label_combo_title = tk.Label(
            self.frame_result, text='Combo: ', 
            font=font_setting_subtitle
        )
        self.label_combo_title.grid(row=1, column=0, padx=10, sticky='W')
        
        self.label_combo_total = tk.Label(
            self.frame_result, text='0', 
            font=font_setting_content
        )
        self.label_combo_total.grid(row=1, column=1, padx=10)

        self.label_combo_list: List[tk.Label] = []
        for i in range(4):
            label_combo_each = tk.Label(
                self.frame_result, text='0', 
                font=font_setting_content,
                width=3,
                background=BoardColor.GetHex(i),
            )
            label_combo_each.grid(row=1, column=i+2, padx=5, )
            self.label_combo_list.append(label_combo_each)
        
        ## 消除個數
        self.label_cntnumber_title = tk.Label(
            self.frame_result, text='match number: ', 
            font=font_setting_subtitle
        )
        self.label_cntnumber_title.grid(row=2, column=0, padx=10, sticky='W')
        
        self.label_cntnumber_total = tk.Label(
            self.frame_result, text='0', 
            font=font_setting_content
        )
        self.label_cntnumber_total.grid(row=2, column=1, padx=10)

        self.label_cntnumber_list: List[tk.Label] = []
        for i in range(4):
            label_cntnumber_each = tk.Label(
                self.frame_result, text='0', 
                font=font_setting_content,
                width=3,
                background=BoardColor.GetHex(i),
            )
            label_cntnumber_each.grid(row=2, column=i+2, padx=5, )
            self.label_cntnumber_list.append(label_cntnumber_each)

        self.label_length_title = tk.Label(
            self.frame_result, text='路徑長度: ', 
            font=font_setting_subtitle
        )
        self.label_length_title.grid(row=3, column=0, padx=10, sticky='W')
        
        self.label_length = tk.Label(
            self.frame_result, text='0', 
            font=font_setting_content
        )
        self.label_length.grid(row=3, column=1, padx=10)
        


        # things to do at the end of init
        self.shuffle()
    
    def train(self):
        result = getResult(self.getBoard(origin=True))
        for i in range(len(result)):
            for j in range(len(result[i])):
                if result[i][j]:
                    self.select(i, j)
                else:
                    self.unselect(i, j)

    def select(self, row, column):
        self.boardList[row][column].config(borderwidth = 3.5)
    def unselect(self, row, column):
        self.boardList[row][column].config(borderwidth = 0.5)
    def isselect(self, row, column):
        return float(self.boardList[row][column].cget("borderwidth")) > 1


    def shuffle(self):
        for i in range(ROW):
            for j in range(COLUMN):
                self.boardList[i][j].config(
                    background=BoardColor.GetHex(random.randint(0, 3)), 
                    borderwidth=0.5
                )
        self.calculate()

    def calculate(self):
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
                        
        score = 0
        board = self.getBoard()
        combolist = [0 for _ in range(4)]
        cntnumlist = [0 for _ in range(4)]
        totalcombo = 0
        totalcntnum = 0
        isTraveled_to_Circle_Region = [[False for _ in range(COLUMN)] for __ in range(ROW)]
        path_cnt = 0
        for i in range(ROW):
            for j in range(COLUMN):
                name = board[i][j]
                if self.isselect(i, j):
                    path_cnt += 1
                isTraveled_to_Check_Combo = [[False for _ in range(COLUMN)] for __ in range(ROW)]
                num = BFS(i, j, name)
                isvalidRegion = is_3_inLine()
                if isvalidRegion:
                    index = BoardColor.GetIndex(name)
                    combolist[index] += 1
                    cntnumlist[index] += num

        totalcombo = sum(combolist)
        totalcntnum = sum(cntnumlist)
        self.label_length.config(text=f'{path_cnt}')
        self.label_totalscore.config(text='{:2d}'.format(score))
        self.label_combo_total.config(text='{:2d}'.format(totalcombo))
        self.label_cntnumber_total.config(text='{:2d}'.format(totalcntnum))
        for i in range(len(self.label_combo_list)):
            self.label_combo_list[i].config(text='{:2d}'.format(combolist[i]))
            
        for i in range(len(self.label_cntnumber_list)):
            self.label_cntnumber_list[i].config(text='{:2d}'.format(cntnumlist[i]))

    def getBoard(self, origin = False):
        ret = []
        for i in range(ROW):
            cur = []
            for j in range(COLUMN):
                name = BoardColor.toName( self.boardList[i][j].cget('background') )
                if origin and self.isselect(i, j):
                    name = BoardColor.NextName(name, 2)
                cur.append(name)
            ret.append(cur)
        return ret

    def switch_mode(self):
        txt = self.button_switchmode.cget('text')
        index = (self.modeList.index(txt) + 1) % 2
        self.button_switchmode.config(text=self.modeList[index])
        if index == 0:
            self.button_train.config(state='disabled')
        else:
            self.button_train.config(state='active')

    def change_item_color(self, row, column):
        if self.button_switchmode.cget('text') != self.modeList[0]: # 訓練。點擊後畫出路徑
            if self.isselect(row, column):
                self.unselect(row, column)
            else:
                self.select(row, column)

            cur_bg_hex = self.boardList[row][column].cget('background')
            next_bg_hex = BoardColor.NextHex(cur_bg_hex, 2)

            self.boardList[row][column].config(bg = next_bg_hex)
            self.calculate()
            
        else:                                                       # 排版。點擊後改變顏色
            cur_bg_hex = self.boardList[row][column].cget('background')
            next_bg_hex = BoardColor.NextHex(cur_bg_hex)

            self.boardList[row][column].config(bg = next_bg_hex)
            self.calculate()

    def show(self):
        self.window.mainloop()
        

if __name__ == '__main__':
    Window().show()