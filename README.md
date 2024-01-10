# Proyecto individual

![1704758694838](image/README/1704758694838.png "Steam")

## Índice

1. Presentación
2. Requerimientos
3. Uso
4. Adicional
5. Información de contacto

## Presentación

Se encuentran los archivos competentes sobre un sistema de recomendaciones para juegos de la plataforma STEAM, dentro de una parte de su catálogo junto con reviews de usuarios como también usuarios con su lista de juegos que les pertenecen

## Requerimientos

Al momento de querer implementar directamente con los recursos presentes, necesita:

1. pandas
2. numpy
3. ntlk
4. scikit-learn
5. matplotlib
6. pyarrow
7. seaborn

```bash
pip install pandas numpy nltk matplotlib pyarrow scikit-learn seaborn
```

Entender que estas dependencias funcionan con todos los archivos presentes.

## Uso

* Copiar el repositorio en su máquina local.

  ```
  git clone https://github.com/jaraycode/steam_games_mlops.git
  ```
* Activar un entorno virtual (virtualenv).

  ```
  python -m virtualenv venv
  ```
* Activar el entorno virtual.

  ```
  source venv/bin/activate
  ```
* Descargar los requerimientos existentes en el archivo requirement.txt.

  ```
  pip install -r requirement.txt
  ```
* Usar el siguiente comando para iniciar la API.

  ```
  uvicorn app:app --host 127.0.0.1 --port 8000
  ```
* Ingresar a "http://127.0.0.1:8000/docs" para poder visualizar todas las consultas disponibles.

## Adicional

Una vez realizado los pasos en el apartado anterior se podrán encontrar las siguientes consultas

* `/playTimeGenre`: a partir de un genero retorna el año de lanzamiento en que los jugadores más jugaron.
* `/userForGenre`: a partir de un genero retorna el usuario que más tiempo de juego tiene, listado por el tiempo que jugo por año.
* `/userRecommend`: a partir de un año retorna los juegos que se lanzaron ese año y que hayan sido más recomendados.
* `/userWorstDeveloper`: a partir de una año retorna el desarrollador de videojuegos que tuvieron peores recomendaciones.
* `/sentimentAnalysis`: buscas a tu empresa desarrolladora favorita y te genera cuantos comentarios negativos, neutros, positivos ha tenido según los datos disponibles.
