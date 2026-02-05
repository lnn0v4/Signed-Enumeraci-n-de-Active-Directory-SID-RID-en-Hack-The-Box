#!/usr/bin/env python3
import subprocess

TARGET = "<TARGET-IP>"
USER = "<USER>"
PASSWORD = "<PASSWORD>"
USERS_FILE = "<FILE>"


def ejecutar_nxc(nombre):
    cmd = (
        f"nxc mssql {TARGET} "
        f"-u '{USER}' -p '{PASSWORD}' "
        f"-q \"select SUSER_SID('{nombre}');\""
    )

    salida = subprocess.getoutput(cmd)

    if "b'" not in salida:
        return None

    try:
        return salida.split("b'")[1].split("'")[0]
    except IndexError:
        return None


def convertir_sid(hex_sid):
    data = bytes.fromhex(hex_sid)

    revision = data[0]
    subauth_count = data[1]
    authority = int.from_bytes(data[2:8], "big")

    subauths = []
    offset = 8

    for _ in range(subauth_count):
        sub = int.from_bytes(data[offset:offset + 4], "little")
        subauths.append(sub)
        offset += 4

    sid = f"S-{revision}-{authority}"
    for s in subauths:
        sid += f"-{s}"

    rid = subauths[-1]
    return sid, rid


def detectar_tipo(nombre, rid):
    """
    Determina si es User, Group o Computer
    """
    if nombre.endswith("$"):
        return "COMPUTER"

    if rid < 1000:
        return "GROUP"

    return "USER"


def procesar_objeto(nombre):
    hex_sid = ejecutar_nxc(nombre)
    if not hex_sid:
        return None

    sid, rid = convertir_sid(hex_sid)
    tipo = detectar_tipo(nombre, rid)

    return sid, rid, tipo


def main():
    print(f"{'NAME':35} {'TYPE':10} {'SID':60} RID")
    print("-" * 120)

    with open(USERS_FILE) as f:
        for linea in f:
            nombre = linea.strip()
            if not nombre:
                continue

            resultado = procesar_objeto(nombre)
            if not resultado:
                continue

            sid, rid, tipo = resultado
            print(f"{nombre:35} {tipo:10} {sid:60} {rid}")


if __name__ == "__main__":
    main()

