import random

def obtenerpreguntas(nombre_arch):
    list_preguntas = []
    with open(nombre_arch,"r") as arch:
        for linea in arch:
            if linea.startswith("#") or not linea.strip():
                continue
            pregunta, respuesta = linea.strip().split("|")
            pregunta = "[V-F] "+pregunta
            list_preguntas.append([pregunta.replace("\\n","\n"), respuesta])

    return list_preguntas

def getpreguntasVerdaderoFalso(unidad, cantidad):
    if unidad == "5":
        list_preguntas_VerdaderoFalso = obtenerpreguntas("Cuestionario/Unidad5/verdaderoFalsoU5.txt")
        return random.sample(list_preguntas_VerdaderoFalso, cantidad)

def main():
    print("Testeo verdaderoFalso (Unidad 5)")
    correctas = 0
    cuestionario = getpreguntasVerdaderoFalso("5",10)
    for pregunta, respuesta in cuestionario:
        usuario_respuesta = input(pregunta + "\n")
        if usuario_respuesta.lower() == respuesta.lower():
            print("Respuesta correcta!")
            correctas += 1
        else:
            print("La respuesta correcta era "+respuesta)

main()