class Pessoa:
    def __init__(self, nome, peso, altura, idade, sexo, objetivo):
        self.nome = nome
        self.peso = peso
        self.altura = altura
        self.idade = idade
        self.sexo = sexo.upper()
        self.objetivo = objetivo.lower()
        
        self.bf = self.calcular_bf()
        self.consumo_agua = self.calcular_agua_diaria()
        self.testosterona = self.calcular_testosterona()
        self.calorias = self.calcular_calorias()
        self.sono_recomendado = self.calcular_sono()
        self.dieta = self.definir_dieta()
        self.tempo_estimado = self.calcular_tempo_objetivo()
        self.resultado_final = self.definir_resultado()
        self.peso_ideal = self.calcular_peso_ideal()

    def calcular_imc(self):
        return round(self.peso / (self.altura ** 2), 2) if self.altura > 0 else 0

    def calcular_bf(self):
        imc = self.calcular_imc()
        if self.sexo == 'M':
            bf = 1.20 * imc + 0.23 * self.idade - 16.2
        else:
            bf = 1.20 * imc + 0.23 * self.idade - 5.4
        return round(max(bf, 3), 2)

    def calcular_gordura(self):
        return round((self.bf / 100) * self.peso, 2)

    def calcular_agua_diaria(self):
        return round(self.peso * 0.035, 2)

    def calcular_testosterona(self):
        fator_idade = max(0.5, (1 - (self.idade - 20) * 0.01))
        fator_imc = 0.8 if self.calcular_imc() < 18.5 else 0.7 if self.calcular_imc() > 24.9 else 1
        fator_gordura = 0.9 if self.bf < 8 else 0.7 if self.bf > 25 else 1
        fator_agua = 0.8 if self.consumo_agua < 2 else 1.1 if self.consumo_agua > 3.5 else 1
        testosterona_base = 700 if self.sexo == 'M' else 50
        return round(testosterona_base * fator_idade * fator_imc * fator_gordura * fator_agua, 2)

    def calcular_calorias(self):
        if self.altura == 0:
            return 0
        tmb = 10 * self.peso + 6.25 * (self.altura * 100) - 5 * self.idade
        tmb += 5 if self.sexo == 'M' else -161
        fator_atividade = {'hipertrofia': 1.6, 'emagrecimento': 1.2, 'manutencao': 1.4}
        return round(tmb * fator_atividade.get(self.objetivo, 1.4))

    def calcular_sono(self):
        return 7 if self.idade > 30 else 8 if self.idade > 18 else 9
    
    def definir_dieta(self):
        dietas = {
            'hipertrofia': "Alta ingestão de proteínas (frango, ovos, peixe), carboidratos complexos (arroz integral, batata doce) e gorduras saudáveis (abacate, azeite).",
            'emagrecimento': "Déficit calórico com proteínas magras, vegetais, grãos integrais e redução de açúcares e gorduras saturadas.",
            'manutencao': "Alimentação equilibrada com proteínas, carboidratos e gorduras saudáveis para manter o peso."
        }
        return dietas.get(self.objetivo, "Dieta balanceada baseada nas necessidades diárias.")
    
    def calcular_tempo_objetivo(self):
        if self.objetivo == 'hipertrofia':
            return "Aproximadamente 6 a 12 meses para ganhos visíveis de massa muscular."
        elif self.objetivo == 'emagrecimento':
            return "Cerca de 3 a 6 meses para uma perda saudável de peso."
        else:
            return "O tempo depende da consistência nos hábitos alimentares e treino."
    
    def definir_resultado(self):
        if self.objetivo == 'hipertrofia':
            return "Aumento de massa muscular e força com definição corporal."
        elif self.objetivo == 'emagrecimento':
            return "Redução de gordura corporal e melhora do condicionamento físico."
        else:
            return "Manutenção do peso e composição corporal equilibrada."
    
    def calcular_peso_ideal(self):
        if self.objetivo == 'hipertrofia':
            return round(24 * (self.altura ** 2), 2)
        elif self.objetivo == 'emagrecimento':
            return round(21 * (self.altura ** 2), 2)
        else:
            return self.peso


def calcular(dados):
    pessoa = Pessoa(**dados)
    return {
        "Nome": pessoa.nome,
        "IMC": pessoa.calcular_imc(),
        "Gordura Corporal (%)": pessoa.bf,
        "Peso de Gordura (kg)": pessoa.calcular_gordura(),
        "Água Diária (L)": pessoa.consumo_agua,
        "Testosterona (ng/dL)": pessoa.testosterona,
        "Calorias Recomendadas": pessoa.calorias,
        "Sono Recomendado": f"{pessoa.sono_recomendado} horas/dia",
        "Dieta Sugerida": pessoa.dieta,
        "Tempo Estimado": pessoa.tempo_estimado,
        "Resultado Esperado": pessoa.resultado_final,
        "Peso Ideal": pessoa.peso_ideal
    }


def main():
    print("=== Calculadora de Saúde ===")
    nome = input("Nome: ")
    peso = float(input("Peso (kg): "))
    altura = float(input("Altura (m): "))
    idade = int(input("Idade: "))
    sexo = input("Sexo (M/F): ")
    objetivo = input("Objetivo (hipertrofia/emagrecimento/manutencao): ")
    
    dados_usuario = {
        "nome": nome,
        "peso": peso,
        "altura": altura,
        "idade": idade,
        "sexo": sexo,
        "objetivo": objetivo
    }
    
    resultado = calcular(dados_usuario)
    
    print("\n=== Resultados ===")
    for chave, valor in resultado.items():
        print(f"{chave}: {valor}")


if __name__ == "__main__":
    main()
