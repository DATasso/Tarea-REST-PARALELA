from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
import jwt
import datetime
from functools import wraps

app = Flask(__name__)
#acceso CORS
CORS(app)

app.config['SECRET_KEY'] = 'clavessupersecreta'

#lista de carreras (se recomienda implementación con base de datos)
from carreras import carreras
#lista de usuarios (se recomienda implementación con base de datos)
from usuarios import usuarios

#Funcion para permitir y obligar el acceso mediante token en el header "acceso-token"
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('acceso-token')
        if not token:
            return jsonify({'message' : 'No se encuentra el token'}), 403
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message' : 'Token invalido!'}), 403

        return f(*args, **kwargs)
    return decorated

#Ruta para el login, implementación sencilla con una lista de usuarios, es recomendable utilizar una base de datos para los usuarios.
#Al llenar los datos, se verifica la existencia de estos y se responde con el token, en cualquier otro caso, se responde con el error correspondiente.
@app.route('/login')
def login():
    auth = request.authorization

    if auth and auth.username and auth.password:
        datosUsuario = [usuario for usuario in usuarios if str(usuario['Usuario']) == auth.username]
        if(len(datosUsuario) == 1):
            if datosUsuario[0]['Contraseña'] == auth.password:
                token = jwt.encode({'user' : auth.username, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
                return jsonify({'token' : token.decode('UTF-8')})
            else:
                return make_response('Contraseña incorrecta', 401, {'WWW-Authenticate' : 'Basic realm="Contraseña incorrecta!"'})
        else:
            return make_response('Usuario no existe', 401, {'WWW-Authenticate' : 'Basic realm="Usuario no existe"'})
    
    return make_response('No se pudo verificar', 401, {'WWW-Authenticate' : 'Basic realm="Login requerido!"'})
    
#Ruta para obtener los datos de todas las carreras.
@app.route('/carreras')
@token_required
def ping():
    return jsonify(carreras)

#Ruta para obtener los datos de una carrera especifica a traves de su codigo
@app.route('/carreras/<string:codigo>')
@token_required
def getCarrera(codigo):
    encontrados = [carrera for carrera in carreras if str(carrera['Código']) == codigo]
    if(len(encontrados) > 0):
        return make_response(jsonify({"Carreras": encontrados}), 200)
    else:
        return("No existe una carrera con ese código")

#Ruta para obtener los datos de una o mas carreras a través de su/s nombre/s
@app.route('/busqueda')
@token_required
def getNombre():
    args = request.args.getlist('nombre')
    if(len(args)>0):
        listaEncontrados = []
        for nombre in args:
            for carrera in carreras:
                if(nombre in carrera['Nombre']):
                    listaEncontrados.append(carrera)
        if (len(listaEncontrados) > 0):
            return jsonify(listaEncontrados), 200
        else:
            return jsonify({"No se encontro ninguno de los siguientes datos": args}), 200
    else:
        return('No se recibieron datos en json con key = "nombre"')

#Ruta para ingresar datos del postulante y obtener las 10 mejores carreras con sus respectivos datos
@app.route('/mejores', methods=['POST'])
@token_required
def pong():
    lista = []
    Nem = request.json.get('Nem')
    Ranking = request.json.get('Ranking')
    Lenguaje = request.json.get('Lenguaje')
    Matemática = request.json.get('Matemática')
    Ciencias = request.json.get('Ciencias')
    Historia = request.json.get('Historia')
    if Nem and Ranking and Lenguaje and Matemática and (Ciencias or Historia):
        if isinstance(Nem, int) and isinstance(Ranking, int) and isinstance(Lenguaje, int) and isinstance(Matemática, int) and (isinstance(Ciencias, int) or isinstance(Historia, int)):
            for i in carreras:
                mayorCienciaHistoria = 0
                if Ciencias and Historia:
                    if(Ciencias >= Historia):
                        mayorCienciaHistoria = Ciencias
                    else:
                        mayorCienciaHistoria = Historia
                elif not Historia:
                    mayorCienciaHistoria = Ciencias
                elif not Ciencias:
                    mayorCienciaHistoria = Historia
                
                puntaje = Nem*i['NEM'] + Ranking*i['Ranking'] + Lenguaje*i['Lenguaje'] + Matemática*i['Matemática'] + mayorCienciaHistoria*i['Ciencias']
                posicion = lugar(puntaje, i['Vacantes'], i['Primero'], i['Último'])
                datos = {"Código de Carrera": i['Código'], "Nombre de la Carrera": i['Nombre'], "Puntaje de Postulación": puntaje, "Lugar Tentativo": posicion}
                lista.append(datos)
            ordenado = sorted(lista, key = lambda i: i['Lugar Tentativo'])
            top10 = ordenado[:10]
            return jsonify(top10), 200
        else:
            return('Error al recibir datos, verifique que los campos "Nem", "Ranking", "Lenguaje", "Matemática" y "Ciencias" o "Historia" sean NUMEROS ENTEROS')
    else:
        return('Error al recibir datos, verifique que se enviaran los campos "Nem", "Ranking", "Lenguaje", "Matemática" y "Ciencias" o "Historia"')

#Función para obtener posición en la carrera segun el puntaje del postulante, las vacantes y el primero y ultimo puntaje del año anterior de la carrera
def lugar(puntaje,vacantes,primero,ultimo):
    pos = 1
    if (puntaje >= primero):
        return pos
    else:
        distancia = (primero-ultimo)/vacantes
        actual = primero
        while(actual > puntaje):
            pos = pos+1
            actual = actual - distancia
        return pos
    
if __name__ == '__main__':
    app.run(debug=True, port=4000)
