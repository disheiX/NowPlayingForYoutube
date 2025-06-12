from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PIL.ImageQt import ImageQt
import time
import sys
import warnings
warnings.simplefilter("ignore", UserWarning)
sys.coinit_flags = 2
from get_data import *
from get_info import *
from Marquee import MarqueeLabel


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        
        # Load stylesheets
        styles_files =["style.qss", 'artistStyle.qss']
        styles = []
        for style in styles_files:
            with open(style,"r") as styleSheet:
                styles.append(styleSheet.read())
        
        # Adding custom fonts
        fontId = QFontDatabase.addApplicationFont("Montserrat-SemiBold.ttf")
        families = QFontDatabase.applicationFontFamilies(fontId)
        # font = QFont(families[0])
        # font_db = QFontDatabase()
        # font_db.addApplicationFont()
        
        uic.loadUi('main.ui', self)
        self.setStyleSheet(styles[0])        
        
        # Setting widgets and stuff
        self.centralWidget = self.findChild(QWidget, 'centralwidget')
        self.imageViewer = self.findChild(QLabel, 'image_viewer')
        self.textTitle = self.findChild(QLabel, 'text_title')
        self.textTitle.setStyleSheet('padding-left: 10px')
        self.artistLabel = self.findChild(QLabel, 'artist_name')
        self.artistLabel.setStyleSheet(styles[1])
        self.artistLabel.setScroll(False)
        self.verticalLayout = self.findChild(QVBoxLayout, 'vertical_layout')
        self.spacer = self.verticalLayout.itemAt(0)
       
        # Setting up threads
        self.thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)
        self.worker.image.connect(self.update_image)
        self.worker.title.connect(self.update_title)
        self.worker.artist.connect(self.set_artist)
        self.thread.start()
        self.worker.start()
        self.show()

    def update_image(self, im):
        # self.imageViewer.setGraphicsEffect(QGraphicsOpacityEffect())
        self.pixmap = QPixmap.fromImage(ImageQt(im))
        self.imageViewer.setPixmap(self.pixmap)
        self.imageViewer.adjustSize()

    def update_title(self, title):
        self.textTitle.setTitle(title)

    def stop_thread(self):
        self.worker.stop()
        self.thread.quit()
        self.thread.wait()

    def set_artist(self, artistName):
        self.remove_artist()
        if artistName != None:
            self.verticalLayout.insertItem(0, self.spacer)
            self.artistLabel.setText(artistName)
        # self.textTitle.h = 22

    def remove_artist(self):
        self.verticalLayout.removeItem(self.spacer)
        self.artistLabel.setText('')
        # self.textTitle.h = 30


class AnimationLabel(QLabel):
    def __init__(self, *args, **kwargs):
        QLabel.__init__(self, *args, **kwargs)
        self.effect = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.effect)
        self.animation = QPropertyAnimation(self.effect, b"opacity")

class Worker(QThread):
    title = pyqtSignal(object)
    image = pyqtSignal(object)
    artist = pyqtSignal(object)
    def __init__(self):
        super(Worker, self).__init__()
        self.run = True
        handle, pid = 197446, 16160
        self.wrapper = get_wrapper(handle, pid)

    @pyqtSlot()
    def run(self):
        while self.run:
            prev_song = clean_song(self.wrapper)        
            data = get_data(self.wrapper)
            while data == None:
                sleep(3)
                data = get_data(self.wrapper)
            img = get_img(data)
            metadata = get_metadata(data)
            if not metadata:
                self.title.emit(data[0])
                self.artist.emit(None)
            else:
                self.title.emit(metadata[0])
                self.artist.emit(metadata[1])
            self.image.emit(img)
            while self.run and clean_song(self.wrapper) == prev_song:
                sleep(3)
        
if __name__ == '__main__': 
    app = QApplication(sys.argv) 
UIWindow = UI()
app.exec()
