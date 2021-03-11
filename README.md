# TEST Movies on CSV

Este es un pequeño proyecto para una prueba técnica.


## Getting Started

Backend Python / DRF:

Armar un proyecto en github con una API en python+django que resuelva la siguiente funcionalidad.

Se desea poder subir un archivo CSV de base de datos de películas (adjunto).

Una vez subido, debe proveerse un endpoint para consultar:

- costo total (budget) de todas las películas cuyo país es USA

- costo promedio por película de todas las películas cuyo país es USA



## Preconditions and assumptions

- Se asume que el csv siempre tiene el mismos campos y separadores.

- Trabajo con el csv en memoria suponiendo que no serán más grande en tamaño (al del ejemplo facilitado).

- Sólo cargo los campos necesarios para el csv por razones de tiempo de entrega.

- Asumo que budget no viene con comas ni puntos (p.e. $ 10,333.03).

- Separo budget en currency y budget (p.e., $ y 10333.03)

- Si no se pueden cargar todos los datos del csv, no carga ninguno.


## Installing

**1)** clonar repositorio

**2)** virtualenv -p python3 .venv && source .venv/bin/activate

**3)** pip install -r requirements.txt

**4)** python manage.py makemigrations

**5)** python manage.py migrate

**6)** python manage.py createsuperuser

**7)** python manage.py runserver



## User Endpoints

Method | Endpoint | Functionality
--- | --- | ---
POST | `/api/movie/load` | Cargar el cvs file
GET | `/api/movie/total-usa` | Costo total (budget) de todas las películas cuyo país es USA
GET | `/api/movie/average-usa` | Costo promedio de todas las películas cuyo país es USA


## Usage and examples

Once you create your superuser, open browser on http://localhost:8000/admin/

- curl -H "Content-Type: application/json" http://localhost:8000/api/movie/total-usa
- curl -H "Content-Type: application/json" http://localhost:8000/api/movie/average-usa


## Built With

* [Python - 3.8.2]
* [Django - 3.0]
* [DRF  - 3.11.1]


## Author

* **Gerardo Velazquez (GV)** - *Software Engineer* -

This project is also for personal research.
