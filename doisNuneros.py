import tkinter as tk
from tkinter import messagebox

def comparar_numeros():
    try:
        # Obtém os valores dos campos de entrada e converte para float
        num1 = float(entry_num1.get())
        num2 = float(entry_num2.get())
        
        # Compara os números e exibe o resultado em uma caixa de mensagem
        if num1 > num2:
            resultado = "O primeiro número é maior que o segundo."
        elif num1 < num2:
            resultado = "O primeiro número é menor que o segundo."
        else:
            resultado = "O primeiro número é igual ao segundo."
        
        # Mostra o resultado na caixa de mensagem
        messagebox.showinfo("Resultado da Comparação", resultado)
    except ValueError:
        # Exibe uma mensagem de erro se a conversão falhar
        messagebox.showerror("Erro", "Por favor, insira números válidos.")

# Cria a janela principal
root = tk.Tk()
root.title("Comparador de Números")

# Configura o layout da interface gráfica
tk.Label(root, text="Digite o primeiro número:").pack(pady=5)
entry_num1 = tk.Entry(root)
entry_num1.pack(pady=5)

tk.Label(root, text="Digite o segundo número:").pack(pady=5)
entry_num2 = tk.Entry(root)
entry_num2.pack(pady=5)

btn_comparar = tk.Button(root, text="Comparar", command=comparar_numeros)
btn_comparar.pack(pady=10)

# Inicia o loop principal da interface gráfica
root.mainloop()
