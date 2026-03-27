from scripts.clientesDjango import ClientesDjango

def run(*args):

    d = {
        "id": 1,
        "nombre": "Cliente prueba Django",
        "direccion": "Calle prueba",
        "telefono": "666666666",
        "tipo_cliente": "normal",
        "barrio": "Centro",
        "geom": "POINT(725000 4370000)"
    }

    c = ClientesDjango()

    print("INSERT")
    print(c.insert(d))

    print("UPDATE")
    print(c.update(d))

    print("SELECT TUPLES")
    print(c.selectAsTuples(d))

    print("SELECT DICTS")
    print(c.selectAsDicts(d))

    print("DELETE")
    print(c.delete(d))