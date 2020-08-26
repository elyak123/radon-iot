# tenemos que:
# por ejemplo, si un rango es definido por los porcentajes 10 - 20 (rango 2 y 3)
# y por el sensor sabemos que ese rango va de 3210 a 2170
# tenemos que sacar el absoluto de la distancia, aunque sea positivo o negativo.
# después de eso, tuviéramos que en porcentaje saber la distancia absoluta entre dos puntos
# del rango donde quedó inmerso, por lo que ahora sabríamos la proporción que le corresponde
# en porcentaje.
# Consideramos dividir en dos el rango donde existe ruptura en la secuencia (en caso de existir)
# Para que el algoritmo nunca pierda el sentido.


def convertir_lectura(self, lectura, tipo):

    rangos = [
        [
            {
                'lectura': 1010,
                'valor': 5
            },
            {
                'lectura': 2050,
                'valor': 10
            },
        ],
        [],
        []
    ]

    topes = rangos[tipo-1]

    for i in range(0, len(topes)-1):
        tope_1 = topes[i]
        tope_2 = topes[i+1]
        if lectura >= tope_1.lectura and lectura < tope_2.lectura:
            distancia = abs(tope_2.lectura - tope_1.lectura)
            distancia_lectura = abs(lectura - tope_1.lectura)
            porcentaje = distancia_lectura / distancia
            return abs(tope_2.valor - tope_1.valor) * porcentaje + tope_1.valor
