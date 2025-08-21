import tkinter as tk
from  tkinter import messagebox
import random

class SodokuGame:
    #Inicicializando la ventana principal
    def __init__(self,master):
        self.master = master
        master.title("Sodoku")
        master.geometry("600x700")

    #definir la cantidad de espacios vacios para regular el nivel de dificultad

        self.boards = {
            "Basico": 40,
            "Intermedio": 50,
            "Avanzado": 60
        }

    #Definir los estados de cada uno de los tableros

        self.original_board = None
        self.current_board = None
        self.solution_board = None

        self.errors = 0
        self.max_errors = 4
        self.selected_cell = (None,None) #Celda que seleccionamos a la hora de jugar

        self.level_frame = tk.Frame(master)
        self.level_frame.pack(pady=10)

        tk.Button(self.level_frame, text="Basico", command= lambda:self.start_game("Basico"),width=10, height=2).pack(side=tk.LEFT, padx=5)
        tk.Button(self.level_frame, text="Intermedio", command= lambda:self.start_game("Intermedio"),width=10, height=2).pack(side=tk.LEFT, padx=5)
        tk.Button(self.level_frame, text="Avanzado", command= lambda:self.start_game("Avanzado"),width=10, height=2).pack(side=tk.LEFT, padx=5)

        #Etiqueta para mostrar los errores

        self.error_label = tk.Label(master, text=f'{self.errors}/{self.max_errors}', font=("Arial,14"))
        self.error_label.pack(pady=10)

        # Marco principal para el tablero de SODOKU
        self.sodoku_frame = tk.Frame(master, bd=5, relief="ridge")
        self.sodoku_frame.pack(padx=20,pady=20)

        self.cells = {}  #Se crea un diccionario para almacenar cada una de las entradas de TKINTER

        # Crear una cuadricula de 9 x 9

        for r in range(9):
            for c in range(9):
                entry = tk.Entry(self.sodoku_frame, width=3, font=('Arial',24),justify="center",relief="solid",bd=1)

                entry.grid(row=r, column=c, ipadx=5, ipady=5)

                #Haciendo un marco para las subcuadriculasd de 3 x 3 
                if( r + 1) % 3 == 0 and r !=8:
                    entry.grid(pady=(0,5))
                if (c + 1) % 3 == 0 and c != 8:
                    entry.grid(padx=(0,5))
                self.cells[(r,c)] = entry

                # Vincalacion del evento con el click de cada celda
                entry.bind("<Button-1>",lambda event, r=r,c=c: self.on_cell_click(r,c))

        #Frame para los botones de juego
        self.control_frame = tk.Frame(master)
        self.control_frame.pack(pady=10)

        #Botones para ingresar numero y borrar
        self.number_buttons = []
        for i in range(1,10):
            button = tk.Button(self.control_frame, text=str(i), width=4,height=2, command=lambda num=i: self.enter_number(num))
            button.pack(side=tk.LEFT,padx=2)
            self.number_buttons.append(button)

        self.clear_button = tk.Button(self.control_frame, text="Borrar",width=6, height=2, command=self.clear_cell)
        self.clear_button.pack(pady=10)

        self.restart_button = tk.Button(master, text="Jugar de nuevo", command=self.reset_game, state=tk.DISABLED, width=15, height=2)
        self.restart_button.pack(pady=10)


    def start_game(self, level):

        self.errors = 0
        self.error_label.config(text=f'Errores: {self.errors}/{self.max_errors}')

        #Generar un nuevo tablero de SODOKU segun el nivel seleccionado

        self.generate_sodoku_puzzle(self.boards[level])

        self.populate_board()
        self.restart_button.config(state=tk.NORMAL)
        self.enable_input_buttons()

    def populate_board(self):
        # Rellena el tablero segun el nivbel de juego


        for r in range(9):
            for c in range(9):
                value = self.current_board[r][c]
                entry = self.cells[(r,c)]
                entry.config(state=tk.NORMAL)
                entry.delete(0, tk.END)
                if value != 0:
                    entry.insert(0, str(value))
                    entry.config(state='readonly',fg='blue')
                else:
                    entry.config(fg='black')
                entry.config(bg='white')



