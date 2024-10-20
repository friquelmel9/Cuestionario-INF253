import random

dict_figuras = dict()

def makeFiguras(unidad):
    if int(unidad) not in dict_figuras:

        dict_figuras[unidad] = dict()
        texto_figura = ""
        cont = 0

        if unidad == 5:
            nombre_arch = "Cuestionario/Unidad5/figurasU5.txt"
        
        with open(nombre_arch,"r") as arch:
            for linea in arch:
                if linea.startswith("figura") or not linea.strip():
                    dict_figuras[unidad][cont] = texto_figura
                    cont += 1
                    texto_figura = ""
                    continue
                texto_figura = texto_figura+linea[1:]

def getVerdaderoFalso(unidad, cantidad):
    nombre_arch = ""
    if unidad == 5:
        nombre_arch = "Cuestionario/Unidad5/verdaderoFalsoU5.txt"
    
    list_preguntas = []
    with open(nombre_arch,"r") as arch:
        for linea in arch:
            if linea.startswith("#") or not linea.strip():
                continue
            pregunta, respuesta = linea.strip().split("|")
            pregunta = "[V-F] "+pregunta
            list_preguntas.append([pregunta.replace("\\n","\n"), respuesta])

    return random.sample(list_preguntas, cantidad)

def getOpcionMultiple(unidad, cantidad):
    nombre_arch = ""
    if unidad == 5:
        nombre_arch = "Cuestionario/Unidad5/opcionMultipleU5.txt"

    list_preguntas = []
    if(unidad not in dict_figuras):
        makeFiguras(unidad)
    pregunta_actual = ["","",""]

    with open(nombre_arch,"r") as arch:
        for linea in arch:
            if linea.startswith("#") or not linea.strip():
                continue
            if linea.startswith("Pregunta") and pregunta_actual != ["","",""]:
                list_preguntas.append(pregunta_actual)
            if linea.startswith("Pregunta"):
                pregunta_actual = ["[a,b,c,d]","",""]
                linea = linea.strip().split("|")
                if linea[1] != " ":
                    figuras = linea[1].split(",")
                    for figura in figuras:
                        pregunta_actual[1] += dict_figuras[unidad][int(figura)]
                pregunta_actual[2] += linea[2]
            else:
                pregunta_actual[0] += linea[1:]

    return random.sample(list_preguntas, cantidad)

def iniciarQuiz(unidad):
    correctas_vf = 0
    correctas_alt = 0
    makeFiguras(unidad)
    opcionesVerdaderoFalso = getVerdaderoFalso(unidad,10)
    for pregunta, respuesta in opcionesVerdaderoFalso:
        usuario_respuesta = input(pregunta + "\n")
        if usuario_respuesta.lower() == respuesta.lower():
            print("Respuesta correcta!")
            correctas_vf += 1
        else:
            print("La respuesta correcta era "+respuesta)
        input("Pulse enter para continuar:\n")

    opcionesMultiples = getOpcionMultiple(unidad,5)
    for pregunta,figuras,respuesta in opcionesMultiples:
        pregunta = pregunta.replace('\n','\n'+figuras,1)
        usuario_respuesta = input(pregunta + "\n")
        if usuario_respuesta.lower() == respuesta.lower():
            print("Respuesta correcta!")
            correctas_alt += 1
        else:
            print("La respuesta correcta era "+respuesta)
        input("Pulse enter para continar:\n")
    
    nota = correctas_alt*10 + correctas_vf*5
    print("TEST TERMINADO: Resultados son:")
    print("Correctas Verdadero y Falso: "+str(correctas_vf)+"\nCorrectas Opcion Multiple: "+str(correctas_alt)+"\nNota final: "+str(nota))

def main():

    print("Inicio Quiz: Que se desea hacer")
    decision = 0
    while(decision != 3):
        decision = input("1. Realizar Quiz (U5) | 2. Realizar Certamen | 3. Salir\n")
        decision = int(decision)
        if(decision == 1):
            iniciarQuiz(5)
        elif(decision == 2):
            print("No disponible Actualmente")



    



    

main()

