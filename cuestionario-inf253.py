import random
import os

# Para estos dict, considere key la unidad, mientras que el valor dentro una lista con todo lo necesario
dict_vf = dict()
dict_alt = dict()
dict_fig = dict()

# Sub dict con aquellas preguntas que vienen referenciadas de anteriores ejemplos
dict_vf_ref = dict()
dict_alt_ref = dict()

def getFig(unidad):

    if(unidad in dict_fig):
        return

    dict_fig[unidad] = list()
    arch_path = "Cuestionario/Unidad{0}/fig{0}.txt".format(unidad)

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
                x,respuesta,explicacion = linea.strip().split("|")
                if explicacion == "":
                    explicacion = "No explicacion entregada"
            elif linea.startswith("figura"):
                x,fig = linea.strip().split(":")
                texto += dict_fig[unidad][int(fig)-1]
            elif linea.startswith("end"):
                if respuesta != "x" or respuesta != "X":
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
    dict_alt[unidad] = leerAlt(unidad,"Cuestionario/Unidad{0}/alt{0}.txt".format(unidad))
    dict_alt_ref[unidad] = leerAlt(unidad,"Cuestionario/Unidad{0}/alt{0}ref.txt".format(unidad))

def leerVf(arch_path):
    list_preguntas = list()
    with open(arch_path,'r') as arch:

        for linea in arch:
            if linea.startswith("#") or not linea.strip():
                continue
            pregunta,respuesta,explicacion = linea.strip().split("|")
            if respuesta != "x" or respuesta != "X":
                list_preguntas.append([pregunta,respuesta,explicacion])

    return list_preguntas

def getVf(unidad):
    if(unidad in dict_vf):
        return
    if(unidad in dict_vf_ref):
        return
    
    dict_vf[unidad] = leerVf("Cuestionario/Unidad{0}/vf{0}.txt".format(unidad))
    dict_vf_ref[unidad] = leerVf("Cuestionario/Unidad{0}/vf{0}ref.txt".format(unidad))
    
def iniciarQuiz(unidad):

    getVf(unidad)
    getAlt(unidad)
    getFig(unidad)

    list_vf = dict_vf[unidad]
    list_vf2 = dict_vf_ref[unidad]
    list_vf.extend(list_vf2)

    list_alt = dict_alt[unidad]
    list_alt_ref = dict_alt_ref[unidad]
    list_alt.extend(list_alt_ref)

    preguntasVf = random.sample(list_vf,10)
    preguntasAlt = random.sample(list_alt,5)

    correcto_vf = 0
    correcto_alt = 0

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
        usuario = input("[a,b,c,d] "+pregunta+"\n")
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

def main():
    decision = 0
    while(decision != 3):
        os.system('cls')            
        print("Bienvenido a Cuestionario.py \n ¿Que desea realizar?")
        decision = int(input("1. Realizar Quiz (Unidad 5) | 2. Realizar Certamen | 3. Terminar \n"))

        if(decision == 1):
            iniciarQuiz(5)
        
        if(decision == 2):
            print("No disponible aun")

main()