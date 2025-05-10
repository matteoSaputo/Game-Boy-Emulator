def load_rom(path):
    with open(path, "rb") as r:
        return r.read()