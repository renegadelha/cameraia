import cv2
import numpy as np
from collections import deque
import requests

rtsp_url = "rtsp://nyfb:kk247n@192.168.0.104:554/live"

cap = cv2.VideoCapture(rtsp_url, cv2.CAP_FFMPEG)

if not cap.isOpened():
    print("Erro ao abrir o fluxo RTSP")
    exit()

ultimas_medias = deque(maxlen=15)

apertei = False
contador = 0
while True:
    ret, frame = cap.read()
    if ret :
        contador += 1
        if contador != 15:
            #cv2.imshow("Detector", frame)
            continue
        frame = cv2.resize(frame, (800, 450))

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if cv2.waitKey(2) & 0xFF == ord('r'):
            apertei = True
            fechado = gray.copy()


        if int(gray.mean()) == 130:
            print('veio tudo cinza')
            continue

        if apertei:
            tam_quadrado = 20
            altura, largura = gray.shape

            frame_diff = gray.copy()

            # Percorre os quadrantes
            for y in range(0, altura, tam_quadrado):
                for x in range(0, largura, tam_quadrado):
                    y2 = min(y + tam_quadrado, altura)
                    x2 = min(x + tam_quadrado, largura)

                    quad1 = gray[y:y2, x:x2]
                    quad2 = fechado[y:y2, x:x2]

                    media1 = quad1.mean()
                    media2 = quad2.mean()
                    diferenca = abs(media1 - media2)

                    # Define um limiar de diferença (ajustável)
                    if diferenca > 30:
                        # Destaca o quadrante que mudou
                        cv2.rectangle(frame_diff, (x, y), (x2, y2), (0, 0, 255), 1)
                        cv2.putText(frame_diff, f"{int(diferenca)}", (x + 1, y + 8),
                                    cv2.FONT_HERSHEY_PLAIN, 0.6, (0, 0, 255), 1)

            cv2.imshow("Detector", frame_diff)
        else:
            cv2.imshow("Detector", gray)
        contador = 0

        if cv2.waitKey(2) & 0xFF == ord('q'):
            break


cap.release()
cv2.destroyAllWindows()
