# Importar el módulo math para operaciones matemáticas
import math
import time

# Definir una clase llamada Tracker
class Tracker:
    # Método constructor (__init__) para inicializar el objeto
    def __init__(self):
        # Diccionario para almacenar las posiciones centrales de los objetos
        self.center_points = {}
        # Contador para llevar un registro de los IDs de los objetos
        self.id_count = 0
        #------#
        self.start_times = {}
    def convert_seconds(self, seconds):
        mins = int(seconds // 60)
        secs = int(seconds % 60)
        return mins, secs

    # Método para actualizar la información de seguimiento en función de los rectángulos de los objetos nuevos
    def update(self, objects_rect):
        # Lista para almacenar las cajas delimitadoras de los objetos y sus IDs
        objects_bbs_ids = []
        current_time = time.time()

        # Recorrer la lista de rectángulos de objetos
        for rect in objects_rect:
            # Desempaquetar las coordenadas del rectángulo
            x, y, w, h = rect
            # Calcular el punto central del rectángulo
            cx = (x + x + w) // 2
            cy = (y + y + h) // 2

            # Inicializar una bandera para verificar si se detecta el mismo objeto
            mismo_objeto_detectado = False

            # Recorrer los objetos rastreados existentes
            for id, pt in self.center_points.items():
                # Calcular la distancia euclidiana entre el centro del objeto actual y el centro del objeto rastreado
                dist = math.hypot(cx - pt[0], cy - pt[1])
                

                # Si la distancia está por debajo de un umbral (35), considerarlo el mismo objeto
                if dist < 5000: #10000
                    # Actualizar el centro del objeto rastreado
                    self.center_points[id] = (cx, cy)
                    duration = current_time - self.start_times[id]
                    duration2 = current_time - self.start_times[id]
                    # Agregar la caja delimitadora del objeto y su ID a la lista
                    objects_bbs_ids.append([x, y, w, h, id, duration,duration2])

                    mins, secs = self.convert_seconds(duration)
                    mins1, secs1 = self.convert_seconds(duration2)
                    #print(f" id {id} estuvo {mins} minutos {secs} segundos en cámara.")
                    # Establecer la bandera para indicar que se ha detectado el mismo objeto
                    mismo_objeto_detectado = True
                    # Salir del bucle ya que se encontró el objeto
                    break

            # Si se detecta un objeto nuevo (la bandera sigue siendo Falsa), asignar un nuevo ID
            if not mismo_objeto_detectado:
                # Almacenar el punto central del nuevo objeto en el diccionario junto con su ID
                self.center_points[self.id_count] = (cx, cy)
                self.start_times[self.id_count] = current_time
                # Agregar la caja delimitadora del objeto y el ID recién asignado a la lista
                objects_bbs_ids.append([x, y, w, h, self.id_count,0,0])
                # Incrementar el contador de IDs para el próximo objeto
                self.id_count += 1

        # Limpiar el diccionario de puntos centrales eliminando los IDs no utilizados
        nuevos_center_points = {}
        for obj_bb_id in objects_bbs_ids:
            _, _, _, _, object_id, duration, duration2 = obj_bb_id
            centro = self.center_points[object_id]
            nuevos_center_points[object_id] = centro

        # Actualizar el diccionario center_points con los datos limpiados
        self.center_points = nuevos_center_points.copy()
        # Devolver la lista de cajas delimitadoras de objetos y sus IDs
        return objects_bbs_ids
    
