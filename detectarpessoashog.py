import cv2


hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

cap = cv2.VideoCapture(0)
frame_count = 0
contador = 0

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    frame = cv2.resize(frame, (320, 240))
    frame_count += 1

    rects = []
    if frame_count % 15 == 0:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rects, _ = hog.detectMultiScale(gray, winStride=(8, 8), padding=(8, 8), scale=1.05)

    if len(rects) > 0:
        nome_arquivo = f"capturas/frame_{contador}.jpg"
        cv2.imwrite(nome_arquivo, frame)
        contador += 1

        print('achei:', len(rects))

cap.release()

