def defineIdade(nome ,idade):
    if not isinstance (idade, int): # Verifica se a idade é um número inteiro
        raise ValueError("A idade precisa ser um número inteiro.")
    
    # Dicionário para armazenar o nome e idade
    dicionario_idades = {}
    dicionario_idades[nome] = idade

    return dicionario_idades