import cv2

from ultralytics import YOLO
model = YOLO("license_plate_detector.pt")

rtsp_url = "rtsp://192.168.0.102:8080/h264_ulaw.sdp"

cap = cv2.VideoCapture(rtsp_url, cv2.CAP_FFMPEG)

if not cap.isOpened():
    print("Erro ao abrir o stream RTSP")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Erro ao capturar frame")
        break


    results = model(frame)

    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = box.conf[0].item()

            if conf > 0.5:
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, "Placa", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)


    cv2.imshow("Reconhecimento de Placas", frame)


    if cv2.waitKey(2) & 0xFF == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()
