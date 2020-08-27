import config as cf
import sys
import csv
from time import process_time 
from ADT import list as lt
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

def loadCSVFile (file, sep=";"):
    lst = lt.newList("ARRAY_LIST") #Usando implementacion arraylist
    print("Cargando archivo ....")
    t1_start = process_time() #tiempo inicial
    dialect = csv.excel()
    dialect.delimiter=sep
    try:
        with open(file, encoding="utf-8") as csvfile:
            spamreader = csv.DictReader(csvfile, dialect=dialect)
            for row in spamreader: 
                lt.addLast(lst,row)
    except:
        print("Hubo un error con la carga del archivo")
    t1_stop = process_time() #tiempo final
    print("Tiempo de ejecución ",t1_stop-t1_start," segundos")
    return lst


def printMenu():
    print("\nBienvenido")
    print("1- Cargar Datos")
    print("2- Consultar buenas películas de cierto director")
    print("3- Consultar ranking de películas")
    print("4- Conocer director")
    print("5- Conocer actor")
    print('6- Conocer genero')
    print("7- Ranking por genero")
    print("0- Salir")

def encontrarBuenasPeli(listaCalif, listaDirector, nombre)->tuple:
    lista1 = lt.newList("ARRAY_LIST")
    contador = 0
    contador2 = 0
    for i in range(0, lt.size(listaCalif)):
        if listaDirector["elements"][i]["director_name"].lower() == nombre.lower():
            lt.addLast(lista1, i)

    tam = lt.size(lista1)

    for i in range(1, tam+1):
        ind = lt.getElement(lista1, i)    
        if float(listaCalif["elements"][ind]["vote_average"]) >= 6:
            contador += float(listaCalif["elements"][ind]["vote_average"])
            contador2 += 1
    if contador2 == 0:
        return 0, 0

    prom = contador/contador2
    return contador2, prom


def rankingPeli(listaCalif, decision, numPel)->list:
    
    if decision == 1:
        listaMasVotos = lt.newList("ARRAY_LIST")
        SSort.shellSort(listaCalif, greaterCount)
        
        for i in range(1, numPel+1):
            ind = lt.getElement(listaCalif, i)
            lt.addLast(listaMasVotos, ind["title"])
        return listaMasVotos["elements"]

    elif decision == 2:
        
        listaMenosVotos = lt.newList("ARRAY_LIST")
        SSort.shellSort(listaCalif, lessCount)
    
        for i in range(1, numPel+1):
            ind = lt.getElement(listaCalif, i)
            lt.addLast(listaMenosVotos, ind["title"])

        return listaMenosVotos["elements"]

    elif decision == 3:
        listaMejorAverage = lt.newList("ARRAY_LIST")
        SSort.shellSort(listaCalif, greaterVote)

        for i in range(1, numPel+1):
            ind = lt.getElement(listaCalif, i)
            lt.addLast(listaMejorAverage, ind["title"])
        return listaMejorAverage["elements"]

    elif decision == 4:
        listaPeorAverage = lt.newList("ARRAY_LIST")
        SSort.shellSort(listaCalif, lessVote)

        for i in range(1, numPel+1):
            ind = lt.getElement(listaCalif, i)
            lt.addLast(listaPeorAverage, ind["title"])
        return listaPeorAverage["elements"]

def conocerDirector(listaCalif, listaDirector, nombre)->tuple:
    lista1 = lt.newList("ARRAY_LIST")
    lista2 = lt.newList("ARRAY_LIST")

    contador = 0
    contador2 = 0
    for i in range(0, lt.size(listaCalif)):
        if listaDirector["elements"][i]["director_name"].lower() == nombre.lower():
            lt.addLast(lista1, i)

    tam = lt.size(lista1)

    for i in range(1, tam+1):
        ind = lt.getElement(lista1, i)    
        contador += float(listaCalif["elements"][ind]["vote_average"])
        contador2 += 1
        titPeli = listaCalif["elements"][ind]["title"]
        lt.addLast(lista2, titPeli)
    if contador2 == 0:
        return lista2["elements"], 0, 0

    prom = contador/contador2
    return lista2["elements"], contador2, prom

def conocerActor(listaCalif, listaDirector, nombre)->tuple:
    lista1 = lt.newList("ARRAY_LIST")
    lista2 = lt.newList("ARRAY_LIST")
    lista3 = lt.newList("ARRAY_LIST")
    diccDirectores = {}

    contador = 0
    contador2 = 0
    for i in range(0, lt.size(listaDirector)):
        if (listaDirector["elements"][i]["actor1_name"].lower() == nombre.lower()) or (listaDirector["elements"][i]["actor2_name"].lower() == nombre.lower()) or (listaDirector["elements"][i]["actor3_name"].lower() == nombre.lower()) or (listaDirector["elements"][i]["actor4_name"].lower() == nombre.lower()) or (listaDirector["elements"][i]["actor5_name"].lower() == nombre.lower()):
            lt.addLast(lista1, i)

    tam = lt.size(lista1)

    for i in range(1, tam+1):
        ind = lt.getElement(lista1, i)    
        contador += float(listaCalif["elements"][ind]["vote_average"])
        contador2 += 1
        titPeli = listaCalif["elements"][ind]["title"]
        titDirec = listaDirector["elements"][ind]["director_name"]
        lt.addLast(lista2, titPeli)
        lt.addLast(lista3, titDirec)
    if contador2 == 0:
        return lista2["elements"], 0, 0, "Ninguno"


    
    for i in range(0, tam):
        if lista3["elements"][i] not in list(diccDirectores.keys()):
            diccDirectores[lista3["elements"][i]] = 1
        else:
            diccDirectores[lista3["elements"][i]] += 1

    llaves = list(diccDirectores.keys())
    valores = list(diccDirectores.values())
    mayor = max(valores)

    director = llaves[valores.index(mayor)]

    

    prom = contador/contador2
    return lista2["elements"], contador2, prom, director

def EntenderGenero(listaCalif, listaDirector, genero)->tuple:
    lista1 = lt.newList("ARRAY_LIST")
    lista2 = lt.newList("ARRAY_LIST")
    for i in range(0, lt.size(listaDirector)):
        if (genero.lower() in listaCalif["elements"][i]["genres"].lower() ):
            lt.addLast(lista1, i)

    tam = lt.size(lista1)

    contador = 0
    contador2 = 0

    for i in range(1, tam+1):
        ind = lt.getElement(lista1, i)    
        contador += float(listaCalif["elements"][ind]["vote_count"])
        contador2 += 1
        titPeli = listaCalif["elements"][ind]["title"]
        lt.addLast(lista2, titPeli)
    if contador2 == 0:
        return lista2["elements"], 0, 0, "Ninguno"
        
    prom=contador/contador2
    return (lista2['elements'], contador2, prom)
    
def RankingGenero (listaCalificacion, listaDirector, genero, numPel, desicion, aod)->tuple:
     
     listaCalif = lt.newList("ARRAY_LIST")
     for i in range(len(listaCalif["elements"])):
         ind = lt.getElement(listaCalif, i)
         if ind["genre"].lower() == genero.lower:
             lt.addLast(listaCalif, ind)
     
    if decision == 1:
        listaMasVotos = lt.newList("ARRAY_LIST")
        SSort.shellSort(listaCalif, greaterCount)
        
        for i in range(1, numPel+1):
            ind = lt.getElement(listaCalif, i)
            lt.addLast(listaMasVotos, ind["title"])
        return listaMasVotos["elements"]

    elif decision == 2:
        listaMenosVotos = lt.newList("ARRAY_LIST")
        SSort.shellSort(listaCalif, lessCount)
    
        for i in range(1, numPel+1):
            ind = lt.getElement(listaCalif, i)
            lt.addLast(listaMenosVotos, ind["title"])

        return listaMenosVotos["elements"]

    elif decision == 3:
        listaMejorAverage = lt.newList("ARRAY_LIST")
        SSort.shellSort(listaCalif, greaterVote)

        for i in range(1, numPel+1):
            ind = lt.getElement(listaCalif, i)
            lt.addLast(listaMejorAverage, ind["title"])
        return listaMejorAverage["elements"]

    elif decision == 4:
        listaPeorAverage = lt.newList("ARRAY_LIST")
        SSort.shellSort(listaCalif, lessVote)

        for i in range(1, numPel+1):
            ind = lt.getElement(listaCalif, i)
            lt.addLast(listaPeorAverage, ind["title"])
        return listaPeorAverage["elements"]



def main():
    while True:
        printMenu() #imprimir el menu de opciones en consola
        inputs =input('Seleccione una opción para continuar:\n') #leer opción ingresada
        if len(inputs)>0:
            if int(inputs[0])==1: #opcion 1
                lista = loadCSVFile("Data/SmallMoviesDetailsCleaned.csv")
                lista2 = loadCSVFile("Data/MoviesCastingRaw-small.csv")
                print("Datos cargados, "+str(lt.size(lista)+lt.size(lista2))+" elementos cargados")
            elif int(inputs[0])==2:
                nombreDir = input("Ingrese el nombre del director: ")
                numPeli, prom = encontrarBuenasPeli(lista, lista2, nombreDir)
                print("El director {0} tiene {1} pelicula(s) buenas con puntaje promedio de {2}.".format(nombreDir, numPeli, prom))
            elif int(inputs[0])==3:
                print("¿Qué tipo de ranking quiere consultar?")
                print("1- Ranking películas más votadas.")
                print("2- Ranking películas menos votadas.")
                print("3- Ranking películas con mejor calificación.")
                print("4- Ranking películas con peor calificación.")
                decision = int(input(""))
                numPel = int(input("¿Cuántas películas quiere meter en el ranking? \n: "))
                resultado = rankingPeli(lista, decision, numPel)
                print("El ranking solicitado es: {0}".format(resultado))
            elif int(inputs[0])==4:
                nombreDir = input("Ingrese el nombre del director: ")
                titulos, numPeli, prom = conocerDirector(lista, lista2, nombreDir)
                print("El director {0} tiene {1} pelicula(s) con puntaje promedio de {2}.\nSus películas son: {3}".format(nombreDir, numPeli, prom, titulos))
            elif int(inputs[0])==5:
                nombreActor = input("Ingrese el nombre del actor: ")
                titulos, numPeli, prom = conocerActor(lista, lista2, nombreActor)
            elif int(inputs[0])==6:
                genero = input('Ingrese el genero: ')
                titulos, numPeli, prom =EntenderGenero(lista,lista2,genero)
                print("El genero {0} tiene {1} pelicula(s) con promedio de votos de: {2}.\nEstas peliculas son: {3}".format(genero, numPeli, prom, titulos))
            elif int(inputs[0])==7
                genero=input("¿Qué generó desea consultar?")
                print("¿Qué tipo de ranking quiere consultar?")
                print("1- Ranking películas más votadas.")
                print("2- Ranking películas menos votadas.")
                print("3- Ranking películas con mejor calificación.")
                print("4- Ranking películas con peor calificación.")
                decision = int(input(""))
                numPel = int(input("¿Cuántas películas quiere meter en el ranking? \n: "))
                resultado = rankingPeli(lista, decision, numPel)
                print("El ranking solicitado es: {0}".format(resultado))
            elif int(inputs[0])==0: #opcion 0, salir
                sys.exit(0)
            

if __name__ == "__main__":
    main()

###SHITSHITSHITSHIT