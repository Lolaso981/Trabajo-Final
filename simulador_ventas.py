import tkinter as tk
from tkinter import ttk, messagebox

#Clase Producto
class Producto:
    def __init__(self, nombre, precio, cantidad):
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad
        self.ventas_realizadas = 0

    def actualizar_cantidad(self, cantidad_vendida):
        if cantidad_vendida > self.cantidad:
            raise ValueError("La cantidad que deseas es insuficiente en el inventario")
        self.cantidad -= cantidad_vendida
        self.ventas_realizadas += cantidad_vendida


#Clase Inventario
class Inventario:
    def __init__(self):
        self.productos = []

    def agregar_producto(self, producto):
        self.productos.append(producto)

    def editar_producto(self, indice, producto_actualizado):
        self.productos[indice] = producto_actualizado

    def eliminar_producto(self, indice):
        del self.productos[indice]

    def obtener_producto_mas_vendido(self):
        if not self.productos:
            return None
        return max(self.productos, key=lambda p: p.ventas_realizadas)


#Clase SimuladorVentas
class SimuladorVentas:
    def __init__(self):
        self.historial_ventas = []

    def registrar_venta(self, producto, cantidad):
        producto.actualizar_cantidad(cantidad)
        total = cantidad * producto.precio
        self.historial_ventas.append({"nombre": producto.nombre, "cantidad": cantidad, "total": total})

    def calcular_total_ventas(self):
        return sum(venta["total"] for venta in self.historial_ventas)


class Interfaz:
    def __init__(self, root):
        self.ventana = root
        self.ventana.title("Simulador de Ventas con Inventario")
        
        self.inventario = Inventario()
        self.simulador = SimuladorVentas()

        #Crear marcos para organizar la interfaz
        self.frame_inventario = tk.Frame(self.ventana, bd=2, relief=tk.SOLID, padx=10, pady=10)
        self.frame_inventario.pack(side=tk.TOP, fill=tk.BOTH, padx=10, pady=5)
        
        self.frame_botones = tk.Frame(self.ventana, bd=2, relief=tk.SOLID, padx=10, pady=10)
        self.frame_botones.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)

        #Inventario - Tabla y etiqueta
        tk.Label(self.frame_inventario, text="Inventario", font=("Arial", 14)).pack(anchor=tk.W, pady=5)
        self.tabla_inventario = ttk.Treeview(self.frame_inventario, columns=("Nombre", "Precio", "Cantidad"), show="headings", height=10)
        self.tabla_inventario.heading("Nombre", text="Nombre")
        self.tabla_inventario.heading("Precio", text="Precio")
        self.tabla_inventario.heading("Cantidad", text="Cantidad")
        self.tabla_inventario.column("Nombre", width=150)
        self.tabla_inventario.column("Precio", width=100, anchor=tk.CENTER)
        self.tabla_inventario.column("Cantidad", width=100, anchor=tk.CENTER)
        self.tabla_inventario.pack(fill=tk.BOTH, expand=True)

        #Botones
        tk.Button(self.frame_botones, text="Agregar Producto", command=self.manejar_agregar_producto, width=20).pack(side=tk.LEFT, padx=5)
        tk.Button(self.frame_botones, text="Eliminar Producto", command=self.manejar_eliminar_producto, width=20).pack(side=tk.LEFT, padx=5)
        tk.Button(self.frame_botones, text="Registrar Venta", command=self.manejar_registro_venta, width=20).pack(side=tk.LEFT, padx=5)
        tk.Button(self.frame_botones, text="Reporte de Ventas", command=self.mostrar_historial_ventas, width=20).pack(side=tk.LEFT, padx=5)

    def mostrar_inventario(self):
        for row in self.tabla_inventario.get_children():
            self.tabla_inventario.delete(row)
        for idx, producto in enumerate(self.inventario.productos):
            self.tabla_inventario.insert("", "end", iid=idx, values=(producto.nombre, producto.precio, producto.cantidad))

    def manejar_agregar_producto(self):
        def guardar_producto():
            nombre = entrada_nombre.get()
            precio = entrada_precio.get()
            cantidad = entrada_cantidad.get()
            
            if nombre and precio.isdigit() and cantidad.isdigit():
                nuevo_producto = Producto(nombre, int(precio), int(cantidad))
                self.inventario.agregar_producto(nuevo_producto)
                self.mostrar_inventario()
                ventana_agregar.destroy()
            else:
                messagebox.showerror("Error", "Por favor, ingresa los datos correctos.")

        ventana_agregar = tk.Toplevel(self.ventana)
        ventana_agregar.title("Agregar Producto")
        
        tk.Label(ventana_agregar, text="Nombre:").pack()
        entrada_nombre = tk.Entry(ventana_agregar)
        entrada_nombre.pack()
        
        tk.Label(ventana_agregar, text="Precio:").pack()
        entrada_precio = tk.Entry(ventana_agregar)
        entrada_precio.pack()
        
        tk.Label(ventana_agregar, text="Cantidad:").pack()
        entrada_cantidad = tk.Entry(ventana_agregar)
        entrada_cantidad.pack()
        
        tk.Button(ventana_agregar, text="Guardar", command=guardar_producto).pack()

    def manejar_eliminar_producto(self):
        selected_item = self.tabla_inventario.selection()
        if selected_item:
            idx = int(selected_item[0])
            self.inventario.eliminar_producto(idx)
            self.mostrar_inventario()
        else:
            messagebox.showwarning("Advertencia", "Por favor, escoge un producto para poder eliminarlo.")

    def manejar_registro_venta(self):
        def guardar_venta():
            producto_idx = combo_productos.current()
            cantidad = entrada_cantidad_venta.get()
            
            if producto_idx >= 0 and cantidad.isdigit():
                try:
                    cantidad = int(cantidad)
                    producto = self.inventario.productos[producto_idx]
                    self.simulador.registrar_venta(producto, cantidad)
                    self.mostrar_inventario()
                    ventana_venta.destroy()
                except ValueError as e:
                    messagebox.showerror("Error", str(e))
            else:
                messagebox.showerror("Error", "Por favor, ingresa los datos adecuados.")
        
        ventana_venta = tk.Toplevel(self.ventana)
        ventana_venta.title("Registrar Venta")
        
        tk.Label(ventana_venta, text="Producto:").pack()
        combo_productos = ttk.Combobox(ventana_venta, values=[p.nombre for p in self.inventario.productos])
        combo_productos.pack()
        
        tk.Label(ventana_venta, text="Cantidad:").pack()
        entrada_cantidad_venta = tk.Entry(ventana_venta)
        entrada_cantidad_venta.pack()
        
        tk.Button(ventana_venta, text="Guardar", command=guardar_venta).pack()

    def mostrar_historial_ventas(self):
        total_ventas = self.simulador.calcular_total_ventas()
        productos_vendidos = {}
        for venta in self.simulador.historial_ventas:
            if venta["nombre"] in productos_vendidos:
                productos_vendidos[venta["nombre"]] += venta["cantidad"]
            else:
                productos_vendidos[venta["nombre"]] = venta["cantidad"]
        
        mas_vendidos = sorted(productos_vendidos.items(), key=lambda x: x[1], reverse=True)
        
        reporte_texto = f"Total de ventas: ${total_ventas}\n\nProductos más vendidos:\n"
        for producto, cantidad in mas_vendidos:
            reporte_texto += f"- {producto}: {cantidad} unidades\n"
        
        messagebox.showinfo("Reporte de Ventas", reporte_texto)

# Iniciar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = Interfaz(root)
    root.mainloop()