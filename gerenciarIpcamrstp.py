import cv2


rtsp_url = "rtsp://nyfb:kk247n@192.168.0.101:554/live"
cap = cv2.VideoCapture(rtsp_url, cv2.CAP_FFMPEG)


while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        frame = cv2.resize(frame, (800, 450))
        cv2.imshow("Detecção de Carros", frame)

        if cv2.waitKey(2) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
