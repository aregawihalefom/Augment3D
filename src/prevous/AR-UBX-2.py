import cv2
import numpy as np


# mouse callback function
def draw_shape(event, x, y, flags, param):
    global draw, xi, yi, new_line, xi_backup, yi_backup
    if event == cv2.EVENT_LBUTTONDOWN:
        draw = True
        xi.append(x)
        yi.append(y)
    # new_line += 1

    elif event == cv2.EVENT_MOUSEMOVE:
        if draw:
            xi.append(x)
            yi.append(y)

    elif event == cv2.EVENT_LBUTTONUP:
        xi.append(-4)
        yi.append(-4)
        new_line += 1
        draw = False

    elif event == cv2.EVENT_MOUSEWHEEL:
        xi_backup, yi_backup = xi, yi
        print(xi_backup)
        print("Cleared Mouse event")
        xi.clear()
        yi.clear()
        new_line = 0
    elif event == cv2.EVENT_RBUTTONDBLCLK:
        print("Button double clicked")
        xi, yi = xi_backup, yi_backup


def main():

    global draw, xi, yi
    start = False
    # pt1_x, pt1_y = 0, 0

    cap = cv2.VideoCapture(0)

    while True:

        _, img = cap.read()

        # find where are the break points for the lines ( -4)
        indices = [i for i, x in enumerate(xi) if x == -4]

        # Get the points of each line

        pts_x = []
        pts_y = []
        started = False
        start = 0

        # starts here
        for i in indices:

            # the first line
            if not started:
                pts_x.append(xi[start:i])
                pts_y.append(yi[start:i])
                started = True
            else:
                pts_x.append(xi[start + 1:i])
                pts_y.append(yi[start + 1:i])

            start = i

        for idx, item in enumerate(indices):

            for i in range(len(pts_x[idx])):
                if not i:  # to pass the first element and start from second
                    continue
                cv2.line(img, (pts_x[idx][i - 1], pts_y[idx][i - 1]), (pts_x[idx][i], pts_y[idx][i]),
                         color=(255, 255, 0), thickness=3)

        cv2.imshow(windowName, img)
        k = cv2.waitKey(1)
        if k == ord('p'):
            cv2.waitKey(-1)
        elif k == 27:
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    windowName = "REMOTE ASSISTANCE WITH AR "
    cv2.namedWindow(windowName)
    cv2.setMouseCallback(windowName, draw_shape)

    # Attributes for drawing
    draw = False  # True to start drawing ( changes when mouse down and off when up)
    show = False
    xi = []
    yi = []
    xi_backup = []
    yi_backup = []
    new_line = 0

    main()
