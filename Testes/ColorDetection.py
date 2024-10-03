import cv2
import numpy as np

# Inicializa a captura de vídeo pela webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Erro ao acessar a webcam")
    exit()

color = "verde"
flag = True

while True:
    # Captura o frame atual da webcam
    ret, frame = cap.read()
    
    if not ret:
        print("Erro ao capturar a imagem da webcam")
        break

    # Converte o frame para o espaço de cores HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define os limites para a cor vermelha no espaço HSV
    # lower_red1 = np.array([0, 120, 70])
    # upper_red1 = np.array([10, 255, 255])
    # lower_red2 = np.array([170, 120, 70])
    # upper_red2 = np.array([180, 255, 255])
    lower_green = np.array([35, 100, 100])
    upper_green = np.array([85, 255, 255])

    # Cria duas máscaras para capturar diferentes tons de vermelho
    mask = cv2.inRange(hsv, lower_green, upper_green)
    # mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

    # Combina as duas máscaras
    # mask = mask1 | mask2

    # Aplica a máscara para obter apenas as áreas vermelhas
    result = cv2.bitwise_and(frame, frame, mask=mask)

    # Encontra os contornos das áreas vermelhas
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if(contours != "()" and flag):
        color_detected = True
        flag = False
    else:
        color_detected = False
        flag = True

    # Loop através dos contornos encontrados
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 800:  # Ignora pequenas áreas para evitar ruído
            # Encontra o bounding box ao redor do objeto vermelho
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)  # Desenha um retângulo verde

    if color_detected:
        print(f"Cor {color} identificada!")
    
    # Exibe o frame original e o resultado com as áreas vermelhas
    cv2.imshow(f"Webcam - Detecção de Cor {color}", frame)
    cv2.imshow("Regiões Vermelhas Detectadas", result)

    # Pressione 'q' para sair
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

# Libera a câmera e fecha as janelas
cap.release()
cv2.destroyAllWindows()
