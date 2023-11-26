import CRUD_Vehiculo
import Menu

print("Inicio proyecto")
root = CRUD_Vehiculo.cargar_arbol_xml()
Menu.menu_principal(root)

print("Fin proyecto")
