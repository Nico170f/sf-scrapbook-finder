# importing libraries
import cv2
import numpy
import win32com.client as comclt
import time

from sf.image import ImageProcess
# https://github.com/jitendrasb24/Motion-Detection-OpenCV

wsh = comclt.Dispatch("WScript.Shell")


class ItemFinder:
    framesToCheck = 5
    characterChangeDelay = 1000
    applicationID = "8224"
    windowTitle = 'Scapbook Finder - Output'

    def __init__(self, solver):
        self.solver = solver
        self.detectionCounter = 0
        self.movedTimer = 0  # self.getMillis() + 1000
        self.itemDetected = False
        self.windowOpen = False

        self.startVideoCapture()

    def getMillis(self, extraDelay=0):
        return round(time.time() * 1000) + extraDelay

    def getMotionDifference(self, frame1, frame2):
        diff = cv2.absdiff(frame1, frame2)
        diff_gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(diff_gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        kernel = numpy.ones((5, 5), numpy.uint8)
        dilated = cv2.dilate(thresh, kernel, iterations=3)
        contours, _ = cv2.findContours(
            dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        return contours

    def movementDetected(self, movementDetected=False):
        if self.movedTimer > self.getMillis() - self.characterChangeDelay:
            return

        if not movementDetected:
            self.incrementDetectionCounter()
            print(f'Frame: {self.detectionCounter}')
            if self.detectionCounter == self.framesToCheck:
                self.moveToNextPlayer()
                self.incrementDetectionCounter(True)
        else:
            self.itemDetected = True
            print('Item has been detected. Press "J" to continue.')

    def setMovementTimer(self, extraDelay=0):
        print('Waiting for timer...')
        self.movedTimer = self.getMillis(extraDelay)

    def incrementDetectionCounter(self, resetCounter=False):
        if resetCounter:
            self.detectionCounter = 0
        else:
            self.detectionCounter += 1

    def moveToNextPlayer(self):
        self.setMovementTimer()
        wsh.AppActivate(self.applicationID)
        wsh.SendKeys("{DOWN}", 0)

    def startVideoCapture(self):
        print('Starting video capture...')

        videoCapture = cv2.VideoCapture(0)
        ret, frame1 = videoCapture.read()
        ret, frame2 = videoCapture.read()
        self.setMovementTimer(500)

        while videoCapture.isOpened():

            if self.itemDetected:
                if (cv2.getWindowProperty(self.windowTitle, cv2.WND_PROP_VISIBLE) < 1):
                    break

                imageStr = f'{self.getMillis()}.jpg'
                # print(imageStr)
                cv2.imwrite(f'output/{imageStr}', frame1)
                ImageProcess(imageStr)
                # return
                self.moveToNextPlayer()
                self.setMovementTimer(500)
                self.itemDetected = False
                # return

                # if cv2.waitKey(50) & 0xFF == ord("q") or 0xFF == ord("j"):
                #     return

                # print('Item has been detected. Press "J" to continue.')
                # if cv2.waitKey(500) & 0xFF == ord("j"):
                #     self.moveToNextPlayer()
                #     self.setMovementTimer(500)
                #     self.itemDetected = False
            else:

                contours = self.getMotionDifference(frame1, frame2)
                if len(contours) == 0:
                    self.movementDetected()
                else:
                    for contour in contours:
                        (x, y, w, h) = cv2.boundingRect(contour)
                        if cv2.contourArea(contour) < 900:
                            continue

                        cv2.rectangle(frame1, (x, y),
                                      (x+w, y+h), (0, 255, 0), 2)
                        cv2.putText(frame1, "STATUS: {}".format('MOTION DETECTED'), (10, 60), cv2.FONT_HERSHEY_SIMPLEX,
                                    1, (217, 10, 10), 2)

                        self.movementDetected(True)

                cv2.imshow(self.windowTitle, frame1)
                frame1 = frame2
                ret, frame2 = videoCapture.read()

                if cv2.waitKey(50) & 0xFF == ord("q"):
                    break

                if (cv2.getWindowProperty(self.windowTitle, cv2.WND_PROP_VISIBLE) < 1):
                    break

        videoCapture.release()
        cv2.destroyAllWindows()
        self.solver.prompt()


# itemFinder = ItemFinder('test')
