def fibo(n):
    """Determina o n-ésimo termo da sequência de Fibonacci."""
    if n == 1 or n == 2:
        return 1
    else:
        return fibo(n-1) + fibo(n-2)

# Calcula o 6º termo da sequência de Fibonacci
vfibo = fibo(8)
print(vfibo)

# Exibe a documentação da função
print(help(fibo))
