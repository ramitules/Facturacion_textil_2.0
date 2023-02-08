import os
import openpyxl as excel
from tkinter import END, PhotoImage, Toplevel, messagebox, ttk
from funciones import cargar, volver
from CRUD import interfaz_crud
from variables_globales import fecha_actual

class ventas(interfaz_crud):
    def __init__(self, master=None):
        super().__init__(master)

        self.b_crear['text'] = "Facturar"
        self.b_modificar.destroy()
        self.b_eliminar.destroy()

        self.facturas = self.cargar_facturas()

        self.cargar_widgets()

    def cargar_facturas(self):
        lista = []

        os.chdir('..')

        try:
            os.chdir('Optitex\\Facturas')

        except FileNotFoundError:
            os.mkdir('Optitex\\Facturas')
            os.chdir('Optitex\\Facturas')

        facturas_dir = os.listdir()        

        if len(facturas_dir) > 0:
            for fac in facturas_dir:
                aux = excel.load_workbook(fac)
                hoja = aux.active

                lista.append([hoja['E1'].value,
                              hoja['B5'].value,
                              hoja['B4'].value,
                              hoja['E31'].value])
        else:
            lista.append([0, 0, 0, 0])

        volver()

        return lista

    def cargar_widgets(self):
        self.tabla = ttk.Treeview(self.fr_lista,
                                  show='headings',
                                  columns=('numero',
                                           'fecha',
                                           'cliente',
                                           'monto_total'))

        self.tabla.column('numero', anchor='center', width=30)
        self.tabla.column('fecha', anchor='center', width=100)
        self.tabla.column('cliente', anchor='center', width=100)
        self.tabla.column('monto_total', anchor='center', width=100)

        self.tabla.heading('numero', text='Numero factura')
        self.tabla.heading('fecha', text='Fecha')
        self.tabla.heading('cliente', text='Cliente')
        self.tabla.heading('monto_total', text='Monto total')

        for factura in self.facturas:
            self.tabla.insert('', END, values=factura)

        self.tabla.place(x=0, y=0, relwidth=1, relheight=1)

    def f_crear(self):
        self.f_cancelar()
        super().f_crear()

        def activar_boton(event):
            self.boton_aceptar['state'] = 'normal'

        self.boton_aceptar.config()
        self.boton_aceptar['state'] = 'disabled'

        self.clientes_bin = cargar('clientes')
        self.clientes = []

        self.articulos_bin = cargar('articulos')
        self.articulos = []

        for cliente in self.clientes_bin:
            self.clientes.append(cliente.nombre)

        for articulo in self.articulos_bin:
            self.articulos.append(articulo.descripcion)

        self.com_cliente = ttk.Combobox(self.fr_atributos,
                                        values=self.clientes,
                                        state='readonly')
        self.com_cliente.place(relx=0.5, rely=0.5, anchor='center')
        self.com_cliente.bind('<<ComboboxSelected>>', activar_boton)
    
    def f_aceptar_crear(self):
        self.tree_factura = ttk.Treeview(self, columns=('cantidad',
                                                        'descripcion',
                                                        'conteo',
                                                        'precio',
                                                        'total'))
        self.boton_crear_factura = ttk.Button(self.tree_factura,
                                              padding=0,
                                              state='disabled',
                                              text='Crear factura',
                                              command=self.crear_factura)
        self.boton_crear_factura.place(rely=0.9, x=0, height='30')

        self.tree_factura.column('#0', width=100)
        self.tree_factura.column('cantidad', anchor='center', width=100)
        self.tree_factura.column('descripcion', anchor='center', width=200)
        self.tree_factura.column('conteo', anchor='center', width=100)
        self.tree_factura.column('precio', anchor='center', width=100)
        self.tree_factura.column('total', anchor='center', width=100)

        self.tree_factura.heading('cantidad', text='Cantidad')
        self.tree_factura.heading('descripcion', text='Descripcion')
        self.tree_factura.heading('conteo', text='Conteo')
        self.tree_factura.heading('precio', text='Precio unitario')
        self.tree_factura.heading('total', text='Total')

        self.tree_factura.pack(fill='both', expand=True)

        for i in range(4):
            self.tree_factura.insert('', i, text=f'Fila {i+1}',
                                     values=('-','-','-','-','-'))

        self.contador = int(0)

        self.crear_combobox(self.tree_factura.get_children()[self.contador])

    def crear_combobox(self, item):
        self.combobox = ttk.Combobox(self.tree_factura,
                                     state='readonly',
                                     values=self.articulos)
        self.combobox.bind('<<ComboboxSelected>>',
                           lambda ev, i=item: self.crear_entry(i))
        self.combobox.place(rely=0.9, relx=0.35, relwidth=0.15, height='30')

    def crear_entry(self, item):
        self.entry = ttk.Entry(self.tree_factura)
        self.entry.insert(0, '0')
        self.entry.place(rely=0.9, relx=0.15, relwidth=0.14, height='30')

        self.img_boton = PhotoImage(file='.media\\anadir_b.png')
        self.boton = ttk.Button(self.tree_factura,
                                image=self.img_boton,
                                command=lambda i=item: self.setear(i),
                                padding=0)
        self.boton.place(rely=0.9, relx=0.1)

    def setear(self, item):
        i = self.articulos.index(self.combobox.get())
        self.tree_factura.set(item, 'cantidad', self.entry.get())
        self.tree_factura.set(item, 'descripcion', self.combobox.get())
        self.tree_factura.set(item, 'conteo', self.articulos_bin[i].conteo)
        self.tree_factura.set(item, 'precio', self.articulos_bin[i].precio_unitario)

        total = float(self.entry.get()) * float(self.articulos_bin[i].precio_unitario)
        self.tree_factura.set(item, 'total', total)

        self.combobox.destroy()
        self.entry.destroy()
        self.boton.destroy()

        self.boton_crear_factura['state'] = 'normal'

        self.contador += 1
        self.crear_combobox(self.tree_factura.get_children()[self.contador])
    
    def crear_factura(self):
        self.valores = {'num_factura': int(self.facturas[-1][0]),
                        'cliente': self.com_cliente.get(),
                        'fecha': fecha_actual}

        plantilla = excel.load_workbook('Plantilla.xlsx')
        self.nueva_factura = plantilla
        self.hoja = self.nueva_factura.active

        self.observaciones()

    def observaciones(self):
        if messagebox.askyesno('Observaciones', 
                               'Desea agregar alguna observacion?'):
            self.ventana = Toplevel(self)
            observacion = ttk.Entry(self.ventana, width=100)
            observacion.pack(side='left')
            observacion.focus_set()

            aceptar = ttk.Button(self.ventana, text='Aceptar',
                                 command=lambda: self.cargar_factura(observacion.get()))
            aceptar.pack(side='left')

        else:
            self.cargar_factura(o='')

    def cargar_factura(self, o):
        try:
            self.ventana.destroy()
        except:
            pass

        total = float(0)

        for i, item in enumerate(self.tree_factura.get_children(), 8):
            if self.tree_factura.set(item, 'cantidad') == '-':
                break

            self.hoja[f'A{i}'] = float(self.tree_factura.set(item, 'cantidad'))
            self.hoja[f'B{i}'] = self.tree_factura.set(item, 'descripcion')
            self.hoja[f'C{i}'] = self.tree_factura.set(item, 'conteo')
            self.hoja[f'D{i}'] = float(self.tree_factura.set(item, 'precio'))
            self.hoja[f'E{i}'] = float(self.tree_factura.set(item, 'total'))

            total += float(self.tree_factura.set(item, 'total'))
        
        self.hoja['E1'] = int(self.valores['num_factura']) + 1
        self.hoja['B4'] = self.valores['cliente']
        self.hoja['B5'] = self.valores['fecha']
        self.hoja['E31'] = total
        self.hoja['B26'] = o

        os.chdir('..')
        os.chdir('Optitex\\Facturas')
        self.nueva_factura.save(f'factura_{self.valores["num_factura"]}_{self.valores["cliente"]}.xlsx')

        if messagebox.askyesno('Exito', 'La factura se ha creado con exito, desea abrirla?'):
            os.startfile(f'factura_{self.valores["num_factura"]}_{self.valores["cliente"]}.xlsx')

        volver()

        self.destroy()
