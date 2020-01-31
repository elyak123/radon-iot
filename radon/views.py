def lectura(event, context):
    # Tenemos que guardar en RDS (Postgres).
    # Tenemos que regresar un OK por cualquier cuestión.
    # Aqui hacer la separación.
    return "Hola desde Lectura"

def decode_float_little_endian(hex_val):
    return struct.unpack("<f", bytes.fromhex(hex_val))[0]

def decode_int_little_endian(hex_val):
    return struct.unpack("<i", bytes.fromhex(hex_val+'0000'))[0]
