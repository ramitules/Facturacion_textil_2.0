import pickle
from tkinter import END, messagebox, ttk
from CRUD import interfaz_crud
from funciones import cargar
from Articulos import art

class crud_articulos(interfaz_crud):
    def __init__(self, master=None):
        super().__init__(master)

        self.binarios = cargar('articulos')
        self.articulos = []

        for x in self.binarios:
            self.articulos.append([x.ID,
                                   x.descripcion,
                                   x.conteo,
                                   x.precio_unitario])

        self.cargar_widgets()

    def cargar_widgets(self):
        self.tabla = ttk.Treeview(self.fr_lista,
                                  columns=('id',
                                           'descripcion',
                                           'conteo',
                                           'p_u'),
                                  show='headings')

        self.tabla.column('id',
                          width=40,
                          anchor='center')
        self.tabla.column('descripcion',
                          width=350,
                          anchor='center')
        self.tabla.column('conteo',
                          width=85,
                          anchor='center')
        self.tabla.column('p_u',
                          width=85,
                          anchor='center')

        self.tabla.heading('id',
                           text='ID')
        self.tabla.heading('descripcion',
                           text='Descripcion')
        self.tabla.heading('conteo',
                           text='Conteo')
        self.tabla.heading('p_u',
                           text='Precio unitario')

        for articulo in self.articulos:
            self.tabla.insert('', END, values=articulo)

        self.tabla.place(x=0, y=0, relwidth=1, relheight=1)

    def f_crear(self):
        self.f_cancelar()
        super().f_crear()

        self.l_descripcion = ttk.Label(self.fr_atributos,
                                       text='Descripcion')
        self.l_conteo = ttk.Label(self.fr_atributos,
                                  text='Conteo')
        self.l_p_u = ttk.Label(self.fr_atributos,
                               text='Precio unitario')

        self.ent_descripcion = ttk.Entry(self.fr_atributos)
        self.ent_conteo = ttk.Entry(self.fr_atributos)
        self.ent_precio = ttk.Entry(self.fr_atributos,
                                    validate='key',
                                    validatecommand=(self.register(self.decimales), '%S'))

        self.l_descripcion.place(x=10, y=50)
        self.ent_descripcion.place(x=10, y=70)

        self.l_conteo.place(x=10, y=110)
        self.ent_conteo.place(x=10, y=130)
        
        self.l_p_u.place(x=10, y=170)
        self.ent_precio.place(x=10, y=190)

        self.ent_descripcion.focus()
        
    def f_aceptar_crear(self):
        nuevo_articulo = art(id=int(1),
                             descripcion=self.ent_descripcion.get(),
                             conteo=self.ent_conteo.get(),
                             precio_unitario=self.ent_precio.get())

        if self.ent_descripcion.get() == '':
            return messagebox.showwarning('Error',
                                            'La descripcion es obligatoria')

        if len(self.articulos) != 0:
            for elemento in self.articulos:
                if elemento[1] == self.ent_descripcion.get():
                    return messagebox.showwarning('Error',
                                                  f'El articulo "{elemento[1]}" ya existe.')
            
                nuevo_articulo.ID = elemento[0] + 1

        with open('articulos.pkl', 'ab') as f:
            pickle.dump(nuevo_articulo, f)

        self.binarios.append(nuevo_articulo)
        self.articulos.append([nuevo_articulo.ID,
                               nuevo_articulo.descripcion,
                               nuevo_articulo.conteo,
                               nuevo_articulo.precio_unitario])

        self.tabla.insert('', END, values=self.articulos[-1])

        self.f_cancelar()

        return messagebox.showinfo('Exito',
                                   'El articulo se ha creado con exito')

    def f_modificar(self):
        self.f_cancelar()

        try:
            item = self.tabla.selection()[0]
            valores = self.tabla.item(item, option='values')
        except IndexError:
            return messagebox.showwarning('Error',
                                          'Debe seleccionar un elemento')

        self.f_crear()

        self.ent_descripcion.insert(0, valores[1])
        self.ent_conteo.insert(0, valores[2])
        self.ent_precio.insert(0, valores[3])

        self.boton_aceptar.configure(command=lambda: self.f_aceptar_modificar(valores))

    def f_aceptar_modificar(self, valores):
        if self.ent_descripcion.get() == '':
            return messagebox.showwarning('Error',
                                          'La descripcion es obligatoria')

        for articulo in self.binarios:
            if int(valores[0]) == articulo.ID:
                articulo.descripcion = self.ent_descripcion.get()
                articulo.conteo = self.ent_conteo.get()
                articulo.precio_unitario = self.ent_precio.get()

        with open('articulos.pkl', 'wb') as f:
            for articulo in self.binarios:
                pickle.dump(articulo, f)

        return messagebox.showinfo('Exito',
                                   'El articulo se ha modificado con exito')

    def f_eliminar(self):
        self.f_cancelar()

        try:
            item = self.tabla.selection()[0]
            valores = self.tabla.item(item, option='values')
        except IndexError:
            return messagebox.showwarning('Error',
                                          'Debe seleccionar un elemento')

        if messagebox.askyesno('Eliminar',
                               'Seguro que desea eliminar el articulo seleccionado?'):
            for i, articulo in enumerate(self.binarios):
                if articulo.ID == int(valores[0]):
                    self.binarios.pop(i)
                    self.articulos.pop(i)

            self.tabla.delete(item)

            with open('articulos.pkl', 'wb') as f:
                for articulo in self.binarios:
                    pickle.dump(articulo, f)

            return messagebox.showinfo('Exito',
                                       'El articulo se ha eliminado con exito')

        else: return