def hex_flip_endian(endian_hex: str) -> str:
    flipped_endian_hex = bytearray.fromhex(endian_hex)[::-1]
    return ''.join(format(x, '02x') for x in flipped_endian_hex)
