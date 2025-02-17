a, b = 0, 1  # Inicializa as variáveis a = 0 e b = 1
while b < 10:  # Enquanto b for menor que 10
    print(b)  # Imprime o valor de b
    a, b = b, a + b  # Atualiza as variáveis: a recebe o valor de b, e b recebe a soma de a e b
