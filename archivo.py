import csv

def guardar_csv(inventario, ruta, incluir_header=True):
    if not inventario:
        print("❌ Error: El inventario está vacío. No hay nada que guardar.")
        return False
    
    try:
        with open(ruta, 'w', newline='', encoding='utf-8') as archivo_csv:
            escritor = csv.writer(archivo_csv)
            
            if incluir_header:
                escritor.writerow(['nombre', 'precio', 'cantidad'])
            
            for producto in inventario:
                escritor.writerow([
                    producto['nombre'],
                    producto['precio'],
                    producto['cantidad']
                ])
        
        print(f"✅ Inventario guardado exitosamente en: {ruta}")
        print(f"   Total de productos guardados: {len(inventario)}")
        return True
    
    except PermissionError:
        print(f"❌ Error: No tiene permisos para escribir en '{ruta}'.")
        print("   Intente con otra ubicación o verifique los permisos.")
        return False
    
    except OSError as e:
        print(f"❌ Error al escribir el archivo: {e}")
        print("   Verifique que la ruta sea válida y tenga espacio disponible.")
        return False
    
    except Exception as e:
        print(f"❌ Error inesperado al guardar: {e}")
        return False

def cargar_csv(ruta, inventario_actual):
    productos_cargados = []
    filas_invalidas = 0
    
    try:
        with open(ruta, 'r', encoding='utf-8') as archivo_csv:
            lector = csv.reader(archivo_csv)
            lineas = list(lector)
    
    except FileNotFoundError:
        print(f"❌ Error: El archivo '{ruta}' no existe.")
        print("   Verifique la ruta e intente nuevamente.")
        return inventario_actual
    
    except UnicodeDecodeError:
        print("❌ Error: El archivo tiene caracteres ilegibles.")
        print("   Asegúrese de que esté codificado en UTF-8.")
        return inventario_actual
    
    except Exception as e:
        print(f"❌ Error inesperado al leer el archivo: {e}")
        return inventario_actual
    
    if not lineas:
        print("❌ Error: El archivo CSV está vacío.")
        return inventario_actual
    
    encabezado = [columna.strip().lower() for columna in lineas[0]]
    
    if encabezado != ['nombre', 'precio', 'cantidad']:
        print("❌ Error: Encabezado inválido.")
        print("   El encabezado debe ser exactamente: nombre,precio,cantidad")
        print(f"   Encabezado encontrado: {','.join(lineas[0])}")
        return inventario_actual
    
    for numero_fila, fila in enumerate(lineas[1:], start=2):
        if len(fila) != 3:
            filas_invalidas += 1
            continue
        
        nombre = fila[0].strip()
        
        if not nombre:
            filas_invalidas += 1
            continue
        
        try:
            precio = float(fila[1].strip())
            if precio < 0:
                filas_invalidas += 1
                continue
        except ValueError:
            filas_invalidas += 1
            continue
        
        try:
            cantidad = int(fila[2].strip())
            if cantidad < 0:
                filas_invalidas += 1
                continue
        except ValueError:
            filas_invalidas += 1
            continue
        
        productos_cargados.append({
            'nombre': nombre,
            'precio': precio,
            'cantidad': cantidad
        })
    
    if not productos_cargados:
        print("❌ Error: No se cargaron productos válidos del archivo.")
        print(f"   Total de filas inválidas: {filas_invalidas}")
        return inventario_actual
    
    print(f"\n✅ Se cargaron {len(productos_cargados)} productos válidos del archivo.")
    
    if inventario_actual:
        print(f"⚠️  El inventario actual tiene {len(inventario_actual)} productos.")
        print("\n¿Qué desea hacer?")
        print("  S - Sobrescribir (reemplazar completamente el inventario actual)")
        print("  F - Fusionar (combinar ambos inventarios)")
        
        while True:
            opcion = input("Seleccione una opción (S/F): ").strip().upper()
            if opcion in ['S', 'F']:
                break
            print("❌ Opción inválida. Ingrese S o F.")
    else:
        opcion = 'S'
    
    if opcion == 'S':
        inventario_final = productos_cargados
        accion = "Inventario sobrescrito completamente"
    
    else:
        print("\n📋 Política de fusión:")
        print("   - Si el producto ya existe: se SUMA la cantidad y se ACTUALIZA el precio")
        print("   - Si el producto es nuevo: se agrega al inventario")
        
        mapa_productos = {p['nombre'].lower(): p for p in inventario_actual}
        productos_nuevos = 0
        productos_actualizados = 0
        
        for producto_nuevo in productos_cargados:
            nombre_lower = producto_nuevo['nombre'].lower()
            
            if nombre_lower in mapa_productos:
                mapa_productos[nombre_lower]['cantidad'] += producto_nuevo['cantidad']
                mapa_productos[nombre_lower]['precio'] = producto_nuevo['precio']
                productos_actualizados += 1
            else:
                inventario_actual.append(producto_nuevo)
                productos_nuevos += 1
        
        inventario_final = inventario_actual
        accion = f"Inventario fusionado ({productos_nuevos} nuevos, {productos_actualizados} actualizados)"
    
    print("\n" + "="*60)
    print("           RESUMEN DE CARGA DE CSV")
    print("="*60)
    print(f"Productos válidos cargados:  {len(productos_cargados)}")
    print(f"Filas inválidas omitidas:    {filas_invalidas}")
    print(f"Acción realizada:            {accion}")
    print(f"Total productos en inventario: {len(inventario_final)}")
    print("="*60)
    
    return inventario_final