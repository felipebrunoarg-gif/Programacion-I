def busqueda_secuencial(vector, clave):
    pos = -1
    i = 0
    while i < len(vector) and pos == -1:
        if vector[i] == clave:
            pos = i
        i = i + 1
    return pos

def contar_apariciones(vector, clave):
    posiciones = []
    for i in range(len(vector)):
        if vector[i] == clave:
            posiciones.append(i)
    return posiciones

n = int(input("Cantidad de números: "))
vector = []
for i in range(n):
    vector.append(int(input(f"Número {i + 1}: ")))
x = int(input("Número a buscar: "))

pos = busqueda_secuencial(vector, x)
if pos != -1:
    print(f"{x} aparece por primera vez en la posición {pos}")
else:
    print(f"{x} no está en el vector")

posiciones = contar_apariciones(vector, x)
print(f"Aparece {len(posiciones)} veces, en las posiciones {posiciones}")