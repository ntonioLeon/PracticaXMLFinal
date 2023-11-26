import datetime


def validar_dni():
    """
    funcion que pide un input, valida la longitud, y si es un dni
    """
    cont = 0
    while cont < 3:
        print("║ Introduzca un dni valido,      ║")
        dni = input("║ Recuerde 00000000X: ")
        if not dni.isspace():
            dni = dni.strip()  # El trim de python
            if len(dni) == 9:
                if dni[0:8].isnumeric():  # Es cerrado por la izquierda abierto por la derecha
                    if dni[8].isalpha():  # Solo coge el noveno caracter
                        print("║ DNI introducido con exito      ║")
                        return dni
                    else:
                        cont += 1
                        print("║ Recuerde el formato: 00000000X ║")
                        print("║ Fallo = ", cont, "                   ║")
                else:
                    cont += 1
                    print("║ Recuerde el formato: 00000000X ║")
                    print("║ Fallo = ", cont, "                   ║")
            else:
                cont += 1
                print("║ Recuerde el formato: 00000000X ║")
                print("║ Fallo = ", cont, "                   ║")
        else:
            cont += 1
            print("║ No introduzca cadenas vacias   ║")
            print("║ Fallo = ", cont, "                   ║")
    if cont == 3:
        print("║ Ha alcanzado el máximo de      ║")
        print("║ intentos. Saliendo del proceso.║")
        print("╚════════════════════════════════╝")
    return None


def validar_fecha(fecha_ini=None):
    """
    funcion que se asegura de que la fecha introducida es correcta.
    @:param la fecha si no se mete nada es none, si se mete una entonces la fecha introducida debera ser mayor a la que entra por parametro
    """
    cont = 0
    anno = ""
    mes = ""
    dia = ""
    check = False
    fin = False
    while not fin:
        if fecha_ini is None:
            print("║ La fecha constará de anno,     ║")
            print("║ mes y dia.                     ║")#Mensaje diferente en base al parametro.

        else:
            print("║ La fecha constará de anno,     ║")
            print("║ mes y dia. Recuerde que debe   ║")
            print("║ ser posterior a "+str(fecha_ini)+"     ║")

        while not check:
            print("║ Introduzca el anno, este debe  ║")
            print("║ estar entre el anno 2000 - 2050║")
            anno = input("║ ")  # Parte de la funcion que se asegura de que el anno es correcta basicamente que es numerico y esta dentro de los limites
            if not anno.isspace():
                anno = anno.strip()
                if anno.isnumeric():
                    if int(anno) >= 2000 and int(anno) <= 2050:
                        print("║ Anno introducido con exito     ║")
                        check = True
                    else:
                        cont += 1
                        print("║ La fecha debe estar contenida  ║")
                        print("║ estar entre el anno 2000 - 2050║")
                        print("║ Fallo = ", cont, "                   ║")
                else:
                    cont += 1
                    print("║ El anno debe ser numerico.     ║")
                    print("║ Fallo = ", cont, "                   ║")
            else:
                cont += 1
                print("║ El anno debe ser numerico.     ║")
                print("║ El anno no puede ser una cadena║")
                print("║ vacia. Fallos = ", cont, "              ║")
            if cont == 3:
                fin = True
                check = True
        if cont < 3:
            check = False
            while not check:
                mes = input("║ Introduzca el mes: ")  # Parte de la funcion que se asegura de que el mes es correcta
                if not (mes.isspace()):
                    mes = mes.strip()
                    if mes.isnumeric():
                        if int(mes) >= 1 and int(mes) <= 12:
                            print("║ Mes introducido con exito      ║")
                            check = True
                        else:
                            cont += 1
                            print("║ El mes debe estar conprendido  ║")
                            print("║ entre 1 y 12. Fallo = ", cont, "        ║")
                    else:
                        cont += 1
                        print("║ El anno debe ser numerico.     ║")
                        print("║ Fallo = ", cont, "                   ║")
                else:
                    cont += 1
                    print("║ No introduzca cadenas vacias   ║")
                    print("║ Fallo = ", cont, "                   ║")
                if cont == 3:
                    fin = True
                    check = True
        if cont < 3:
            check = False
            while not check:
                if int(mes) == 1 or int(mes) == 3 or int(mes) == 5 or int(mes) == 7 or int(mes) == 8 or int(
                        mes) == 10 or int(mes) == 12:
                    dia = input("║ Introduzca un dia entre 1 y 31 ║\n║ ")  # Parte de la funcion que se asegura de que el dia es correcta
                    if not (dia.isspace()):
                        dia = dia.strip()
                        if dia.isnumeric():
                            if int(dia) >= 1 and int(dia) <= 31:
                                print("║ Dia introducido con exito      ║")
                                print("╠════════════════════════════════╣")
                                check = True
                            else:
                                cont += 1
                                print("║ El dia debe estar comprendido  ║")
                                print("║ entre 1 y 31. Fallos = ", cont, "       ║")
                        else:
                            cont += 1
                            print("║ El dia debe ser numerico       ║")
                            print("║ Fallo = ", cont, "                   ║")
                    else:
                        cont += 1
                        print("║ No introduzca cadenas vacias   ║")
                        print("║ Fallo = ", cont, "                   ║")
                elif int(mes) == 4 or int(mes) == 6 or int(mes) == 9 or int(mes) == 11:
                    dia = input("║ Introduzca un dia entre 1 y 30 ║\n║ ")
                    if not (dia.isspace()):
                        dia = dia.strip()
                        if dia.isnumeric():
                            if int(dia) >= 1 and int(dia) <= 30:
                                print("║ Dia introducido con exito      ║")
                                print("╠════════════════════════════════╣")
                                check = True
                            else:
                                cont += 1
                                print("║ El dia debe estar comprendido  ║")
                                print("║ entre 1 y 30. Fallos = ", cont, "       ║")
                        else:
                            cont += 1
                            print("║ El dia debe ser numerico       ║")
                            print("║ Fallo = ", cont, "                   ║")
                    else:
                        cont += 1
                        print("║ No introduzca cadenas vacias   ║")
                        print("║ Fallo = ", cont, "                   ║")
                elif int(mes) == 2:
                    dia = input("║ Introduzca un dia entre 1 y 28 ║\n║ ")
                    if not (dia.isspace()):
                        dia = dia.strip()
                        if dia.isnumeric():
                            if int(dia) >= 1 and int(dia) <= 28:
                                print("║ Dia introducido con exito      ║")
                                print("╠════════════════════════════════╣")
                                check = True
                            else:
                                cont += 1
                                print("║ El dia debe estar comprendido  ║")
                                print("║ entre 1 y 28. Fallos = ", cont, "       ║")
                        else:
                            cont += 1
                            print("║ El dia debe ser numerico       ║")
                            print("║ Fallo = ", cont, "                   ║")
                    else:
                        cont += 1
                        print("║ No introduzca cadenas vacias   ║")
                        print("║ Fallo = ", cont, "                   ║")
                if cont == 3:
                    fin = True
                    check = True
            if cont < 3:
                if fecha_ini is None:  # Aqui si no hay parametro retornamos la fehca sin mas
                    print("║ Fecha introducida con exito    ║") #WTF?????
                    return datetime.date(int(anno), int(mes), int(dia))
                else:  # Si la fecha ha de ser comparada se compara y se comprueba que es mayor que la introducida por parametro.
                    date = datetime.date(int(anno), int(mes), int(dia))
                    if fecha_ini < date:
                        fin = True
                        return date
                    else:
                        cont += 1
                        print("║ Recuerde, la fecha no puede    ║")
                        print("║ ser anterior a " + str(fecha_ini) + "    ║")
                        print("║ Fallo = ", cont, "                   ║")
            else:
                print("║ Ha alcanzado el máximo de      ║")
                print("║ intentos. Saliendo del proceso.║")
                print("╚════════════════════════════════╝")
                return None


def validar_kilometraje(km_ini=None):
    """
    funcion que se asegura de que el kilometraje es correcta.
    @:param el kilometraje si no se mete nada es none, si se mete una entonces el kilometraje introducida debera ser mayor a la que entra por parametro
    """
    cont = 0
    while cont < 3:
        if km_ini is None:  # Nos aseguramos de que el campo no esta vacio, es numerico.

            print("║ Introduzca un kilometraje      ║")
            print("║ valido, este debe ser un numero║")

            km = input("║ ")
        else:
            print("║ Introduzca un kilometraje      ║")
            print("║ valido, mayor que "+ km_ini+" "*(13-len(str(km_ini)))+"║")
            km = input("║ ")
        if len(km.strip()) > 0:
            km = km.strip()
            if km.isdigit():
                if km_ini is None:  # Si no hay parametro nada
                    print("║ Kilometraje introducido        ║")
                    return km
                else:  # Si lo hay comprobamos que es mayor al parametetro
                    if int(km) > int(km_ini):
                        print("║ Kilometraje introducido        ║")
                        return km
                    else:
                        cont += 1
                        print("║ El kilometrake debe ser mayor  ║")
                        print("║ que "+km_ini+"                       ║")
                        print("║ Fallo = ", cont, "                   ║")
            else:
                cont += 1
                print("║ El dia kilometraje ser numerico║")
                print("║ Fallo = ", cont, "                   ║")
        else:
            cont += 1
            print("║ No introduzca cadenas vacias   ║")
            print("║ Fallo = ", cont, "                   ║")

    print("║ Ha alcanzado el máximo de      ║")
    print("║ intentos. Saliendo del proceso.║")
    print("╚════════════════════════════════╝")
    return None


def id_existe_vehiculo(root, identificacion):
    """
    funcion que se asegura que el id existe entre los alquileres
    """
    vehiculos = root.find("Vehiculos")
    if vehiculos is not None:
        vehiculo = vehiculos.findall("Vehiculo")
        if vehiculo is not None:
            for vehi in vehiculo:
                for attr in vehi.attrib:
                    attr_name = attr
                    attr_value = vehi.attrib[attr_name]
                    if attr_value == identificacion:
                        return True
    return False


def id_existe_alquiler(root, identificacion):
    """
    funcion que se asegura que el id existe entre los vehiculos
    """
    alquileres = root.find("Alquileres")
    if alquileres is not None:
        alquiler = alquileres.findall("Alquiler")
        if alquiler is not None:
            for alq in alquiler:
                for attr in alq.attrib:
                    attr_name = attr
                    attr_value = alq.attrib[attr_name]
                    if attr_value == identificacion:
                        return True
    return False


def validar_id(root, tipo):
    """
    Funcion que se asegura de que el id es correcto por medio de ver si no esta vacio, es numerico y existe en el sistema.
    Esta funcion no se usa para crear un id (son autoincrementales), solo para buscarlos.
    """
    cont = 0
    while cont < 3:
        identification = input("Introduzca un id valido, este debe ser un numero ")
        if len(identification.strip()) > 0:
            identification = identification.strip()
            if identification.isnumeric():
                if tipo == "1":
                    if id_existe_vehiculo(root, identification):
                        return identification
                    else:
                        cont += 1
                        print("El id no se corresponde con el de ningun vehiculo existente. Fallos = ", cont)
                else:
                    if id_existe_alquiler(root, identification):
                        return identification
                    else:
                        cont += 1
                        print("El id no se corresponde con el de ningun vehiculo existente. Fallos = ", cont)
            else:
                cont += 1
                print("El id debe ser un numero. Fallos = ", cont)
        else:
            cont += 1
            print("El id no puede tratarse de una cadena vacia o solo de espacios. Fallos = ", cont)
    print("La obtencion del id se suspendio debido a que se fallaron demasiadas veces seguidas.")
    return None


def matricula_esite(root, mat):
    """
    Funcion que comprueba que una matricula existe
    :param root: que se recorre
    :param mat: que se comprueba
    :return: True si exsite False si no
    """
    vehiculos = root.find("Vehiculos")
    if vehiculos is None:
        return False
    vehiculo = vehiculos.findall("Vehiculo")
    if vehiculo is None:
        return False
    for coche in vehiculo:
        if coche[0].text == mat:
            return True


def validar_y_comprobar_matricula(root):
    """
    Funcion que se asegura de que la matricula es valida y existe.
    :param root: que se recorrera. para comprobar su valided
    :return: La matricula validada o None si se falla
    """
    cont = 0
    while cont < 3:
        print("║ Introduzca la matricula del    ║")
        print("║ vehiculo que desea alquilar.   ║")
        mat = input("║ Recuerde AAA000: ")
        if not mat.isspace():
            mat = mat.strip()  # El trim de python
            if len(mat) == 6:
                if mat[:3].isalpha():  # Comprobamos que los valores son correcots
                    if mat[3:6].isnumeric():
                        if matricula_esite(root, mat):
                            print("║ Matricula introducida con exito║")
                            return mat
                        else:
                            cont += 1
                            print("║ La matricula introducida       ║")
                            print("║ no corresponde con ninguna     ║")
                            print("║ matricula existente Fallos = ", cont, "║")
                    else:
                        cont += 1
                        print("║ Los tres ultimos caracteres    ║")
                        print("║ deben ser numericos. Fallos = ", cont, "║")
                else:
                    cont += 1
                    print("║ Los tres ultimos caracteres    ║")
                    print("║ deben ser alfabeticos. Fallos = ", cont, "║")
            else:
                cont += 1
                print("║ La matricula debe tener 6      ║")
                print("║ caracteres. Fallos = ", cont, "         ║")
        else:
            cont += 1
            print("║ No introduzca cadenas vacias   ║")
            print("║ Fallos = ", cont, "                     ║")

    print("║ Ha alcanzado el máximo de      ║")
    print("║ intentos. Saliendo del proceso.║")
    print("╚════════════════════════════════╝")
    return None
