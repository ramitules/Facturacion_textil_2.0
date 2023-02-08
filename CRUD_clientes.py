import os
import pickle
from tkinter import END, messagebox, ttk
from CRUD import interfaz_crud
from funciones import cargar, volver
from Clientes import cli

class crud_clientes(interfaz_crud):
    def __init__(self, master=None):
        super().__init__(master)

        self.binarios = cargar('clientes')
        self.clientes = []

        for x in self.binarios:
            self.clientes.append([x.ID, x.nombre])

        self.cargar_widgets()

    def cargar_widgets(self):
        self.tabla = ttk.Treeview(self.fr_lista,
                                  columns=('id', 'nombre'),
                                  show='headings')

        self.tabla.column('id', anchor='center', width=40)
        self.tabla.column('nombre', anchor='center', width=500)

        self.tabla.heading('id', text='ID')
        self.tabla.heading('nombre', text='Nombre')

        for cliente in self.clientes:
            self.tabla.insert('', END, values=cliente)

        self.tabla.place(x=0, y=0, relwidth=1, relheight=1)

    def f_crear(self):
        self.f_cancelar()
        super().f_crear()

        self.l_nombre = ttk.Label(self.fr_atributos, text='Nombre')
        self.ent_nombre = ttk.Entry(self.fr_atributos)

        self.l_nombre.place(x=10, y=20)
        self.ent_nombre.place(x=10, y=40)

        self.ent_nombre.focus()

    def f_aceptar_crear(self):
        nuevo_cliente = cli(id=int(1),
                            nombre=self.ent_nombre.get())

        if self.ent_nombre.get() == '':
            return messagebox.showwarning('Error',
                                            f'El nombre es obligatorio')

        if len(self.clientes) != 0:
            for elemento in self.clientes:
                if elemento[1] == self.ent_nombre.get():
                    return messagebox.showwarning('Error',
                                                  f'El cliente "{elemento[1]}" ya existe.')
                nuevo_cliente.ID = elemento[0] + 1

        self.crear_directorios(self.ent_nombre.get())

        with open('clientes.pkl', 'ab') as f:
            pickle.dump(nuevo_cliente, f)

        self.binarios.append(nuevo_cliente)
        self.clientes.append([nuevo_cliente.ID, nuevo_cliente.nombre])

        self.f_cancelar()

        return messagebox.showinfo('Exito',
                                   'El cliente se ha creado con exito')

    def f_modificar(self):
        self.f_cancelar()

        try:
            item = self.tabla.selection()[0]
            valores = self.tabla.item(item, option='values')
        except IndexError:
            return messagebox.showwarning('Error', 'Debe seleccionar un elemento')

        self.f_crear()

        self.ent_nombre.insert(0, valores[1])

        self.boton_aceptar.configure(command=lambda: self.f_aceptar_modificar(valores))

    def f_aceptar_modificar(self, valores):
        for cliente in self.clientes:
            if cliente[1] == self.ent_nombre.get():
                return messagebox.showwarning('Error',
                                              f'El cliente "{cliente[1]}" ya existe.')

        if self.ent_nombre.get() == '':
            return messagebox.showwarning('Error',
                                          'El nombre es obligatorio')

        for cliente in self.binarios:
            if int(valores[0]) == cliente.ID:
                cliente.nombre = self.ent_nombre.get()

        with open('clientes.pkl', 'wb') as f:
            for cliente in self.binarios:
                pickle.dump(cliente, f)

        return messagebox.showinfo('Exito',
                                   'El cliente se ha modificado con exito')

    def f_eliminar(self):
        self.f_cancelar()

        try:
            item = self.tabla.selection()[0]
            valores = self.tabla.item(item, option='values')
        except IndexError:
            return messagebox.showwarning('Error', 'Debe seleccionar un elemento')

        if messagebox.askyesno('Eliminar',
                               'Seguro que desea eliminar el cliente seleccionado?'):
            for i, cliente in enumerate(self.binarios):
                if cliente.ID == int(valores[0]):
                    self.binarios.pop(i)
                    self.clientes.pop(i)

            self.tabla.delete(item)

            with open('clientes.pkl', 'wb') as f:
                for cliente in self.binarios:
                    pickle.dump(cliente, f)

            return messagebox.showinfo('Exito',
                                       'El cliente se ha eliminado con exito')

        else: return

    def crear_directorios(self, nombre):
        os.chdir('..')
        os.chdir('Optitex')

        try: 
            os.mkdir(f'{nombre}')
            os.mkdir(f'{nombre}\\Vista previa')
            os.mkdir(f'{nombre}\\Molderias')
            os.mkdir(f'{nombre}\\Tizadas')
            messagebox.showinfo('Nuevos directorios',
                                f'Se han creado las carpetas "Vista previa", "Molderias" y "Tizadas" para el nuevo cliente {nombre}')

        except FileExistsError: 
            messagebox.showinfo('Existente',
                                f'El cliente {nombre} ya tenia carpetas existentes. No se han creado nuevas carpetas')

        volver()
