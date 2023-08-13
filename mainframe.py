from tkinter import TOP, PhotoImage, ttk
from ttkthemes import ThemedTk
from CRUD_articulos import crud_articulos
from CRUD_clientes import crud_clientes
from CRUD_ventas import ventas

class programa(ThemedTk):
    def __init__(self):
        super().__init__(theme='equilux', themebg=True)

        self.wm_title('Facturacion textil')
        self.iconbitmap(default='.media\\favicon.ico')
        self.configure(width=1280, height=720)

        self.cargar_frames()
        self.cargar_imagenes()
        self.cargar_botones()

        self.cargar_widgets()
        
    def cargar_frames(self):
        self.fr_principal = ttk.Frame(self)
        self.fr_principal.place(
            relx=0.5, rely=0.5,
            width=480, height=160,
            anchor='center')

    def cargar_imagenes(self):
        self.img_salir = PhotoImage(file='.media\\salir_b.png')
        self.img_ventas = PhotoImage(file='.media\\venta_b.png')
        self.img_clientes = PhotoImage(file='.media\\cliente_b.png')
        self.img_articulos = PhotoImage(file='.media\\articulo_b.png')
        self.img_darkmode = PhotoImage(file='.media\\oscuro_b.png')
        
    def cargar_botones(self):
        self.boton_dark = ttk.Button(
            self,
            text='Dark mode',
            image=self.img_darkmode,
            padding=0,
            compound=TOP,
            command=self.switch_darkmode)
        self.boton_dark.place(relx=0.99, rely=0.11, anchor='se')

        self.salir = ttk.Button(
            self,
            text='Salir',
            image=self.img_salir,
            compound=TOP,
            command=self.destroy)
        self.salir.place(relx=0.01, rely=0.5, anchor='w')
        
        self.boton_1 = ttk.Button(
            self.fr_principal,
            text='Ventas',
            image=self.img_ventas,
            compound=TOP,
            command=self.ventas)
        
        self.boton_2 = ttk.Button(
            self.fr_principal,
            text='Clientes',
            image=self.img_clientes,
            compound=TOP,
            command=self.clientes)
        
        self.boton_3 = ttk.Button(
            self.fr_principal,
            text='Articulos',
            image=self.img_articulos,
            compound=TOP,
            command=self.articulos)
        
        self.boton_1.place(relwidth=0.33, relheight=1, relx=0)
        self.boton_2.place(relwidth=0.33, relheight=1, relx=0.33)
        self.boton_3.place(relwidth=0.33, relheight=1, relx=0.66)

    def ventas(self):
        fr_secundario = ventas(self)

    def clientes(self):
        fr_secundario = crud_clientes(self)

    def articulos(self):
        fr_secundario = crud_articulos(self)

    def switch_darkmode(self):
        if self.current_theme == 'equilux':
            self.set_theme('adapta')

        else:
            self.set_theme('equilux')
