from tkinter import *


class TicTacToeView:
    def __init__(self, width, height, f_move, f_new_game):
        self.width = width
        self.height = height
        self.f_move = f_move
        self.f_new_game = f_new_game

        self.sootv = {}

        self.tkinter = Tk()
        self.tkinter.title("Крестики-нолики")
        self.c = Canvas(self.tkinter, width=self.width, height=self.height)
        self.c.pack()
        self.label = Label()
        self.label.pack(side=LEFT)
        but = Button(text='Start new game', command=lambda: self.new_game())
        but.pack(side=RIGHT)
        self.c.bind("<Button-1>", self.mouse_click)

        self.new_game()

    def loop(self):
        self.tkinter.mainloop()

    def new_game(self):
        self.f_new_game()
        self.c.create_rectangle(0, 0, self.width, self.height, fill='black')
        self.draw_field(self.width, self.height)
        w = self.width
        h = self.height
        self.sootv = {
            1: [0, 0], 2: [w // 3, 0], 3: [w // 3 * 2, 0],
            4: [0, h // 3], 5: [w // 3, h // 3],
            6: [w // 3 * 2, h // 3], 7: [0, h // 3 * 2],
            8: [w // 3, h // 3 * 2], 9: [w // 3 * 2, h // 3 * 2]
        }
        self.print_state('Сейчас ходят: крестики')

    def print_state(self, text):
        self.label['text'] = text

    def numcell(self, x, y):
        if 0 <= x < self.width // 3 and 0 <= y < self.height // 3:
            return 1

        if self.width // 3 <= x < self.width // 3 * 2 and 0 <= y < self.height // 3:
            return 2

        if self.width // 3 * 2 <= x < self.width and 0 <= y < self.height // 3:
            return 3

        if 0 <= x < self.width // 3 and self.width // 3 <= y < self.height // 3 * 2:
            return 4

        if self.width // 3 <= x < self.width // 3 * 2 and self.width // 3 <= y < self.height // 3 * 2:
            return 5

        if self.width // 3 * 2 <= x < self.width and self.width // 3 <= y < self.height // 3 * 2:
            return 6

        if 0 <= x < self.width // 3 and self.width // 3 * 2 <= y < self.height:
            return 7

        if self.width // 3 <= x < self.width // 3 * 2 and self.width // 3 * 2 <= y < self.height:
            return 8

        if self.width // 3 * 2 <= x < self.width and self.width // 3 * 2 <= y < self.height:
            return 9

        return 0

    def draw_x(self, x, y):
        self.c.create_polygon(x + 30, y + 10, x + 10, y + 30, x + 90, y + 110, x + 110, y + 90, fill='red')
        self.c.create_polygon(x + 90, y + 10, x + 110, y + 30, x + 30, y + 110, x + 10, y + 90, fill='red')

    def draw_null(self, x, y):
        self.c.create_oval(x + 15, y + 15, x + 105, y + 105, fill='black', outline='blue', width=10)

    def draw_field(self, maxx, maxy):
        self.c.create_line(120, 0, 120, 360, fill='white')
        self.c.create_line(240, 0, 240, 360, fill='white')
        self.c.create_line(0, 120, 360, 120, fill='white')
        self.c.create_line(0, 240, 360, 240, fill='white')

    def mouse_click(self, event):
        numcell = self.numcell(event.x, event.y)
        if numcell == 0:
            return
        basepoint = self.sootv[numcell]
        res = self.f_move(numcell)

        if res[0] == 'X':
            self.draw_x(basepoint[0], basepoint[1])
        elif res[0] == '0':
            self.draw_null(basepoint[0], basepoint[1])

        if res[1]:
            self.print_state(res[1])


class TicTacToeBoard:
    def __init__(self):
        self.wincomb = [(1, 2, 3), (4, 5, 6),
                     (7, 8, 9), (1, 4, 7),
                     (2, 5, 8), (3, 6, 9),
                     (1, 5, 9), (3, 5, 7)]
        self.new_game()

    def new_game(self):
        self.field = ['-' for i in range(9)]
        self.hod = 'X'
        self.pob = False

    def check_field(self):
        win = None
        for sym in ['X', '0']:
            for comb in self.wincomb:
                if self.field[comb[0] - 1] == sym and\
                   self.field[comb[1] - 1] == sym and\
                   self.field[comb[2] - 1] == sym:
                    win = sym
                    break
        if not win:
            win = "D"
            for i in self.field:
                if i == '-':
                    win = None
                    break

        return win

    def make_move(self, celln):
        celln -= 1
        flag = False
        for i in self.field:
            if i == '-':
                flag = True
        if not flag:
            return [None, 'Игра уже завершена']

        if self.pob:
            return [None, 'Игра уже завершена']
        if self.field[celln] != '-':
            return [None, 'Клетка ' + str(celln) + ' уже занята']

        currhod = self.hod
        prov = self.check_field()
        text = ""
        if not prov:
            self.field[celln] = self.hod
            if self.hod == '0':
                self.hod = 'X'
                text = "крестики"
            else:
                self.hod = '0'
                text = "нолики"

        prov = self.check_field()
        if not prov:
            return [currhod, 'Сейчас ходят: ' + text]

        elif prov == 'X':
            self.pob = True
            return ["X", 'Победил игрок X']

        elif prov == '0':
            self.pob = True
            return ["0", 'Победил игрок 0']

        elif prov == 'D':
            self.pob = True
            return [currhod, 'Ничья']


tc = TicTacToeBoard()
tv = TicTacToeView(360, 360, tc.make_move, tc.new_game)
tv.loop()
