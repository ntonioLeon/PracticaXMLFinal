import datetime
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, Comment, ElementTree
import os
import Validador
import Utiles

file_path = ".\\datos.xml"


def prettify(elem, level=0):
    """
    funcion que reescribe el xml para que no este en una linea y tenga una estructura valida.
    @:param elem, el elemento que va a ser reestructurado.
    """
    indent = "    "  # 4 espacios por nivel
    i = "\n" + level * indent
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + indent
        for subelem in elem:
            prettify(subelem, level + 1)
        if not elem[-1].tail or not elem[-1].tail.strip():
            elem[-1].tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def esta_dispinible(root, id_vehiculo):
    """
    funcion que comprueba si un vehiculo esta disponible o no.
    :param root: que se recorrera
    :param id_vehiculo: El que se va a comprobar
    :return: trye si esta disponible false si no
    """
    vehiculos = root.find("Vehiculos")
    if vehiculos is not None:
        vehiculo = vehiculos.findall("Vehiculo")  # Nos situamos en vehiculo en el arbol.
        if vehiculo is not None:  # si hay vehiculos
            for vehi in vehiculo:
                for attr in vehi.attrib:  # Recorremos los atributos de los vehiculos.
                    attr_name = attr
                    attr_value = vehi.attrib[attr_name]
                    if attr_value == id_vehiculo:  # si coincide con el parametro es decir lo encontramos.
                        if vehi[4].text == "Disponible":
                            return True
                        else:
                            return False
    return False


def obtener_ultimo_id_alquiler(root):
    """
    funcion que recorre los alquileres para saber cual es el siguiente id valido.
    @:param root, que sera recorrido en busca de alquileres.
    @:return 1 si no hay alquileres, el ultimo id + 1 si hay alquileres.
    """
    alquileres = root.find('Alquileres')  # Encuentra los alquileres.
    ultimos_alquileres = alquileres.findall('Alquiler[@idAlquiler]')  # lista con los ids de los alquileres.

    if ultimos_alquileres:  # Si hay ids de alquiler
        ultimo_id = max(
            int(alquiler.get('idAlquiler')) for alquiler in ultimos_alquileres)  # Recorremos la lista de ids.
        return ultimo_id + 1  # devolvemos el ultimo + 1.
    else:
        return 1  # Si no hay ids el id sera 1.


def obtener_matricula_por_id(root, id_vehiculo):
    """
    Funcion que devuelve una matricula a partir de un id
    :param root: que se recorre
    :param id_vehiculo: que se busca
    :return: la matricula
    """
    vehiculos = root.find("Vehiculos")
    if vehiculos is None:
        return
    lista_vehiculo = vehiculos.findall("Vehiculo")
    if lista_vehiculo is not None:
        for vehiculo in lista_vehiculo:
            if vehiculo.attrib["idVehiculo"] == id_vehiculo:
                return vehiculo[0].text


def conseguir_precio_por_id(root, id_vehiculo):
    """
    funcion que a partir de un id devuelve el precio del vehiculo.
    @:param root que sera recorrida y id del vehiculo que queremos encontrar.
    @:return el precio del vehiculo, como los id se validan no puede no encontrar un precio.
    """
    vehiculos = root.find("Vehiculos")
    if vehiculos is not None:
        vehiculo = vehiculos.findall("Vehiculo")  # Nos situamos en vehiculo en el arbol.
        if vehiculo is not None:  # si hay vehiculos
            for vehi in vehiculo:
                for attr in vehi.attrib:  # Recorremos los atributos de los vehiculos.
                    attr_name = attr
                    attr_value = vehi.attrib[attr_name]
                    if attr_value == id_vehiculo:  # si coincide con el parametro es decir lo encontramos.
                        return vehi[3].text  # devolvemos el precio.


def cambiarDisponibilidad(root, id_vehiculo, estado):
    """
    funcion que re escribre el estado de los coches una vez son alquilados
    @:param root se recorre, id_vehiculo identifica, estado marca la accion a realizar
    """
    vehiculos = root.find("Vehiculos")
    if vehiculos is not None:
        vehiculo = vehiculos.findall("Vehiculo")
        if vehiculo is not None:
            for vehi in vehiculo:
                for attr in vehi.attrib:
                    attr_name = attr
                    attr_value = vehi.attrib[attr_name]
                    if attr_value == id_vehiculo:
                        if str(estado) == "Alquilado":  # Me encantaria saber por que si no casteo el estado falla...
                            vehi[4].text = "Alquilado"
                        elif str(estado) == "Disponible":
                            vehi[4].text = "Disponible"


def esta_finalizado(alquiler, id_alquiler):
    """
    funcion que comprueba que un alquiler esta finalizado por medio de comprobar los campos que solo se rellenan en la finalizacion
    @:param alquiler el alquiler que se comprueba.
    """
    if alquiler[4].text is None and alquiler[6].text is None:
        return False
    else:
        return True


def cargar_arbol_xml():
    """
    funcion que crea el arbol si no exsite con 'Renting'. 'Vehiculos' y 'Alquileres'
    """
    if not os.path.exists(file_path):
        root = ET.Element('Renting')
        vehiculos = ET.SubElement(root, 'Vehiculos')
        alquileres = ET.SubElement(root, 'Alquileres')
        tree = ET.ElementTree(root)
        tree.write(file_path, encoding="utf-8", xml_declaration=True, method="xml", short_empty_elements=False)
    else:
        tree = ET.parse(file_path)
        root = tree.getroot()
        vehiculos = root.find('Vehiculos')
        alquileres = root.find('Alquileres')

        if vehiculos is None:
            vehiculos = ET.SubElement(root, 'Vehiculos')
        if alquileres is None:
            alquileres = ET.SubElement(root, 'Alquileres')
        tree.write(file_path, encoding="utf-8", xml_declaration=True, method="xml", short_empty_elements=False)
    prettify(root)


def id_por_mat(root, mat):
    vehiculos = root.find("Vehiculos")
    if vehiculos is None:
        return
    vehiculo = vehiculos.findall("Vehiculo")
    if vehiculo is None:
        return
    for coche in vehiculo:
        if coche[0].text == mat:
            return coche.attrib["idVehiculo"]


# Alta
def crear_alquiler(root):
    """
    funcion que pide campos, si todos son validos procede a situarse en alquileres y crear los correspondientes subelementos.
    @:param root, para ser recorrido y trabajado
    """
    done = False
    print("Creacion de alquileres")
    while not done:  # Bucle que servira para realizar mas de un alquiler
        # En estas lineas nos apoyaremos en los functions de Validador para conseguir campos correctos
        mat = Validador.validar_y_comprobar_matricula(root)
        if mat is not None:
            id_del_vehiculo = id_por_mat(root, mat)  # En estas lineas nos apoyaremos en los funcions de Validador para conseguir campos correctos
            if not esta_dispinible(root, id_del_vehiculo):
                print("El vehiculo no esta disponible para ser alquilado")
                id_del_vehiculo = None
                mat = None
        if mat is not None:
            dni_del_cliente = Validador.validar_dni()
        if mat is not None and dni_del_cliente is not None:
            print("Fecha de inicio:")
            fecha_del_ini = Validador.validar_fecha()
        if mat is not None and dni_del_cliente is not None and fecha_del_ini is not None:
            print("Fecha de fin:")
            fecha_del_fin = Validador.validar_fecha(fecha_del_ini)
        if mat is not None and dni_del_cliente is not None and fecha_del_ini is not None and fecha_del_fin is not None:
            km_del_ini = Validador.validar_kilometraje()
        if mat is not None and dni_del_cliente is not None and fecha_del_ini is not None and fecha_del_fin is not None and km_del_ini is not None:
            # Si todos los campos estan correctos procedemos a crear el subelemento

            alquileres = root.find("Alquileres")  # Nos situamos en alquileres
            if alquileres is None:  # Si no exsie los creamos
                print("Fallo al encontrar Alquileres")
                alquileres = ET.SubElement(root, "Alquileres")
            # Creamos el alquiler con el id como atributo
            alquiler = ET.SubElement(alquileres, "Alquiler", idAlquiler=str(obtener_ultimo_id_alquiler(root)))
            # Vamos creando los subelementos uno a uno y confiriendoles valores.
            id_vehiculo = ET.SubElement(alquiler, "idVehiculo", {'Matricula': mat})  # En el caso de idVheiculo le pondremos como atributo la matricula
            id_vehiculo.text = id_del_vehiculo
            dni_cliente = ET.SubElement(alquiler, "dniCliente")
            dni_cliente.text = dni_del_cliente
            fecha_ini_alq = ET.SubElement(alquiler, "FechaIniAlq")
            fecha_ini_alq.text = str(fecha_del_ini)  # Antes era datetime
            fecha_fin_alq = ET.SubElement(alquiler, "FechaFinAlq")
            fecha_fin_alq.text = str(fecha_del_fin)  # Antes era datetime
            fecha_devo = ET.SubElement(alquiler, "FechaDevolucion")
            km_ini = ET.SubElement(alquiler, "KmInicial")
            km_ini.text = str(km_del_ini)
            km_fin = ET.SubElement(alquiler, "KmFinal")
            precio_final = ET.SubElement(alquiler, "PrecioFinal")
            recargo = ET.SubElement(alquiler, "Recargo")
            cambiarDisponibilidad(root, id_del_vehiculo, "Alquilado")  # Cambiamos el estado del vehuiculo

            prettify(root)  # Re hacemos la estructura del xml
            ElementTree(root).write(file_path)  # Escribimos el archivo

            if not Utiles.si_no(
                    "Desea dar de alta otro alquiler?"):  # Preguntamos si quiere hacer otro y en caso de que no salimos
                done = True
        else:  # Si se falla en los campos te saca del menu.
            done = True


# Mostrar
def mostrar_todos_alquileres(root):
    """
    funcion que recorre el arbol desde la raiz y printea los alquileres
    @:param root
    """
    alquileres = root.find("Alquileres")  # Encontramos los alquileres
    vehiculos = root.find("Vehiculos")  # Encontramos los Vehiculos
    if alquileres is not None and len(alquileres) > 0 and vehiculos is not None and len(vehiculos) > 0:
        for alquileres in root:
            for alquiler in alquileres:
                if "Alquiler" == alquiler.tag:
                    for attr in alquiler.attrib:
                        print("ID del alquiler: ", alquiler.attrib[attr])
                    for i in alquiler:
                        if i.tag == "idVehiculo":
                            print("Matricula", ": ", i.attrib["Matricula"])
                        else:
                            print(i.tag, ": ", i.text)
                    print()
    else:
        if alquileres is None or len(alquileres) == 0:
            print("No hay alquileres en el sistema")
        else:
            print("No hay vehiculos en el sistema")


def mostrar_por_dni(root):
    """
    funcion que recorre el arbol desde la raiz y printea los alquileres que correspondan a un dni
    @:param root
    """
    alquileres = root.find("Alquileres")  # Encontramos los alquileres
    vehiculos = root.find("Vehiculos")  # Encontramos los Vehiculos
    if alquileres is not None and len(alquileres) > 0 and vehiculos is not None and len(vehiculos) > 0:
        esta = False
        dni = Validador.validar_dni()
        for alquileres in root:
            for alquiler in alquileres:
                if "Alquiler" == alquiler.tag:
                    if dni == alquiler[1].text:
                        esta = True
                        for attr in alquiler.attrib:
                            print("ID del alquiler: ", alquiler.attrib[attr])
                        for i in alquiler:
                            if i.tag == "idVehiculo":
                                print("Matricula", ": ", i.attrib["Matricula"])
                            else:
                                print(i.tag, ": ", i.text)
                    print()

        if not esta:
            print("El DNI introducido no se correspondia con el de nadie que hubiese realizado un alquiler")
    else:
        if alquileres is None or len(alquileres) == 0:
            print("No hay alquileres en el sistema")
        else:
            print("No hay vehiculos en el sistema")


def mostrar_por_matricula(root):
    """
    funcion que recorre el arbol desde la raiz y printea los alquileres que correspondan a una matricula
    @:param root
    """
    alquileres = root.find("Alquileres")  # Encontramos los alquileres
    vehiculos = root.find("Vehiculos")  # Encontramos los Vehiculos
    if alquileres is not None and len(alquileres) > 0 and vehiculos is not None and len(vehiculos) > 0:
        esta = False
        esta_alq = False
        mat = input("Introduzca la matricula por la que desea buscar un alquiler: ")
        for alquileres in root:
            for alquiler in alquileres:
                if "Alquiler" == alquiler.tag:
                    print(alquiler[0].attrib["Matricula"])
                    if alquiler[0].attrib["Matricula"] == mat:
                        esta_alq = True
                        for attr in alquiler.attrib:
                            print("ID del alquiler: ", alquiler.attrib[attr])
                        for i in alquiler:
                            if i.tag == "idVehiculo":
                                print("Matricula", ": ", i.attrib["Matricula"])
                            else:
                                print(i.tag, ": ", i.text)
                    print()
        if not esta_alq:
            print("La matricula introducida con se corresponde con la de ningun alquiler")
        else:
            print("La matricula introducida con se corresponde con la de ningun vehiculo")
    else:
        if alquileres is None or len(alquileres) == 0:
            print("No hay alquileres en el sistema")
        else:
            print("No hay vehiculos en el sistema")


# Finalizar
def calcular_recargo(alquiler, fecha_devo):
    """
    funcion que comprueba si la fecha de devolucion sobrepasa la del final del alquiler
    @:param alquiler que se va a finalizar la fecha de devolucion
    @:return true si la fecha fin es menor que la de devolucion
    """
    fecha = alquiler[3].text  # Obtenemos la fecha final
    fecha = str(fecha)
    fecha_aux = fecha.split("-")  # Sacamos una lista con los datos
    fecha_formateada = datetime.date(int(fecha_aux[0]), int(fecha_aux[1]), int(fecha_aux[2]))  # Reconstruimos la fecha final
    if fecha_formateada < fecha_devo:  # Comprobamos cual es mayor
        return True
    else:
        return False


def finalizar(root, alquiler, id_alquiler):
    """
    function que finaliza los campos de un alquiler.
    @:param root que se escribira alquiler que se actualizara
    """
    print("Introduzca la fecha de devolucion del vehiculo")
    campos = str(alquiler[2].text).split("-")  # Obtenemos la fecha inicial
    fecha_ini = datetime.date(int(campos[0]), int(campos[1]), int(campos[2]))  # Reconstruimos la fecha inicial
    campos_fin = str(alquiler[3].text).split("-")  # Obtenemos la fecha final
    fecha_fin = datetime.date(int(campos_fin[0]), int(campos_fin[1]), int(campos_fin[2]))  # Reconstruimos la fecha final
    fecha_devo = Validador.validar_fecha(fecha_ini)  # pedimos la fecha de devolucion
    if fecha_devo is not None:  # comprobamos que los campos son validos
        km_fin = Validador.validar_kilometraje(alquiler[5].text)  # Pedimos kmfinal
    if fecha_devo is not None and km_fin is not None:  # Si los campos son correctos damos el alquiler por finalizado
        if Utiles.si_no("Seguro que quiere finalizar este alquiler? Esto lo hara inmodificable."):
            alquiler[4].text = str(fecha_devo)
            alquiler[6].text = km_fin  # Escribimos los campos
            '''Linea que calcula el precio*dias por medio de restar fechas, pasarlas a dias, convertirlas a string porque 
            castear de date a int explota y concluye multiplicando los dias por el precio/dia del vehiculo.'''
            if calcular_recargo(alquiler, fecha_devo):  # Comprobamos si merece recargo o no y lo aplicamos si es necesario
                recargo = 30 * int(str((fecha_devo - fecha_fin).days))
                alquiler[8].text = str(recargo)
                precio = int(str((fecha_devo - fecha_ini).days)) * float(conseguir_precio_por_id(root, alquiler[0].text)) + recargo
                alquiler[7].text = str(precio)
            else:
                alquiler[8] = "Sin recargo"
                precio = int(str((fecha_fin - fecha_ini).days)) * float(conseguir_precio_por_id(root, alquiler[0].text))
                alquiler[7].text = str(precio)

            cambiarDisponibilidad(root, alquiler[0].text, "Disponible")  # Cambiamos el estado del vehuiculo
            prettify(root)
            ElementTree(root).write(file_path)  # Re escribimos el xml

        print("Alquiler finalizado")
    else:
        print("Volviendo al menu de finalizacion.")


def conseguir_id_por_matricula(root, matricula):
    """
    Funcion que regresa un id al usuario a partir de una matricula
    :param root: que se recorre
    :param matricula: por la que se busca
    :return: El id del alquiler seleccionado
    """
    alquileres = root.find("Alquileres")
    if alquileres is None:
        return False
    alquiler = alquileres.findall("Alquiler")
    if alquiler is None:
        return False
    for alq in alquiler:
        id_alq = alq.attrib["idAlquiler"]
        if alq[0].attrib["Matricula"] == matricula and not esta_finalizado(alq, id_alq):
            return alq.attrib["idAlquiler"]


def finalizar_alquiler(root):
    """
    funcion que pide un id de alquiler y si no esta finalizado lo finaliza.
    @:param root que se recorrera
    """
    done = False
    esta = False
    alquileres = root.find("Alquileres")  # Encontramos los alquileres
    vehiculos = root.find("Vehiculos")  # Encontramos los Vehiculos
    if alquileres is not None and len(alquileres) > 0 and vehiculos is not None and len(vehiculos) > 0:
        while not done:  # Para finalizar mas de uno si se quiere
            print("Devolucion del vehiculo.")
            matricula = Validador.validar_y_comprobar_matricula(root)  # Pelidmos id
            id_alquiler = conseguir_id_por_matricula(root, matricula)
            alquiler = alquileres.findall("Alquiler")
            if alquiler is not None and len(alquiler) > 0:  # consequimos una lista de alquileres
                for i in alquiler:  # Recorremos los alquileres
                    if id_alquiler == i.attrib["idAlquiler"]:  # Si el id se corresponde con el que buscamos
                        esta = True  # Marcamos true para que luego no salte lo de que no se encontro
                        if not esta_finalizado(i, id_alquiler):  # Comprobamos si ya esta finalizado
                            finalizar(root, i, id_alquiler)  # Si no lo esta lo mandamos finalizar.
                        else:
                            print("El alquiler que desea finalizar ya fue finalizado anteriormente.")
                if not esta:
                    print("El id introducido no coincide con el de ningun alquiler")
            else:
                print("No hay alquileres en el sistema")
            if not Utiles.si_no("Quiere tratar de finalizar otro alquiler?"):
                done = True
    else:
        if alquileres is None or len(alquileres) == 0:
            print("No hay alquileres en el sistema")
        else:
            print("No hay vehiculos en el sistema")


def modificar(root, alq):
    """
    Funcion que Realiza las modifiaciones en el alquiler y rescribe el fichero
    :param root: que se reescribira
    :param alq: que se modificara.
    """
    elec = ""
    while elec != "0":
        print("----MENU DE MODIFICACION----")
        print("1. Matricula\n3. Fecha de inicio\n4. fecha de finalizacion\n5. Kilometraje inicial\n0. Salir")
        elec = input("Elija el campo que desea modificar (1/2/3/4/0):\n")
        if elec == "1": #Matricula
            print("Modificacion de matricula.")
            mat = Validador.validar_y_comprobar_matricula(root)
            if mat is not None: #Comprobamos que la matricula sea correcta
                id_vehiculo = id_por_mat(root, mat) #Obtenemos el id
                print(mat, id_vehiculo)
                if esta_dispinible(root, id_vehiculo): #Vemos si esta disponible el posible nuevo vehiculo
                    if Utiles.si_no("Seguro que desea sustituir la matricula "+ alq[0].attrib["Matricula"] +" por "+ mat +"?"): #Si lo esta y confirma
                        alq[0].text = id_vehiculo #Realizamos los cambios
                        alq[0].attrib["Matricula"] = mat
                        print("Matricula modificada con existo")
                    else:
                        print("Modificacion cancelada.")
                else:
                    print("El vehiculo por el que desea modificar la matricula no esta disponible actualmente.")
        elif elec == "2": #DNI
            print("Modificacion de DNI.")
            dni = Validador.validar_dni()
            if dni is not None: #Valodamos campos
                if Utiles.si_no("Seguro que desea modificar el dni del cliente por " + dni + "?"): #Pedimos confirmacion
                    alq[1].text = dni #Aplicamos
                    print("DNI modificado con existo")
                else:
                    print("Modificacion cancelada.")
        elif elec == "3": #fecha inicio
            print("Modificacion de la fecha inicial: Si esta sobrepasa la fecha final estimada esta tambien pedirá modificada.")
            fecha_ini = Validador.validar_fecha()
            if fecha_ini is not None: #Comprobamos que el cmapo es correcto
                campos_fin = alq[3].text.split("-")
                fecha_fin = datetime.date(int(campos_fin[0]),int(campos_fin[1]),int(campos_fin[2]))
                if fecha_ini > fecha_fin: #Comprobamos que no es posterior a la antigua fecha de fin
                    print("La nueva fecha de inicio sobrepasa la antigua fecha de fin estimada. Modifique la fecha de fin.") #Notificamos
                    nueva_fecha_fin = Validador.validar_fecha(fecha_ini)
                    if nueva_fecha_fin is not None:  #Comprobamos la nueva fecha fin
                        if Utiles.si_no("Seguro que desea cambiar la fecha inicial de "+ alq[2].text +" a "+ str(fecha_ini) +" y la fecha final por "+ str(nueva_fecha_fin) +"?"): #Confirmacion
                            alq[2].text = str(fecha_ini) #Aplicar cambios
                            alq[3].text = str(nueva_fecha_fin)
                            print("Fecha inicial y final modificada")
                        else:
                            print("Fecha inicial modificada")
                else: #Si no se pasa
                    if Utiles.si_no("Seguro que desea cambiar la fecha inicial de "+ alq[2].text +" a "+ str(fecha_ini) +"?"):
                        alq[2].text = str(fecha_ini) #Aplicar cambios
                        print("Fecha inicial modificada")
                    else:
                        print("Modificacion cancelada.")
        elif elec == "4": #fecha fin
            print("Modificacion de la fecha final.")
            campos_ini = alq[2].text.split("-")
            fecha_ini = datetime.date(int(campos_ini[0]),int(campos_ini[1]),int(campos_ini[2]))
            fecha_fin = Validador.validar_fecha(fecha_ini)
            if fecha_fin is not None: #Comprobamos que el nuevo campo es correco
                if Utiles.si_no("Seguro que desea cambiar la fecha de fin de alquiler por "+ str(fecha_fin) +"?"):
                    alq[3].text = str(fecha_fin) #Ejecutamos cambio
                    print("Fecha final modificada")
                else:
                    print("Modificacion cancelada.")
        elif elec == "5": #Km inicial
            print("Modificacion del kilometraje inicial.") #Pedimos el campo
            km_ini = Validador.validar_kilometraje()
            if km_ini is not None: #Comprobamos
                if Utiles.si_no("Seguro que desea cambiar el kilometraje inicial por "+ km_ini +"?"): #Pedimos confirmacion
                    alq[5].text = km_ini #Ejecutamos cambio
                    print("Kilometraje inicial modificado")
                else:
                    print("Modificacion cancelada.")
        else:
            print("Eleccion no valida.")
        prettify(root)
        ElementTree(root).write(file_path)  # Re escribimos el xml


def modificar_alquiler(root):
    """
    Funcion que encuentra el alquiler a modificar y los manda a la funcion de modificacion
    :param root: que se recorrera en busca del alquiler
    """
    alquileres = root.find("Alquileres")  # Encontramos los alquileres
    vehiculos = root.find("Vehiculos")  # Encontramos los Vehiculos
    if alquileres is not None and len(alquileres) > 0 and vehiculos is not None and len(vehiculos) > 0:
        done = False
        esta = False
        while not done:  # Para finalizar mas de uno si se quiere
            print("Modificacion de Alquiler.. Recuerde que solo puede modificar alquileres sin finalizar.")
            matricula = Validador.validar_y_comprobar_matricula(root)  # pedimos la matricula
            if matricula is not None: #Si es correcta
                id_alquiler = conseguir_id_por_matricula(root, matricula) #Conseguimos el id
                alquiler = alquileres.findall("Alquiler")
                for alq in alquiler:
                    if alq[0].attrib["Matricula"] == matricula and not esta_finalizado(alq, id_alquiler): #Si el alquiler existe y no esta finalizado lo mandamos a modificar.
                        modificar(root, alq)
                    else:
                        print("La matricula que usted introduce no tiene ningun alquiler abierto que modificar.")
            if not Utiles.si_no("Quiere modificar otro alquiler?"):
                done = True
    else:
        if alquileres is None or len(alquileres) == 0:
            print("No hay alquileres en el sistema")
        else:
            print("No hay vehiculos en el sistema")


def menu_alquiler(root):
    """
    funcion que actua como un menu y dispara los funcions
    @:param root que se manda por los funcions
    """
    choice = ""
    while choice != "0":
        print("\nMenu de Alquileres:")
        print("1. Crear un alquiler")
        print("2. Buscar un alquiler")
        print("3. Modificar un alquiler")
        print("4. Finalizar un alquiler")
        print("0. Volver al menu principal")

        choice = input("Selecciona una opcion (1/2/3/4/0): ")

        if choice == "1":
            crear_alquiler(root)
        elif choice == "2":
            menu_busqueda(root)
        elif choice == "3":
            modificar_alquiler(root)
        elif choice == "4":
            finalizar_alquiler(root)
        elif choice == "0":
            print("Saliendo del menu de alquileres")
        else:
            print("Opcion no valida.")


def menu_busqueda(root):
    """
    Menu con los tres tipo de busqueda
    @:param root que se manda por los funcions
    """
    choice = ""
    while choice != "0":
        print("\nMenu de Alquileres:")
        print("1. Mostrar todos los alquileres")
        print("2. Buscar todos los alquileres de una matricula")
        print("3. Buscar todos los alquileres de un cliente (DNI)")
        print("0. Volver al menu de alquileres")

        choice = input("Selecciona una opcion (1/2/3/0): ")
        if choice == "1":
            mostrar_todos_alquileres(root)
        elif choice == "2":
            mostrar_por_matricula(root)
        elif choice == "3":
            mostrar_por_dni(root)
        elif choice == "0":
            print("Saliendo del menu de busqueda.")
        else:
            print("Opcion no valida.")
