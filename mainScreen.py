from cv2 import cv2
import os
from datetime import datetime
from imutils.video import VideoStream
import face_recognition
import imutils
import pickle
import time
import cv2
from imutils import paths
detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
def screen(data_obj):

    while(data_obj.get_mode()):

        if(data_obj.get_screen()):
            frame = cv2.imread("resim.jpg")
            s = data_obj.get_data()
            cv2.putText(frame,"Yeni kayit yapmak icin 'Yeni'",(170,150),cv2.FONT_ITALIC,1,(255,255,255),2)
            cv2.putText(frame,"Cihazi baslatmak icin 'baslat'",(170,200),cv2.FONT_ITALIC,1,(255,255,255),2)
            cv2.putText(frame,"diye seslenebilirsiniz",(220,250),cv2.FONT_ITALIC,1,(255,255,255),2)
            cv2.putText(frame, "{}".format(s[0]), (220, 300), cv2.FONT_ITALIC, 1, (255, 255, 255), 2)
            cv2.putText(frame, "{}".format(s[1]), (170, 350), cv2.FONT_ITALIC, 1, (255, 255, 255), 2)
            cv2.imshow("Frame", frame)
        else:
            detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
            total = 0
            cap = cv2.VideoCapture(0)
            datadir = 'dataset'
            name=data_obj.get_name()
            if os.path.isdir('dataset'):
                pass
            else:
                os.mkdir(datadir)
            path1 = '{}'.format(name)
            path = os.path.join(datadir, path1)
            os.mkdir(path)
            a = datetime.now()
            while (True):
                ret,frame = cap.read()
                orig = frame.copy()
                frame = imutils.resize(frame, width=800)
                rects = detector.detectMultiScale(
                    cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), scaleFactor=1.1,
                    minNeighbors=5, minSize=(30, 30))
                for (x, y, w, h) in rects:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                cv2.imshow("Frame", frame)

                b = datetime.now()
                if ((b - a).seconds >= 2):
                    a = b
                    p = os.path.sep.join([path, "{}.png".format(
                        str(total))])
                    cv2.imwrite(p, orig)
                    if total == 10:
                        break
                    total += 1

            cap.release()
            data_obj.set_screen(True)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
    if (not data_obj.get_mode()):

        imagePaths = list(paths.list_images("dataset"))

        knownEncodings = []
        knownNames = []

        for (i, imagePath) in enumerate(imagePaths):
            name = imagePath.split(os.path.sep)[-2]

            image = cv2.imread(imagePath)
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            boxes = face_recognition.face_locations(rgb, model="hog")
            encodings = face_recognition.face_encodings(rgb, boxes)

            for encoding in encodings:
                knownEncodings.append(encoding)
                knownNames.append(name)

        data = {"encodings": knownEncodings, "names": knownNames}
        f = open("encodings.pickle", "wb")
        f.write(pickle.dumps(data))
        f.close()

        data = pickle.loads(open("encodings.pickle", "rb").read())
        detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

        vs = VideoStream(src=0).start()
        time.sleep(2.0)

        while True:
            frame = vs.read()
            frame = imutils.resize(frame, width=800)

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            rects = detector.detectMultiScale(gray, scaleFactor=1.1,
                                              minNeighbors=5, minSize=(30, 30),
                                              flags=cv2.CASCADE_SCALE_IMAGE)

            boxes = [((int)(y), (int)(x + w), (int)(y + h), (int)(x)) for (x, y, w, h) in rects]

            encodings = face_recognition.face_encodings(rgb, boxes)
            names = []

            for encoding in encodings:
                matches = face_recognition.compare_faces(data["encodings"],
                                                         encoding)
                name = "Bilinmeyen"

                if True in matches:
                    matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                    counts = {}

                    for i in matchedIdxs:
                        name = data["names"][i]
                        counts[name] = counts.get(name, 0) + 1

                    name = max(counts, key=counts.get)

                names.append(name)

            for ((top, right, bottom, left), name) in zip(boxes, names):
                cv2.rectangle(frame, (left, top), (right, bottom),
                              (0, 255, 0), 2)
                y = top - 15 if top - 15 > 15 else top + 15
                cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
                            0.75, (0, 255, 0), 2)

            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                break

        cv2.destroyAllWindows()
