def calcular_imc(peso, altura):
    return peso / (altura ** 2)

def calcular_percentual_gordura(imc, idade, sexo):
    # Sexo: 1 para homens e 0 para mulheres
    return 1.2 * imc + 0.23 * idade - 5.4 - (10.8 * sexo)

def avaliar_percentual_gordura(percentual_gordura, sexo):
    # Critérios genéricos para avaliação (esses valores são apenas exemplos)
    if sexo == 1:  # Masculino
        if percentual_gordura < 10:
            return "abaixo da média"
        elif 10 <= percentual_gordura <= 20:
            return "na média"
        else:
            return "acima da média"
    else:  # Feminino
        if percentual_gordura < 20:
            return "abaixo da média"
        elif 20 <= percentual_gordura <= 30:
            return "na média"
        else:
            return "acima da média"

def main():
    while True:
        try:
            peso = float(input("Digite seu peso (em kg): "))
            altura = float(input("Digite sua altura (em metros): "))
            idade = int(input("Digite sua idade: "))
            sexo = int(input("Digite seu sexo (1 para masculino, 0 para feminino): "))
            
            # Validação das entradas
            if peso <= 0 or altura <= 0 or idade <= 0:
                print("Peso, altura e idade devem ser valores positivos. Tente novamente.")
                continue
            
            if sexo not in [0, 1]:
                print("Sexo deve ser 0 (feminino) ou 1 (masculino). Tente novamente.")
                continue

            imc = calcular_imc(peso, altura)
            percentual_gordura = calcular_percentual_gordura(imc, idade, sexo)
            avaliacao = avaliar_percentual_gordura(percentual_gordura, sexo)
            
            print(f"Seu IMC é: {imc:.2f}")
            print(f"Seu percentual de gordura corporal estimado é: {percentual_gordura:.2f}%")
            print(f"Sua gordura corporal está {avaliacao}.")
            break
        
        except ValueError:
            print("Entrada inválida. Certifique-se de que você está digitando números válidos. Tente novamente.")

if __name__ == "__main__":
    main()
