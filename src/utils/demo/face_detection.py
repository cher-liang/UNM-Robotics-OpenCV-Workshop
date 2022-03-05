import cv2 as cv

face_cascade = cv.CascadeClassifier('data/models/haarcascade_frontalface_default.xml')


def face_detection():
    cap= cv.VideoCapture(0,cv.CAP_DSHOW)

    while True:
        ret,frame=cap.read()

        if ret:
            gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

            faces = face_cascade.detectMultiScale(gray, 1.1, 4)

            for (x, y, w, h) in faces:
                cv.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

            cv.imshow('Video',frame)
            
            k = cv.waitKey(30) & 0xff
            if k == 27: # press 'ESC' to quit
                break
        else:
            break

    cap.release()

    cv.destroyAllWindows()

if __name__ == '__main__':

    face_detection()