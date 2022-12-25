from typing import List
from EA3 import getPathLength, getCombo, getMatchedNum, getResult
from Font import *
from Constant import *
import tkinter as tk
import random
from Board import BoardColor


class Window():
    modeList = ['排版', '轉珠']
    def __init__(self) -> None:
        self.window = tk.Tk()
        self.window.title(str_window_title)
        self.window.attributes('-topmost', True)

        self.frame_setting = tk.Frame(self.window)
        self.frame_setting.grid(row=0, column=0, sticky='W', padx = 10, pady=10)

        self.frame_origin_board = tk.Frame(self.window)
        self.frame_origin_board.grid(row=1, column=0, padx=10, pady=10)

        self.label_arrow = tk.Label(self.window, text='=>', font=font_setting_title)
        self.label_arrow.grid(row=1, column=1, padx=5, pady=5, )

        self.frame_result = tk.Frame(self.window)
        self.frame_result.grid(row=0, column=2, sticky='W', padx = 10, pady=10)
        
        self.frame_result_board = tk.Frame(self.window)
        self.frame_result_board.grid(row=1, column=2, sticky='W', padx = 10, pady=10)

                
        # origin board
        self.boardList: List[List[tk.Button]] = []
        button_size = 7
        for i in range(ROW):
            curlist = []
            for j in range(COLUMN):
                item = tk.Button(
                    self.frame_origin_board, 
                    name=f'item {i} {j}', text=f'({i}, {j})', 
                    width=button_size, height=button_size//2,
                    font=font_board_index,
                    borderwidth=0.5,
                    command=lambda row=i, column = j: self.change_item_color(row, column)
                )

                item.grid(row=i, column=j)

                curlist.append(item)
            self.boardList.append(curlist)

        # result board
        self.resultboardList: List[List[tk.Button]] = []
        button_size = 7
        for i in range(ROW):
            curlist = []
            for j in range(COLUMN):
                item = tk.Button(
                    self.frame_result_board, 
                    name=f'item {i} {j}', text=f'({i}, {j})', 
                    width=button_size, height=button_size//2,
                    font=font_board_index,
                    borderwidth=0.5,
                    command=lambda row=i, column = j: self.change_item_color(row, column)
                )

                item.grid(row=i, column=j)

                curlist.append(item)
            self.resultboardList.append(curlist)

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

        # iter
        self.label_iter_title = tk.Label(
            self.frame_setting, text='迭代次數: ', 
            font=font_setting_subtitle
        )
        self.label_iter_title.grid(row=4, column=0, padx=10, columnspan=2, sticky='W')
        
        self.str_iter = tk.IntVar()
        self.str_iter.set(3000)
        self.label_iter = tk.Entry(
            self.frame_setting, textvariable=self.str_iter,
            width=6,
            font=font_setting_content
        )
        self.label_iter.grid(row=4, column=2, columnspan=2, padx=10)

        # popu
        self.label_timeout_title = tk.Label(
            self.frame_setting, text='time out: ', 
            font=font_setting_subtitle
        )
        self.label_timeout_title.grid(row=5, column=0, padx=10, columnspan=2, sticky='W')
        
        self.str_timeout = tk.IntVar()
        self.str_timeout.set(1000)
        self.label_popu = tk.Entry(
            self.frame_setting, textvariable=self.str_timeout,
            width=6,
            font=font_setting_content
        )
        self.label_popu.grid(row=5, column=2, columnspan=2, padx=10)

        self.label_target_score_title = tk.Label(
            self.frame_setting, text='目標分數: ', 
            font=font_setting_subtitle
        )
        self.label_target_score_title.grid(row=6, column=0, padx=10, columnspan=2, sticky='W')
        
        self.str_target_score = tk.IntVar()
        self.str_target_score.set(2000)
        self.label_target_score = tk.Entry(
            self.frame_setting, textvariable=self.str_target_score,
            width=6,
            font=font_setting_content
        )
        self.label_target_score.grid(row=6, column=2, columnspan=2, padx=10)



        # things to do at the end of init
        self.shuffle()
    
    def train(self):
        for i in range(ROW):
            for j in range(COLUMN):
                self.unselect(i, j)

        result = getResult(self.getBoard(origin=True), self.str_iter.get(), self.str_timeout.get(), self.str_target_score.get())
        for i in range(len(result)):
            for j in range(len(result[i])):
                if result[i][j]:
                    self.select(i, j)
                else:
                    self.unselect(i, j)
        self.calculate()

    def select(self, row, column):
        if self.isselect(row, column):
            return
            
        self.resultboardList[row][column].config(borderwidth = 3.5, foreground='red')
        cur_bg_hex = self.resultboardList[row][column].cget('background')
        next_bg_hex = BoardColor.NextHex(cur_bg_hex, 2)
        self.resultboardList[row][column].config(bg = next_bg_hex)

    def unselect(self, row, column):
        if not self.isselect(row, column):
            return

        self.resultboardList[row][column].config(borderwidth = 0.5, foreground='black')
        cur_bg_hex = self.resultboardList[row][column].cget('background')
        next_bg_hex = BoardColor.NextHex(cur_bg_hex, 2)
        self.resultboardList[row][column].config(bg = next_bg_hex)

    def isselect(self, row, column):
        return float(self.resultboardList[row][column].cget("borderwidth")) > 1


    def shuffle(self):
        for i in range(ROW):
            for j in range(COLUMN):
                color = BoardColor.GetHex(random.randint(0, 3))
                self.boardList[i][j].config(
                    background=color, 
                    foreground='black',
                    borderwidth=0.5
                )
                self.resultboardList[i][j].config(
                    background=color, 
                    foreground='black',
                    borderwidth=0.5
                )
        self.calculate()

    def getSelected(self):
        board = [[self.isselect(i, j) for j in range(COLUMN)] for i in range(ROW)]
        return board

    def calculate(self):
        board = self.getBoard()
        selected = self.getSelected()
        
        path_cnt = getPathLength(selected)
        combolist = getCombo(board)
        cntnumlist = getMatchedNum(board)

        totalcombo = sum(combolist)
        totalcntnum = sum(cntnumlist)
        self.label_length.config(text=f'{path_cnt}')
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
        if self.button_switchmode.cget('text') == self.modeList[0]: # 排版。點擊後改變顏色
            cur_bg_hex = self.boardList[row][column].cget('background')
            next_bg_hex = BoardColor.NextHex(cur_bg_hex)

            self.boardList[row][column].config(bg = next_bg_hex)
            self.resultboardList[row][column].config(bg = next_bg_hex)
            self.calculate()
        # else: do nothing # 訓練。點擊後畫出路徑

    def show(self):
        self.window.mainloop()
        

if __name__ == '__main__':
    Window().show()