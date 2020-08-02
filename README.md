# Proyecto REST Computación Paralela y Distribuida
Proyecto SOAP para la asignatura computación paralela y distribuida en la UTEM, semestre 1 2020; docente: Sebastián Salazar.
 El proyecto consiste en desarrollar un servicio REST que entregue en función de los puntajes obtenidos por el estudiante, las 10 carreras en las que tiene mayores opciones de ingreso desde la que tiene mejor opción hasta la que tiene menor opción.
#### Autores
- Daniel Aguilera Tasso
- Nicolás Andrews Sandoval

## Dependencias y compilación
Se recomienda una versión de python mayor a 3.2, preferiblemente 3.8.2 . Y las librerías `flask` , `flask-cors` y `pyjwt`. Además se hace uso de los módulos `datetime` y `wraps` de `functools`

**En Ubuntu:**
```
pip3 install flask
pip3 install flask-cors
pip3 install PyJWT
```

#### Correr el programa:
El servicio rest debe usar el archivo `rest.py` desde la terminal.
`$ python3 rest.py`


##  Rutas del servicio:
**'/login' GET**<br>
Utilizar Basic Auth (Usuario y Contraseña) para autenticar y obtener token (JWT)

**'/carreras' GET**<br>
Retorna un JSON con todas las carreras y sus respectivos datos. Es necesario incluir la cabecera o header "acceso-token" con el token correspondiente.

**'/carreras/<string:codigo>' GET**<br>
Retorna un JSON con los datos de la carrera que corresponde al código ingresado. Funcionamiento mediante Path Param, EJ: `localhost:4000/carreras/21041`. Es necesario incluir la cabecera o header "acceso-token" con el token correspondiente.

**'/busqueda' GET**<br>
Retorna un listado de todas las carreras que contengan el nombre ingresado, en formato JSON. Funcionamiento mediante Query Param con un key:`nombre`,
EJ: `localhost:4000/busqueda?nombre="Ingeniería`. Esta función permite multiples búsquedas, es decir, multiples key `nombre`. Es necesario incluir la cabecera o header "acceso-token" con el token correspondiente.

**'/mejores' POST**<br>
Retorna un listado de las 10 primeras mejores carreras(ordenadas desde el mejor al peor lugar tentativo), en formato JSON. Funcionamiento mediante Body Request (JSON) que contenga un `Nem`,`Ranking`,`Lenguaje`,`Matemática`y (`Ciencias` o `Historia)`. Es necesario incluir la cabecera o header "acceso-token" con el token correspondiente.

Ej Body (JSON):
```
{
  "Nem": 600,
  "Ranking": 600,
  "Lenguaje": 600,
  "Matemática": 600,
  "Ciencias": 600,
  "Historia": 600,
}
```
