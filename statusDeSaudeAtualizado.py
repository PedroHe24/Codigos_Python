import math

class Pessoa:
    def __init__(self, nome, peso, altura, idade, sexo):
        self.nome = nome
        self.peso = peso  # em KG
        self.altura = altura  # em metros
        self.idade = idade
        self.sexo = sexo  # 'M' para masculino, 'F' para feminino
        self.bf = self.calcular_bf()  # Percentual de gordura corporal automático
        self.consumo_agua = self.calcular_agua_diaria()
        self.testosterona = self.calcular_testosterona()

    def calcular_imc(self):
        """Calcula o Índice de Massa Corporal (IMC)."""
        return round(self.peso / (self.altura ** 2), 2)

    def calcular_bf(self):
        """Calcula automaticamente o percentual de gordura corporal baseado no sexo e idade."""
        imc = self.calcular_imc()
        if self.sexo == 'M':
            bf = 1.20 * imc + 0.23 * self.idade - 16.2  # Fórmula para homens
        else:
            bf = 1.20 * imc + 0.23 * self.idade - 5.4  # Fórmula para mulheres
        return round(bf, 2)

    def calcular_gordura(self):
        """Calcula a quantidade de gordura corporal em KG."""
        return round((self.bf / 100) * self.peso, 2)

    def calcular_agua_diaria(self):
        """Calcula a quantidade de água recomendada por dia (35 mL por Kg de peso)."""
        return round(self.peso * 0.035, 2)  # em litros
    
    def calcular_testosterona(self):
        """Calcula o nível estimado de testosterona."""
        fator_idade = max(0.5, (1 - (self.idade - 20) * 0.01))

        if self.calcular_imc() < 18.5:
            fator_imc = 0.8
        elif self.calcular_imc() > 24.9:
            fator_imc = 0.7
        else:
            fator_imc = 1

        if self.bf < 8:
            fator_gordura = 0.9
        elif self.bf > 25:
            fator_gordura = 0.7
        else:
            fator_gordura = 1

        if self.consumo_agua < 2:
            fator_agua = 0.8
        elif self.consumo_agua > 3.5:
            fator_agua = 1.1
        else:
            fator_agua = 1

        testosterona_base = 700 if self.sexo == 'M' else 50  # Mulheres têm níveis muito menores
        testosterona_estimada = testosterona_base * fator_idade * fator_imc * fator_gordura * fator_agua

        return round(testosterona_estimada, 2)
    
    def avaliar_nivel_testosterona(self):
        """Classifica o nível estimado de testosterona."""
        nivel = self.testosterona
        if self.sexo == 'M':
            if nivel < 300:
                return f"{nivel} ng/dL (Baixo)"
            elif 300 <= nivel <= 1000:
                return f"{nivel} ng/dL (Normal)"
            else:
                return f"{nivel} ng/dL (Alto, consulte um médico)"
        else:
            if nivel < 15:
                return f"{nivel} ng/dL (Baixo)"
            elif 15 <= nivel <= 70:
                return f"{nivel} ng/dL (Normal)"
            else:
                return f"{nivel} ng/dL (Alto, consulte um médico)"

    def exibir_resultados(self):
        """Exibe os resultados calculados."""
        gordura_kg = self.calcular_gordura()
        print(f"\nNome: {self.nome}")
        print(f"IMC: {self.calcular_imc()}")
        print(f"Percentual de Gordura Corporal: {self.bf}% ({gordura_kg} KG)")
        print(f"Ingestão de água recomendada: {self.consumo_agua} Litros/dia")
        print(f"Nível estimado de Testosterona: {self.avaliar_nivel_testosterona()}")

def avaliar_percentual_gordura(percentual_gordura, sexo):
    """Classifica o percentual de gordura corporal."""
    if sexo == 'M':  # Masculino
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
            nome = input("Nome: ")
            peso = float(input("Peso (Kg): "))
            altura = float(input("Altura (m): "))
            idade = int(input("Idade: "))
            sexo = input("Sexo (M/F): ").strip().upper()

            if sexo not in ['M', 'F']:
                print("Sexo inválido! Digite M para masculino ou F para feminino.")
                continue

            # Criar objeto Pessoa
            pessoa = Pessoa(nome, peso, altura, idade, sexo)
            pessoa.exibir_resultados()
            classificacao = avaliar_percentual_gordura(pessoa.bf, sexo)
            print(f"Classificação da gordura corporal: {classificacao}\n")
            break
        except ValueError:
            print("Entrada inválida. Certifique-se de inserir números válidos.")

if __name__ == "__main__":
    main()
