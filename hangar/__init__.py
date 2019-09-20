from skimage import io
import httplib2
import cv2
import sys
import logging
from PyQt4 import QtGui, QtCore # QtCore to make button do things
ESP_IP = '192.168.1.21'
IMG_URL = 'https://openapi.icloseli.com/rest/service/camera/xxxxS_000c43b93fdb/thumbnail/current?size=1920x1080&token=5001423dc99544fc839c88f7f0bd86c8'

"""
    Class created for all hangar operations, such as:
    - Turning on and off illumination
    - Opening and closing the hangar itself
    - Locking drone for recharge and releasing it # TO BE IMPLEMENTED! #
"""
class Hangar():
    def __init__(self, esp_ip=ESP_IP, img_url=IMG_URL):
        self.state = None
        ## Url to access the hangar camera image ##
        self.image_url = IMG_URL if img_url==None else esp_ip
        # ESP32 IP adress
        self.esp_ip = ESP_IP if esp_ip==None else esp_ip
        self.http = httplib2.Http()

    def show_img(self):
        while not KeyboardInterrupt:
            # Reads image from url
            img = io.imread(self.image_url)

            # Converts color type from BGR to RGB
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # The image size can be changed in the line below
            img = cv2.resize(img, (640, 480), interpolation=cv2.INTER_CUBIC)
            cv2.imshow("Image", img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            frequency = 2.0 # Hz
            time.sleep(1/frequency)

    def get_img(self):
        """
            Method that returns the hangar camera image at the moment it's called
        """
        return io.imread(IMG_URL)# cv2.cvtColor(,cv2.COLOR_BGR2RGB)

    def open(self):
        """
            Method that sends a request to the ESP32, on the pre-established IP adress,
            with the string 'open'
            It is inferred that in the ESP32, there is implemented the functions
            that actually move the actuators in order to get the hangar openned
        """
        logging.warning("Abrindo Hangar")
        PATH = 'open'
        data = 'open'
        url = "http://" + self.esp_ip + '/' + PATH
        try:
            self.state = 'open'
            response, content = self.http.request(url, "PUT", body=data)
        except Exception as e:
            print(e)
            pass


    def close(self):
        """
            Method that sends a request to the ESP32, on the pre-established IP adress,
            with the string 'close'
            It is inferred that in the ESP32, there is implemented the functions
            that actually move the actuators in order to get the hangar closed
        """
        logging.warning("Fechando Hangar")
        PATH = 'close'
        data = 'close'
        url = "http://" + self.esp_ip + '/' + PATH
        try:
            self.state = 'closed'
            response, content = self.http.request(url, "PUT", body=data)
        except Exception as e:
            print(e)
            pass


    def stop(self):
        """
            TEMPORARY
            Method that sends a request to the ESP32, on the pre-established IP adress,
            with the string 'stop'
            (It is inferred that in the ESP32, there is implemented the functions
            that stop all hangar's motors)
        """
        logging.warning("Parando Hangar")
        PATH = 'stop'
        data = 'stop'
        url = "http://" + self.esp_ip + '/' + PATH
        try:
            response, content = self.http.request(url, "PUT", body=data)
        except Exception as e:
            pass

    def lights_on(self):
        """
            Method that sends a request to the ESP32, on the pre-established IP adress,
            with the string 'lights_on'
        """
        logging.warning("Acendendo luzes do hangar")
        PATH = 'lights_on'
        data = 'lights_on'
        url = "http://" + self.esp_ip + '/' + PATH
        try:
            response, content = self.http.request(url, "PUT", body=data)
        except Exception as e:
            print(e)
            pass

    def lights_off(self):
        """
            Method that sends a request to the ESP32, on the pre-established IP adress,
            with the string 'lights_off'
        """
        logging.warning("Apagando luzes do hangar")
        PATH = 'lights_off'
        data = 'lights_off'
        url = "http://" + self.esp_ip + '/' + PATH
        try:
            response, content = self.http.request(url, "PUT", body=data)
        except Exception as e:
            print(e)
            pass
