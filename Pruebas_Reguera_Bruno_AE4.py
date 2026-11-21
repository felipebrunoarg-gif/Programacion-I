"""Pruebas de Logix_Dependencias_Reguera_Bruno_AE4.py. Ejecutar: python Pruebas_Reguera_Bruno_AE4.py"""
import builtins
import os
import Logix_Dependencias_Reguera_Bruno_AE4 as L

fallos = 0


def probar(id_, caso, esperado, funcion):
    """Ejecuta funcion() y compara con esperado ('ValueError' si debe fallar)."""
    global fallos
    try:
        obtenido = funcion()
    except ValueError:
        obtenido = "ValueError"
    ok = obtenido == esperado
    fallos += not ok
    print(f"{id_} | {caso} | esperado: {esperado} | obtenido: {obtenido} | "
          f"{'Validado' if ok else 'FALLO'}")


def recorrido(g, ini):
    v = []
    L.dfs_recursivo(g, ini, v)
    return v


def con_teclado(entradas, funcion):
    """Simula al usuario escribiendo 'entradas' en input()."""
    it = iter(entradas)
    original = builtins.input
    builtins.input = lambda _="": next(it)
    try:
        return funcion()
    finally:
        builtins.input = original


def agregar_api():
    g = L.cargar_grafo("logix_legacy.txt")
    L.agregar_modulo(g, "API")
    L.agregar_dependencia(g, "PED", "API")
    return g["PED"], L.calcular_grados(g)["API"]


G = L.cargar_grafo("logix_legacy.txt")
G2 = L.cargar_grafo("logix_reestructurado.txt")

probar("P01", "Carga de topologia original", (9, 14),
       lambda: (len(G), sum(len(d) for d in G.values())))
probar("P02", "Calculo de grados (INV y CLI)", ((1, 4), (0, 1)),
       lambda: (L.calcular_grados(G)["INV"], L.calcular_grados(G)["CLI"]))
probar("P03", "DFS desde PED",
       ["PED", "CLI", "INV", "ROB", "ASG", "RUT", "SEG"], lambda: recorrido(G, "PED"))
probar("P04", "Impacto en cascada de INV (todos menos CLI)",
       [m for m in G if m != "CLI"], lambda: L.modulos_afectados(G, "INV"))
probar("P05", "Deteccion de ciclos en G",
       [["INV", "ROB"], ["ASG", "RUT", "SEG"]], lambda: L.detectar_ciclos(G))
probar("P06", "Limite: orden topologico con ciclos", "ValueError",
       lambda: L.orden_topologico_kahn(G))
probar("P07", "Orden topologico en G'",
       ["CLI", "INV", "SEG", "ROB", "RUT", "ASG", "PED", "ENT", "REP"],
       lambda: L.orden_topologico_kahn(G2))
probar("P08", "Agregar modulo API y arista PED -> API",
       (["CLI", "INV", "ASG", "API"], (0, 1)), agregar_api)
probar("P09", "Limite: BFS desde modulo inexistente (el menu avisa)", None,
       lambda: con_teclado(["XYZ"], lambda: L.ejecutar("5", G) and None))
probar("P10", "Limite: archivo inexistente", "ValueError",
       lambda: L.cargar_grafo("no_existe.txt"))

# Pruebas extra
mods, mat = L.generar_matriz_adyacencia(G2)
probar("P11", "Extra: matriz de adyacencia de G' (fila ASG)", [0, 0, 1, 0, 0, 1, 1, 0, 0],
       lambda: mat[mods.index("ASG")])
probar("P12", "Extra: eliminar dependencia INV -> ROB deja a INV sin dependencias", [],
       lambda: (lambda g: (L.eliminar_dependencia(g, "INV", "ROB"), g["INV"])[1])(
           L.cargar_grafo("logix_legacy.txt")))
probar("P13", "Extra: dependencia a modulo inexistente", "ValueError",
       lambda: L.agregar_dependencia(L.cargar_grafo("logix_legacy.txt"), "PED", "XYZ"))
probar("P14", "Extra: eliminar modulo ROB lo quita tambien de INV", [],
       lambda: (lambda g: (L.eliminar_modulo(g, "ROB"), g["INV"])[1])(
           L.cargar_grafo("logix_legacy.txt")))


def reporte_ok():
    L.exportar_reporte(G, "reporte_analisis.txt")
    with open(L.ruta("reporte_analisis.txt"), encoding="utf-8") as f:
        t = f.read()
    return "INV -> ROB -> INV" in t and "ASG -> RUT -> SEG -> ASG" in t


probar("P15", "Extra: reporte exportado informa los ciclos", True, reporte_ok)


def archivo_mal_formado():
    ruta = L.ruta("malo.tmp")
    with open(ruta, "w", encoding="utf-8") as f:
        f.write("PED CLI\n")
    try:
        return L.cargar_grafo("malo.tmp")
    finally:
        os.remove(ruta)


probar("P16", "Extra: archivo sin ':' en una linea", "ValueError", archivo_mal_formado)

print("Todas las pruebas pasaron" if not fallos else f"{fallos} prueba(s) fallaron")
