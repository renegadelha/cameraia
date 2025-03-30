import cv2

# Abre a webcam (0 é o índice da webcam padrão)
cap = cv2.VideoCapture(1)

if not cap.isOpened():
    print("Erro ao abrir a webcam.")
    exit()

while True:
    # Captura frame por frame
    ret, frame = cap.read()

    if not ret:
        print("Não foi possível capturar o frame.")
        break

    # Exibe o frame
    cv2.imshow('Webcam', frame)

    # Sai do loop quando a tecla 'q' for pressionada
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera os recursos
cap.release()
cv2.destroyAllWindows()
