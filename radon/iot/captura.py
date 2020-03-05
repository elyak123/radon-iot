import struct


def lectura(message):
    # Tenemos que guardar en RDS (Postgres).
    # Tenemos que regresar un OK por cualquier cuestión.
    # Aqui hacer la separación.
    angulo = decode_int_little_endian(message[0:4])
    temperatura = decode_float_little_endian(message[4:12])
    humedad = decode_float_little_endian(message[4:12])
    return angulo, temperatura, humedad


def decode_float_little_endian(hex_val):
    return struct.unpack("<f", bytes.fromhex(hex_val))[0]


def decode_int_little_endian(hex_val):
    return struct.unpack("<i", bytes.fromhex(hex_val+'0000'))[0]
