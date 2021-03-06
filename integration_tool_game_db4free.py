#!/usr/bin/python
#coding=utf8
 
import random,sys
from PyQt4 import QtCore, QtGui  

class Tetris(QtGui.QFrame):  
    TetrisWidth = 10  
    TetrisHeight = 22  
    Speed = 300  
    def __init__(self, parent):  
        QtGui.QFrame.__init__(self, parent) 
        self.setGeometry(0,0, 600, 365)
        self.frame = QtGui.QFrame(parent)
        self.frame.setGeometry(QtCore.QRect(0, 0, 600, 365))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.frame.setFrameShadow(QtGui.QFrame.Sunken)
        self.frame.hide() 
        self.timer = QtCore.QBasicTimer()  
        self.isWaitingAfterLine = False  
        self.curPiece = Shape()  
        self.nextPiece = Shape()  
        self.curX = 0  
        self.curY = 0  
        self.numLinesRemoved = 0  
        self.tetris = []  
        self.setFocusPolicy(QtCore.Qt.StrongFocus)  
        self.isStarted = False  
        self.isPaused = False  
        self.clearTetris()  
        self.nextPiece.setRandomShape() 
    def shapeAt(self, x, y):  
        return self.tetris[(y * Tetris.TetrisWidth) + x]  
    def setShapeAt(self, x, y, shape):  
        self.tetris[(y * Tetris.TetrisWidth) + x] = shape  
    def squareWidth(self):  
        return self.contentsRect().width() / Tetris.TetrisWidth  
    def squareHeight(self):  
        return self.contentsRect().height() / Tetris.TetrisHeight  
    def start(self):  
        if self.isPaused:  
            return  
        self.isStarted = True  
        self.isWaitingAfterLine = False  
        self.numLinesRemoved = 0  
        self.clearTetris()  
        self.emit(QtCore.SIGNAL("messageToStatusbar(QString)"),  
            str(self.numLinesRemoved))  
        self.newPiece()  
        self.timer.start(Tetris.Speed, self)  
    def pause(self):  
        if not self.isStarted:  
            return  
        self.isPaused = not self.isPaused  
        if self.isPaused:  
            self.timer.stop()  
            self.emit(QtCore.SIGNAL("messageToStatusbar(QString)"), "paused")  
        else:  
            self.timer.start(Tetris.Speed, self)  
            self.emit(QtCore.SIGNAL("messageToStatusbar(QString)"),  
                str(self.numLinesRemoved))  
        self.update()  
    def paintEvent(self, event):  
        painter = QtGui.QPainter(self)  
        rect = self.contentsRect()  
        tetrisTop = rect.bottom() - Tetris.TetrisHeight * self.squareHeight()  
        for i in range(Tetris.TetrisHeight):  
            for j in range(Tetris.TetrisWidth):  
                shape = self.shapeAt(j, Tetris.TetrisHeight - i - 1)  
                if shape != Tetrominoes.NoShape:  
                    self.drawSquare(painter,  
                        rect.left() + j * self.squareWidth(),  
                        tetrisTop + i * self.squareHeight(), shape)  
        if self.curPiece.shape() != Tetrominoes.NoShape:  
            for i in range(4):  
                x = self.curX + self.curPiece.x(i)  
                y = self.curY - self.curPiece.y(i)  
                self.drawSquare(painter, rect.left() + x * self.squareWidth(),  
                    tetrisTop + (Tetris.TetrisHeight - y - 1) * self.squareHeight(),  
                    self.curPiece.shape())  
    def keyPressEvent(self, event):  
        if not self.isStarted or self.curPiece.shape() == Tetrominoes.NoShape:  
            QtGui.QWidget.keyPressEvent(self, event)  
            return  
        key = event.key()  
        if key == QtCore.Qt.Key_P:  
            self.pause()  
            return  
        if self.isPaused:  
            return  
        elif key == QtCore.Qt.Key_Left:  
            self.tryMove(self.curPiece, self.curX - 1, self.curY)  
        elif key == QtCore.Qt.Key_Right:  
            self.tryMove(self.curPiece, self.curX + 1, self.curY)  
        elif key == QtCore.Qt.Key_Down:  
            self.tryMove(self.curPiece.rotatedRight(), self.curX, self.curY)  
        elif key == QtCore.Qt.Key_Up:  
            self.tryMove(self.curPiece.rotatedLeft(), self.curX, self.curY)  
        elif key == QtCore.Qt.Key_Space:  
            self.dropDown()  
        elif key == QtCore.Qt.Key_D:  
            self.oneLineDown()  
        else:  
            QtGui.QWidget.keyPressEvent(self, event)  
    def timerEvent(self, event):  
        if event.timerId() == self.timer.timerId():  
            if self.isWaitingAfterLine:  
                self.isWaitingAfterLine = False  
                self.newPiece()  
            else:  
                self.oneLineDown()  
        else:  
            QtGui.QFrame.timerEvent(self, event)  
    def clearTetris(self):  
        for i in range(Tetris.TetrisHeight * Tetris.TetrisWidth):  
            self.tetris.append(Tetrominoes.NoShape)  
    def dropDown(self):  
        newY = self.curY  
        while newY > 0:  
            if not self.tryMove(self.curPiece, self.curX, newY - 1):  
                break  
            newY -= 1  
        self.pieceDropped()  
    def oneLineDown(self):  
        if not self.tryMove(self.curPiece, self.curX, self.curY - 1):  
            self.pieceDropped()  
    def pieceDropped(self):  
        for i in range(4):  
            x = self.curX + self.curPiece.x(i)  
            y = self.curY - self.curPiece.y(i)  
            self.setShapeAt(x, y, self.curPiece.shape())  
        self.removeFullLines()  
        if not self.isWaitingAfterLine:  
            self.newPiece()  
    def removeFullLines(self):  
        numFullLines = 0  
        rowsToRemove = []  
        for i in range(Tetris.TetrisHeight):  
            n = 0  
            for j in range(Tetris.TetrisWidth):  
                if not self.shapeAt(j, i) == Tetrominoes.NoShape:  
                    n = n + 1  
            if n == 10:  
                rowsToRemove.append(i)  
        rowsToRemove.reverse()  
        for m in rowsToRemove:  
            for k in range(m, Tetris.TetrisHeight):  
                for l in range(Tetris.TetrisWidth):  
                    self.setShapeAt(l, k, self.shapeAt(l, k + 1))  
        numFullLines = numFullLines + len(rowsToRemove)  
        if numFullLines > 0:  
            self.numLinesRemoved = self.numLinesRemoved + numFullLines  
            self.emit(QtCore.SIGNAL("messageToStatusbar(QString)"),  
                str(self.numLinesRemoved))  
            self.isWaitingAfterLine = True  
            self.curPiece.setShape(Tetrominoes.NoShape)  
            self.update()  
    def newPiece(self):  
        self.curPiece = self.nextPiece  
        self.nextPiece.setRandomShape()  
        self.curX = Tetris.TetrisWidth / 2 + 1  
        self.curY = Tetris.TetrisHeight - 1 + self.curPiece.minY()  
        if not self.tryMove(self.curPiece, self.curX, self.curY):  
            self.curPiece.setShape(Tetrominoes.NoShape)  
            self.timer.stop()  
            self.isStarted = False  
            self.emit(QtCore.SIGNAL("messageToStatusbar(QString)"), "Game over")  
    def tryMove(self, newPiece, newX, newY):  
        for i in range(4):  
            x = newX + newPiece.x(i)  
            y = newY - newPiece.y(i)  
            if x < 0 or x >= Tetris.TetrisWidth or y < 0 or y >= Tetris.TetrisHeight:  
                return False  
            if self.shapeAt(x, y) != Tetrominoes.NoShape:  
                return False  
        self.curPiece = newPiece  
        self.curX = newX  
        self.curY = newY  
        self.update()  
        return True  
    def drawSquare(self, painter, x, y, shape):  
        colorTable = [0x000000, 0xCC6666, 0x66CC66, 0x6666CC,  
                      0xCCCC66, 0xCC66CC, 0x66CCCC, 0xDAAA00]  
        color = QtGui.QColor(colorTable[shape])  
        painter.fillRect(x + 1, y + 1, self.squareWidth() - 2,  
            self.squareHeight() - 2, color)  
        painter.setPen(color.light())  
        painter.drawLine(x, y + self.squareHeight() - 1, x, y)  
        painter.drawLine(x, y, x + self.squareWidth() - 1, y)  
        painter.setPen(color.dark())  
        painter.drawLine(x + 1, y + self.squareHeight() - 1,  
            x + self.squareWidth() - 1, y + self.squareHeight() - 1)  
        painter.drawLine(x + self.squareWidth() - 1,  
            y + self.squareHeight() - 1, x + self.squareWidth() - 1, y + 1)  
class Tetrominoes():  
    NoShape = 0  
    ZShape = 1  
    SShape = 2  
    LineShape = 3  
    TShape = 4  
    SquareShape = 5  
    LShape = 6  
    MirroredLShape = 7  
class Shape():  
    coordsTable = (  
        ((0, 0),     (0, 0),     (0, 0),     (0, 0)),  
        ((0, -1),    (0, 0),     (-1, 0),    (-1, 1)),  
        ((0, -1),    (0, 0),     (1, 0),     (1, 1)),  
        ((0, -1),    (0, 0),     (0, 1),     (0, 2)),  
        ((-1, 0),    (0, 0),     (1, 0),     (0, 1)),  
        ((0, 0),     (1, 0),     (0, 1),     (1, 1)),  
        ((-1, -1),   (0, -1),    (0, 0),     (0, 1)),  
        ((1, -1),    (0, -1),    (0, 0),     (0, 1))  
    )  
    def __init__(self):  
        self.coords = [[0,0] for i in range(4)]  
        self.pieceShape = Tetrominoes.NoShape  
        self.setShape(Tetrominoes.NoShape)  
    def shape(self):  
        return self.pieceShape  
    def setShape(self, shape):  
        table = Shape.coordsTable[shape]  
        for i in range(4):  
            for j in range(2):  
                self.coords[i][j] = table[i][j]  
        self.pieceShape = shape  
    def setRandomShape(self):  
        self.setShape(random.randint(1, 7))  
    def x(self, index):  
        return self.coords[index][0]  
    def y(self, index):  
        return self.coords[index][1]  
    def setX(self, index, x):  
        self.coords[index][0] = x  
    def setY(self, index, y):  
        self.coords[index][1] = y  
    def minX(self):  
        m = self.coords[0][0]  
        for i in range(4):  
            m = min(m, self.coords[i][0])  
        return m  
    def maxX(self):  
        m = self.coords[0][0]  
        for i in range(4):  
            m = max(m, self.coords[i][0])  
        return m  
    def minY(self):  
        m = self.coords[0][1]  
        for i in range(4):  
            m = min(m, self.coords[i][1])  
        return m  
    def maxY(self):  
        m = self.coords[0][1]  
        for i in range(4):  
            m = max(m, self.coords[i][1])  
        return m  
    def rotatedLeft(self):  
        if self.pieceShape == Tetrominoes.SquareShape:  
            return self  
        result = Shape()  
        result.pieceShape = self.pieceShape  
        for i in range(4):  
            result.setX(i, self.y(i))  
            result.setY(i, -self.x(i))  
        return result  
    def rotatedRight(self):  
        if self.pieceShape == Tetrominoes.SquareShape:  
            return self  
        result = Shape()  
        result.pieceShape = self.pieceShape  
        for i in range(4):  
            result.setX(i, -self.y(i))  
            result.setY(i, self.x(i))  
        return result  
