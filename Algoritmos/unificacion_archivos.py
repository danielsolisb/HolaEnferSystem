import os
from tkinter import filedialog, Tk

def seleccionar_archivos_txt():
    root = Tk()
    root.withdraw()
    return filedialog.askopenfilenames(
        title="Selecciona los archivos .txt a combinar",
        filetypes=[("Text files", "*.txt")]
    )

def seleccionar_archivo_salida():
    root = Tk()
    root.withdraw()
    return filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt")],
        title="Selecciona el archivo final"
    )

def combinar_txt_archivos(lista_archivos, archivo_destino):
    with open(archivo_destino, "w", encoding="utf-8") as final:
        for ruta in lista_archivos:
            nombre_archivo = os.path.basename(ruta)
            try:
                with open(ruta, "r", encoding="utf-8") as f:
                    contenido = f.read()
                final.write(f'"{nombre_archivo}"\n')
                final.write(f"{contenido}\n\n")
                print(f"[✔] Añadido: {nombre_archivo}")
            except Exception as e:
                print(f"[✖] Error leyendo {nombre_archivo}: {e}")

if __name__ == "__main__":
    archivos = seleccionar_archivos_txt()

    if archivos:
        archivo_salida = seleccionar_archivo_salida()
        if archivo_salida:
            combinar_txt_archivos(archivos, archivo_salida)
            print(f"\n✅ Archivos combinados en: {archivo_salida}")
        else:
            print("❌ Selección del archivo de salida cancelada.")
    else:
        print("❌ No se seleccionaron archivos.")
