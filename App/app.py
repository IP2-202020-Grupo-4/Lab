import config as cf
import sys
import csv
from time import process_time 
from ADT import list as lt
from Sorting import shellsort as SSort



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
    print('6- Conocer género')
    print("7- Consultar ranking por género")
    print("0- Salir")

def encontrarBuenasPeli(listaCalif, listaDirector, nombre)->tuple:
    contador = 0
    contador2 = 0
    for i in range(0, lt.size(listaCalif)):
        if listaDirector["elements"][i]["director_name"].lower() == nombre.lower():
            if float(listaCalif["elements"][i]["vote_average"]) >= 6:
                contador += float(listaCalif["elements"][i]["vote_average"])
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

    contador = 0
    contador2 = 0
    for i in range(0, lt.size(listaCalif)):
        if listaDirector["elements"][i]["director_name"].lower() == nombre.lower():
            contador += float(listaCalif["elements"][i]["vote_average"])
            contador2 += 1
            titPeli = listaCalif["elements"][i]["title"]
            lt.addLast(lista1, titPeli)

    if contador2 == 0:
        return lista1["elements"], 0, 0

    prom = contador/contador2
    return lista1["elements"], contador2, prom

def conocerActor(listaCalif, listaDirector, nombre)->tuple:
    lista1 = lt.newList("ARRAY_LIST")
    lista2 = lt.newList("ARRAY_LIST")
    diccDirectores = {}

    contador = 0
    contador2 = 0
    for i in range(0, lt.size(listaDirector)):
        if (listaDirector["elements"][i]["actor1_name"].lower() == nombre.lower()) or (listaDirector["elements"][i]["actor2_name"].lower() == nombre.lower()) or (listaDirector["elements"][i]["actor3_name"].lower() == nombre.lower()) or (listaDirector["elements"][i]["actor4_name"].lower() == nombre.lower()) or (listaDirector["elements"][i]["actor5_name"].lower() == nombre.lower()):
            lt.addLast(lista1, i)
            contador += float(listaCalif["elements"][i]["vote_average"])
            contador2 += 1
            titPeli = listaCalif["elements"][i]["title"]
            titDirec = listaDirector["elements"][i]["director_name"]
            lt.addLast(lista1, titPeli)
            lt.addLast(lista2, titDirec)

    tam = lt.size(lista2)
    
    if contador2 == 0:
        return lista1["elements"], 0, 0, "Ninguno"


    
    for i in range(0, tam):
        if lista2["elements"][i] not in list(diccDirectores.keys()):
            diccDirectores[lista2["elements"][i]] = 1
        else:
            diccDirectores[lista2["elements"][i]] += 1

    llaves = list(diccDirectores.keys())
    valores = list(diccDirectores.values())
    mayor = max(valores)

    director = llaves[valores.index(mayor)]

    

    prom = contador/contador2
    return lista1["elements"], contador2, prom, director

def entenderGenero(listaCalif, genero)->tuple:
    lista1 = lt.newList("ARRAY_LIST")
    contador = 0
    contador2 = 0

    for i in range(0, lt.size(listaCalif)):
        if (genero.lower() in listaCalif["elements"][i]["genres"].lower() ):
            contador += float(listaCalif["elements"][i]["vote_count"])
            contador2 += 1
            titPeli = listaCalif["elements"][i]["title"]
            lt.addLast(lista1, titPeli)

    if contador2 == 0:
        return lista1["elements"], 0, 0, "Ninguno"
        
    prom=contador/contador2
    return (lista1['elements'], contador2, prom)
    
def rankingGenero (listaDetalles, genero, numPel, decision)->tuple:
    listaCalif = lt.newList("ARRAY_LIST")
    contador = 0
    contador2 = 0

    for i in range(0, lt.size(listaDetalles)):
        if (genero.lower() in listaDetalles["elements"][i]["genres"].lower()):
            ind = listaDetalles["elements"][i]
            lt.addLast(listaCalif, ind)

    if decision == 1:
        listaMasVotos = lt.newList("ARRAY_LIST")
        SSort.shellSort(listaCalif, greaterCount)
        
        for i in range(0, numPel+1):
            elem = listaCalif["elements"][i]
            lt.addLast(listaMasVotos, elem["title"])
            contador += float(elem["vote_count"])
            contador2 += 1

        if contador2 == 0:
            return "No hay títulos.", 0

        prom = contador/contador2
        
        return listaMasVotos["elements"], prom

    elif decision == 2:
        listaMenosVotos = lt.newList("ARRAY_LIST")
        SSort.shellSort(listaCalif, lessCount)
    
        for i in range(0, numPel+1):
            elem = listaCalif["elements"][i]
            lt.addLast(listaMenosVotos, elem["title"])
            contador += float(elem["vote_count"])
            contador2 += 1

        if contador2 == 0:
            return "No hay títulos.", 0
        
        prom = contador/contador2

        return listaMenosVotos["elements"], prom

    elif decision == 3:
        listaMejorAverage = lt.newList("ARRAY_LIST")
        SSort.shellSort(listaCalif, greaterVote)

        for i in range(0, numPel+1):
            elem = listaCalif["elements"][i]
            lt.addLast(listaMejorAverage, elem["title"])
            contador += float(elem["vote_average"])
            contador2 += 1
        

        if contador2 == 0:
            return "No hay títulos.", 0

        prom = contador/contador2

        return listaMejorAverage["elements"], prom

    elif decision == 4:
        listaPeorAverage = lt.newList("ARRAY_LIST")
        SSort.shellSort(listaCalif, lessVote)

        for i in range(0, numPel+1):
            elem = listaCalif["elements"][i]
            lt.addLast(listaPeorAverage, elem["title"])
            contador += float(elem["vote_average"])
            contador2 += 1
        
        if contador2 == 0:
            return "No hay títulos.", 0
        
        prom = contador/contador2

        return listaPeorAverage["elements"], prom



def main():
    while True:
        printMenu() #imprimir el menu de opciones en consola
        inputs =input('Seleccione una opción para continuar:\n') #leer opción ingresada
        if len(inputs)>0:
            if int(inputs[0])==1: #opcion 1
                lista = loadCSVFile("Data/AllMoviesDetailsCleaned.csv")
                lista2 = loadCSVFile("Data/AllMoviesCastingRaw.csv")
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
                titulos, numPeli, prom, director = conocerActor(lista, lista2, nombreActor)
                print("El actor {0} tiene {1} pelicula(s) con puntaje promedio de {2}.\nEl director con el cual más ha colaborado es {3}. \nSus películas son: {4}".format(nombreActor, numPeli, prom, director, titulos))
            elif int(inputs[0])==6:
                genero = input('Ingrese el género: ')
                titulos, numPeli, prom = entenderGenero(lista,genero)
                print("El género {0} tiene {1} película(s) con promedio de votos de: {2}.\nEstas películas son: {3}".format(genero, numPeli, prom, titulos))
            elif int(inputs[0])==7:
                genero = input("Ingrese el género a consultar: ")
                print("¿Qué tipo de ranking quiere consultar?")
                print("1- Ranking películas más votadas.")
                print("2- Ranking películas menos votadas.")
                print("3- Ranking películas con mejor calificación.")
                print("4- Ranking películas con peor calificación.")
                decision = int(input(""))
                numPel = int(input("¿Cuántas películas quiere meter en el ranking? \n: "))
                titulos, promedio = rankingGenero(lista, genero, numPel, decision)
                print("El ranking solicitado tiene un promedio de {0} es: {1}".format(promedio, titulos))
            elif int(inputs[0])==0:
                sys.exit(0)
            

if __name__ == "__main__":
    main()