import tkinter as tk

def atualizar_coordenadas(event):
    x = event.x
    y = event.y
    label_coordenadas["text"] = f"Coordenadas do mouse (botão direito): x={x}, y={y}"

# Criando a Janela
janela = tk.Tk()
janela.title("Tratamento de Eventos - Coordenadas do Mouse")

# Criando o widget de rótulo
label_coordenadas = tk.Label(janela, text="Clique com o botão direito para ver as coordenadas")
label_coordenadas.pack(padx=200, pady=100)

# Ligando o evento de clique com o botão direito à função
janela.bind("<Button-3>", atualizar_coordenadas)

# Rodando o loop principal
janela.mainloop()
