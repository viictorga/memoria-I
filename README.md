## Estructura

```
notebooks/fase1_entrenamiento.ipynb   Entrenamiento y comparativa de PatchCore y PaDiM (Google Colab)
src/inspeccionar.py                   Herramienta de inspección por línea de comandos
resultados/                           Métricas obtenidas en la comparativa
```

## Instalación

Requiere Python 3.10 o superior.

```
python -m venv .venv
.venv\Scripts\activate          # En Windows
pip install -r requirements.txt
```

Los modelos entrenados no se incluyen en el repositorio por su tamaño. Hay que generarlos con
la sección "Descargar los modelos" del notebook

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
sin problema. Ni `salida/` ni `results/` se suben al repositorio.

## Documentación

Enlaces a la documentación oficial de las librerías y funciones utilizadas en el notebook
(`notebooks/fase1_entrenamiento.ipynb`) y en la herramienta (`src/inspeccionar.py`).



### Anomalib

- `MVTecAD`. Link: https://anomalib.readthedocs.io/en/latest/markdown/guides/reference/data/datamodules/image/mvtecad.html
- `Patchcore`. Link: https://anomalib.readthedocs.io/en/latest/markdown/guides/reference/models/image/patchcore.html
- `Padim`. Link: https://anomalib.readthedocs.io/en/latest/markdown/guides/reference/models/image/padim.html
- `Engine`. Link: https://anomalib.readthedocs.io/en/latest/markdown/guides/reference/engine/index.html
- `PredictDataset`. Link: https://anomalib.readthedocs.io/en/latest/markdown/get_started/anomalib.html

### PyTorch y Lightning

- `torch.__version__, torch.cuda.is_available()`. Link: https://docs.pytorch.org/docs/stable/cuda.html
- `torch.cuda.empty_cache()`. Link: https://github.com/pytorch/pytorch/blob/v2.14.0/torch/cuda/memory.py
- `Tensor.squeeze(), Tensor.cpu(), Tensor.numpy()`. Link: https://docs.pytorch.org/docs/stable/tensors.html
- `trainer.save_checkpoint()`. Link: https://lightning.ai/docs/pytorch/stable/common/checkpointing_intermediate.html

### Matplotlib

- `matplotlib.use("Agg")`. Link: https://matplotlib.org/stable/api/matplotlib_configuration_api.html y https://matplotlib.org/stable/users/explain/figure/backends.html
- `plt.figure()`. Link: https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.figure.html
- `plt.imshow()`. Link: https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.imshow.html
- `plt.title()`. Link: https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.title.html
- `plt.axis()`. Link: https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.axis.html
- `plt.show()`. Link: https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.show.html
- `plt.savefig()`. Link: https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.savefig.html
- `plt.close()`. Link: https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.close.html
- Escala de colores `jet`. Link: https://matplotlib.org/stable/users/explain/colors/colormaps.html

### Pillow

- `Image.open()`. Link: https://pillow.readthedocs.io/en/stable/reference/Image.html
- `Image.convert(), Image.resize()`. Link: https://pillow.readthedocs.io/en/stable/reference/Image.html


### pandas

- `pd.read_csv()`. Link: https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html
- `pd.DataFrame()`. Link: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html
- `DataFrame.to_csv()`. Link: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_csv.html
- `DataFrame.to_dict()`. Link: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_dict.html
- `DataFrame.drop()`. Link: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.drop.html
- `DataFrame.groupby()`. Link: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.groupby.html

### Biblioteca estándar de Python

- `argparse` (`ArgumentParser`, `add_argument`, `parse_args`). Link: https://docs.python.org/3/library/argparse.html
- `logging.getLogger()` y `setLevel()`. Link: https://docs.python.org/3/library/logging.html
- `warnings.filterwarnings()`. Link: https://docs.python.org/3/library/warnings.html
- `sys.exit()`. Link: https://docs.python.org/3/library/sys.html
- `gc.collect()`. Link: https://docs.python.org/3/library/gc.html
- `pathlib.Path`. Link: https://docs.python.org/3/library/pathlib.html

### Google Colab y comandos de terminal

- Comandos con `!`. Link: https://ipython.readthedocs.io/en/stable/interactive/reference.html
- `zip -qr`. Link: https://linux.die.net/man/1/zip
- Entorno virtual (`python -m venv`). Link: https://docs.python.org/3/library/venv.html

## Licencias

El código se basa en [Anomalib](https://github.com/open-edge-platform/anomalib) (Apache 2.0).
El dataset [MVTec AD](https://www.mvtec.com/company/research/datasets/mvtec-ad) se distribuye
bajo licencia CC BY-NC-SA 4.0 y solo puede usarse con fines no comerciales.