def read_id(f):
    b0 = f.read(1)
    if not b0:
        raise EOFError
    first = b0[0]
    mask, length = 0x80, 1
    while length < 4 and not (first & mask):
        mask >>= 1; length += 1
    rest = f.read(length - 1)
    return int.from_bytes(b0 + rest, "big"), length

def read_size(f):
    b0 = f.read(1)
    if not b0:
        raise EOFError
    first = b0[0]
    mask, length = 0x80, 1
    while length < 8 and not (first & mask):
        mask >>= 1; length += 1
    value = first & (mask - 1)
    for _ in range(length - 1):
        b = f.read(1)
        if not b:
            raise EOFError
        value = (value << 8) | b[0]
    return value, length

def read_vint(f):
    b0 = f.read(1)
    if not b0:
        raise EOFError
    first = b0[0]
    mask, length = 0x80, 1
    while length < 8 and not (first & mask):
        mask >>= 1; length += 1
    value = first & (mask - 1)
    for _ in range(length - 1):
        b = f.read(1)
        if not b:
            raise EOFError
        value = (value << 8) | b[0]
    return value, length
