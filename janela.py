from tkinter import *

# Cria a janela principal
janelaPrincipal = Tk()

# Cria um rótulo (Label) com o texto "minha janela exibida"
texto = Label(master=janelaPrincipal, text="minha janela exibida")

# Posiciona o rótulo na janela principal
texto.place(x=50, y=100)

# Inicia o loop principal da interface gráfica
janelaPrincipal.mainloop()
