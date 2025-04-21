import cv2
import numpy as np
from collections import deque
import requests
from datetime import datetime, time, date, timedelta


rtsp_url = "rtsp://nyfb:kk247n@192.168.0.104:554/live"
cap = cv2.VideoCapture(rtsp_url, cv2.CAP_FFMPEG)

if not cap.isOpened():
    print("Erro ao abrir o fluxo RTSP")
    exit()

ultimas_medias = deque(maxlen=15)
armou_apito = False
contador = 0
ultimo_minuto = 99
while True:
    ret, frame = cap.read()
    if ret:
        contador += 1
        if contador != 15:
            continue

        frame = cv2.resize(frame, (800, 450))

        x0 = 115
        x1 = x0 + 15
        y0 = 240
        y1 = y0 + 15
        roi = frame[y0:y1, x0:x1]

        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        media_lumin_regiao = gray.mean()
        ultimas_medias.append(media_lumin_regiao)

        mediana = np.median(ultimas_medias)
        #print(f"Mediana: {mediana:.2f}")
        agora = datetime.now()

        hora = agora.strftime('%H')
        minuto = agora.strftime('%M')

        if minuto != ultimo_minuto:
            arquivo = open('dados.csv', 'a')
            arquivo.write(str(mediana) + ', ' + hora + ', ' + minuto + '\n')
            arquivo.close()
        ultimo_minuto = minuto

        if mediana > 120:
            if not armou_apito:
                try:
                    arquivo = open('portao_aberto.csv', 'a')
                    arquivo.write(str(mediana) + ', ' + hora + ', ' + minuto + '\n')
                    arquivo.close()

                    #print("Mediana maior que 100! Enviando requisição...")
                    requests.get("http://192.168.0.123/apitar", timeout=0.5)
                    armou_apito = True
                except Exception as e:
                    print("Erro ao enviar requisição:", e)
        else:
            armou_apito = False

        #cv2.rectangle(frame, (x0, y0), (x1, y1), (0, 0, 255), 1)

        #cv2.imshow("Detector", frame)
        contador = 0

        if cv2.waitKey(2) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
