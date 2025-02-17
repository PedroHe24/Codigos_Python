# Dicionário para armazenar nome e idade
idades = {}

# Função para definir a idade
def defineIdade(nome, idade):
    # Verifica se a idade é um número inteiro
    if isinstance(idade, int):
        idades[nome] = idade
        print(f"Idade de {nome} foi definida como {idade}.")
    else:
        print("Erro: A idade deve ser um número inteiro.")

# Exemplo de uso
defineIdade("Carlos", 24)  # Corretamente insere
defineIdade("Maria", "vinte")  # Gera erro
