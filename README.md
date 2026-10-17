

## Estructura

```
notebooks/fase1_entrenamiento.ipynb   Entrenamiento y comparativa de PatchCore y PaDiM (Colab)
src/inspeccionar.py                   Herramienta de inspección por línea de comandos
resultados/                           Métricas obtenidas en la comparativa de Golab
```

## Instalación

Requiere Python 3.10 o superior.

```
python -m venv .venv
.venv\Scripts\activate          # En Windows
source .venv/bin/activate       # En Linux o macOS
pip install -r requirements.txt
```

Los modelos entrenados no se incluyen en el repositorio por su tamaño. Hay que generarlos con
la sección "Guardar los modelos finales de PatchCore" del notebook y descomprimir `modelos.zip`
en la raíz del proyecto, de forma que quede:

```
modelos/patchcore_bottle.ckpt
modelos/patchcore_screw.ckpt
modelos/patchcore_metal_nut.ckpt
```

## Uso

```
python src/inspeccionar.py --entrada <imagen o carpeta> --categoria <bottle|screw|metal_nut>
```

| Opción | Descripción |
| --- | --- |
| `--entrada` | Imagen o carpeta de imágenes a inspeccionar |
| `--categoria` | Tipo de pieza: `bottle`, `screw` o `metal_nut` |

El comando se ejecuta desde la raíz del proyecto, porque los modelos se leen de la carpeta `modelos/`.
La inferencia se hace en CPU, por lo que no hace falta tener una GPU.

La herramienta muestra por pantalla el resultado de cada pieza (buena o defectuosa) con su puntuación, y guarda en
`salida/` una imagen por pieza con el mapa de calor superpuesto (azul = normal, rojo = anomalía). Cada imagen se nombra
con la carpeta de origen y el nombre del archivo, por ejemplo `broken_large_000_mapa.png`.

Anomalib crea además una carpeta `results/` con sus archivos internos de trabajo, que se puede borrar
sin problema. Nxi `salida/` ni `results/` se suben al repositorio.

## Licencias

El código se basa en [Anomalib](https://github.com/open-edge-platform/anomalib) (Apache 2.0).
El dataset [MVTec AD](https://www.mvtec.com/company/research/datasets/mvtec-ad) se distribuye
bajo licencia CC BY-NC-SA 4.0 y solo puede usarse con fines no comerciales.