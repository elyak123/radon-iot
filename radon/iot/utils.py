"""
tenemos que:
por ejemplo, si un rango es definido por los porcentajes 10 - 20 (rango 2 y 3)
y por el sensor sabemos que ese rango va de 3210 a 2170
tenemos que sacar el absoluto de la distancia, aunque sea positivo o negativo.
después de eso, tuviéramos que en porcentaje saber la distancia absoluta entre dos puntos
del rango donde quedó inmerso, por lo que ahora sabríamos la proporción que le corresponde
en porcentaje.
Consideramos dividir en dos el rango donde existe ruptura en la secuencia (en caso de existir)
Para que el algoritmo nunca pierda el sentido.
"""


def convertir_lectura(lectura, tipo=1, modo=0):
    rangos = [
        [
            {
                'lectura': 2935,
                'valor': 0
            },
            {
                'lectura': 2780,
                'valor': 5
            },
            {
                'lectura': 2420,
                'valor': 10
            },
            {
                'lectura': 2115,
                'valor': 15
            },
            {
                'lectura': 1845,
                'valor': 20
            },
            {
                'lectura': 1625,
                'valor': 25
            },
            {
                'lectura': 1440,
                'valor': 30
            },
            {
                'lectura': 1320,
                'valor': 35
            },
            {
                'lectura': 1220,
                'valor': 40
            },
            {
                'lectura': 1120,
                'valor': 45
            },
            {
                'lectura': 1035,
                'valor': 50
            },
            {
                'lectura': 940,
                'valor': 55
            },
            {
                'lectura': 851,
                'valor': 60
            },
            {
                'lectura': 760,
                'valor': 65
            },
            {
                'lectura': 635,
                'valor': 70
            },
            {
                'lectura': 446,
                'valor': 75
            },
            {
                'lectura': 200,
                'valor': 80
            },
            {
                'lectura': 0,
                'valor': 82
            },
            {
                'lectura': 4095,
                'valor': 82
            },
            {
                'lectura': 3915,
                'valor': 85
            },
            {
                'lectura': 3610,
                'valor': 90
            },
            {
                'lectura': 3230,
                'valor': 95
            },
            {
                'lectura': 3134,
                'valor': 100
            },
        ],
        [
            {
                'lectura': 850,
                'valor': 0
            },
            {
                'lectura': 580,
                'valor': 5
            },
            {
                'lectura': 162,
                'valor': 10
            },
            {
                'lectura': 0,
                'valor': 15
            },
            {
                'lectura': 4095,
                'valor': 15
            },
            {
                'lectura': 3839,
                'valor': 20
            },
            {
                'lectura': 3513,
                'valor': 30
            },
            {
                'lectura': 3260,
                'valor': 40
            },
            {
                'lectura': 2970,
                'valor': 50
            },
            {
                'lectura': 2730,
                'valor': 60
            },
            {
                'lectura': 2410,
                'valor': 70
            },
            {
                'lectura': 2080,
                'valor': 80
            },
            {
                'lectura': 1830,
                'valor': 85
            },
            {
                'lectura': 1602,
                'valor': 90
            },
            {
                'lectura': 1274,
                'valor': 95
            },
            {
                'lectura': 1168,
                'valor': 100
            }
        ],
        []
    ]

    topes = rangos[tipo-1]
    if not modo:
        for i in range(0, len(topes)-1):
            tope_1 = topes[i]
            tope_2 = topes[i+1]
            resultado = None
            if not tope_1['lectura'] < tope_2['lectura']:
                if lectura < tope_1['lectura'] and lectura >= tope_2['lectura']:
                    print("aqui llegue")
                    distancia = abs(tope_2['lectura'] - tope_1['lectura'])
                    distancia_lectura = abs(lectura - tope_1['lectura'])
                    porcentaje = distancia_lectura / distancia
                    resultado = abs(tope_2['valor'] - tope_1['valor']) * porcentaje + tope_1['valor']
                    return round(resultado, 2)
    else:
        for i in range(0, len(topes)-1):
            tope_1 = topes[i]
            tope_2 = topes[i+1]
            resultado = None
            if not tope_1['valor'] > tope_2['valor']:
                if lectura > tope_1['valor'] and lectura <= tope_2['valor']:
                    distancia = abs(tope_2['valor'] - tope_1['valor'])
                    distancia_lectura = abs(lectura - tope_1['valor'])
                    porcentaje = distancia_lectura / distancia
                    resultado = - abs(tope_2['lectura'] - tope_1['lectura']) * porcentaje + tope_1['lectura']
                    return round(resultado, 2)
    return 0
