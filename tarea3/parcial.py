import json
import os
from datetime import datetime

class HistorialDescargas:
    def __init__(self):
        self.historial_completadas = []
        self.cola_descargas = []
        self.descargas = []

    def cargar_descargas_desde_json(self, archivo_json):
        self.historial_completadas = []
        self.cola_descargas = []
        self.descargas = []
        with open(archivo_json, 'r') as file:
            datos = json.load(file)
            for descarga_data in datos:
                descarga = Descarga(
                    url=descarga_data['url'],
                    tamano=descarga_data['tamano'],
                    fecha_inicio=descarga_data['fecha_inicio'],
                    estado=descarga_data['estado']
                )
                if descarga.estado == 'completada':
                    self.historial_completadas.append(descarga)
                    self.descargas.append(descarga)
                else:
                    self.cola_descargas.append(descarga)
                    self.descargas.append(descarga)

        print("Descargas cargadas correctamente desde el archivo JSON.")

    def mostrar_descargas(self):
        print("\nDescargas en la cola (pendientes y en progreso):")
        for descarga in self.cola_descargas:
            print(f"{descarga.url} {descarga.tamano} {descarga.fecha_inicio} {descarga.estado}")

        print("\nDescargas completadas:")
        for descarga in self.historial_completadas:
            print(f"{descarga.url} {descarga.tamano} {descarga.fecha_inicio} {descarga.estado}")

class Descarga:
    def __init__(self, url, tamano, fecha_inicio, estado):
        self.url = url
        self.dominio = (((url.split("//"))[1]).split("/"))[0]
        self.tamano = tamano
        self.fecha_inicio = fecha_inicio
        self.fecha_hora = datetime.strptime(self.fecha_inicio, "%Y-%m-%d %H:%M:%S")
        self.estado = estado

class Reporte:
    def __init__(self, historialDescargas):
        self.historialDescargas = historialDescargas

    def dividir(self, lista):
        pivote = lista[0].tamano
        mayor = []
        menor = []
        for i in range(len(lista)):
            if lista[i].tamano < pivote:
                menor.append(lista[i])
            if lista[i].tamano > pivote:
                mayor.append(lista[i])
            if lista[i].tamano == pivote and i != 0:
                mayor.append(lista[i])

        return menor, lista[0], mayor

    def quicksort(self, lista):
        if len(lista) < 2:
            return lista
        
        menor, pivote, mayor = self.dividir(lista)
        return list(self.quicksort(mayor)) + [pivote] + list(self.quicksort(menor))

    def mergesort(self, lista):
        if len(lista) == 1:
            return lista
        
        divisor = len(lista) // 2
        lista_1 = lista[divisor:]
        lista_2 = lista[:divisor]

        lista_derecha = self.mergesort(lista_1)
        lista_izquierda = self.mergesort(lista_2)

        return self.acomodador(lista_derecha, lista_izquierda)

    def acomodador(self, lista_derecha, lista_izquierda):
        nueva_lista = []
        while len(lista_derecha) > 0 and len(lista_izquierda) > 0:
            if lista_derecha[0].fecha_hora > lista_izquierda[0].fecha_hora: 
                nueva_lista.append(lista_izquierda[0])
                lista_izquierda.pop(0)
            else:
                nueva_lista.append(lista_derecha[0])
                lista_derecha.pop(0)

        while len(lista_derecha) > 0:
            nueva_lista.append(lista_derecha[0])
            lista_derecha.pop(0)
        
        while len(lista_izquierda) > 0:
            nueva_lista.append(lista_izquierda[0])
            lista_izquierda.pop(0)

        return nueva_lista

    def heapify(self, lista, n, i):
        largest = i  
        left = 2 * i + 1    
        right = 2 * i + 2    

        if left < n and lista[left].fecha_hora < lista[largest].fecha_hora:
            largest = left

        if right < n and lista[right].fecha_hora < lista[largest].fecha_hora:
            largest = right

        if largest != i:
            lista[i], lista[largest] = lista[largest], lista[i]  
            self.heapify(lista, n, largest)

    def heap_sort(self, lista, fecha, dominio):
        n = len(lista)
        fecha = datetime.strptime(fecha, "%Y-%m-%d %H:%M")
        listaT = []
        for i in range(n // 2 - 1, -1, -1):
            self.heapify(lista, n, i)

        for i in range(n - 1, 0, -1):
            lista[i], lista[0] = lista[0], lista[i] 
            self.heapify(lista, i, 0)
        lista = lista[::-1]

        for i in range(len(lista)):
            if (lista[i].fecha_hora > fecha) and (dominio == lista[i].dominio):
                listaT.append(lista[i])
        listaT = self.quicksort(listaT)
        listaT = listaT[::-1]
        print()
        for i in range(len(listaT)):
            print(f"{listaT[i].url} {listaT[i].tamano} {listaT[i].fecha_inicio} {listaT[i].estado}")

    def shell_sort(self, lista, estado, intervalo=None):
        if intervalo is None:
            intervalo = len(lista) // 2 
        if intervalo < 1:
            for i in lista:
                if i.estado == estado:
                    print(f"{i.url} {i.tamano} {i.fecha_inicio} {i.estado}")
            return

        for i in range(intervalo, len(lista)):
            temp = lista[i]
            j = i
            while j >= intervalo and (len(lista[j - intervalo].url) > len(temp.url)):
                lista[j] = lista[j - intervalo]
                j -= intervalo
            lista[j] = temp

        self.shell_sort(lista, estado, intervalo // 2)

    def agregar(self):
        url = input("ingrese la url")
        tamano = int(input("tamaño"))
        fecha_inicio = input("ingrese la fecha de inicio")
        estado = input("ingrese el estado")
        descarga = {"url": url, "tamano": tamano, "fecha_inicio": fecha_inicio, "estado": estado}
        if os.path.exists("descargas.json"):
            with open("descargas.json", 'r') as archivo:
                datos = json.load(archivo)
        datos.append(descarga)
        with open("descargas.json", 'w') as archivo:
            json.dump(datos, archivo, indent=4)

        self.historialDescargas.cargar_descargas_desde_json("descargas.json")

    def modificar(self):
        if os.path.exists("descargas.json"):
            with open("descargas.json", 'r') as archivo:
                datos = json.load(archivo)
        cont = 0
        for i in datos:
            texto = f"{cont} {i['url']} {i['tamano']} {i['fecha_inicio']} {i['estado']}"
            cont += 1
            print(texto)   
        modificar = int(input("ingrese el registro que desee modificar"))
        url = input("ingrese la url")
        tamano = int(input("tamaño"))
        fecha_inicio = input("ingrese la fecha de inicio")
        estado = input("ingrese el estado")
        descarga = {"url": url, "tamano": tamano, "fecha_inicio": fecha_inicio, "estado": estado}
        datos[modificar] = descarga
        with open("descargas.json", 'w') as archivo:
            json.dump(datos, archivo, indent=4)

    def mostrar(self, lista):
        for descarga in lista:
            print(f"{descarga.url} {descarga.tamano} {descarga.fecha_inicio} {descarga.estado}")

    def menu(self):
        bandera = 0
        print()
        while bandera == 0:
            try:
                print()
                print("1) lista de las descargas completadas de forma descendente por tamaño")
                print("2) Listar las descargas que no han sido completadas de forma ascendente ")
                print("3) Listar las descargas a partir de una fecha")
                print("4) Listar las descargar de forma descendente por la longitud de su url")
                print("5) Agregar una nueva descarga")
                print("6) Modificar una descarga")
                print("7) Historial de las descargas")
                print("0) Salir")
                
                opcion = int(input("git  "))
                print()
                
                if opcion == 1:
                    self.historialDescargas.historial_completadas = self.quicksort(self.historialDescargas.historial_completadas)
                    self.mostrar(self.historialDescargas.historial_completadas)
                    historial.cargar_descargas_desde_json("descargas.json")

                elif opcion == 2:
                    self.historialDescargas.cola_descargas = self.mergesort(self.historialDescargas.cola_descargas)
                    self.mostrar(self.historialDescargas.cola_descargas)
                    historial.cargar_descargas_desde_json("descargas.json")
                elif opcion == 3:
                    año = input("ingrese el año ")
                    mes = input("ingrese el mes ")
                    dias = input("ingrese el dias ")
                    hora = input("ingrese la hora ")
                    minutos = input("ingrese los minutos ")
                    dominio = input("ingrese el dominio al que desea acceder ")
                    fecha = f"{año}-{mes}-{dias} {hora}:{minutos}"
                    self.heap_sort(self.historialDescargas.descargas, fecha, dominio)
                elif opcion == 4:
                    estado = input("ingrese el estado ")
                    self.shell_sort(self.historialDescargas.descargas, estado)
                elif opcion == 5:
                    self.agregar()
                elif opcion == 6:
                    self.modificar()
                elif opcion == 7:
                    self.historialDescargas.mostrar_descargas()
                elif opcion == 0:
                    print("Fin del proceso")
                    bandera = 1
            except Exception as e:
                print(f" Dato ingresado erroneo, error de tipo : {e}")

historial = HistorialDescargas()
historial.cargar_descargas_desde_json("descargas.json")
repo = Reporte(historial)
repo.menu()
