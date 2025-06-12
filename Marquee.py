# from PyQt6.QtGui import *
# from PyQt6.QtWidgets import *
# from PyQt6.QtCore import *

import sys

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class MarqueeLabel(QLabel):
    def __init__(self, parent=None):
        QLabel.__init__(self, parent)
        self.h = self.height()
        self.px = 45
        self.py = self.h
        self._direction = Qt.LayoutDirection.RightToLeft
        self.setWordWrap(True)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(24)
        self._speed = 0
        self.textLength = 0
        self.fontPointSize = 0
        self.timeAnimation = 0
        self.allowScroll = True
        # self.effect = QGraphicsOpacityEffect()

        # self.setGraphicsEffect(self.effect)
        # print(help(self.effect.draw(self.painter)))
        # self.animation = QPropertyAnimation(self.effect, b"opacity")

        # self.setFixedHeight(self.fontMetrics().height())

    def setFont(self, font):
        QLabel.setFont(self, font)
        # self.setFixedHeight(self.fontMetrics().height())

    def updateCoordinates(self):
        self.fontPointSize = self.font().pointSize() / 2
        self.textLength = self.fontMetrics().boundingRect(self.text()).width()

    def resizeEvent(self, event):
        self.textLength = self.fontMetrics().boundingRect(self.text()).width()
        QLabel.resizeEvent(self, event)
        if self.textLength > 350 and self.allowScroll:
            self.setSpeed(1)
        else:
            self.setSpeed(0)

    def setTitle(self, title):
        self.setText(title)
        self.textLength = self.fontMetrics().boundingRect(self.text()).width()
        self.px = 45
        self.timeAnimation = 0
        if self.textLength > 350:
            self.setSpeed(1)

    def paintEvent(self, event):
        painter = QPainter(self)
        if self.timeAnimation < 30:
            self.animate(painter)
        else:
            if self.textLength > 350:
                self.px -= self.speed()
                if self.px <= -self.textLength:
                    self.px = self.width()
            else:
                self.px = 15
        painter.drawText(self.px, self.py + self.fontPointSize, self.text())
        painter.translate(self.px, 0)

    def speed(self):
        return self._speed

    def setSpeed(self, speed):
        self._speed = speed

    def animate(self, painter):
        painter.setOpacity(self.timeAnimation/30)
        if self.speed() == 0:
            self.px -= 1
        else:        
            self.px -= self.speed()
        self.timeAnimation+=1

    def setScroll(self, option):
        self.allowScroll = option
    