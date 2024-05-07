# from __future__ import print_function
# import threading
# from time import sleep
# import traceback
# from sys import _current_frames


# class Sampler:
#     def __init__(self, tid) -> None:
#         self.tid = tid
#         self.t = threading.Thread(target=self.sample, args=())
#         self.active = True
        
#     def start(self):
#         self.active = True
#         self.t.start()

#     def stop(self):
#         self.active = False
        
#     def checkTrace(self):
#         for thread_id, frames in _current_frames().items():
#             if thread_id == self.tid:
#                 frames = traceback.walk_stack(frames)
#                 stack = []
#                 for frame, _ in frames: 
#                     code = frame.f_code.co_name
#                     stack.append(code)
#                 stack.reverse()
#                 print(stack)  # Esta linea imprime el stack despues de invertirlo la pueden comentar o descomentar si quieren
    
#     def sample(self):
#         while self.active:
#             self.checkTrace()
#             sleep(1)

#     def print_report(self):
#         # Este metodo debe imprimir el reporte del call context tree
#         pass

from __future__ import print_function
import threading
from time import sleep, time
import traceback
from sys import _current_frames

class Sampler:
    def __init__(self, tid):
        self.tid = tid # Thread id
        self.t = threading.Thread(target=self.sample, args=()) # Thread que ejecuta el metodo sample
        self.active = True # El sampler esta activo
        self.call_tree = {}  # Diccionario que representa el call context tree y su tiempo de ejecucion

    def start(self):
        self.active = True # El sampler esta activo
        self.t.start() # Inicia el thread

    def stop(self):
        self.active = False # El sampler no esta activo, se detiene

    def checkTrace(self):
        for thread_id, frames in _current_frames().items(): # Itera sobre los frames de los threads
            if thread_id == self.tid: # Si el thread es el mismo que el del sampler
                frames = traceback.walk_stack(frames) # Obtiene los frames del thread
                stack = [] # Lista que almacena el stack # creo que esta logica esta mal, porque se reinicia?
                for frame, _ in frames: # Itera sobre los frames
                    code = frame.f_code.co_name # Obtiene el nombre del codigo
                    stack.append(code) # Agrega el nombre del codigo al stack
                stack.reverse() # Invierte el stack, para que se vea de manera correcta, desde la capa mas baja a la mas alta
                return stack # Retorna el stack

    def sample(self): # Metodo que se encarga de muestrear el stack
        while self.active: # Mientras el sampler este activo
            stack = self.checkTrace() # Obtiene el stack
            if stack: # Si el stack no esta vacio
                self.update_call_tree(stack) # Actualiza el call context tree
            sleep(1) # Duerme el sampler por 1 segundo

    def update_call_tree(self, stack):
        current_node = self.call_tree # Nodo actual es el call context tree
        for func in stack: # Itera sobre las funciones del stack
            current_node = current_node.setdefault(func, {'time': 0, 'children': {}}) # Obtiene la funcion actual y si no existe la crea
            current_node['time'] += 1  # Aumenta el tiempo de ejecucion de la funcion en 1

    def print_report(self):
        self.print_tree(self.call_tree) # Imprime el call context tree
        
    def print_tree(self, node, indent=1): # Imprime el call context tree
        total_time = sum(child['time'] for child in node.values()) # Obtiene el tiempo total de ejecucion
        print(f"total ({total_time} seconds)") # Imprime el tiempo total de ejecucion
        for func, data in node.items(): # Itera sobre las funciones y sus datos
            print(f"{indent * ' '}{func} ({data['time']} seconds)") # Imprime la funcion y su tiempo de ejecucion # algo pasa que no se imprime bien
            self.print_tree(data['children'], indent + 1) # Imprime los hijos de la funcion # solo se entra en bootstrap