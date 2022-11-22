import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

CELL_SIZE = 100

WHITE = 1
BLACK = 2
EMPTY = 0

RES_EAT = 2
RES_MOVE = 1
RES_FAIL = 0

class CHEngine:
    def __init__(self):
        self.board = [[0 for i in range(8)] for g in range(8)]

    def __str__(self):
        #return str([g for i in self.board for g in i])
        teststr = ''
        for i in self.board:
            for j in i:
                if j == WHITE:
                    teststr += 'W '
                elif j == BLACK:
                    teststr += 'B '
                else:
                    teststr += '- '
            teststr += '\n'
        return teststr

    def _checkeat(self, cfrom, cto):
        color = self.board[cfrom['y']][cfrom['x']]

        mult = [[1, 1], [-1, 1], [1, -1], [-1, -1]]
        for i in mult:
            sx = i[0]
            sy = i[1]
            if (cto['y'], cto['x']) == (cfrom['y'] + sy*2, cfrom['x'] + sx*2):
                if self.board[cfrom['y'] + sy*1][cfrom['x'] + sx*1] != EMPTY and \
                  self.board[cfrom['y'] + sy*1][cfrom['x'] + sx*1] != color:
                    return (cfrom['y'] + sy*1, cfrom['x'] + sx*1)
                else:
                    return ()

    def _checkmove(self, cfrom, cto):
        color = self.board[cfrom['y']][cfrom['x']]
        dir = 0
        if color == BLACK:
            dir = 1
        else:
            dir = -1

        if (cto['y'], cto['x']) == (cfrom['y'] + dir, cfrom['x'] + 1) or\
                (cto['y'], cto['x']) == (cfrom['y'] + dir, cfrom['x'] - 1):
            return True
        else:
            return False

    def check_move(self, cfrom, cto):
        if self.board[cto['y']][cto['x']] != EMPTY:
            return False

        elif cfrom == cto:
            return False

        elif abs(cfrom['y'] - cto['y']) == 2 and abs(cfrom['x'] - cto['x']) == 2:
            if self._checkeat(cfrom, cto):
                return True
            else:
                return False

        elif abs(cfrom['y'] - cto['y']) == 1 and abs(cfrom['x'] - cto['x']) == 1:
            if self._checkmove(cfrom, cto):
                return True
            else:
                return False

        else:
            return False

    def can_eat(self, cfrom):
        curx = cfrom['x']
        cury = cfrom['y']
        color = self.board[cury][curx]

        res = RES_FAIL

        mult = [[2, 2], [-2, 2], [2, -2], [-2, -2]]
        for i in mult:
            shifty = cury + i[0]
            shiftx = curx + i[1]
            if (shifty < 0 or shifty > 7) or \
                    (shiftx < 0 or shiftx > 7):
                continue
            else:
                if self._checkeat(cfrom, {'x': shiftx, 'y': shifty}) and \
                     self.check_move(cfrom, {'x': shiftx, 'y': shifty}):
                    res = RES_EAT
                    break
        return res

    def _new_game(self, color, row):
        for i in range(row, row + 3):
            if i % 2 == 0:
                for j in range(1, 8, 2):
                    self.board[i][j] = color
            else:
                for j in range(0, 7, 2):
                    self.board[i][j] = color

    def new_game(self):
        self._new_game(BLACK, 0)
        self._new_game(WHITE, len(self.board) - 3)

    def isempty(self, cfrom):
        return self.board[cfrom['y']][cfrom['x']] == EMPTY

    def make_move(self, cfrom, cto):
        if self.check_move(cfrom, cto):
            stat = self._checkeat(cfrom, cto)
            stat2 = self._checkmove(cfrom, cto)
            if stat:
                self.board[cto['y']][cto['x']] = self.board[cfrom['y']][cfrom['x']]
                self.board[cfrom['y']][cfrom['x']] = EMPTY
                self.board[stat[0]][stat[1]] = EMPTY
                return RES_EAT
            elif stat2:
                self.board[cto['y']][cto['x']] = self.board[cfrom['y']][cfrom['x']]
                self.board[cfrom['y']][cfrom['x']] = EMPTY
                return RES_MOVE

        return RES_FAIL


class View(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.f_makemove = None
        self.selected = {}
        self.oldRect = 0
        self.flag = False
        self.first = True
        self.x = 0
        self.y = 0
        self.board = None
        self.isselected = False
        self.oldFigures = None
        self.statustext = ''
        self.statusobj = None
        self.hod = WHITE

    def initUI(self):
        self.setGeometry(300, 100, 900, 900)
        self.setWindowTitle('Шашки')
        self.scene = QGraphicsScene()
        self.graphics_view = QGraphicsView()
        self.graphics_view.setScene(self.scene)
        self.graphics_view.setSceneRect(0, 0, 800, 800)
        self.setCentralWidget(self.graphics_view)
        self.pixmapB = QPixmap("/home/linuxlite/Downloads/blackfigure.png")
        self.pixmapW = QPixmap("/home/linuxlite/Downloads/whitefigure.png")

    def SetEngineMethod(self, f_makemove, f_empty, f_caneat):
        self.f_makemove = f_makemove
        self.f_empty = f_empty
        self.f_caneat = f_caneat

    def paintEvent(self, e):
        if self.first: # если первый запуск то рисуем шахматную доску
            xx = 5
            yy = 5
            for i in range(8):
                for j in range(8):
                    if (8 - i + 1 + j) % 2 == 0:
                        Rect = QGraphicsRectItem(i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                        Rect.setBrush(QColor(101, 67, 33))
                    else:
                        Rect = QGraphicsRectItem(i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                        Rect.setBrush(QColor(255, 255, 255))
                    self.scene.addItem(Rect)
            for _ in range(12):
                Rect = QGraphicsRectItem(xx, yy, 10, 10)
                Rect.setPen(QPen(Qt.red,  2,))


        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == BLACK:
                    pic = self.scene.addPixmap(self.pixmapB.scaled(90, 90))
                    pic.setOffset(j * CELL_SIZE + 5, i * CELL_SIZE + 5)

                elif self.board[i][j] == WHITE:
                    pic = self.scene.addPixmap(self.pixmapW.scaled(90, 90))
                    pic.setOffset(j * CELL_SIZE + 5, i * CELL_SIZE + 5)

        if self.flag and self.y < 800 and self.x < 800 and self.selected:  # рисуем прямоугольник выделенную ячейку
            if self.oldRect != 0:
                self.scene.removeItem(self.oldRect)
            Rect = QGraphicsRectItem(self.x, self.y, CELL_SIZE, CELL_SIZE)
            Rect.setPen(QPen(Qt.red, 2))
            self.scene.addItem(Rect)
            self.flag = False
            self.oldRect = Rect
        self.showstatus(self.statustext)

    def set_board(self, board):
        self.board = board
        self.repaint()

    def showstatus(self, text):
        if self.statusobj:
            self.scene.removeItem(self.statusobj)
        if text:
            self.statusobj = QGraphicsTextItem(text)
            self.statusobj.setPos(200, 810)
            self.scene.addItem(self.statusobj)

    def mousePressEvent(self, event):
        self.statustext = ''
        self.x = int((event.pos().x() - CELL_SIZE // 2) / CELL_SIZE) * CELL_SIZE
        self.y = int((event.pos().y() - CELL_SIZE // 2) / CELL_SIZE) * CELL_SIZE
        self.flag = True
        cell = {'x': self.x // CELL_SIZE, 'y': self.y // CELL_SIZE}
        if not self.selected:
            self.statustext = ''
            if self.f_empty(cell):
                return
            if self.board[cell['y']][cell['x']] != self.hod:
                self.statustext = 'Сейчас ходит другой цвет'
                self.repaint()
                return
            self.selected = cell
        else:
            print(self.selected)
            moveok = self.f_makemove(self.selected, cell)
            if moveok == RES_FAIL:
                self.statustext = 'Неверный ход'
            if moveok == RES_EAT:
                if self.f_caneat(cell):
                    self.selected = None
                    self.statustext = 'Можно съесть ещё раз'
                    self.repaint()
                    return

            self.selected = None
            if self.hod == WHITE and moveok:
                self.hod = BLACK
            elif self.hod == BLACK and moveok:
                self.hod = WHITE

        self.repaint()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    engine = CHEngine()
    engine.new_game()

    boardview = View()
    boardview.set_board(engine.board)
    boardview.show()

    boardview.SetEngineMethod(engine.make_move, engine.isempty, engine.can_eat)

    sys.exit(app.exec())


