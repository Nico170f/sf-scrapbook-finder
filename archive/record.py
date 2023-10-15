import cv2
import numpy
import time
import mss


def getDifference(a, b):
    print(a, b)
    if a > 0 and b > 0:
        return b - a

    if a < 0 and b < 0:
        return abs(a - b)

    if a < 0 and b > 0:
        return b - a


with mss.mss() as sct:
    # Part of the screen to capture

    positions = [
        (-769, 271),
        (-89, 840)
    ]

    # monitor = {"top": 100, "left": -762, "width": 800, "height": 640}
    width = getDifference(positions[0][0], positions[1][0])
    height = positions[1][1] - positions[0][1]
    print(height)
    print(width)
    monitor = {"top": positions[0][1],
               "left": positions[0][0], "width": width, "height": height}

    while "Screen capturing":
        last_time = time.time()

        # Get raw pixels from the screen, save it to a Numpy array
        img = numpy.array(sct.grab(monitor))

        # Display the picture
        cv2.imshow("OpenCV/Numpy normal", img)

        # Display the picture in grayscale
        # cv2.imshow('OpenCV/Numpy grayscale',
        #            cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY))

        # print(f"fps: {1 / (time.time() - last_time)}")

        # Press "q" to quit
        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break
