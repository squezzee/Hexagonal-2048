from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QPushButton, QGraphicsView, QGraphicsItem, \
    QWidget
from PySide2.QtGui import QBrush, QPen, QFont, QPolygon, QPolygonF, QPainter, QColor, QTextOption
from PySide2.QtCore import Qt, QPoint, QRectF, QPointF
import sys
import numpy as np
import math
from colorama import Fore, Style
import random

HEX_SIDE = 40


class Board(QGraphicsItem):
    def __init__(self, hex_count):
        super().__init__()
        self.cells = hex_count
        self.val = random.choice([0, 0, 0, 0, 2, 4])
        self.side = HEX_SIDE


class Hexagon(QGraphicsItem):
    def __init__(self, centre):
        super().__init__()
        self.x, self.y = centre
        self.val = random.choice([0, 0, 0, 0, 2, 4])
        self.side = HEX_SIDE

        self.points = [
            QPointF(self.x - self.side * math.sqrt(3) / 2, self.y - 0.5 * self.side),
            QPointF(self.x, self.y - self.side),
            QPointF(self.x + self.side*math.sqrt(3)/2, self.y - 0.5*self.side),
            QPointF(self.x + self.side*math.sqrt(3)/2, self.y + 0.5*self.side),
            QPointF(self.x, self.y + self.side),
            QPointF(self.x - self.side*math.sqrt(3)/2, self.y + 0.5*self.side)
        ]

        self.hex = QPolygonF(self.points)
        self.blackPen = QPen(Qt.black)
        self.blackPen.setWidth(2)

        self.color_dict = {0:    '#bcd6dd',
                           2:    '#add9d8',
                           4:    '#9fdcd4',
                           8:    '#91e0d0',
                           16:   '#83e3cc',
                           32:   '#75e7c8',
                           64:   '#67eac4',
                           128:  '#58edc0',
                           256:  '#4af1bc',
                           512:  '#3cf4b8',
                           1024: '#20fbb0',
                           2048: '#12ffac'}

    def boundingRect(self):
        return self.hex.boundingRect()

    def paint(self, painter, option, widget=None):
        painter.setPen(self.blackPen)
        painter.setBrush(QBrush(QColor(self.color_dict[self.val])))
        painter.drawPolygon(self.hex)
        opt = QTextOption()
        opt.setAlignment(Qt.AlignCenter)
        if self.val != 0:
            painter.drawText(QRectF(self.x - 0.75*self.side, self.y - self.side/2, 1.5*self.side, self.side), str(self.val), opt)


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Pyside2 QGraphic View")
        self.setGeometry(0, 0, 840, 640)
        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene, self)
        self.view.setGeometry(0, 0, 640, 640)
        self.view.setRenderHints(QtGui.QPainter.Antialiasing | QtGui.QPainter.HighQualityAntialiasing)
        self.view.setViewportUpdateMode(QtWidgets.QGraphicsView.FullViewportUpdate)
        self.centralwidget = QWidget()
        self.left_button = QPushButton(self)
        self.left_button.setText('left')
        self.left_button.setGeometry(640, 0, 200, 50)
        self.right_button = QPushButton(self)
        self.right_button.setText('right')
        self.right_button.setGeometry(640, 50, 200, 50)
        self.right_button.clicked.connect(self.move_right)
        self.upright_button = QPushButton(self)
        self.upright_button.setText('upright')
        self.upright_button.setGeometry(640, 100, 200, 50)
        self.downright_button = QPushButton(self)
        self.downright_button.setText('downright')
        self.downright_button.setGeometry(640, 150, 200, 50)
        self.upleft_button = QPushButton(self)
        self.upleft_button.setText('upleft')
        self.upleft_button.setGeometry(640, 200, 200, 50)
        self.downleft_button = QPushButton(self)
        self.downleft_button.setText('downleft')
        self.downleft_button.setGeometry(640, 250, 200, 50)


        self.size = 3
        self.hex_size = HEX_SIDE
        self.offset = 20
        self.start_point = [self.offset + self.hex_size*math.sqrt(3)/2, self.offset + self.hex_size]
        self.score = 0
        self.board, self.board_mask = self.set_2d_array()
        self.display_board_mask = self.get_2d_display_board_mask()
        print(self.board_mask)

        self.create_ui()

        self.board = self.get_cells_vals()
        self.console_board_show()

        self.show()

    def set_2d_array(self):
        board = np.zeros(shape=(2*self.size-1, 2*self.size-1))
        board_mask = np.zeros(shape=(2 * self.size - 1, 2 * self.size - 1))
        for i in range(2*self.size - 1):
            for j in range(2 * self.size - 1):
                if 7 > i + j > 1:   # HARDCODED
                    board[i, j] = 10 * i + j
                    board_mask[i, j] = 1
        return board, board_mask

    def get_2d_display_board_mask(self):
        display_board_mask = []
        even_array_len = 2 * self.size - 2
        odd_array_len = 2 * self.size - 1
        start_size = self.size
        increment = 1
        for i in range(2*self.size - 1):
            if start_size % 2 == 0:
                row_mask = np.ones(shape=even_array_len)
                skip_display_count = int((2*self.size - start_size - 1)/2)
                row_mask[0:skip_display_count] = 0
                row_mask[len(row_mask) - skip_display_count:len(row_mask)] = 0
                display_board_mask.append(row_mask.tolist())
                start_size = start_size + increment
            else:
                row_mask = np.ones(shape=odd_array_len)
                skip_display_count = int((2*self.size - start_size - 1)/2)
                row_mask[0:skip_display_count] = 0
                row_mask[len(row_mask) - skip_display_count:len(row_mask)] = 0
                display_board_mask.append(row_mask.tolist())
                start_size = start_size + increment
            if start_size > 2*self.size - 1:
                start_size = start_size - 2
                increment = -1
        return display_board_mask

    def console_board_show(self):
        space = '       '
        row_string = ''
        score_string = 'Your score is: ' + str(self.score)
        for row in self.board:
            for item in row:
                if item >= 0:
                    row_string += str(int(item)) + space
            row_string = row_string[0:len(row_string) - len(space)]
            print(f'{Fore.GREEN}' + row_string.center(50, ' ') + f'{Style.RESET_ALL}')
            row_string = ''
            print('\n')
        print(f'{Fore.BLUE}' + score_string.center(50, ' ') + f'{Style.RESET_ALL}')

    def create_ui(self):
        blackPen = QPen(Qt.black)
        blackPen.setWidth(2)

        start_x = self.start_point[0]
        temp_point = self.start_point
        if self.size % 2 == 0:
            one_more = False
        else:
            one_more = True
        for i in range(2*self.size - 1):
            if one_more:
                for j in range(2*self.size - 1):
                    if self.display_board_mask[i][j] == 1:
                        hex = Hexagon(temp_point)
                        hex.setPos(QPointF(temp_point[0], temp_point[1]))
                        self.scene.addItem(hex)
                    temp_point[0] += self.hex_size*math.sqrt(3) / 2
                one_more = False
                temp_point[0] = start_x
                temp_point[1] += 1.5 * self.hex_size / 2
            else:
                temp_point[0] = temp_point[0] + self.hex_size * math.sqrt(3) / 4
                for j in range(2*self.size - 2):
                    if self.display_board_mask[i][j] == 1:
                        hex = Hexagon(temp_point)
                        hex.setPos(QPointF(temp_point[0], temp_point[1]))
                        self.scene.addItem(hex)
                    temp_point[0] += self.hex_size*math.sqrt(3) / 2
                one_more = True
                temp_point[0] = start_x
                temp_point[1] += 1.5 * self.hex_size / 2

    def get_cells_vals(self):
        cells_list = self.scene.items()
        cells_list.reverse()
        cells_val_list = []
        for cell in cells_list:
            cells_val_list.append(cell.val)

        board = np.zeros(shape=(2*self.size - 1, 2*self.size - 1))

        for i in range(2*self.size - 1):
            for j in range(2*self.size - 1):
                if self.board_mask[i, j] != 0:
                    board[i, j] = cells_val_list.pop(0)
                else:
                    board[i, j] = -1

        return board

    def move_right(self):
        #print(self.board)
        for i in range(len(self.board[:, 0]) - 2, 0, -1):
            for j in range(0, len(self.board[0, :]) - 1):
                print(i, j, self.board[i, j])
                if self.board_mask[i, j] > 0 and self.board_mask[i+1, j] > 0:
                    self.board[i+1, j] = self.board[i, j]
        #print(self.board)
        self.console_board_show()




app = QApplication(sys.argv)
window = Window()
sys.exit(app.exec_())
