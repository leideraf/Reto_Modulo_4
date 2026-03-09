import customtkinter as ctk
from tkinter import ttk
from controllers.horario_controller import HorarioController
from mysql.connector import IntegrityError

class MenuHorarioFull:
    def __init__(self, db=None, tema_actual="System"):
        self.db = db
        self.tema_actual = tema_actual
        self.root = ctk.CTk()
        self.root.title("Menu Horario")
        self.root.attributes("-fullscreen", True)  # <- pantalla completa
        self.horario_controller = HorarioController(db)

        # Configurar el tema de la ventana
        ctk.set_appearance_mode(tema_actual)

        # Configuracion de cierra de ventana
        self.root.protocol("WM_DELETE_WINDOW", self.regresar_menu_principal)

        ancho_pantalla = self.root.winfo_screenwidth()
        alto_pantalla = self.root.winfo_screenheight()

        # Asignar tamaño de la ventana
        self.root.geometry(f"{ancho_pantalla}x{alto_pantalla}")
        self.root.state("zoomed")

        # Titulo de la ventana
        self.titulo = ctk.CTkLabel(self.root, text="Menu Horario", font=("Arial", 16))
        self.titulo.pack(pady=20)

        # Crear un frame principal para la tabla y los botones
        self.frame_principal = ctk.CTkFrame(self.root)
        self.frame_principal.pack(pady=20, padx=40, fill="both", expand=True)

        # Crear un frame para la tabla
        self.frame_tabla = ctk.CTkFrame(self.frame_principal)
        self.frame_tabla.pack(side="left", fill="both", expand=True, padx=(0, 20))

        # Crear la tabla (usando Treeview de tkinter)
        self.tabla = ttk.Treeview(self.frame_tabla, columns=("ID", "Dia", "Hora_Inicio", "Hora_Fin", "Curso_ID", "Curso_Nombre"), show="headings")
        self.tabla.pack(expand=True, fill="both", padx=20)

        # Configurar encabezados
        self.tabla.heading("ID", text="ID Horario")
        self.tabla.heading("Dia", text="Día")
        self.tabla.heading("Hora_Inicio", text="Hora Inicio")
        self.tabla.heading("Hora_Fin", text="Hora Fin")
        self.tabla.heading("Curso_ID", text="ID Curso")
        self.tabla.heading("Curso_Nombre", text="Curso")

        # Ajustar el ancho de las columnas
        self.tabla.column("ID", width=100)
        self.tabla.column("Dia", width=120)
        self.tabla.column("Hora_Inicio", width=120)
        self.tabla.column("Hora_Fin", width=120)
        self.tabla.column("Curso_ID", width=100)
        self.tabla.column("Curso_Nombre", width=200)

        # Crear un frame para los botones verticales
        self.frame_botones = ctk.CTkFrame(self.frame_principal, width=250)
        self.frame_botones.pack(side="right", fill="y", padx=(0, 20))
        self.frame_botones.pack_propagate(False)

        # Botón para registrar horario
        self.btn_registrar = ctk.CTkButton(self.frame_botones, text="Registrar Horario", command=self.registrar_horario, width=200)
        self.btn_registrar.pack(pady=10, padx=10, fill="x")

        # Botón para actualizar horario
        self.btn_actualizar = ctk.CTkButton(self.frame_botones, text="Actualizar Horario", command=self.actualizar_horario, width=200)
        self.btn_actualizar.pack(pady=10, padx=10, fill="x")

        # Botón para eliminar horario
        self.btn_eliminar = ctk.CTkButton(self.frame_botones, text="Eliminar Horario", command=self.eliminar_horario, width=200)
        self.btn_eliminar.pack(pady=10, padx=10, fill="x")

        # Botón para cambiar tema
        self.btn_tema = ctk.CTkButton(self.frame_botones, text="Cambiar Tema", command=self.cambiar_tema, width=200)
        self.btn_tema.pack(pady=10, padx=10, fill="x")

        # Cargar los datos de la tabla
        self.cargar_datos_tabla()

        # Agregar espacio vertical
        self.espacio_vertical = ctk.CTkLabel(self.root, text="")
        self.espacio_vertical.pack(pady=20)

        # Crear un frame para el botón de regresar
        self.frame_boton = ctk.CTkFrame(self.root)
        self.frame_boton.pack(pady=10, padx=40, fill="x")

        # Botón para regresar al menú principal
        self.btn_regresar = ctk.CTkButton(self.frame_boton, text="Regresar", command=self.regresar_menu_principal)
        self.btn_regresar.pack(side="left", padx=10)

    def cargar_datos_tabla(self):
        try:
            horarios = self.horario_controller.listar_horarios()
            # Limpiar la tabla antes de cargar nuevos datos
            for row in self.tabla.get_children():
                self.tabla.delete(row)

            for horario in horarios:
                # Insertar filas en la tabla
                self.tabla.insert("", "end", values=(
                    horario.id_horario,
                    horario.dia_semana,
                    horario.hora_inicio,
                    horario.hora_fin,
                    horario.curso_id,
                    horario.curso_nombre
                ))

        except IntegrityError as e:
            print(f"Error al cargar los datos: {e}")

    def registrar_horario(self):
        from view.viewTkinter.viewHorario.registrarHorario import RegistrarHorario
        self.root.destroy()
        registrar_horario = RegistrarHorario(db=self.db, tema_actual=self.tema_actual)
        registrar_horario.root.mainloop()

    def actualizar_horario(self):
        from view.viewTkinter.viewHorario.actualizarHorario import ActualizarHorario
        self.root.destroy()
        actualizar_horario = ActualizarHorario(db=self.db, tema_actual=self.tema_actual)
        actualizar_horario.root.mainloop()

    def eliminar_horario(self):
        from view.viewTkinter.viewHorario.eliminarHorario import EliminarHorario
        self.root.destroy()
        eliminar_horario = EliminarHorario(db=self.db, tema_actual=self.tema_actual)
        eliminar_horario.root.mainloop()

    def cambiar_tema(self):
        if self.tema_actual == "Light":
            ctk.set_appearance_mode("Dark")
            self.tema_actual = "Dark"
        else:
            ctk.set_appearance_mode("Light")
            self.tema_actual = "Light"

    def regresar_menu_principal(self):
        from view.viewTkinter.menuPrincipal import MenuPrincipal
        self.root.destroy()
        menu_principal = MenuPrincipal(db=self.db, tema_actual=self.tema_actual)
        menu_principal.root.mainloop()
