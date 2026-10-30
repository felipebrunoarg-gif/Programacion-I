import json
 
def leer_inscriptos():
    try:
        archivo = open("inscriptos.json", "r", encoding="utf-8")
        jugadores = json.load(archivo)
        archivo.close()
    except FileNotFoundError:
        jugadores = []
    return jugadores
 
 
def leer_parejas():
    try:
        archivo = open("parejas.json", "r", encoding="utf-8")
        parejas = json.load(archivo)
        archivo.close()
    except FileNotFoundError:
        parejas = []
    return parejas
 
 
def cargar_jugadores():
    jugadores = []
    
    cantidad_str = input("¿Cuántos jugadores van a participar en el torneo? (Debe ser un número par): ")
    while not cantidad_str.isdigit() or int(cantidad_str) <= 0 or int(cantidad_str) % 2 != 0:
        print("Error: La cantidad debe ser un número entero positivo y par para poder armar parejas.")
        cantidad_str = input("¿Cuántos jugadores van a participar en el torneo? (Debe ser un número par): ")
    
    cantidad = int(cantidad_str)
    
    for i in range(cantidad):
        nombre = input(f"Ingrese el nombre del jugador {i + 1}: ")
        
        categoria_str = input(f"Ingrese la categoría del jugador {i + 1} (por ejemplo, 4ª, 5ª o 6ª): ")
        while not categoria_str.isdigit():
            print("Error: Debe ingresar un número entero.")
            categoria_str = input(f"Ingrese la categoría del jugador {i + 1} (por ejemplo, 4ª, 5ª o 6ª): ")
        
        categoria = int(categoria_str)
        jugadores.append({"nombre": nombre, "categoria": categoria})
    return jugadores
 
def armar_parejas(jugadores):
    parejas = []
    cantidad_parejas = int(input("¿Cuántas parejas querés armar? "))
    for i in range(cantidad_parejas):
        nombre_pareja = input(f"Ingrese el nombre de la pareja {i + 1}: ")
        print("Seleccione los jugadores para esta pareja:")
        for j, jugador in enumerate(jugadores):
            print(f"{j + 1}. {jugador['nombre']} ({jugador['categoria']})")
        indices = input("Ingrese los números de los dos jugadores separados por un espacio: ").split()
        jugador1 = jugadores[int(indices[0]) - 1]
        jugador2 = jugadores[int(indices[1]) - 1]
        parejas.append({"nombre": nombre_pareja, "jugadores": [jugador1, jugador2], "puntos": 0})
    return parejas
 
def guardar_jugadores(jugadores):
    archivo = open("inscriptos.json", "w", encoding="utf-8")
    json.dump(jugadores, archivo, indent=4, ensure_ascii=False)
    archivo.close()
 
def guardar_parejas(parejas):
    archivo = open("parejas.json", "w", encoding="utf-8")
    json.dump(parejas, archivo, indent=4, ensure_ascii=False)
    archivo.close()
 
def ordenar_seleccion_nombre(lista):
    n = len(lista)
    comparaciones = 0
    intercambios = 0
    for i in range(n - 1):
        pos_min = i
        for j in range(i + 1, n):
            comparaciones = comparaciones + 1
            if lista[j]["nombre"] < lista[pos_min]["nombre"]:
                pos_min = j
        lista[i], lista[pos_min] = lista[pos_min], lista[i]
        intercambios = intercambios + 1
    return comparaciones, intercambios
 
 
def ordenar_burbuja_categoria(lista):
    n = len(lista)
    comparaciones = 0
    intercambios = 0
    for i in range(n - 1):
        for j in range(n - 1 - i):
            comparaciones = comparaciones + 1
            izq = lista[j]
            der = lista[j + 1]
            if izq["categoria"] > der["categoria"] or (izq["categoria"] == der["categoria"] and izq["nombre"] > der["nombre"]):
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
                intercambios = intercambios + 1
    return comparaciones, intercambios
 
 
def ordenar_seleccion_puntos(lista):
    n = len(lista)
    for i in range(n - 1):
        pos_max = i
        for j in range(i + 1, n):
            if lista[j]["puntos"] > lista[pos_max]["puntos"]:
                pos_max = j
        lista[i], lista[pos_max] = lista[pos_max], lista[i]
        
def mostrar_menu():
    print("\n1. Inscribir jugadores")
    print("2. Armar parejas")
    print("3. Lista alfabética")
    print("4. Lista por categoría")
    print("5. Cargar puntos")
    print("6. Tabla de posiciones")
    print("7. Salir")
 
 
def main():
    jugadores = leer_inscriptos()
    parejas = leer_parejas()
    opcion = ""
    while opcion != "7":
        mostrar_menu()
        opcion = input("Elegí una opción: ")
        if opcion == "1":
            nuevos = cargar_jugadores()
            for jugador in nuevos:
                jugadores.append(jugador)
            guardar_jugadores(jugadores)
            print("Jugadores guardados en inscriptos.json")
        elif opcion == "2":
            nuevas = armar_parejas(jugadores)
            for pareja in nuevas:
                parejas.append(pareja)
            guardar_parejas(parejas)
            print("Parejas guardadas en parejas.json")
        elif opcion == "3":
            copia = jugadores.copy()
            comp, inter = ordenar_seleccion_nombre(copia)
            print("Comparaciones:", comp, "- Intercambios:", inter)
            print("\nInscriptos en orden alfabético:")
            for jugador in copia:
                print(jugador["nombre"])
        elif opcion == "4":
            copia = jugadores.copy()
            comp, inter = ordenar_burbuja_categoria(copia)
            print("Comparaciones:", comp, "- Intercambios:", inter)
            categoria_actual = 0
            for jugador in copia:
                if jugador["categoria"] != categoria_actual:
                    categoria_actual = jugador["categoria"]
                    print("\nCategoría", categoria_actual)
                print("  ", jugador["nombre"])
        elif opcion == "5":
            for i in range(len(parejas)):
                print(i + 1, "-", parejas[i]["nombre"], "(", parejas[i]["puntos"], "puntos )")
            num = int(input("Número de pareja: "))
            puntos = int(input("Puntos ganados: "))
            parejas[num - 1]["puntos"] = parejas[num - 1]["puntos"] + puntos
            guardar_parejas(parejas)
            print("Puntos cargados")
        elif opcion == "6":
            copia = parejas.copy()
            ordenar_seleccion_puntos(copia)
            print("\nTabla de posiciones:")
            for i in range(len(copia)):
                print(i + 1, "-", copia[i]["nombre"], "-", copia[i]["puntos"], "puntos")
 
 
main()