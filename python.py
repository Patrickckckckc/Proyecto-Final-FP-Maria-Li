import os
from datetime import datetime

# Archivo permanente de datos (Tema 5: Persistencia de datos)
ARCHIVO_EXPEDIENTES = "expedientes.txt"


# ===================================================================
# TEMA 4: CADENAS DE CARACTERES Y VALIDACIONES
# ===================================================================
def validar_dni(dni):
    """Valida que el DNI contenga exactamente 8 dígitos numéricos."""
    return dni.isdigit() and len(dni) == 8


def validar_texto(texto):
    """Valida que la cadena no esté vacía ni contenga solo espacios."""
    return len(texto.strip()) > 0


def formatear_expediente(codigo, dni, remitente, asunto, fecha, estado):
    """Formatea los datos del expediente en una sola línea delimitada por '|'."""
    return f"{codigo}|{dni}|{remitente}|{asunto}|{fecha}|{estado}\n"


# ===================================================================
# TEMA 5: PERSISTENCIA DE DATOS CON ARCHIVOS
# ===================================================================
def guardar_expediente_archivo(registro):
    """Escribe un nuevo registro de expediente al final del archivo plano."""
    with open(ARCHIVO_EXPEDIENTES, "a", encoding="utf-8") as archivo:
        linea = formatear_expediente(*registro)
        archivo.write(linea)


def cargar_expedientes_archivo():
    """Lee el archivo plano y carga los datos en arreglos paralelos en memoria."""
    codigos, dnis, remitentes, asuntos, fechas, estados = [], [], [], [], [], []

    if os.path.exists(ARCHIVO_EXPEDIENTES):
        with open(ARCHIVO_EXPEDIENTES, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                linea = linea.strip()
                if linea:
                    partes = linea.split("|")
                    if len(partes) == 6:
                        codigos.append(partes[0])
                        dnis.append(partes[1])
                        remitentes.append(partes[2])
                        asuntos.append(partes[3])
                        fechas.append(partes[4])
                        estados.append(partes[5])

    return codigos, dnis, remitentes, asuntos, fechas, estados


# ===================================================================
# TEMA 3: ARREGLOS Y PROCESAMIENTO DE DATOS LINEALES
# ===================================================================
def buscar_expediente_por_codigo(codigos, cod_buscado):
    """Realiza una búsqueda lineal en el arreglo de códigos."""
    cod_buscado = cod_buscado.strip().upper()
    for i in range(len(codigos)):
        if codigos[i] == cod_buscado:
            return i  # Retorna el índice del expediente en los arreglos paralelos
    return -1


def ordenar_expedientes_burbuja(
    codigos, dnis, remitentes, asuntos, fechas, estados
):
    """
    Ordena los expedientes por código ascendente usando el Algoritmo de Burbuja,
    mantiendolos sincronizados en los arreglos paralelos.
    """
    n = len(codigos)
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if codigos[j] > codigos[j + 1]:
                # Intercambio simultáneo de elementos en los arreglos paralelos
                codigos[j], codigos[j + 1] = codigos[j + 1], codigos[j]
                dnis[j], dnis[j + 1] = dnis[j + 1], dnis[j]
                remitentes[j], remitentes[j + 1] = (
                    remitentes[j + 1],
                    remitentes[j],
                )
                asuntos[j], asuntos[j + 1] = asuntos[j + 1], asuntos[j]
                fechas[j], fechas[j + 1] = fechas[j + 1], fechas[j]
                estados[j], estados[j + 1] = estados[j + 1], estados[j]


# ===================================================================
# TEMA 2: FUNCIONES Y MODULARIDAD
# ===================================================================
def registrar_nuevo_expediente(
    codigos, dnis, remitentes, asuntos, fechas, estados
):
    """Gestiona la captura, validación y persistencia de un nuevo expediente."""
    print("\n---------------------------------------------")
    print("        REGISTRO DE NUEVO EXPEDIENTE         ")
    print("---------------------------------------------")

    # Generación de código correlativo único (e.g., EXP-2026-001)
    correlativo = len(codigos) + 1
    codigo = f"EXP-2026-{correlativo:03d}"

    # Entrada y validación de DNI
    dni = input("Ingrese DNI del ciudadano (8 dígitos): ").strip()
    while not validar_dni(dni):
        dni = input(
            "   [ERROR] DNI inválido. Reingrese DNI (8 dígitos): "
        ).strip()

    # Entrada y validación de Remitente
    remitente = input("Ingrese nombre completo del remitente: ").strip().title()
    while not validar_texto(remitente):
        remitente = (
            input("   [ERROR] El nombre no puede estar vacío. Reingrese: ")
            .strip()
            .title()
        )

    # Entrada y validación de Asunto
    asunto = input("Ingrese el asunto o descripción del trámite: ").strip()
    while not validar_texto(asunto):
        asunto = input(
            "   [ERROR] El asunto no puede estar vacío. Reingrese: "
        ).strip()

    fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
    estado = "RECIBIDO"

    # Inserción en arreglos paralelos en memoria
    codigos.append(codigo)
    dnis.append(dni)
    remitentes.append(remitente)
    asuntos.append(asunto)
    fechas.append(fecha)
    estados.append(estado)

    # Persistencia en archivo de texto
    registro = (codigo, dni, remitente, asunto, fecha, estado)
    guardar_expediente_archivo(registro)

    print(
        f"\n✓ Expediente registrado con éxito. Código asignado: [{codigo}]"
    )


def consultar_expediente(
    codigos, dnis, remitentes, asuntos, fechas, estados
):
    """Busca y muestra la información detallada de un expediente específico."""
    print("\n---------------------------------------------")
    print("           CONSULTA DE EXPEDIENTE            ")
    print("---------------------------------------------")

    if not codigos:
        print("No hay expedientes registrados en el sistema.")
        return

    cod = input("Ingrese el código a buscar (ej. EXP-2026-001): ")
    pos = buscar_expediente_por_codigo(codigos, cod)

    if pos != -1:
        print("\n================ DETALLE ENCONTRADO ================")
        print(f" Código:     {codigos[pos]}")
        print(f" DNI:        {dnis[pos]}")
        print(f" Remitente:  {remitentes[pos]}")
        print(f" Asunto:     {asuntos[pos]}")
        print(f" Fecha:      {fechas[pos]}")
        print(f" Estado:     {estados[pos]}")
        print("====================================================")
    else:
        print(f"\n✗ No se encontró ningún expediente con el código '{cod}'.")


def listar_expedientes(
    codigos, dnis, remitentes, asuntos, fechas, estados
):
    """Ordena los arreglos por código y muestra un reporte tabulado."""
    print("\n--------------------------------------------------------------------------------")
    print("                       LISTADO DE EXPEDIENTES REGISTRADOS                       ")
    print("--------------------------------------------------------------------------------")

    if not codigos:
        print("No existen expedientes registrados para mostrar.")
        return

    # Se aplica el ordenamiento antes de la presentación
    ordenar_expedientes_burbuja(
        codigos, dnis, remitentes, asuntos, fechas, estados
    )

    print(
        f"{'CÓDIGO':<14} | {'DNI':<9} | {'REMITENTE':<22} | {'FECHA':<16} | {'ESTADO'}"
    )
    print("-" * 80)
    for i in range(len(codigos)):
        # Recorte de cadenas para mantener el formato tabulado en consola
        remitente_corto = (
            remitentes[i][:19] + "..."
            if len(remitentes[i]) > 22
            else remitentes[i]
        )
        print(
            f"{codigos[i]:<14} | {dnis[i]:<9} | {remitente_corto:<22} | {fechas[i]:<16} | {estados[i]}"
        )
    print("-" * 80)


# ===================================================================
# PROGRAMA PRINCIPAL Y MENÚ INTERACTIVO
# ===================================================================
def main():
    # Cargar datos persistidos desde el archivo plano al iniciar el programa
    codigos, dnis, remitentes, asuntos, fechas, estados = (
        cargar_expedientes_archivo()
    )

    while True:
        print("\n=============================================")
        print("    MESA DE PARTES DIGITAL - MUNICIPALIDAD   ")
        print("=============================================")
        print(" 1. Registrar nuevo expediente")
        print(" 2. Buscar expediente por código")
        print(" 3. Listar expedientes (Ordenados por Código)")
        print(" 4. Salir")
        print("=============================================")

        opcion = input("Seleccione una opción (1-4): ").strip()

        if opcion == "1":
            registrar_nuevo_expediente(
                codigos, dnis, remitentes, asuntos, fechas, estados
            )
        elif opcion == "2":
            consultar_expediente(
                codigos, dnis, remitentes, asuntos, fechas, estados
            )
        elif opcion == "3":
            listar_expedientes(
                codigos, dnis, remitentes, asuntos, fechas, estados
            )
        elif opcion == "4":
            print(
                "\nGuardando sesión y cerrando el sistema... ¡Hasta luego!"
            )
            break
        else:
            print(
                "\n[ERROR] Opción no válida. Por favor, ingrese un número del 1 al 4."
            )


if __name__ == "__main__":
    main()
