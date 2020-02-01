import struct


def lectura(event, context):
    # Tenemos que guardar en RDS (Postgres).
    # Tenemos que regresar un OK por cualquier cuestión.
    # Aqui hacer la separación.
    angulo = decode_int_little_endian(event['Records']['Sns']['Message'][0:4])
    temperatura = decode_float_little_endian(event['Records']['Sns']['Message'][4:12])
    humedad = decode_float_little_endian(event['Records']['Sns']['Message'][4:12])
    return "Hola desde Lectura\n{}\n{}\nangulo:{}\ntemperatura:{}\nhumedad:{}".format(
        str(event), str(context), angulo, temperatura, humedad)


def decode_float_little_endian(hex_val):
    return struct.unpack("<f", bytes.fromhex(hex_val))[0]


def decode_int_little_endian(hex_val):
    return struct.unpack("<i", bytes.fromhex(hex_val+'0000'))[0]
