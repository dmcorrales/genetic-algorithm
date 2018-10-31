# encoding: utf-8
# decode: utf-8
from decimal import Decimal
import random
class AlgoritmoGenetico:
    def __init__(self):
        self.poblacionTotal = [] # población inicial
        self.totalFitness = 0

        self.poblacionSeleccionada = []
        self.cantidadCromosomasPoblacionInicial = 8 

    #CARGO LAS PALABRAS (con filtro)
    def leerArchivo(self):
        file = open("palabras.txt","r")
        linea = file.readline()
        while linea:
            tempArray = linea.split(" ")
            cromosomaActual = Cromosoma(tempArray[0])
            self.totalFitness += cromosomaActual.funcionFitness
            self.poblacionTotal.append(cromosomaActual) #Cargo toda la población
            linea = file.readline()
        print("Total de palabras:" , len(self.poblacionTotal))
        print("Fitness:" , self.totalFitness)
        print("Fitness Promedio:", self.totalFitness/len(self.poblacionTotal))

    def ordenarPorFitness(self):
        self.poblacionTotal = sorted(self.poblacionTotal, key=lambda x: x.funcionFitness, reverse=True)


    #PRE-SELECCION. FILTRO QUE CARGA ESPECÍFICAMENTE 8 CROMOSOMAS DEL LISTADO DE FORMA ALEATORIA.
    #def seleccionarPoblacion(self):
    #    print("Palabras de la población seleccionada:")
    #    for i in range(self.cantidadCromosomasPoblacionInicial):
    #        randValue = random.randint(0,len(self.poblacionTotal))
    #        self.poblacionSeleccionada.append(self.poblacionTotal[randValue])
    #        print(self.poblacionSeleccionada[i].palabra, "Cantidad de letras correctas:", self.poblacionSeleccionada[i].funcionFitness)

    #def calcularFitness(self):
    #    for i in range(len(self.poblacionSeleccionada)):
    #        self.totalFitness += self.poblacionSeleccionada[i].funcionFitness

    #Se utiliza el proceso de selección RULETA.
    def seleccionReglaRuleta(self):
        #Inicio generando los valores respectivos de la torta.
        for i in range(len(self.poblacionTotal)):
            elementoActual = self.poblacionTotal[i]
            elementoActual.porcionRuleta = float(format(Decimal(elementoActual.funcionFitness * 100)))
            elementoActual.porcionRuleta /= float(format(Decimal(self.totalFitness)))

        for w in range(self.cantidadCromosomasPoblacionInicial):
            randValue = random.random() # Por cada cromosoma genero un nuevo número aleatorio
            valorAcumulado = 0
            for i in range(len(self.poblacionTotal)):
                valorAcumulado += self.poblacionTotal[i].porcionRuleta
                if(valorAcumulado >= randValue):
                    self.poblacionSeleccionada.append(self.poblacionTotal[i])
                    print("Dato guardado:" , self.poblacionTotal[i].palabra)
                    break

    #Se utiliza el proceso de cruce 2 puntos.
    def cruceCromosomas(self):
        i = 0
        while i < len(self.poblacionSeleccionada): #Asigno una pareja a cada cromosoma
            sum = i+1
            self.poblacionSeleccionada[i].crucePos = sum
            self.poblacionSeleccionada[sum].crucePos = i
            i += 2
        print("antes del proceso de cruzamiento:")
        self.mostrarTablaActual()
        minCruce = 1 #VALOR MÍNIMO A CONSIDERAR DENTRO DE LA AMPLITUD 
        maxCruce = 3 #VALOR MÁXIMO A CONSIDERAR DENTRO DE LA AMPLITUD
        i = 0
        while i < len(self.poblacionSeleccionada):
            strPalabra1 = self.poblacionSeleccionada[i].palabra
            max = i+1
            strPalabra2 = self.poblacionSeleccionada[max].palabra
            strList1 = list(strPalabra1)
            strList2 = list(strPalabra2)
            strList11 = list(strPalabra1)
            strList1[minCruce:maxCruce] = strList2[minCruce:maxCruce]
            strList2[minCruce:maxCruce] = strList11[minCruce:maxCruce]
            self.poblacionSeleccionada[i].newPalabra = ''.join(strList1)
            self.poblacionSeleccionada[max].newPalabra = ''.join(strList2)
            i+=2
        print("Luego del proceso de cruzamiento:")
        self.mostrarTablaActual()

    #Proceso Opcional (..)
    def procesoMutacion(self):
        for i in range(len(self.poblacionSeleccionada)):
            strPalabara = self.poblacionSeleccionada[i].newPalabra
            strListPalabra = list(strPalabara)
            
            #PALABRAS A INTERCAMBIAR
            aux = strListPalabra[1]
            aux1 = strListPalabra[2]

            strListPalabra[1] = aux1
            strListPalabra[2] = aux

            self.poblacionSeleccionada[i].newPalabra = ''.join(strListPalabra)

        self.mostrarTablaActual()


    def mostrarTablaActual(self):
        print('Palabra', 'Fitness', 'Cruce []', ' Palabra despues del cruce o mutacion')
        for i in range(len(self.poblacionSeleccionada)):
            print(self.poblacionSeleccionada[i].palabra, self.poblacionSeleccionada[i].funcionFitness, self.poblacionSeleccionada[i].crucePos,self.poblacionSeleccionada[i].newPalabra)
            
class Cromosoma:
    def __init__(self, palabra):
        self.palabra = palabra
        self.fraseObjeto = "MUNDO"
        self.funcionFitness = self.calcularFunctionFitness()
        self.porcionRuleta = Decimal(0.0)
        self.crucePos = 0 #Posición de mi cruce
        self.newPalabra = self.palabra

    #La función fitness y la palabra inicial está preestablecida.
    def calcularFunctionFitness(self):
        totalPalabras = 0
        for i in range(len(self.fraseObjeto)):
            if(len(self.fraseObjeto) == len(self.palabra)):
                if(self.fraseObjeto[i] == self.palabra[i]):
                    totalPalabras +=1
            else:
                print("El tamaño de los cromosomas no coinciden.")
        #Establezco el valor Fitness
        return 2**totalPalabras 

algoGen = AlgoritmoGenetico()
algoGen.leerArchivo()
algoGen.ordenarPorFitness()
algoGen.seleccionReglaRuleta()
algoGen.cruceCromosomas()
algoGen.procesoMutacion()

