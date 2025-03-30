import cv2
from ultralytics import YOLO

#fc = cv2.CascadeClassifier()
#fc.load('haarcascade_frontalface_default.xml')

#car_cascade_src = 'cars.xml'
#car_cascade = cv2.CascadeClassifier(car_cascade_src)

model = YOLO("yolov8n.pt")

cor = (0, 0, 255)

rtsp_url = "rtsp://nyfb:kk247n@192.168.0.104:554/live"

cap = cv2.VideoCapture(rtsp_url, cv2.CAP_FFMPEG)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1000)

if not cap.isOpened():
    print("Erro ao abrir o fluxo RTSP")
    exit()

ret, frame = cap.read()
width = int(frame.shape[1] * 50 / 100)
height = int(frame.shape[0] * 50 / 100)
new_size = (width, height)

contador = 0
while True:
    ret, frame = cap.read()
    if ret :
        contador += 1
        if contador != 5:
            #cv2.imshow("Detector", frame)
            continue
        frame = cv2.resize(frame, new_size)
        #framegray = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        #carros = car_cascade.detectMultiScale(framegray)
        results = model(frame)

        for result in results:
            for box in result.boxes:
                cls = int(box.cls[0])
                if cls == 0:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, "Pessoa", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        cv2.imshow("Detector", frame)
        contador = 0

        if cv2.waitKey(2) & 0xFF == ord('q'):
            break


cap.release()
cv2.destroyAllWindows()
