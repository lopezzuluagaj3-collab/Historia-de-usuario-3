from produccion import (
    agregar_producto,
    mostrar_inventario,
    buscar_producto,
    actualizar_producto,
    eliminar_producto,
    calcular_estadisticas
)
from archivo import guardar_csv, cargar_csv

inventario = []

def mostrar_menu():
    print("\n" + "="*50)
    print("     SISTEMA DE GESTIÓN DE INVENTARIO")
    print("="*50)
    print("1. Agregar producto")
    print("2. Mostrar inventario")
    print("3. Buscar producto")
    print("4. Actualizar producto")
    print("5. Eliminar producto")
    print("6. Mostrar estadísticas")
    print("7. Guardar inventario en CSV")
    print("8. Cargar inventario desde CSV")
    print("9. Salir")
    print("="*50)

def obtener_opcion():
    try:
        opcion = input("\nSeleccione una opción (1-9): ").strip()
        if opcion in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
            return opcion
        else:
            print("❌ Error: Debe ingresar un número entre 1 y 9.")
            return None
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return None

def solicitar_datos_producto():
    try:
        nombre = input("\nNombre del producto: ").strip()
        if not nombre:
            print("❌ El nombre no puede estar vacío.")
            return None
        
        while True:
            try:
                precio = float(input("Precio del producto: $"))
                if precio < 0:
                    print("❌ El precio no puede ser negativo.")
                    continue
                break
            except ValueError:
                print("❌ Error: El precio debe ser un número válido (use . para decimales).")
        
        while True:
            try:
                cantidad = int(input("Cantidad en stock: "))
                if cantidad < 0:
                    print("❌ La cantidad no puede ser negativa.")
                    continue
                break
            except ValueError:
                print("❌ Error: La cantidad debe ser un número entero.")
        
        return nombre, precio, cantidad
    
    except Exception as e:
        print(f"❌ Error al solicitar datos: {e}")
        return None

def ejecutar_opcion(opcion):
    global inventario
    
    try:
        if opcion == '1':
            datos = solicitar_datos_producto()
            if datos:
                nombre, precio, cantidad = datos
                agregar_producto(inventario, nombre, precio, cantidad)
                print(f"✅ Producto '{nombre}' agregado exitosamente.")
        
        elif opcion == '2':
            mostrar_inventario(inventario)
        
        elif opcion == '3':
            nombre = input("\nIngrese el nombre del producto a buscar: ").strip()
            producto = buscar_producto(inventario, nombre)
            if producto:
                print(f"\n✅ Producto encontrado:")
                print(f"   Nombre: {producto['nombre']}")
                print(f"   Precio: ${producto['precio']:.2f}")
                print(f"   Cantidad: {producto['cantidad']}")
            else:
                print(f"❌ Producto '{nombre}' no encontrado.")
        
        elif opcion == '4':
            if not inventario:
                print("❌ El inventario está vacío. No hay productos para actualizar.")
                return True
            
            mostrar_inventario(inventario)
            nombre = input("\nIngrese el nombre del producto a actualizar: ").strip()
            
            if not buscar_producto(inventario, nombre):
                print(f"❌ Producto '{nombre}' no encontrado.")
                return True
            
            print("\n¿Qué desea actualizar?")
            print("1. Precio")
            print("2. Cantidad")
            print("3. Ambos")
            sub_opcion = input("Opción: ").strip()
            
            nuevo_precio = None
            nueva_cantidad = None
            
            if sub_opcion in ['1', '3']:
                while True:
                    try:
                        nuevo_precio = float(input("Nuevo precio: $"))
                        if nuevo_precio < 0:
                            print("❌ El precio no puede ser negativo.")
                            continue
                        break
                    except ValueError:
                        print("❌ Debe ingresar un número válido.")
            
            if sub_opcion in ['2', '3']:
                while True:
                    try:
                        nueva_cantidad = int(input("Nueva cantidad: "))
                        if nueva_cantidad < 0:
                            print("❌ La cantidad no puede ser negativa.")
                            continue
                        break
                    except ValueError:
                        print("❌ Debe ingresar un número entero.")
            
            if actualizar_producto(inventario, nombre, nuevo_precio, nueva_cantidad):
                print(f"✅ Producto '{nombre}' actualizado exitosamente.")
            else:
                print(f"❌ No se pudo actualizar el producto.")
        
        elif opcion == '5':
            if not inventario:
                print("❌ El inventario está vacío. No hay productos para eliminar.")
                return True
            
            mostrar_inventario(inventario)
            nombre = input("\nIngrese el nombre del producto a eliminar: ").strip()
            
            confirmar = input(f"¿Está seguro de eliminar '{nombre}'? (S/N): ").strip().upper()
            if confirmar == 'S':
                if eliminar_producto(inventario, nombre):
                    print(f"✅ Producto '{nombre}' eliminado exitosamente.")
                else:
                    print(f"❌ Producto '{nombre}' no encontrado.")
            else:
                print("Operación cancelada.")
        
        elif opcion == '6':
            stats = calcular_estadisticas(inventario)
            
            print("\n" + "="*50)
            print("     ESTADÍSTICAS DEL INVENTARIO")
            print("="*50)
            print(f"Total de productos: {len(inventario)}")
            print(f"Unidades totales en stock: {stats['unidades_totales']}")
            print(f"Valor total del inventario: ${stats['valor_total']:.2f}")
            
            if stats['producto_mas_caro']:
                print(f"\nProducto más caro:")
                print(f"  → {stats['producto_mas_caro']['nombre']}: ${stats['producto_mas_caro']['precio']:.2f}")
            
            if stats['producto_mayor_stock']:
                print(f"\nProducto con mayor stock:")
                print(f"  → {stats['producto_mayor_stock']['nombre']}: {stats['producto_mayor_stock']['cantidad']} unidades")
            
            print("="*50)
        
        elif opcion == '7':
            ruta = input("\nIngrese la ruta del archivo CSV (ej: inventario.csv): ").strip()
            if not ruta:
                ruta = "inventario.csv"
            guardar_csv(inventario, ruta)
        
        elif opcion == '8':
            ruta = input("\nIngrese la ruta del archivo CSV a cargar: ").strip()
            inventario = cargar_csv(ruta, inventario)
        
        elif opcion == '9':
            print("\n👋 ¡Gracias por usar el sistema de inventario!")
            print("Saliendo del programa...")
            return False
        
        return True
    
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        print("Volviendo al menú principal...")
        return True

def main():
    print("\n¡Bienvenido al Sistema de Gestión de Inventario!")
    
    while True:
        mostrar_menu()
        opcion = obtener_opcion()
        
        if opcion:
            continuar = ejecutar_opcion(opcion)
            if not continuar:
                break
        
        input("\nPresione Enter para continuar...")

if __name__ == "__main__":
    main()

