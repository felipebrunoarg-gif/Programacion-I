def secuencial_con_corte(vector, clave):
    comparaciones = 0
    pos = -1
    i = 0
    sigue = True
    while i < len(vector) and sigue:
        comparaciones = comparaciones + 1
        if vector[i] == clave:
            pos = i
            sigue = False
        elif vector[i] > clave:
            sigue = False
        i = i + 1
    return pos, comparaciones

vector = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
pos, comp = secuencial_con_corte(vector, 100)
print("Posición:", pos, "- Comparaciones:", comp)

#Clave	Comparaciones sin corte	Comparaciones con corte
#20	10	6
#1	10	1
#56	8	8
#100	10	10
#1.	¿En qué casos el corte no ahorra ninguna comparación?
#El corte no ahorra comparaciones en dos casos: cuando la clave está en el vector (como el 56), porque las dos búsquedas se detienen al encontrarla,
#y cuando la clave es mayor que todos los elementos (como el 100), porque nunca aparece un elemento mayor que permita cortar y se recorre el vector completo.

