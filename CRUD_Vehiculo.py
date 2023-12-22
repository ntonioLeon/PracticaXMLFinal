import xml.etree.ElementTree as ET
import os
import Utiles


def cargar_arbol_xml():
    """
    metodo que se encarga de cargar el de cargar el fichero XML
    """
    if not os.path.exists(Utiles.path()):
        root = ET.Element('Renting')
        vehiculos = ET.SubElement(root, 'Vehiculos')
        alquileres = ET.SubElement(root, 'Alquileres')
        tree = ET.ElementTree(root)
        tree.write(Utiles.path(), encoding="utf-8", xml_declaration=True, method="xml", short_empty_elements=False)
    else:
        tree = ET.parse(Utiles.path())
        root = tree.getroot()
        vehiculos = root.find('Vehiculos')
        alquileres = root.find('Alquileres')

        if vehiculos is None:
            vehiculos = ET.SubElement(root, 'Vehiculos')
        if alquileres is None:
            alquileres = ET.SubElement(root, 'Alquileres')
        tree.write(Utiles.path(), encoding="utf-8", xml_declaration=True, method="xml", short_empty_elements=False)
    prettify(root)
    return root


def prettify(elem, level=0):
    """
    prettify, encargado de reorganizar el fichero XML
    """
    indent = "    "  # 4 espacios por nivel
    i = "\n" + level * indent
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + indent
        for subelem in elem:
            prettify(subelem, level + 1)
            if not subelem.tail or not subelem.tail.strip():
                subelem.tail = i + indent
        if not elem[-1].tail or not elem[-1].tail.strip():
            elem[-1].tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def obtener_ultimo_id():
    """
    metodo que retona el ultimo id+1 para crear un nuevo vehiculo y asignarle un id valido
    """
    tree = ET.parse(Utiles.path())
    root = tree.getroot()

    vehiculos = root.find('Vehiculos')
    ultimos_vehiculos = vehiculos.findall('Vehiculo[@idVehiculo]')

    if ultimos_vehiculos:
        ultimo_id = max(int(vehiculo.get('idVehiculo')) for vehiculo in ultimos_vehiculos)
        return ultimo_id + 1
    else:
        return 1


def crear_vehiculo(vehiculo, root):
    """
    Metodo encargado de crear un nuevo vehiculo
    @:param  root y los datos necesarios para crear un vehiculo
    """
    tree = ET.ElementTree(root)
    id = obtener_ultimo_id()
    coche = ET.Element('Vehiculo', {'idVehiculo': str(id)})

    for key, value in vehiculo.items():
        if key != 'idVehiculo':
            sub_element = ET.Element(key)
            sub_element.text = str(value)
            coche.append(sub_element)

    vehiculos = root.find('Vehiculos')
    vehiculos.append(coche)

    prettify(root)

    tree.write(Utiles.path())


def check_status(root):
    """
    Metodo encargado de verificar si existen vehiculos en el fichero XML
    @:param root
    """
    vehiculos = root.find('Vehiculos')

    if vehiculos is not None and vehiculos.findall('Vehiculo'):
        return True  # Hay vehículos
    else:
        print("║  No hay vehiculos registrados  ║")
        print("║                                ║")
        print("╚════════════════════════════════╝")
        return False  # No hay vehículos


def mostrar_todos(root):
    """
    Metodo encargado de imprimir por pantalla los vehiculos en el fichero XML
    @:param root
    """
    vehiculos = root.find('Vehiculos')

    if vehiculos is not None and vehiculos.findall('Vehiculo'):
        for vehiculo in vehiculos.findall('Vehiculo'):
            print("║ID de Vehículo: ", vehiculo.get('idVehiculo') + " " * (15 - len(vehiculo.get('idVehiculo'))) + "║")
            for element in vehiculo:
                print(
                    "║" + f"{element.tag}: {element.text}" + " " * (30 - (len(element.text) + len(element.tag))) + "║")
            print("╠════════════════════════════════╣")
        print("║   Volviendo a menu Vehiculo    ║")
        print("╚════════════════════════════════╝")
        prettify(root)
        return True  # Hay vehículos
    else:
        print("║  No hay vehiculos registrados  ║")
        print("║                                ║")
        print("╚════════════════════════════════╝")
        return False  # No hay vehículos


def obtener_vehiculo(matricula):
    """
    Metodo encargado de devolver los datos de un vehiculo en el XML
    @:param matricula
    return: datos del vehiculo
    """
    try:
        tree = ET.parse(Utiles.path())
        root = tree.getroot()

        vehiculos = root.find('Vehiculos')

        if vehiculos is not None:
            for vehiculo in vehiculos.findall('Vehiculo'):
                if vehiculo.find('Matricula').text == matricula.upper():
                    vehiculo_dic = {'idVehiculo': vehiculo.get('idVehiculo')}
                    for element in vehiculo:
                        vehiculo_dic[element.tag] = element.text
                    return vehiculo_dic
        print(f"║No se encontró ningún vehículo  ║\n║con la matrícula: {matricula.upper()}║")
        return None

    except Exception as e:
        print(f"Error al procesar el XML: {e}")
        return None


def buscar_vehiculo(matricula):
    """
    Permite buscar vehiculos en el XML por matricula
    """
    tree = ET.parse(Utiles.path())
    root = tree.getroot()

    vehiculos = root.find('Vehiculos')

    if vehiculos is not None:
        for vehiculo in vehiculos.findall('Vehiculo'):
            if vehiculo.find('Matricula').text == matricula:
                print("\nID de Vehículo:", vehiculo.get('idVehiculo'))
                for element in vehiculo:
                    print(
                        f"{element.tag}: {element.text}")  # f es como el printf en java es mas felxible para imprimir expresiones
                return True
    print(f"║No se encontró ningún vehículo  ║\n║con la matrícula: {matricula}║")
    return False


def obtener_id_por_matricula(matricula):
    """
    Devuelve el id de un vehiculo a partir de la matricula de este
    @:param matricula
    return: id vehiculo
    """
    tree = ET.parse(Utiles.path())
    root = tree.getroot()

    vehiculos = root.find('Vehiculos')
    if vehiculos is not None:
        for vehiculo in vehiculos.findall('Vehiculo[Matricula="{0}"]'.format(matricula)):
            return vehiculo.get('idVehiculo')

    return None


def verificar_matricula(cadena):
    """
    verifica si el formato introducido es el de una matricula: AAA000
    @:param cadena
    return: true= lo cumple
    return: false= no lo cumple
    """
    if len(cadena) == 6:
        letras = cadena[:3]
        numeros = cadena[3:]
        if letras.isalpha() and numeros.isdigit():
            return True
        else:
            return False
    else:
        return False


def matricula_en_uso(matricula, root):
    """
    Verifica si la matricula introducida esta ya registrada
    @:param matricula y root
    return: true= ya esta registrada
    return: false= no esta registrada
    """
    try:
        tree = ET.ElementTree(root)
        vehiculos = tree.find('.//Vehiculos')
        if vehiculos is not None:
            for vehiculo in vehiculos.findall('.//Vehiculo/Matricula'):
                if vehiculo.text == matricula.upper():
                    return True
        return False
    except Exception as e:
        print(f"Error al verificar matrícula: {e}")
        return False


def entrada_teclado(campo):
    """
    verifica que la entrada de teclado no es null
    @:param campo
    """
    contador = 0
    while True:
        entrada = input("Introduce una  " + campo + ": ")
        if entrada.strip():
            return entrada
        else:
            print("Por favor, no ingresa una cadena vacía.")
            contador += 1
            if contador == 3:
                return None


def fails(fallos, modificacion):
    """
    Metodo de apoyo para verificacion de datos
    @:param fallos(int), modificacion(str)= datos para la informacion
    return: numero de fallos
    """
    fallos += 1
    print(str(fallos) + "/3 fallos hasta salir del " + modificacion)
    return fallos


def isdecima(num):
    """
    verifica si un numero es decimal, si es un int lo combierte a float
    @:param num(int), num(float), num(str)
    return: num(float)
    return: None
    """
    try:
        numero = int(num)
        if 50 <= numero <= 250:
            return str(numero) + ".00"
    except ValueError:
        try:
            numero = float(num)
            if 50 <= numero <= 250:
                return round(numero, 2)
        except ValueError:
            return None


def alta_datos(root):
    """
    Metodo legado de alta vehiculos realmete no se usa
    @:param root
    """
    renuncia = False
    fallos = 0
    while not renuncia:
        print("ALTA NUEVO VEHICULO")
        exito = False

        while not exito:
            matricula = input("Introduzca una matricula valida, recuerde el formato valido de matricula es AAA000.")
            if matricula is not None and not matricula_en_uso(matricula, root) and verificar_matricula(matricula):
                print("**Matricula introducida con exito")
                exito = True
            elif matricula is None:
                print("Es una cadena vacia")
                fallos = fails(fallos, "Alta")
            elif not verificar_matricula(matricula):
                print("El formato de la matricula no es correcto")
                fallos = fails(fallos, "Alta")
            elif matricula_en_uso(matricula, root):
                print("La matricula ya esta en uso")
                fallos = fails(fallos, "Alta")

            if fallos == 3:
                print("Ha alcanzado el máximo de intentos. Saliendo del proceso de alta.")
                exito = True
                renuncia = True

        if fallos < 3:
            fallos = 0
            exito = False
            while not exito:
                marca = input("Introduzca una marca valida.").split()
                if marca is not None:
                    print("**Marca introducida con exito")
                    exito = True
                elif marca is None:
                    print("Es una cadena vacia.")
                    fallos = fails(fallos, "Alta")

                if fallos == 3:
                    print("Ha alcanzado el máximo de intentos. Saliendo del proceso de alta.")
                    exito = True
                    renuncia = True

        if fallos < 3:
            fallos = 0
            exito = False
            while not exito:
                modelo = input("Introduzca un modelo valido.").split()
                if modelo is not None:
                    print("**Modelo introducida con exito.")
                    exito = True
                elif modelo is None:
                    print("Es una cadena vacia.")
                    fallos = fails(fallos, "Alta")

                if fallos == 3:
                    print("Ha alcanzado el máximo de intentos. Saliendo del proceso de alta.")
                    exito = True
                    renuncia = True

        if fallos < 3:
            fallos = 0
            exito = False
            while not exito:
                anno = input(
                    "Introduzca una fecha de fabricacion valida. Recuerde nuestros modelos abarcan entre 1970 y 2023")
                if anno is not None:
                    if anno.isnumeric():
                        anno = int(anno)
                        if 1970 <= anno <= 2023:
                            print("**Fecha de fabricacion introducida con exito")
                            exito = True
                        else:
                            print("No ha introducido una fecha valida.")
                            fallos = fails(fallos, "Alta")
                    else:
                        print("No ha introducido una fecha.")
                        fallos = fails(fallos, "Alta")
                elif anno is None:
                    print("Es una cadena vacia")
                    fallos = fails(fallos, "Alta")

                if fallos == 3:
                    print("Ha alcanzado el máximo de intentos. Saliendo del proceso de alta.")
                    exito = True
                    renuncia = True

        if fallos < 3:
            fallos = 0
            exito = False
            while not exito:
                tarifa = input("Introduzca una tarifa. Recuerde nuestros modelos abarcan entre 50 y 250€ al dia")
                tarifa = isdecima(tarifa)
                if tarifa is not None:
                    print("**Tarifa introducida con exito")
                    exito = True
                else:
                    fallos = fails(fallos, "Alta")

                if fallos == 3:
                    print("Ha alcanzado el máximo de intentos. Saliendo del proceso de alta.")
                    exito = True
                    renuncia = True

        if fallos < 3:
            retorno = False
            fallos = 0
            vehicle = {'Matricula': matricula, 'MarcaModelo': marca, 'AnnoFabricacion': anno, 'TarifaDia': tarifa,
                       'Estado': 'Disponible'}
            print(vehicle)
            if Utiles.si_no("Desea agregar un nuevo vehiculo con estas caracteristicas?"):
                crear_vehiculo(vehicle, root)
                print("** Nuevo vehiculo agregado")
                retorno = True
            else:
                print("Alta cancelada")
                retorno = True
            if retorno:
                if Utiles.si_no("Desea volver a agregar un nuevo vehiculo?"):
                    print("Volviendo al menu principal")
                    retono = False
                else:
                    print("Volviendo al menu principal")
                    renuncia = True


def eliminar_vehiculo(root, id_vehiculo):
    """

    :param root:
    :param id_vehiculo:
    :return:
    """
    tree = ET.ElementTree(root)
    try:
        vehiculo_a_eliminar = None

        # Buscar el vehículo con el ID dado
        for vehiculo in root.findall(".//Vehiculo"):
            if vehiculo.get("idVehiculo") == str(id_vehiculo):
                vehiculo_a_eliminar = vehiculo
                break

        if vehiculo_a_eliminar is not None:
            # Eliminar el vehículo del árbol
            root.find('.//Vehiculos').remove(vehiculo_a_eliminar)
            print("║ Vehiculo eliminado con exito   ║")
        else:
            print("║ Vehiculo no encontrado         ║")

        prettify(root)
        tree.write(Utiles.path())
    except Exception as e:
        print("║ Error al procesar el fichero.  ║")


def modificar_vehiculo(root, matricula, datos):
    """
    Modifica un vehiculo exsistente en el XML

    :param root: Elemento raiz del arbol XML
    :param matricula: Matricula del vehiculo susceptible del cambio, no comprueba si existe
    :param datos: Diccionario con los nuevos datos del vehiculo, los modificados y los no modificados
    :return: None
    """
    tree = ET.ElementTree(root)
    id_nue = obtener_id_por_matricula(matricula)
    try:
        for vehiculo in root.findall(".//Vehiculo[Matricula='" + matricula + "']"):
            for key, value in datos.items():
                # Verificar si el elemento ya existe
                elemento = vehiculo.find(key)
                if elemento is not None:
                    elemento.text = str(value)
                    # Actualizar el valor existente
                else:
                    # Crear un nuevo elemento si no existe
                    nuevo = ET.Element(key)
                    nuevo.text = str(value)
                    vehiculo.append(nuevo)
        tree.write(Utiles.path())
        #for alquiler in root.findall(root.find(".//idVehiculo").get("Matricula")==matricula):
        for alquiler in root.findall(".//Alquiler[0].get('Matricula')="+matricula+""):
        #for alquiler in root.findall(".//Alquiler[idVehiculo@Matricula='" + id_nue + "']"):
        #for alquiler in root.findall(".//Alquiler[idVehiculo='" + id_nue + "']"):
            alquiler[0].attrib["Matricula"] = str(datos["Matricula"])

        prettify(root)

        tree.write(Utiles.path())
        print("║"f"Vehículo con matrícula {matricula}" + " " * (25 - len("Vehículo con matrícula ")+len({matricula})) + "║")
        print("║ modificado correctamente.      ║")
        print("║              ----              ║")
    except Exception as e:
        print("║ Error al procesar el fichero.  ║")


''' Estructura de datos de un vehiculo.
vehicle_data = {
    'Matricula': 'ABC123',
    'MarcaModelo': 'Esto es un test3',
    'AnnoFabricacion': '1979',
    'TarifaDia': '50.00',
    'Estado': 'Disponible'
}
'''
