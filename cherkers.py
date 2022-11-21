import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


WHITE = 1
BLACK = 2
EMPTY = 0


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
                return True
            elif stat2:
                self.board[cto['y']][cto['x']] = self.board[cfrom['y']][cfrom['x']]
                self.board[cfrom['y']][cfrom['x']] = EMPTY
                return True

        return False


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
        self.x1 = 0
        self.y1 = 0
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

    def SetEngineMethod(self, f_makemove, f_empty):
        self.f_makemove = f_makemove
        self.f_empty = f_empty

    def paintEvent(self, e):
        if self.first: # если первый запуск то рисуем шахматную доску
            xx = 5
            yy = 5
            for i in range(8):
                for j in range(8):
                    if (8 - i + 1 + j) % 2 == 0:
                        Rect = QGraphicsRectItem(i * 100, j * 100, 100, 100)
                        Rect.setBrush(QColor(101, 67, 33))
                    else:
                        Rect = QGraphicsRectItem(i * 100, j * 100, 100, 100)
                        Rect.setBrush(QColor(255, 255, 255))
                    self.scene.addItem(Rect)
            for _ in range(12):
                Rect = QGraphicsRectItem(xx, yy, 10, 10)
                Rect.setPen(QPen(Qt.red,  2,))


        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == BLACK:
                    pic = self.scene.addPixmap(self.pixmapB.scaled(90, 90))
                    pic.setOffset(j * 100 + 5, i * 100 + 5)

                elif self.board[i][j] == WHITE:
                    pic = self.scene.addPixmap(self.pixmapW.scaled(90, 90))
                    pic.setOffset(j * 100 + 5, i * 100 + 5)


        if self.flag and self.y < 800 and self.x < 800 and self.selected:  # рисуем прямоугольник выделенную ячейку
            if self.oldRect != 0:
                self.scene.removeItem(self.oldRect)
            Rect = QGraphicsRectItem(self.x, self.y, 100, 100)
            Rect.setPen(QPen(Qt.red, 2, ))
            self.scene.addItem(Rect)
            self.flag = False
            self.oldRect = Rect
        self.showstatus(self.statustext)

    def set_board(self, board):
        self.board = board
        self.repaint()

    def showstatus(self, text):
        if text:
            self.statusobj = QGraphicsTextItem(text)
            self.statusobj.setPos(200, 810)
            self.scene.addItem(self.statusobj)
        else:
            self.scene.removeItem(self.statusobj)

    def mousePressEvent(self, event):
        self.statustext = ''
        self.x = int((event.pos().x() - 50) / 100) * 100
        self.y = int((event.pos().y() - 50) / 100) * 100
        self.flag = True
        cell = {'x': self.x // 100, 'y': self.y // 100}
        if not self.selected:
            if self.f_empty(cell):
                return
            self.selected = cell
        else:
            moveok = self.f_makemove(self.selected, cell)
            if not moveok:
                self.statustext = 'Неверный ход'
            self.selected = None
        print(engine)
        self.x1 = self.x
        self.y1 = self.y
        self.repaint()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    engine = CHEngine()
    engine.new_game()

    boardview = View()
    boardview.set_board(engine.board)
    boardview.show()

    boardview.SetEngineMethod(engine.make_move, engine.isempty)

    sys.exit(app.exec())


