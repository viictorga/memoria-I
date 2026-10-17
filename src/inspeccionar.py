import argparse # para leer --entrada y --categoria
import logging # es para silenciar mensajes de lightnign, se hace pesado queremos ver solo resultados
import sys # para poder sacar errores
import time
import warnings
from pathlib import Path # para trabajar con rutas de archivos

import matplotlib

matplotlib.use("Agg")  # dibuja en archivos, sin abrir ventanas,  es mas comodo, tiene que ir antes de la liunea 17, porque cuando lo pones matplot ya ha decidod como dibujar
import matplotlib.pyplot as plt
from anomalib.data import PredictDataset
from anomalib.engine import Engine
from anomalib.models import Patchcore
from PIL import Image

warnings.filterwarnings("ignore")
logging.getLogger("lightning").setLevel(logging.ERROR)
logging.getLogger("lightning_fabric").setLevel(logging.ERROR) # sin estas lineas el terminal se llenaria de cosas muy tecnicas de la prediccion

#  leer y comprobar los argumentos
parser = argparse.ArgumentParser(description="Detecta defectos en piezas industriales") # esto es por si alguien pone --help, se genera automaticamente por argparse
parser.add_argument("--entrada", required=True, help="Imagen o carpeta de imágenes") # aqui indicamos las dos entradas posibles, required es la obligatoriedad, y help es la descripcion que saldria si llegan a ejecutar help
parser.add_argument("--categoria", required=True, choices=["bottle", "screw", "metal_nut"])

args = parser.parse_args() # esta linea lee tu terminal y lo guarda en args, args tiene dos valores que son .entrada (la ruta de la imagen/es a analizar) y la ,categoria que tiene 3 valores y asi podemos escoger modelo

entrada = Path(args.entrada)
modelo = Path("modelos") / f"patchcore_{args.categoria}.ckpt"

if not entrada.exists():
    sys.exit(f"Error: no existe la ruta '{entrada}'.")
archivos = [entrada] if entrada.is_file() else list(entrada.iterdir())
if not any(p.suffix.lower() in {".png", ".jpg", ".jpeg"} for p in archivos):
    sys.exit(f"Error: '{entrada}' no contiene ninguna imagen válida.")
if not modelo.exists():
    sys.exit(f"Error: no se encuentra el modelo '{modelo}'.")

# el modelo analiza las imágenes
print(f"Inspeccionando con {modelo.name}...\n")
inicio = time.time()
engine = Engine(accelerator="cpu", enable_progress_bar=False)
lotes = engine.predict(
    model=Patchcore(),
    dataset=PredictDataset(path=entrada, image_size=(256, 256)),
    ckpt_path=modelo,
)

# MAPAS DE CALOR Y SALIDAS
salida = Path("salida")
salida.mkdir(exist_ok=True)
total = defectuosas = 0

for lote in lotes: # si hay una sola imagen pues solo hay un lote pero podrian existir varios
    for ruta, puntuacion, etiqueta, mapa in zip(lote.image_path, lote.pred_score, lote.pred_label, lote.anomaly_map): #este recorre las imagenes de este lote, guarda los datos de cada imagen, ruta, score, prediccion y el mapa de calor
        ruta = Path(ruta) # la pasamos a path para mas adelante poder dividirla
        estado = "DEFECTUOSA" if bool(etiqueta) else "BUENA"# si etiqueta es true (la decision del modelo) pues es defectuosa, al contratio es buena
        total += 1 # sumamos uno al total de imagenes procesadas
        defectuosas += estado == "DEFECTUOSA" # sumamos uno a defectuosas, si y solo si el estado es exactamente "DEFECTUOSO"

        # imagen original con el mapa de calor encima (azul = normal, rojo = se detecta anomalia)
        plt.imshow(Image.open(ruta).convert("RGB").resize((256, 256))) # abrimos la foto, pasamos a colores, porque algunas imagenes estan en blanco y negro y la pone al tamaño del mapa de calor 256x256
        plt.imshow(mapa.squeeze().cpu().numpy(), cmap="jet", alpha=0.5, vmin=0, vmax=1)
        plt.title(f"{ruta.name}: {estado} ({float(puntuacion):.3f})")# el titulo es el nombre de ruta el estado y añadomos la puntuacion en float, :,3f muestra tres decimales de la puntuacion
        plt.axis("off") #quita los ejes para que se vea bien
        plt.savefig(salida / f"{ruta.parent.name}_{ruta.stem}_mapa.png") # aqui aprivechamos la linea 61 y podemos hacer el.parent (el nombre de la carpeta donde este) y .stem es el nombre del archivo sin la extension
        plt.close() #quedando asi un ejemplo: salida/broken_large_000_mapa.png

        print(f"  {ruta.name:<15} {estado:<11} {float(puntuacion):.3f}")# el <15 y <11 es para que en el output por terminal quede bien indetado, tambien ponemos la puntuacion con 3 decimales

segundos = time.time() - inicio
# resumen
print(f"\nPiezas: {total} | Defectuosas: {defectuosas} | {segundos / total:.2f} s por imagen")
print(f"Mapas de calor guardados en: {salida}") # sacamos pequeño resumen de tiempo tardado defectuosas y buenas e indicamos donde se ha guardado