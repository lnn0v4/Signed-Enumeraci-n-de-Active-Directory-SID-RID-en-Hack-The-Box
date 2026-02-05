# Signed-Enumeraci-n-de-Active-Directory-SID-RID-en-Hack-The-Box
📌 Descripción

Este script en Python3 fue desarrollado como parte de la máquina Signed de Hack The Box. Su objetivo es enumerar objetos de Active Directory a través de MSSQL, obteniendo el SID, el RID y determinando si cada objeto corresponde a un User, Group o Computer.
El script se apoya en nxc (NetExec) para consultar el SID asociado a un nombre de cuenta y luego realiza el parseo manual del SID, sin utilizar librerías externas, con fines educativos.
⚙️ ¿Qué hace el script?

*Ejecuta consultas MSSQL autenticadas usando nxc
*Extrae el SID en formato hexadecimal
*Convierte el SID hexadecimal a formato legible (S-1-5-21-...)
*Obtiene el RID (Relative Identifier)
*Clasifica el objeto como:
-USER
-GROUP
-COMPUTER
*Muestra los resultados en una tabla clara por consola

🧠 Lógica de clasificación

La detección del tipo de objeto se realiza de forma sencilla y efectiva:
-Si el nombre termina en $ → COMPUTER
-Si el RID es menor a 1000 → GROUP
-En cualquier otro caso → USER

▶️ Ejecución

python3 signed_sid_enum.py


Salida de ejemplo:

NAME                                TYPE       SID                                                          RID
------------------------------------------------------------------------------------------------------------------------
SIGNED\Domain Admins                GROUP      S-1-5-21-4088429403-1159899800-2753317549-512                512
SIGNED\DC01$                        COMPUTER   S-1-5-21-4088429403-1159899800-2753317549-1000               1000
SIGNED\john.doe                     USER       S-1-5-21-4088429403-1159899800-27533175




