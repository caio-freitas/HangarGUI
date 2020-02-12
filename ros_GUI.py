#!/usr/bin/env python

import os
import rospy
from MAV import MAV
import sys
import cv2
from hangar import *
import time
from skimage import io
import skimage
#rom dronekit import Vehicle

from PyQt4 import QtGui, QtCore # QtCore to make button do things
#from takeoff_n_land import run as takeoffnland


#thumbnail_url = 'https://openapi.icloseli.com/rest/service/camera/xxxxS_000c43b93fdb/thumbnail/current?size=1920x1080&token=5001423dc99544fc839c88f7f0bd86c8'
#thumbnail_url = 'https://file-us-ali.closeli.com/d0dc3a80-ebf7-42ef-afc4-c0afc7ed4b66'


rospy.init_node("GUI")
drone = MAV("Shomer")

IMG_SIZE = (924, 520)

class CamThread(QtCore.QThread):

    changePixmap = QtCore.pyqtSignal(QtGui.QImage)
    hangar = Hangar()

    def run(self):
        import skimage
        im = self.hangar.get_img()
        if im == None:
            pixmap = QtGui.QPixmap(os.getcwd() + '/imgs/no_image.png')
            pixmap = pixmap.scaled(530, 300)
        else:
            im = skimage.transform.resize(im, (300, 530))
            arr = skimage.img_as_ubyte(im)
            img = QtGui.QImage(arr.data, arr.shape[1], arr.shape[0],
                        arr.strides[0], QtGui.QImage.Format_RGB888)
            pixmap = QtGui.QPixmap.fromImage(img)
        image = QtGui.QLabel(self)

        image.setGeometry(670, 138, 530, 300)
        image.setPixmap(pixmap)
        image.show()

class Window(QtGui.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        self.closed = True
        self.lights = "off"
        self.charge = 0
        dw = 400
        dh = 300
        self.setGeometry(0, 0, 1280, 720)

        self.setWindowIcon(QtGui.QIcon('imgs/H.png'))
        self.hangar = Hangar()
        self.setWindowTitle("Control - " + str(self.hangar.state))

        #self.drone = Vehicle()

        takeoffDrone = QtGui.QAction("Takeoff Drone", self)
        takeoffDrone.setShortcut("Ctrl+Shift+T")
        takeoffDrone.setStatusTip("Takes drone off")
        takeoffDrone.triggered.connect(self.takeoff_drone) # do something

        landDrone = QtGui.QAction("Land Drone", self)
        landDrone.setShortcut("Ctrl+Shift+L")
        landDrone.setStatusTip("Lands drone")
        landDrone.triggered.connect(self.land_drone)

        self.statusBar()

        mainMenu = self.menuBar()
        droneMenu = mainMenu.addMenu("&Drone")
        droneMenu.addAction(takeoffDrone) #whatever action
        droneMenu.addAction(landDrone)
        #self.setBackgroundRole(QtGui.QPalette.brightText)

        #QtGui.QApplication.setStyle(QtGui.QStyleFactory.create("cleanlooks"))
        self.setStyleSheet("QWidget{background-image: url(./imgs/background.jpeg)}")
        self.setToolButtonStyle(2)
        self.backgroundRole()
        self.show_camera()

        self.home()

    def closeEvent(self, event):
        event.ignore()
        self.close_application()

    def home(self):
        self.setWindowTitle("Hangar Control - " + str(self.hangar.state))



        width = self.frameGeometry().getRect()[2] - self.frameGeometry().getRect()[0]
        height = self.frameGeometry().getRect()[3] - self.frameGeometry().getRect()[1]

        ############## Open / Close button #################
        self.h_btn = QtGui.QPushButton(self)
        self.h_btn.resize(80, 80)#sizeHint()
        self.h_btn.move(1050, 587)
        self.h_btn.setStyleSheet("background:gray; font:bold 18px; padding:3px; ")
        self.h_btn.clicked.connect(self.toggle_hangar)    # What to do when button is clicked
                # Safety
        # else:
        #     logging.error("Hanger neither closed or open")
        ############## Show Image button ##################
        img_btn = QtGui.QPushButton("Show Image", self)
        img_btn.resize(143, 142)
        img_btn.move(716, 549)
        img_btn.setStyleSheet("background:gray; font:bold 18px; padding:3px")
        img_btn.clicked.connect(self.show_camera)    # What to do when button is clicked
        #self.show_camera()
        ##################################################
        ############## lights toggle button ##################
        self.lights_btn = QtGui.QPushButton(self)
        self.lights_btn.resize(28, 28)
        self.lights_btn.move(634, 548)
        self.lights_btn.setStyleSheet("background:green; font:bold 18px; padding:3px")
        self.lights_btn.clicked.connect(self.toggle_lights)    # What to do when button is clicked
        #self.show_camera()
        ##################################################

        ######### Toolbar Actions ###############
        takeoffAction = QtGui.QAction(QtGui.QIcon('imgs/takeoff.png'), "Takeoff the drone", self)
        takeoffAction.triggered.connect(self.takeoff_drone)

        landAction = QtGui.QAction(QtGui.QIcon('imgs/land.svg'), "Land the drone", self)
        landAction.triggered.connect(self.land_drone)

        #################################################
        # Toolbar itself
        self.toolBar = self.addToolBar("Drone")
        self.toolBar.addAction(takeoffAction)
        self.toolBar.addAction(landAction)


        self.batteryProgress = QtGui.QProgressBar(self)
        self.batteryProgress.setGeometry(95, 184, 382, 140)
        self.batteryProgress.setValue(drone.battery.percentage)

        self.btn = QtGui.QPushButton("Charge", self)
        self.btn.move(20, 225)
        self.btn.resize(60, 80)

        self.btn.clicked.connect(self.charge_drone)
        self.btn.setStyleSheet("background:gray")
        print(self.style().objectName())
        #self.styleChoice = QtGui.QLabel("Windows", self)

        th = CamThread()
        th.changePixmap.connect(self.show_pixmap)
        th.start()

        self.show()

    def show_pixmap(self, img):
        pixmap = QtGui.QPixmap.fromImage(img)
        image = QtGui.QLabel(self)
        image.setGeometry(670, 138, 530, 300)
        image.setPixmap(pixmap)
        image.show()

    def show_camera(self):
        import skimage
        im = self.hangar.get_img()
        if im == None:
            pixmap = QtGui.QPixmap(os.getcwd() + '/imgs/no_image.png')
            pixmap = pixmap.scaled(530, 300)
        else:
            im = skimage.transform.resize(im, (300, 530))
            arr = skimage.img_as_ubyte(im)
            img = QtGui.QImage(arr.data, arr.shape[1], arr.shape[0],
                        arr.strides[0], QtGui.QImage.Format_RGB888)
            pixmap = QtGui.QPixmap.fromImage(img)
        image = QtGui.QLabel(self)

        image.setGeometry(670, 138, 530, 300)
        image.setPixmap(pixmap)
        image.show()

    def charge_drone(self):
        self.batteryProgress.setValue(drone.battery.percentage)
        self.batteryProgress.show()
        ###### Show off #########
        # while self.charge < 100:
        #     self.charge += 0.0001
        #     self.batteryProgress.setValue(self.charge)
        #     #time.sleep(0.1)



    def close_application(self):
        choice = QtGui.QMessageBox.question(QtGui.QWidget(), 'Leave?',
                                            "Are you quitting?",
                                            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if choice == QtGui.QMessageBox.Yes:
            print("Closing Windows!")
            sys.exit()

    def toggle_hangar(self):
        print(self.closed)
        if self.closed == True:
            self.hangar.open()
            self.setWindowTitle("Hangar Control - Open - " + str(self.charge) + "%")
            self.h_btn = QtGui.QPushButton("Close", self)
            self.h_btn.setStyleSheet("background : red")
            self.closed = False
            # h_btn.resize(80, 80)#sizeHint()
            # h_btn.move(int(0.7*width), 300)
            #h_btn.clicked.connect(self.open_hangar)    # What to do when button is clicked
        else:
            self.hangar.close()
            self.setWindowTitle("Hangar Control - Closed - " + str(self.charge) + "%")
            self.h_btn = QtGui.QPushButton("Open", self)
            self.h_btn.setStyleSheet("background : green")
            self.closed = True

        self.h_btn.clicked.connect(self.toggle_hangar)
        self.h_btn.resize(80, 80)#sizeHint()
        self.h_btn.move(1050, 587)
        self.h_btn.show()

    def toggle_lights(self):
        if self.lights == "on":
            self.hangar.lights_off()
            self.lights_btn = QtGui.QPushButton("Off", self)
            self.lights_btn.setStyleSheet("background:red; font:bold 12px")
            self.lights = "off"

        elif self.lights == "off":
            self.hangar.lights_on()
            self.lights_btn = QtGui.QPushButton("On", self)
            self.lights_btn.setStyleSheet("background:green; font:bold 12px")
            self.lights = "on"
        self.lights_btn.clicked.connect(self.toggle_lights)
        self.lights_btn.resize(28, 28)
        self.lights_btn.move(634, 548)
        self.lights_btn.show()



    ######### fake methods ##########
    def takeoff_drone(self):
        choice = QtGui.QMessageBox.question(QtGui.QWidget(), 'Takeoff the drone',
                                            "Are you sure you want to takeoff the drone?",
                                            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        #choice.setStyleSheet("background: white")
        if choice == QtGui.QMessageBox.Yes:
            print("Takeoff drone")
            drone.takeoff(3)


    def land_drone(self):
        choice = QtGui.QMessageBox.question(QtGui.QWidget(), 'Land the drone',
                                            "Are you sure you want to land the drone?",
                                            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if choice == QtGui.QMessageBox.Yes:
            print("Landing drone")
            drone.precision_landing()
        
    #################################
def run():
    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())


if __name__ == "__main__":
    run()
