import requests
import time
url = 'https://file-us-ali.closeli.com/d0dc3a80-ebf7-42ef-afc4-c0afc7ed4b66'
deviceId = 'xxxxS_000c43b93fdb'
productKey = '6f425be2-e27'
#url = 'https://eyeplusiot.com/g/managed_switch/list'
url = 'https://eyeplusiot.com/api/lookup/sendMessage'
#url = 'https://eyeplusiot.com/dist/cdn/eyeplus_201908291450/'
#xxxxS_000c43b93fdb

#r = requests.get(url , auth=('caiofreitas@usp.br', 'INVTech1'), verify=False)
#   print(r.status_code)
# r = requests.post(url,auth=('caiofreitas@usp.br1563218667505', 'INVTech1'), data='1', verify=False)
# print(r.status_code)

# APPNAME = "https://www.eyeplusiot.com"
# url = APPNAME + "/device/startLive?deviceId="+"xxxxS_000c43b93fdb"+"&did=" + "1203406"
# liveUrl=url+"&isFormEvent=true"+"&startTime=" + str(time.time()) + "&endTime=" + str(time.time() + 1) +"&eventId=" +object.eventId+"&c_key=" +object.c_key+'&downloadServer='+object.downloadServer;
"""

new Image().src = API_CAMERA_LIST + '?update=true';

function sendPing() {

    _cmdId++;

    var arcMessage = {};
    arcMessage.type = 7;
    arcMessage.cmdId = _cmdId;
    doSend(arcMessage);
    console.log("sendPing");

}

function doSend(message) {
    //console.log("send:"+JSON.stringify(message));
    if (_isConnected) {
        try {
            _socket.send(JSON.stringify(message));
        } catch (e) {
            console.log("handle exception");
        }
    } else {
        console.log("websocket is lost connection");
    }
}
"""
import cv2
import urllib
import pdb
import numpy as np

class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        #self.video = urllib.urlopen('https://file-us-ali.closeli.com/c382230a-5fe7-43af-945d-da95fa32aa89')   #cv2.VideoCapture(0)
        self.video = urllib.urlopen('https://openapi.icloseli.com/rest/service/camera/xxxxS_000c43b93fdb/thumbnail/current?size=1920x1080&token=5001423dc99544fc839c88f7f0bd86c8')
    # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')
    def __del__(self):
        self.video.release()
    def get_frame(self):
        bytes=''

        while True:
            # pdb.set_trace()
            bytes+=self.video.read(1024)
            a = bytes.find('\xff\xd8')
            b = bytes.find('\xff\xd9')
            if a!=-1 and b!=-1:
                jpg = bytes[a:b+2]
                bytes= bytes[b+2:]
                img = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.IMREAD_COLOR)
                # pdb.set_trace()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                return gray#.tobytes()



def main():
    cam = VideoCamera()
    while not cv2.waitKey(5) & 0xFF == 27:
        cv2.imshow('img', cam.get_frame())
        time.sleep(0.1)
    #print(cam.get_frame())

if __name__ == "__main__":
    main()
