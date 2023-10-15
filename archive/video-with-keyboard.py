# importing libraries
import cv2
import numpy
import win32com.client as comclt
import time
# https://github.com/jitendrasb24/Motion-Detection-OpenCV


def motionDetection():
    wsh = comclt.Dispatch("WScript.Shell")

    def getMillis():
        return round(time.time() * 1000)

    cap = cv2.VideoCapture(0)
    # reading frames sequentially
    ret, frame1 = cap.read()
    ret, frame2 = cap.read()

    detectionCounter = 0
    movedTimer = getMillis() + 500
    itemDetected = False

    def getMotionDifference():
        diff = cv2.absdiff(frame1, frame2)
        diff_gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(diff_gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)

        kernel = numpy.ones((5, 5), numpy.uint8)
        dilated = cv2.dilate(thresh, kernel, iterations=3)
        contours, _ = cv2.findContours(
            dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        return contours

    def movementDetected(detected=False):

        if movedTimer > getMillis() - 400:
            print('Waiting for timer...')
            return

        if not detected:
            counter = incrementDetectionCounter()
            print('counter', counter)
            if counter == 5:
                moveToNextPlayer()
                incrementDetectionCounter(True)
        else:
            nonlocal itemDetected
            itemDetected = True
            print("Item has been detected!")

    def setMovementTimer(extra=0):
        nonlocal movedTimer
        movedTimer = getMillis() + extra

    def incrementDetectionCounter(reset=False):
        nonlocal detectionCounter

        if reset:
            detectionCounter = 0
            return

        detectionCounter += 1
        return detectionCounter

    def moveToNextPlayer():
        setMovementTimer()
        wsh.AppActivate("8224")     # select another application
        wsh.SendKeys("{DOWN}", 0)   # send the keys you want

    while cap.isOpened():

        if itemDetected:
            print('itemDetected', itemDetected)
            if cv2.waitKey(100) & 0xFF == ord("j"):
                moveToNextPlayer()
                setMovementTimer(500)
                itemDetected = False
        else:

            contours = getMotionDifference()
            if len(contours) == 0:
                movementDetected()

            else:
                for contour in contours:
                    (x, y, w, h) = cv2.boundingRect(contour)
                    if cv2.contourArea(contour) < 900:
                        continue

                    cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    cv2.putText(frame1, "STATUS: {}".format('MOTION DETECTED'), (10, 60), cv2.FONT_HERSHEY_SIMPLEX,
                                1, (217, 10, 10), 2)
                    movementDetected(True)

            cv2.imshow("Video", frame1)
            frame1 = frame2
            ret, frame2 = cap.read()

            if cv2.waitKey(50) & 0xFF == ord("q"):
                break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    motionDetection()
