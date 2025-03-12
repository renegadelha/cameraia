import cv2


rtsp_url = "rtsp://192.168.0.102:8080/h264_ulaw.sdp"

car_cascade_src = 'haarcascade_car.xml'
car_cascade = cv2.CascadeClassifier(car_cascade_src)

cap = cv2.VideoCapture(rtsp_url, cv2.CAP_FFMPEG)


while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Erro ao receber frame")
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cars = car_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4, minSize=(80, 80))

    for (x, y, w, h) in cars:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)


    cv2.imshow("Detecção de Carros", frame)

    if cv2.waitKey(2) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
