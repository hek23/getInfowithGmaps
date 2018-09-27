# -*- coding: utf-8 -*-
#Libreria para hacer consultas HTTP
import requests
import json
#Formatos para hacer la obtención de datos desde Google
baseURI = "https://maps.googleapis.com/maps/api/directions/json?origin={0}&destination={1}&key={2}&alternatives=true"
#Clave de desarrollador para poder obtener datos desde Google
key = "KEY"
#Numero usado para monitoreo del proceso
i= 1
#Se enuncia una clase Punto para mejor manejo de la información.
#Esta representa cada punto a buscar
class Punto:
  def __init__(self, coordX, coordY):
    self.x = float(coordX)
    self.y = float(coordY)
  #Transforma un punto en un string para la busqueda en GMaps
  def toGoogleCoord(self):
    return str(self.x)+","+str(self.y)

#Funcion que abre el archivo y retorna la información formateada para su uso
def abrirArchivo (fileName):
  #Se abre el archivo
  archivo = open(fileName, "r")
  #Se enuncia en donde se guardarán los lugares a buscar
  lugares = []
  #Se recorre el archivo. Se sabe que cada linea es un punto
  for lugar in archivo.readlines():
    #Se dividen usando la coma, dado el formato de la linea
    #para así pasar cada componente de la coordenada como corresponde
    puntoNuevo = lugar.split(',')
    #Se guarda el nuevo punto enunciado como un objeto en la lista
    #Anteriormente generada
    lugares.append(Punto(puntoNuevo[0], puntoNuevo[1]))
  #Se cierra el archivo
  archivo.close()
  #Se retornan los puntos procesados
  return lugares

#Funcion que con dos puntos (origen y destino), obtiene la distancia de la ruta
#sugerida por Google
def getDistance(origin, destiny):
  #Se indica que se trabajará con las variables globales baseURI y key
  global baseURI, key
  #Se realiza la solicitud a GoogleMaps, usando el formato y reemplazando los {}, con
  #los parametros necesarios
  requestGoogle = requests.get(baseURI.format(origin.toGoogleCoord(),destiny.toGoogleCoord(),key)).json()
  #Si por alguna razón falla, se envia de nuevo la solicitud
  while requestGoogle['status'] != "OK":
    print("Retry")
    print("origin " + origin.toGoogleCoord())
    print("destiny " + destiny.toGoogleCoord())
    requestGoogle = requests.get(baseURI.format(origin.toGoogleCoord(),destiny.toGoogleCoord(),key)).json()
  #Para estudios posteriores se genera un archivo de respaldo de las solicitudes
  #Se retorna la distancia en metros de la ruta más pequeña
  distances = []
  for route in requestGoogle['routes']: 
    for leg in route['legs']:
      distances.append(leg['distance']['value'])
  return min(distances)

#Funcion que construye la matriz euclidiana en base a una lista de puntos
def getEuclidian(points):
  global i
  #Se define la matriz en si, pero vacía
  euclidian = []
  #Se recorren los puntos, seleccionando el origen
  for origen in points:
    #Se crea una fila vacía, que contendra la distancia desde este punto al resto
    fila = []
    #Se recorren los puntos, seleccionando el origen
    for destino in points:
      #Se añade la distancia obtenida de Google a la fila
      fila.append(getDistance(origen,destino))
      #Lo siguiente es para tener monitoreo del procedimiento
      print(i)
      i = i+1
    #Se añade la fila a la matriz inicial
    euclidian.append(fila)
  #Se retorna la matriz para su uso
  return euclidian

#Funcion que escribe la matriz en un archivo de texto usando formato standard directo
def escribirMatrizArchivo(matriz):
    archivo= open("Matriz.txt", "w")
    linea =""
    for indice in range(1,len(matriz)+1):
        linea = linea+ str(indice) + "\t"
    linea = linea.strip()
    linea = linea + "" + '\n'
    archivo.write(linea)
    for origen in range(1,len(matriz)+1):
        linea = str(origen) + "\t"
        for destino in range(0,len(matriz)):
            linea = linea + str(matriz[origen-1][destino]) + "\t"
        linea = linea.strip("\t") + '\n'
        archivo.write(linea)
    archivo.close()
    return 0

fileName = raw_input("Inserte el nombre del archivo que contiene los puntos: ")
puntos = abrirArchivo(fileName)
print("Archivo Cargado")
matriz = getEuclidian(puntos)
print("Matriz lista")
escribirMatrizArchivo(matriz)
