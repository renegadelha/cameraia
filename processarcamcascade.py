import cv2

body_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)

frame_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    #frame = cv2.resize(frame, (320, 240))
    frame_count += 1

    if frame_count % 10 == 0:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        bodies = body_cascade.detectMultiScale(gray, 1.1, 3, minSize=(30, 30))
    else:
        bodies = []

    print(len(bodies))
    #for (x, y, w, h) in bodies:
    #    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)


cap.release()

