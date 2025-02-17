import tkinter as tk

# Create the main window
janelaPrincipal = tk.Tk()
janelaPrincipal.title("Minha Aplicação Tkinter")

# Add a label widget
label = tk.Label(janelaPrincipal, text="Olá, Tkinter!")
label.pack()

# Run the application
janelaPrincipal.mainloop()
