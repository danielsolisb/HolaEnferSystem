import os
from tkinter import filedialog, Tk

def seleccionar_directorio(titulo="Selecciona un directorio"):
    root = Tk()
    root.withdraw()  # Oculta la ventana principal
    carpeta = filedialog.askdirectory(title=titulo)
    return carpeta

def convertir_py_a_txt(origen, destino):
    for carpeta_raiz, _, archivos in os.walk(origen):
        for archivo in archivos:
            if archivo.endswith(".py"):
                ruta_completa = os.path.join(carpeta_raiz, archivo)
                try:
                    with open(ruta_completa, "r", encoding="utf-8") as f_py:
                        contenido = f_py.read()

                    # Generar nombre con guiones bajos
                    ruta_relativa = os.path.relpath(ruta_completa, origen)
                    nombre_txt = ruta_relativa.replace(os.sep, "_").replace(".py", ".txt")
                    ruta_salida = os.path.join(destino, nombre_txt)

                    with open(ruta_salida, "w", encoding="utf-8") as f_txt:
                        f_txt.write(contenido)

                    print(f"[✔] Archivo convertido: {ruta_salida}")
                except Exception as e:
                    print(f"[✖] Error con {ruta_completa}: {e}")

if __name__ == "__main__":
    print("Selecciona la carpeta de origen donde están los archivos .py")
    carpeta_origen = seleccionar_directorio("Selecciona la carpeta origen")
    
    print("Selecciona la carpeta de destino donde se guardarán los .txt")
    carpeta_destino = seleccionar_directorio("Selecciona la carpeta destino")

    if carpeta_origen and carpeta_destino:
        convertir_py_a_txt(carpeta_origen, carpeta_destino)
    else:
        print("Debes seleccionar ambas carpetas.")
