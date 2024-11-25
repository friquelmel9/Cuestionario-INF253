# -*- coding: utf-8 -*-


import random
import os

import re
# Para estos dict, considere key la unidad, mientras que el valor dentro una lista con todo lo necesario
dict_vf = dict()
dict_alt = dict()
dict_fig = dict()

# Sub dict con aquellas preguntas que vienen referenciadas de anteriores ejemplos
dict_vf_ref = dict()
dict_alt_ref = dict()

re_figvf = r'\[(\d+)\]'

listVf_All = []
listAlt_All = []
isCertamen = False

def getFig(unidad):

    if(unidad in dict_fig):
        return

    dict_fig[unidad] = list()
    arch_path = "Cuestionario/Quiz{0}/fig{0}.txt".format(unidad)

    with open(arch_path,'r') as arch:
        texto = ""
        cont = 0

        for linea in arch:
            if linea.startswith("#") or not linea.strip:
                continue
            if linea.startswith("begin"):
                texto = ""
            elif linea.startswith("end"):
                dict_fig[unidad].append(texto)
                cont += 1
            else:
                texto += linea

def leerAlt(unidad,arch_path):
    list_preguntas = list()
    with open(arch_path,'r') as arch:

        texto = ""
        respuesta = ""
        explicacion = ""

        for linea in arch:
            if linea.startswith("#") or not linea.strip:
                continue
            if linea.startswith("begin"):
                x,respuesta,explicacion = linea.strip().split("-|-")
                if explicacion == "":
                    explicacion = "No explicacion entregada"
            elif linea.startswith("figura"):
                x,fig = linea.strip().split(":")
                texto += dict_fig[unidad][int(fig)-1]
            elif linea.startswith("end"):
                if respuesta.lower() != "x":
                    list_preguntas.append([texto,respuesta,explicacion])
                texto = ""
                respuesta = ""
                explicacion = ""
            else:
                texto += linea

    return list_preguntas

def getAlt(unidad):
    if(unidad in dict_alt):
        return
    if(unidad in dict_alt_ref):
        return
    
    getFig(unidad)
    dict_alt[unidad] = leerAlt(unidad,"Cuestionario/Quiz{0}/alt{0}.txt".format(unidad))
    dict_alt_ref[unidad] = leerAlt(unidad,"Cuestionario/Quiz{0}/alt{0}ref.txt".format(unidad))

def leerVf(unidad, arch_path):
    list_preguntas = list()
    with open(arch_path,'r') as arch:
        for linea in arch:
            if linea.startswith("#") or not linea.strip():
                continue
            pregunta,respuesta,explicacion = linea.strip().split("-|-")
            pregunta = pregunta.replace("\\n","\n")
            if(explicacion == ""):
                explicacion = "No explicacion entregada"
            figura = re.findall(re_figvf,pregunta)
            if(figura):
                num = int(figura[-1])
                pregunta = re.sub(re_figvf, dict_fig[unidad][num-1], pregunta)
            if respuesta.lower() != "x":
                list_preguntas.append([pregunta,respuesta,explicacion])

    return list_preguntas

def getVf(unidad):
    if(unidad in dict_vf):
        return
    if(unidad in dict_vf_ref):
        return
    
    dict_vf[unidad] = leerVf(unidad, "Cuestionario/Quiz{0}/vf{0}.txt".format(unidad))
    dict_vf_ref[unidad] = leerVf(unidad,"Cuestionario/Quiz{0}/vf{0}ref.txt".format(unidad))

def iniciarQuiz():

    os.system('cls')
    unidad = int(input("¿Que unidad quieres realizar? [3-4-5]\n"))

    getFig(unidad)
    getVf(unidad)
    getAlt(unidad)

    list_vf = dict_vf[unidad]
    list_vf_ref = dict_vf_ref[unidad] 
    list_vf_total = list_vf + list_vf_ref

    list_alt = dict_alt[unidad]
    list_alt_ref = dict_alt_ref[unidad]
    list_alt_total = list_alt + list_alt_ref

    decision = int(input("¿Que tipo de test desea realizar? \n 1. Todo tipo de preguntas | 2. Preguntas de quiz/Certamenes pasados \n"))
        
    if(decision == 1):
        preguntasVf = random.sample(list_vf_total,10)
        preguntasAlt = random.sample(list_alt_total,5)
    
    elif(decision == 2):
       preguntasVf = random.sample(list_vf_ref,10)
       preguntasAlt = random.sample(list_alt_ref,5)
        
    
    correcto_vf = 0
    correcto_alt = 0

    input("Pulsar enter para continuar")

    os.system('cls')
    for pregunta,respuesta,explicacion in preguntasVf:
        usuario = input("[V-F] "+pregunta+"\n")
        if (usuario.lower() == respuesta.lower()):
            print("Respuesta correcta!")
            correcto_vf += 1
        else:
            print("La respuesta correcta era: "+respuesta+"\n Explicacion: "+explicacion)

        input("Pulsar enter para continuar")
        os.system('cls')

    for pregunta,respuesta,explicacion in preguntasAlt:
        usuario = input("[a,b,c,d,e] "+pregunta+"\n")
        if (usuario.lower() == respuesta.lower()):
            print("Respuesta correcta!")
            correcto_alt += 1
        else:
            print("La respuesta correcta era: "+respuesta+"\n Explicacion: "+explicacion)

        input("Pulsar enter para continuar")
        os.system('cls')

    print("Quiz terminado")
    print("Verdadero-falso correctas: "+str(correcto_vf))
    print("Alternativas correctas: "+str(correcto_alt))
    puntaje = correcto_alt*10 + correcto_vf*5
    print("Puntaje obtenido: "+str(puntaje))
    input("Pulsar enter para continuar")

def iniciarCertamen():
    
    listVf = []
    listAlt = []
    
    for i in range(1,6):
        print("unidad actual: "+str(i))
        getFig(i)
        getVf(i)
        getAlt(i)
        
        listVf_helper = []
        listVf_helper = listVf_helper + dict_vf[i]
        listVf_helper = listVf_helper + dict_vf_ref[i]
        listVf = listVf + random.sample(listVf_helper,4)
        
        listAlt_helper = []
        listAlt_helper = listAlt_helper + dict_alt[i]
        listAlt_helper = listAlt_helper + dict_alt_ref[i]
        listAlt = listAlt + random.sample(listAlt_helper,3)
        
    correctasVf = 0
    correctasAlt = 0
    
    input("Pulsar enter para continuar")
    os.system('cls')
    
    for pregunta,respuesta,explicacion in listVf:
        usuario = input("[V-F] "+pregunta+"\n")
        if(usuario.lower() == respuesta.lower()):
            print("Respuesta correcta!")
            correctasVf += 1
        else:
            print("La respuesta correcta era: "+respuesta+"\n Explicacion: "+explicacion)
        
        input("Pulsar enter para continuar")
        os.system('cls')
        
    for pregunta,respuesta,explicacion in listAlt:
        usuario = input("[a,b,c,d,e] "+pregunta+"\n")
        if (usuario.lower() == respuesta.lower()):
            print("Respuesta correcta!")
            correctasAlt += 1
        else:
            print("La respuesta correcta era: "+respuesta+"\n Explicacion: "+explicacion)

        input("Pulsar enter para continuar")
        os.system('cls')
        
    print("Certamen terminado")
    print("Cantidad de vf correctas: "+str(correctasVf)+" de 20 totales")
    print("Cantidad de alt correctas: "+str(correctasAlt)+" de 15 totales")
    print("Calculo de la nota no disponible")
    input("Pulse enter para continuar")

def main():
    decision = 0
    while(decision != 3):
        os.system('cls')            
        print("Bienvenido a Cuestionario.py \n ¿Que desea realizar?")
        decision = int(input("1. Realizar Quiz | 2. Realizar Certamen | 3. Terminar \n"))

        if(decision == 1):
            iniciarQuiz()
        
        if(decision == 2):
            iniciarCertamen()

main()