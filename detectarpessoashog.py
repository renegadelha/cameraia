import cv2


hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

cap = cv2.VideoCapture(0)
frame_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    frame = cv2.resize(frame, (320, 240))
    frame_count += 1

    rects = []
    if frame_count % 10 == 0:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rects, _ = hog.detectMultiScale(gray, winStride=(8, 8), padding=(8, 8), scale=1.05)

    if len(rects) > 0:
        print('achei:', len(rects))
    #for (x, y, w, h) in rects:
    #    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    #cv2.imshow("Detecção HOG + SVM", frame)

cap.release()

