import customtkinter as ctk
from view.viewTkinter.viewEstudiante.menuEstudiante import MenuEstudiante
from view.viewTkinter.viewDocenteFull.menuDocenteFull import MenuDocenteFull

#Crear la clase principal de la ventana la cual se encargar de recibir a las demas ventanas
class MenuPrincipal:
    def __init__(self, db=None, tema_actual="System"):
        self.db = db
        self.root = ctk.CTk()
        self.root.title("Menu Principal")

        #Configurar el tema de la ventana
        ctk.set_appearance_mode(tema_actual)

        # Obtener el ancho y alto de la pantalla
        ancho_pantalla = self.root.winfo_screenwidth()
        alto_pantalla = self.root.winfo_screenheight()

        # Asignar tamaño de la ventana
        ancho_ventana = int(ancho_pantalla * 0.2)
        alto_ventana = int(alto_pantalla * 0.45)
        self.root.geometry(f"{ancho_ventana}x{alto_ventana}")

        #Configuraracion de restricciones de la ventana
        self.root.resizable(False, False)

        # Coordenadas centradas
        x = (ancho_pantalla // 2) - (ancho_ventana // 2)
        y = (alto_pantalla // 2) - (alto_ventana // 2)

        # Establecer geometría con posición centrada
        self.root.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")

        #Crear el titulo de la ventana
        self.titulo = ctk.CTkLabel(self.root, text="Menu Principal", font=("Arial", 16))
        self.titulo.pack(pady=10)

        #Crear 5 botones para acceder a las ventras de los menus
        botones = [
            ("Estudiantes", self.abrir_ventana_estudiantes),
            ("Docentes", self.abrir_ventana_docentes),
            ("Cursos", self.abrir_ventana_cursos),
            ("Horarios", self.abrir_ventana_horarios),
            ("Matriculas", self.abrir_ventana_matriculas)
        ]

        for i, (texto, comando) in enumerate(botones):
            btn = ctk.CTkButton(self.root, text=texto, command=comando)
            btn.pack(pady=10)

        #Botont para cambiar el tema de la ventana
        self.tema_actual = "System"
        self.btn_cambiar_tema = ctk.CTkButton(self.root, text="Cambiar Tema", command=self.cambiar_tema)
        self.btn_cambiar_tema.pack(pady=10)

    def abrir_ventana_estudiantes(self):
        self.root.destroy()
        menu_estudiante = MenuEstudiante(db = self.db, tema_actual = self.tema_actual)
        menu_estudiante.root.mainloop()


    def abrir_ventana_docentes(self):
        self.root.destroy()
        menu_docente = MenuDocenteFull(db = self.db, tema_actual = self.tema_actual)
        menu_docente.root.mainloop()

    def abrir_ventana_cursos(self):
        pass

    def abrir_ventana_horarios(self):
        pass

    def abrir_ventana_matriculas(self):
        pass

    def cambiar_tema(self):
        if self.tema_actual == "Light":
            ctk.set_appearance_mode("Dark")
            self.tema_actual = "Dark"
        else:
            ctk.set_appearance_mode("Light")
            self.tema_actual = "Light"