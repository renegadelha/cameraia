import cv2
import torch

#fc = cv2.CascadeClassifier()
#fc.load('haarcascade_frontalface_default.xml')

#car_cascade_src = 'cars.xml'
#car_cascade = cv2.CascadeClassifier(car_cascade_src)

model = torch.hub.load('ultralytics/yolov5', 'custom', 'yolov5n.pt')
model.conf = 0.5  # confiança mínima (opcional)

cor = (0, 0, 255)


rtsp_url = "rtsp://nyfb:kk247n@192.168.0.104:554/live"

cap = cv2.VideoCapture(rtsp_url, cv2.CAP_FFMPEG)

#cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Erro ao abrir o fluxo RTSP")
    exit()


contador = 0
while True:
    ret, frame = cap.read()
    if ret :
        contador += 1
        if contador != 10:
            #cv2.imshow("Detector", frame)
            continue
        frame = cv2.resize(frame, (800, 450))

        results = model(frame)

        for *box, conf, cls in results.xyxy[0]:
            label = model.names[int(cls)]

            if label == 'person':
                x1, y1, x2, y2 = map(int, box)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        cv2.imshow("Detector", frame)
        contador = 0

        if cv2.waitKey(2) & 0xFF == ord('q'):
            break


cap.release()
cv2.destroyAllWindows()
