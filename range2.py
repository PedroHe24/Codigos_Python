for num in range(1000, 10000):
    menor = num % 100  # obtém os algarismos menos significativos
    maior = num // 100  # obtém os algarismos mais significativos
    raiz = menor + maior  # obtém a raiz

    if (raiz * raiz) == num:  # valida se a raiz gera o número testado
        print(num)
        print(menor)
        print(maior)
        print(raiz)
        
print('terminou')
print('saiu', num)
97
