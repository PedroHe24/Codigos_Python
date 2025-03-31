class Pessoa:
    def __init__(self, nome, peso, altura, idade, sexo, objetivo, nivel):
        self.nome = nome
        self.peso = peso
        self.altura = altura
        self.idade = idade
        self.sexo = sexo.upper()
        self.objetivo = objetivo.lower()
        self.nivel = nivel.lower()
        
        self.imc = self.calcular_imc()
        self.bf = self.calcular_bf()
        self.peso_gordura = self.calcular_gordura()
        self.ficha_treino = self.definir_ficha_treino()
    
    def calcular_imc(self):
        return round(self.peso / (self.altura ** 2), 2) if self.altura > 0 else 0

    def calcular_bf(self):
        if self.sexo == 'M':
            bf = 1.20 * self.imc + 0.23 * self.idade - 16.2
        else:
            bf = 1.20 * self.imc + 0.23 * self.idade - 5.4
        return round(max(bf, 3), 2)

    def calcular_gordura(self):
        return round((self.bf / 100) * self.peso, 2)
    
    def definir_ficha_treino(self):
        treinos = {
            "hipertrofia": {
                "iniciante": "Treino Full Body 3x/semana com foco em técnica e progressão de carga.",
                "intermediario": "Treino ABC com divisão entre membros superiores e inferiores, 4-5x/semana.",
                "avancado": "Treino ABCD com intensidade alta e variações de carga, 5-6x/semana."
            },
            "emagrecimento": {
                "iniciante": "Circuito funcional 3x/semana + caminhada leve.",
                "intermediario": "Treino HIIT 4x/semana + musculação moderada.",
                "avancado": "HIIT + musculação 5-6x/semana com maior volume de treino."
            },
            "manutencao": {
                "iniciante": "Musculação leve 3x/semana + cardio moderado.",
                "intermediario": "Treino ABC 4x/semana + atividades aeróbicas.",
                "avancado": "Treino ABCD 5x/semana equilibrando força e resistência."
            }
        }
        return treinos.get(self.objetivo, {}).get(self.nivel, "Plano de treino não definido.")


def gerar_ficha(dados):
    pessoa = Pessoa(**dados)
    return {
        "Nome": pessoa.nome,
        "IMC": pessoa.imc,
        "Gordura Corporal (%)": pessoa.bf,
        "Peso de Gordura (kg)": pessoa.peso_gordura,
        "Ficha de Treino": pessoa.ficha_treino
    }


def main():
    print("=== Ficha de Treino Personalizada ===")
    nome = input("Nome: ")
    peso = float(input("Peso (kg): "))
    altura = float(input("Altura (m): "))
    idade = int(input("Idade: "))
    sexo = input("Sexo (M/F): ")
    objetivo = input("Objetivo (hipertrofia/emagrecimento/manutencao): ")
    nivel = input("Nível (iniciante/intermediario/avancado): ")
    
    dados_usuario = {
        "nome": nome,
        "peso": peso,
        "altura": altura,
        "idade": idade,
        "sexo": sexo,
        "objetivo": objetivo,
        "nivel": nivel
    }
    
    resultado = gerar_ficha(dados_usuario)
    
    print("\n=== Resultados ===")
    for chave, valor in resultado.items():
        print(f"{chave}: {valor}")


if __name__ == "__main__":
    main()
