from flask import Flask, jsonify, request

app = Flask(__name__)

from carreras import carreras

@app.route('/carreras')
def ping():
    return jsonify(carreras)

@app.route('/carreras/<string:codigo>')
def getCarrera(codigo):
    encontrados = [carrera for carrera in carreras if str(carrera['Código']) == codigo]
    if(len(encontrados) > 0):
        return jsonify({"Carreras": encontrados})
    else:
        return("No existe una carrera con ese código")

@app.route('/nombre')
def getNombre():
    args = request.args.getlist('nombre')
    listaEncontrados = []
    for nombre in args:
        for carrera in carreras:
            if(carrera['Nombre'] == nombre):
                listaEncontrados.append(carrera)
    if (len(listaEncontrados) > 0):
        return jsonify(listaEncontrados)
    else:
        return jsonify({"No se encontraron los siguientes datos": args})
@app.route('/okey', methods=['POST'])
def pong():
    lista = []
    Nem = request.json['Nem']
    Ranking = request.json['Ranking']
    Lenguaje = request.json['Lenguaje']
    Matemática = request.json['Matemática']
    Ciencias = request.json['Ciencias']
    Historia = request.json['Historia']
    for i in carreras:
        mayorCienciaHistoria = 0
        if(Ciencias >= Historia):
            mayorCienciaHistoria = Ciencias
        else:
            mayorCienciaHistoria = Historia
        puntaje = Nem*i['NEM'] + Ranking*i['Ranking'] + Lenguaje*i['Lenguaje'] + Matemática*i['Matemática'] + mayorCienciaHistoria*i['Ciencias']
        posicion = lugar(puntaje, i['Vacantes'], i['Primero'], i['Último'])
        datos = {"Código de Carrera": i['Código'], "Nombre de la Carrera": i['Nombre'], "Puntaje de Postulación": puntaje, "Lugar Tentativo": posicion}
        lista.append(datos)
    ordenado = sorted(lista, key = lambda i: i['Lugar Tentativo'])
    top10 = ordenado[:10]
    return jsonify(top10)

def lugar(puntaje,vacantes,primero,ultimo):
    if (puntaje >= primero):
        return 1
    else:
        pos = 1
        distancia = (primero+ultimo) / vacantes
        actual = primero
        while(actual > puntaje):
            pos = pos+1
            actual = actual - distancia
        return pos
if __name__ == '__main__':
    app.run(debug=True, port=4000)