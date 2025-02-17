# Solicita os valores do usuário
numero_inteiro = input("Digite um número inteiro: ")
numero_flutuante = input("Digite um número de ponto flutuante: ")
valor_booleano = input("Digite um valor booleano (True ou False): ")

# Converte os valores para os tipos corretos
numero_inteiro_convertido = int(numero_inteiro)
numero_flutuante_convertido = float(numero_flutuante)
valor_booleano_convertido = valor_booleano.lower() == 'true'

# Exibe os valores convertidos e seus tipos
print("\nValores convertidos:")
print(f"- Número inteiro: {numero_inteiro_convertido} (tipo: {type(numero_inteiro_convertido).__name__})")
print(f"- Número de ponto flutuante: {numero_flutuante_convertido} (tipo: {type(numero_flutuante_convertido).__name__})")
print(f"- Valor booleano: {valor_booleano_convertido} (tipo: {type(valor_booleano_convertido).__name__})")
