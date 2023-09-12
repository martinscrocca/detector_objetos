import cv2  # Importa la biblioteca OpenCV para procesar imágenes y videos.
# Importa la biblioteca pandas para manejar datos en forma de tablas.
import pandas as pd
# Importa la clase YOLO de la biblioteca ultralytics para detección de objetos.
from ultralytics import YOLO
# Importa las funciones de seguimiento de objetos de un archivo llamado "tracker".
from tracker import*
# Importa la biblioteca cvzone para realizar operaciones en imágenes y videos.
import cvzone
import requests
import os
import datetime
import requests
from PIL import Image


# ----------------------Telegram--------------------------------------
"""
def telegram_bot_sendtext(bot_message):

    bot_token = os.getenv('bot_token')
    bot_chatID = os.getenv('bot_chatID')
    # text = (f"Alerta - {c} - detectado - Tiempo de duración: {round(duration,2)} seg. "
    # f"Hora: {hora_actual.hour}:{hora_actual.minute}:{hora_actual.second}")
    #send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    # Envia la imagen y el mensaje a través de requests.post
    
    with open(frame_filename, 'rb') as img_file:
        response = requests.post('https://api.telegram.org/bot' + bot_token + '/sendPhoto', files={
                                 'photo': (frame_filename, img_file)}, data={'chat_id': bot_chatID, 'caption': bot_message})

        # Verifica la respuesta de la solicitud
        if response.status_code == 200:
            print('Imagen enviada correctamente.')
        else:
            print('Error al enviar la imagen:', response.text)
    

    #response = requests.get(send_text)

    return response.json()
"""
bot_token ="6292967776:AAHEnP00XxDm701wanwfDr97aYAeqZ5kf6c"
bot_chatID = "763046828"

def send_optimized_image(frame_filename, bot_token, bot_chatID, bot_message):
    # Abre la imagen y la redimensiona para reducir su resolución
    img = Image.open(frame_filename)
    img = img.resize((480, 300))  # Reducción de resolución a 800x600

    # Guarda la imagen comprimida con calidad 85
    img.save('compressed_' + frame_filename, quality=85)  # Compresión de imagen

    # Abre la imagen comprimida para enviarla a través de la API de Telegram
    with open('compressed_' + frame_filename, 'rb') as img_file:
        # Realiza una solicitud POST para enviar la imagen a Telegram
        response = requests.post('https://api.telegram.org/bot' + bot_token + '/sendPhoto', files={
                                'photo': ('compressed_' + frame_filename, img_file)}, data={'chat_id': bot_chatID, 'caption': bot_message})

        # Verifica la respuesta de la solicitud
        if response.status_code == 200:
            print('Imagen enviada correctamente.')
        else:
            print('Error al enviar la imagen:', response.text)
"""
if __name__ == "__main__":
    # Reemplaza estos valores con los tuyos
    frame_filename = "nombre_de_tu_imagen.jpg"
    bot_token = "tu_token_de_bot"
    bot_chatID = "tu_chat_id"
    bot_message = "Mensaje opcional"

    # Llama a la función para enviar la imagen optimizada
    send_optimized_image(frame_filename, bot_token, bot_chatID, bot_message)

"""

# Crea una instancia del modelo YOLO cargando el archivo de pesos 'yolov8s.pt'.
model = YOLO('yolov8n.pt')

# Define una función llamada "RGB" que se usará cuando se interactúe con la ventana llamada "RGB".


def RGB(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:  # Si el evento es un movimiento del mouse.
        point = [x, y]  # Guarda las coordenadas del puntero del mouse.
        print(point)  # Imprime las coordenadas en la consola.


# Crea una ventana llamada "RGB" y asocia la función "RGB" al evento del mouse.
cv2.namedWindow('RGB')
cv2.setMouseCallback('RGB', RGB)

# Abre un archivo de video llamado 'vidp.mp4' para procesar los fotogramas.
#cap = cv2.VideoCapture(0)
#cap = cv2.VideoCapture('imou2.mp4')
cap = cv2.VideoCapture(os.getenv('url'))

# Abre y lee el contenido de un archivo de texto llamado "coco.txt".
my_file = open("coco.txt", "r")
data = my_file.read()

# Divide el contenido del archivo en líneas y almacena las clases en una lista llamada "class_list".
class_list = data.split("\n")
print(class_list)  # Imprime la lista de clases en la consola.

# Inicializa un contador para llevar el seguimiento de los fotogramas procesados.
count = 0
# Un diccionario para rastrear la posición de personas que se están moviendo hacia abajo.
persondown = {}
# Crea una instancia de la clase Tracker para seguir objetos en el video.
tracker = Tracker()
# Una lista para almacenar identificadores de personas que van hacia abajo.
counter1 = []
check = False
# Un diccionario para rastrear la posición de personas que se están moviendo hacia arriba.
personup = {}
# Una lista para almacenar identificadores de personas que van hacia arriba.
counter2 = []
last_alert_time = 0
id2=588888888

cy1 = 194  # Coordenada Y para la línea de detección inferior.
cy2 = 220  # Coordenada Y para la línea de detección superior.
offset = 6  # Un valor de ajuste para las líneas de detección.

# Comienza un bucle infinito para procesar los fotogramas del video.
while True:
    hora_actual = datetime.datetime.now()
    # Lee un fotograma del video. "ret" indica si se ha leído correctamente.
    ret, frame = cap.read()

    # Si no se pudo leer el fotograma (fin del video), sale del bucle.
    if not ret:
        break

    count += 1  # Incrementa el contador de fotogramas.
    # Procesa cada tercer fotograma (controla la velocidad de procesamiento).
    if count % 3 != 0:
        continue

    # Cambia el tamaño del fotograma a 1020x500.
    frame = cv2.resize(frame, (1020, 500))

    # Realiza la detección de objetos en el fotograma.
    results = model.predict(frame)
    a = results[0].boxes.data  # Obtiene los datos de las cajas del resultado.
    # Convierte los datos en un DataFrame de pandas.
    px = pd.DataFrame(a).astype("float")

    # Una lista para almacenar las coordenadas de las cajas de interés.
    list = []

    # Itera a través de las filas del DataFrame para obtener las coordenadas y clases de las cajas detectadas.
    # Este bucle for itera a través de las filas del DataFrame px, que contiene las coordenadas y otras propiedades de las cajas detectadas en el fotograma. Para cada fila, se extraen las coordenadas y el índice de la clase. Luego, se verifica si la clase es "person" o "car" y, si es así, se agregan las coordenadas de la caja a la lista list. Esta lista contendrá las coordenadas de las cajas de interés que contienen personas o autos detectados en el fotograma.
    for index, row in px.iterrows():
        #print(row)
        
        # Obtiene la coordenada X del punto superior izquierdo de la caja.
        x1 = int(row[0])
        # Obtiene la coordenada Y del punto superior izquierdo de la caja.
        y1 = int(row[1])
        # Obtiene la coordenada X del punto inferior derecho de la caja.
        x2 = int(row[2])
        # Obtiene la coordenada Y del punto inferior derecho de la caja.
        y2 = int(row[3])
        d = int(row[5])  # Obtiene el índice de la clase detectada.

        c = class_list[d]  # Obtiene la clase correspondiente del índice "d".
        # Si la clase es 'person' o 'car' o  'cat.
        if 'person' in c or 'car' in c or 'cat' in c or 'dog' in c:
            list.append([x1, y1, x2, y2])  # Agrega las coordenadas a la lista.

    # Actualiza el seguimiento de las cajas y obtiene identificadores.
    bbox_id = tracker.update(list)

    # Itera a través de las cajas con sus identificadores obtenidos.
    
    for bbox in bbox_id:
        # Obtiene las coordenadas y el identificador.
        
        x3, y3, x4, y4, id, duration, duration2 = bbox
        cx = int((x3 + x4) / 2)  # Calcula la coordenada X del centro.
        cy = int((y3 + y4) / 2)  # Calcula la coordenada Y del centro.
       

        

        # Dibuja un círculo en el centro de la caja.
        cv2.circle(frame, (cx, cy), 4, (255, 0, 255), -1)

        # Detecta si una persona cruza las líneas de detección para conteo.
        # if cy1 < (cy + offset) and cy1 > (cy - offset):
        #     cv2.rectangle(frame, (x3, y3), (x4, y4), (0, 0, 255), 2)
        #     cvzone.putTextRect(frame, f'{id}', (x3, y3), 1, 2)
        #     persondown[id] = (cx, cy)  # Almacena la posición de la persona que va hacia abajo.

        # # Realiza un seguimiento de las personas que cruzan la línea de detección inferior.
        # if id in persondown:
        #     if cy2 < (cy + offset) and cy2 > (cy - offset):
        #         cv2.rectangle(frame, (x3, y3), (x4, y4), (0, 255, 255), 2)
        #         cvzone.putTextRect(frame, f'{id}', (x3, y3), 1, 2)
        #         if counter1.count(id) == 0:
        #             counter1.append(id)

        # # Realiza un seguimiento de las personas que cruzan la línea de detección superior.
        # if cy2 < (cy + offset) and cy2 > (cy - offset):
        #     cv2.rectangle(frame, (x3, y3), (x4, y4), (0, 0, 255), 2)
        #     cvzone.putTextRect(frame, f'{id}', (x3, y3), 1, 2)
        #     personup[id] = (cx, cy)

        # # Realiza un seguimiento de las personas que cruzan la línea de detección superior.
        # if id in personup:
        #     if cy1 < (cy + offset) and cy1 > (cy - offset):
        #         cv2.rectangle(frame, (x3, y3), (x4, y4), (0, 255, 255), 2)
        #         cvzone.putTextRect(frame, f'{id}', (x3, y3), 1, 2)
        #         if counter2.count(id) == 0:
        #             counter2.append(id)
        #----------------------------------------------------------##

        # Dibuja un rectángulo alrededor de la caja y muestra el identificador y la clase.
        cv2.rectangle(frame, (x3, y3), (x4, y4), (0, 0, 255), 2)
        cvzone.putTextRect(
            frame, f' {id} ,tipo: {c}, time: {round(duration,1)}', (x3-20, y3-20), 1, 2)
        #cvzone.putTextRect(frame, f'{id} ,tipo: {c}, time: {round(duration,1)}', (600, 35), 2, 2)
        persondown[id] = (cx, cy)
        current_time = time.time()
        
       
       
        
        #print(f'Duration={duration} tipo: {c}')
        if current_time-last_alert_time >= 10:

            
            

                if duration < 4 and duration > 3.6:
                    
                    print(f'------------------------------Objeto detectado ------------------\n-duración: {duration} \n-tipo: {c}' )

                    # Capturar el frame actual
                    """"""
                    # if current_time-last_alert_time>=10:

                    frame_filename = f"captura de {c}.png"
                    cv2.imwrite(frame_filename, frame)
                    imagen = cv2.imread(f"captura de {c}.png")
                    print(f"captura del momento {frame_filename}")
                    """
                    test = telegram_bot_sendtext(
                        f"--------------------------------Alerta--------------------------- \nObjeto detectado: {c}\nTiempo de duración: {round(duration,2)}seg. \nHora: {hora_actual.hour}:{hora_actual.minute}:{hora_actual.second}")
                        """
                    #test=send_optimized_image(frame_filename, os.getenv('bot_token'), os.getenv('bot_chatID'),
                    test=send_optimized_image(frame_filename, bot_token, bot_chatID, f"--------------------------------Alerta--------------------------- \nObjeto detectado: {c}\nTiempo de duración: {round(duration,2)}seg. \nHora: {hora_actual.hour}:{hora_actual.minute}:{hora_actual.second}")

                    

                    #print(test)
                    # Actualizar el tiempo del último alerta
                    last_alert_time = current_time
                    #print(last_alert_time)
                    # print(f'id1= {id} id2 = {id2}')
                    # id2=id
                    # print(f'id1= {id} id2 = {id2}')

                elif duration < 20 and duration > 19.7 and (c == 'car' or c == 'truck' or 'traffic light' or 'fire hydrant' or 'toilet'):
                    # Capturar el frame actual
                    """"""
                    frame_filename = f"captura de {c}.png"
                    cv2.imwrite(frame_filename, frame)
                    imagen = cv2.imread(f"captura de {c}.png")
                    print(f"captura del momento {frame_filename}\n--------------------------------Alerta--------------------------- \nObjeto detectado: {c}\nTiempo de duración: {round(duration,2)}seg. \nHora: {hora_actual.hour}:{hora_actual.minute}:{hora_actual.second}")

                    test=send_optimized_image(frame_filename, os.getenv('bot_token'), os.getenv('bot_chatID'),
                        f"--------------------------------Alerta--------------------------- \nObjeto detectado: {c}\nTiempo de duración: {round(duration,2)}seg. \nHora: {hora_actual.hour}:{hora_actual.minute}:{hora_actual.second}")
                    #print(test)
                    last_alert_time = current_time
                  
                    

                elif duration < 80 and duration > 79.6:
                    # Capturar el frame actual
                    """"""
                    frame_filename = f"captura de {c}.png"
                    cv2.imwrite(frame_filename, frame)
                    imagen = cv2.imread(f"captura de {c}.png")
                    print(f"captura del momento {frame_filename}-------------------------Alerta!!--------------------- 1 minuto Objeto detectado: {c} parado en la puerta -----------\nTiempo de duración: {round(duration,2)}seg. \nHora: {hora_actual.hour}:{hora_actual.minute}:{hora_actual.second}")

                    test=send_optimized_image(frame_filename, os.getenv('bot_token'), os.getenv('bot_chatID'),
                        f"-------------------------Alerta!!--------------------- 1 minuto Objeto detectado: {c} parado en la puerta -----------\nTiempo de duración: {round(duration,2)}seg. \nHora: {hora_actual.hour}:{hora_actual.minute}:{hora_actual.second}")
                    #print(test)
                    last_alert_time = current_time
                   

                elif duration < 120 and duration > 110:
                    # Capturar el frame actual
                    """"""
                    frame_filename = f"captura de {c}.png"
                    cv2.imwrite(frame_filename, frame)
                    imagen = cv2.imread(f"captura de {c}.png")
                    print(f"captura del momento {frame_filename}")

                    test=send_optimized_image(frame_filename, os.getenv('bot_token'), os.getenv('bot_chatID'),
                        f"Alerta!! 2 minutos {c} parado en la puerta \n Tiempo de duración: {round(duration,2)}seg. \nHora: {hora_actual.hour}:{hora_actual.minute}:{hora_actual.second}")
                    #print(test)
                    last_alert_time = current_time
                    

    #

    # cv2.line(frame,(3,cy1),(1018,cy1),(0,255,0),2)
    # cv2.line(frame,(5,cy2),(1019,cy2),(0,255,255),2)
    # down = len(counter1)  # Calcula la cantidad de personas que van hacia abajo.
    # cvzone.putTextRect(frame, f'down {down}', (50, 60), 2, 2)  # Muestra el conteo en la imagen.

    # up = len(counter2)  # Calcula la cantidad de personas que van hacia arriba.
    # cvzone.putTextRect(frame, f'up {up}', (50, 160), 2, 2)  # Muestra el conteo en la imagen.

    # print(persondown)
    cv2.imshow("RGB", frame)  # Muestra el fotograma con las anotaciones.

    #print(f" id {id} {c} estuvo {duration}.")

    # Espera por la tecla 'Esc' para salir del bucle.
    if cv2.waitKey(1) & 0xFF == 27:
        break


# ----------------------telegram------------------------------------------------------

cap.release()  # Libera el recurso de la captura de video.
cv2.destroyAllWindows()  # Cierra todas las ventanas abiertas.
