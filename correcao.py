def minha_funcao(msg):
    print(msg)
 
if True:
    print("Condição verdadeira")
 
n = 0

# Evitar a divisão por zero
if n != 0:
    resultado = 10 / n
    minha_funcao(resultado)
else:
    print("Divisão por zero não permitida.")
