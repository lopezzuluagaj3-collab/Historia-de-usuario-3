def agregar_producto(inventario, nombre, precio, cantidad):
    for producto in inventario:
        if producto['nombre'].lower() == nombre.lower():
            print(f"⚠️  Advertencia: El producto '{nombre}' ya existe.")
            confirmar = input("¿Desea actualizar la cantidad sumando? (S/N): ").strip().upper()
            if confirmar == 'S':
                producto['cantidad'] += cantidad
                producto['precio'] = precio
                print(f"✅ Cantidad actualizada. Nueva cantidad: {producto['cantidad']}")
            return
    
    nuevo_producto = {
        "nombre": nombre,
        "precio": precio,
        "cantidad": cantidad
    }
    
    inventario.append(nuevo_producto)

def mostrar_inventario(inventario):
    if not inventario:
        print("\n📦 El inventario está vacío.")
        return
    
    print("\n" + "="*70)
    print("                        INVENTARIO ACTUAL")
    print("="*70)
    print(f"{'ID':<5} {'NOMBRE':<25} {'PRECIO':<15} {'CANTIDAD':<10}")
    print("-"*70)
    
    for idx, producto in enumerate(inventario, start=1):
        print(f"{idx:<5} {producto['nombre']:<25} ${producto['precio']:<14.2f} {producto['cantidad']:<10}")
    
    print("="*70)
    print(f"Total de productos: {len(inventario)}")

def buscar_producto(inventario, nombre):
    for producto in inventario:
        if producto['nombre'].lower() == nombre.lower():
            return producto
    return None

def actualizar_producto(inventario, nombre, nuevo_precio=None, nueva_cantidad=None):
    producto = buscar_producto(inventario, nombre)
    
    if not producto:
        return False
    
    if nuevo_precio is not None:
        producto['precio'] = nuevo_precio
    
    if nueva_cantidad is not None:
        producto['cantidad'] = nueva_cantidad
    
    return True

def eliminar_producto(inventario, nombre):
    for idx, producto in enumerate(inventario):
        if producto['nombre'].lower() == nombre.lower():
            inventario.pop(idx)
            return True
    return False

def calcular_estadisticas(inventario):
    if not inventario:
        return {
            "unidades_totales": 0,
            "valor_total": 0.0,
            "producto_mas_caro": None,
            "producto_mayor_stock": None
        }
    
    subtotal = lambda p: p["precio"] * p["cantidad"]
    
    unidades_totales = sum(producto['cantidad'] for producto in inventario)
    valor_total = sum(subtotal(producto) for producto in inventario)
    producto_mas_caro = max(inventario, key=lambda p: p['precio'])
    producto_mayor_stock = max(inventario, key=lambda p: p['cantidad'])
    
    return {
        "unidades_totales": unidades_totales,
        "valor_total": valor_total,
        "producto_mas_caro": {
            "nombre": producto_mas_caro['nombre'],
            "precio": producto_mas_caro['precio']
        },
        "producto_mayor_stock": {
            "nombre": producto_mayor_stock['nombre'],
            "cantidad": producto_mayor_stock['cantidad']
        }
    }