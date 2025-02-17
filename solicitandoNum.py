# Solicita ao usuário que insira um número inteiro
numero_inteiro = input("Digite um número inteiro: ")

# Solicita ao usuário que insira um número de ponto flutuante
numero_ponto_flutuante = input("Digite um número de ponto flutuante: ")

# Solicita ao usuário que insira um valor booleano
valor_booleano = input("Digite um valor booleano (True ou False): ")

# Converte os valores para os tipos corretos
numero_inteiro = int(numero_inteiro)
numero_ponto_flutuante = float(numero_ponto_flutuante)
valor_booleano = valor_booleano == 'True'

# Exibe os valores convertidos ao usuário de forma formatada
print("\nValores convertidos:")
print(f"- Número inteiro: {numero_inteiro} (tipo: {type(numero_inteiro).__name__})")
print(f"- Número de ponto flutuante: {numero_ponto_flutuante} (tipo: {type(numero_ponto_flutuante).__name__})")
print(f"- Valor booleano: {valor_booleano} (tipo: {type(valor_booleano).__name__})")
