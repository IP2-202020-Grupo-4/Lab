"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad de Los Andes
 * 
 * Contribución de:
 *
 * Cristian Camilo Castellanos
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.

 COMENTARIO
 """

"""
  Este módulo es una aplicación básica con un menú de opciones para cargar datos, contar elementos, y hacer búsquedas sobre una lista.
"""

import config as cf
import sys
import csv
from time import process_time 
from ADT import list as lst
from Sorting import insertionsort as insSort
from Sorting import shellsort as SSort
from Sorting import selectionsort as selSort

def lessVote(element1, element2):
    if float(element1['vote_average']) < float(element2['vote_average']):
        return True
    return False

def lessCount(element1, element2):
    if float(element1['vote_count']) < float(element2['vote_count']):
        return True
    return False

def greaterCount(element1, element2):
    if float(element1['vote_count']) > float(element2['vote_count']):
        return True
    return False

def greaterVote(element1, element2):
    if float(element1['vote_average']) > float(element2['vote_average']):
        return True
    return False

def loadCSVFile (file, lst, sep=";"):
    """
    Carga un archivo csv a una lista
    Args:
        file 
            Archivo de texto del cual se cargaran los datos requeridos.
        lst :: []
            Lista a la cual quedaran cargados los elementos despues de la lectura del archivo.
        sep :: str
            Separador escodigo para diferenciar a los distintos elementos dentro del archivo.
    Try:
        Intenta cargar el archivo CSV a la lista que se le pasa por parametro, si encuentra algun error
        Borra la lista e informa al usuario
    Returns: None   
    """
    del lst[:]
    print("Cargando archivo ....")
    t1_start = process_time() #tiempo inicial
    dialect = csv.excel()
    dialect.delimiter=sep
    try:
        with open(file, encoding="utf-8") as csvfile:
            spamreader = csv.DictReader(csvfile, dialect=dialect)
            for row in spamreader: 
                lst.append(row)
    except:
        del lst[:]
        print("Se presentó un error en la carga del archivo")
    
    t1_stop = process_time() #tiempo final
    print("Tiempo de ejecución ",t1_stop-t1_start," segundos")

def printMenu():
    """
    Imprime el menu de opciones
    """
    print("\nBienvenido")
    print("1- Cargar Datos")
    print("2- Contar los elementos de la Lista")
    print("4- Consultar buenas películas de cierto director")
    print("5- Consultar ranking de películas")
    print("6- Conocer director")
    print("0- Salir")

def countElementsFilteredByColumn(criteria, column, lst):
    """
    Retorna cuantos elementos coinciden con un criterio para una columna dada  
    Args:
        criteria:: str
            Critero sobre el cual se va a contar la cantidad de apariciones
        column
            Columna del arreglo sobre la cual se debe realizar el conteo
        list
            Lista en la cual se realizará el conteo, debe estar inicializada
    Return:
        counter :: int
            la cantidad de veces ue aparece un elemento con el criterio definido
    """
    if len(lst)==0:
        print("La lista esta vacía")  
        return 0
    else:
        t1_start = process_time() #tiempo inicial
        counter=0 #Cantidad de repeticiones
        for element in lst:
            if criteria.lower() in element[column].lower(): #filtrar por palabra clave 
                counter+=1
        t1_stop = process_time() #tiempo final
        print("Tiempo de ejecución ", t1_stop - t1_start," segundos")
    return counter

def encontrarBuenasPeli(listaCalif, listaDirector, nombre)->tuple:
    lista1 = lst.newList("ARRAY_LIST")
    contador = 0
    contador2 = 0
    for i in range(0, len(listaCalif)):
        if listaDirector[i]["director_name"].lower() == nombre.lower():
            lst.addLast(lista1, i)

    tam = lst.size(lista1)

    for i in range(1, tam+1):
        ind = lst.getElement(lista1, i)    
        if float(listaCalif[ind]["vote_average"]) >= 6:
            contador += float(listaCalif[ind]["vote_average"])
            contador2 += 1
    if contador2 == 0:
        return 0, 0

    prom = contador/contador2
    return contador2, prom


def rankingPeli(listaCalif, decision, numPel)->list:
    listaTAD = lst.newList("ARRAY_LIST")
    
    for i in listaCalif:
        lst.addLast(listaTAD, i)

    if decision == 1:
        listaMasVotos = lst.newList("ARRAY_LIST")
        SSort.shellSort(listaTAD, greaterCount)
        
        for i in range(1, numPel+1):
            ind = lst.getElement(listaTAD, i)
            lst.addLast(listaMasVotos, ind["title"])
        return listaMasVotos["elements"]

    elif decision == 2:
        
        listaMenosVotos = lst.newList("ARRAY_LIST")
        SSort.shellSort(listaTAD, lessCount)
    
        for i in range(1, numPel+1):
            ind = lst.getElement(listaTAD, i)
            lst.addLast(listaMenosVotos, ind["title"])

        return listaMenosVotos["elements"]

    elif decision == 3:
        listaMejorAverage = lst.newList("ARRAY_LIST")
        SSort.shellSort(listaTAD, greaterVote)

        for i in range(1, numPel+1):
            ind = lst.getElement(listaTAD, i)
            lst.addLast(listaMejorAverage, ind["title"])
        return listaMejorAverage["elements"]

    elif decision == 4:
        listaPeorAverage = lst.newList("ARRAY_LIST")
        SSort.shellSort(listaTAD, lessVote)

        for i in range(1, numPel+1):
            ind = lst.getElement(listaTAD, i)
            lst.addLast(listaPeorAverage, ind["title"])
        return listaPeorAverage["elements"]

def conocerDirector(listaCalif, listaDirector, nombre)->tuple:
    lista1 = lst.newList("ARRAY_LIST")
    lista2 = lst.newList("ARRAY_LIST")

    contador = 0
    contador2 = 0
    for i in range(0, len(listaCalif)):
        if listaDirector[i]["director_name"].lower() == nombre.lower():
            lst.addLast(lista1, i)

    tam = lst.size(lista1)

    for i in range(1, tam+1):
        ind = lst.getElement(lista1, i)    
        contador += float(listaCalif[ind]["vote_average"])
        contador2 += 1
        titPeli = listaCalif[ind]["title"]
        lst.addLast(lista2, titPeli)
    if contador2 == 0:
        return lista2["elements"], 0, 0

    prom = contador/contador2
    return lista2["elements"], contador2, prom

def pruebaCarga(listaCalif):
    
    listaTAD = lst.newList("SINGLE_LINKED")
    
    for i in listaCalif:
        lst.addLast(listaTAD, i)

    start = process_time()
    selSort.selectionSort(listaTAD, greaterCount)
    stop = process_time()

    print("Tiempo de ejecución ", stop-start ," segundos")


def main():
    """
    Método principal del programa, se encarga de manejar todos los metodos adicionales creados

    Instancia una lista vacia en la cual se guardarán los datos cargados desde el archivo
    Args: None
    Return: None 
    """
    lista = [] #instanciar una lista vacia
    lista2 = []
    while True:
        printMenu() #imprimir el menu de opciones en consola
        inputs =input('Seleccione una opción para continuar:\n') #leer opción ingresada
        if len(inputs)>0:
            if int(inputs[0])==1: #opcion 1
                loadCSVFile(r"C:\Users\Juan PC\Documents\Python Scripts\Lab\Data\SmallMoviesDetailsCleaned.csv", lista)
                loadCSVFile(r"C:\Users\Juan PC\Documents\Python Scripts\Lab\Data\MoviesCastingRaw-small.csv", lista2)
                print("Datos cargados, "+str(len(lista)+len(lista2))+" elementos cargados")
            elif int(inputs[0])==2: #opcion 2
                if len(lista)==0: #obtener la longitud de la lista
                    print("La lista esta vacía")    
                else: print("La lista tiene "+str(len(lista))+" elementos")
            elif int(inputs[0])==3: #opcion 3
                criteria =input('Ingrese el criterio de búsqueda\n')
                counter=countElementsFilteredByColumn(criteria, "nombre", lista) #filtrar una columna por criterio  
                print("Coinciden ",counter," elementos con el crtierio: ", criteria  )
            elif int(inputs[0])==4:
                nombreDir = input("Ingrese el nombre del director: ")
                numPeli, prom = encontrarBuenasPeli(lista, lista2, nombreDir)
                print("El director {0} tiene {1} pelicula(s) buenas con puntaje promedio de {2}.".format(nombreDir, numPeli, prom))
            elif int(inputs[0])==5:
                print("¿Qué tipo de ranking quiere consultar?")
                print("1- Ranking películas más votadas.")
                print("2- Ranking películas menos votadas.")
                print("3- Ranking películas con mejor calificación.")
                print("4- Ranking películas con peor calificación.")
                decision = int(input(""))
                numPel = int(input("¿Cuántas películas quiere meter en el ranking? \n: "))
                resultado = rankingPeli(lista, decision, numPel)
                print("El ranking solicitado es: {0}".format(resultado))
            elif int(inputs[0])==6:
                nombreDir = input("Ingrese el nombre del director: ")
                titulos, numPeli, prom = conocerDirector(lista, lista2, nombreDir)
                print("El director {0} tiene {1} pelicula(s) con puntaje promedio de {2}.\nSus películas son: {3}".format(nombreDir, numPeli, prom, titulos))
            elif int(inputs[0])==7:
                pruebaCarga(lista)
            elif int(inputs[0])==0: #opcion 0, salir
                sys.exit(0)

if __name__ == "__main__":
    main()

