from radon.iot import utils


def test_convertir_lectura_tipo_1_normal():
    resultado = utils.convertir_lectura(298.4)
    assert resultado == 78


def test_convertir_lectura_tipo_1_fuera_de_rango():
    resultado = utils.convertir_lectura(3000)
    assert resultado == 0


def test_convertir_lectura_tipo_2_normal():
    resultado = utils.convertir_lectura(1891.25, tipo=2)
    assert resultado == 83.78


def test_convertir_lectura_tipo_2_fuera_de_rango():
    resultado = utils.convertir_lectura(1000, tipo=2)
    assert resultado == 0


def test_convertir_lectura_inversa_tipo_1_normal():
    resultado = utils.convertir_lectura(78, modo=1)
    assert resultado == 298.4


def test_convertir_lectura_inversa_tipo_2_normal():
    resultado = utils.convertir_lectura(83.775, tipo=2, modo=1)
    assert resultado == 1891.25
