import unicodedata

class AvaliadorSaudeMental:
    def __init__(self):
        self.questoes_depressao = [
            ("Você tem sentido pouco interesse ou prazer nas coisas?", 0),
            ("Você tem se sentido para baixo, desanimado ou sem esperança?", 0),
            ("Tem tido dificuldades para dormir ou dormido excessivamente?", 0),
            ("Tem sentido cansaço ou falta de energia?", 0),
            ("Tem percebido alterações no apetite (comendo demais ou de menos)?", 0),
            ("Tem se sentido mal consigo mesmo ou como se tivesse decepcionado alguém?", 0),
            ("Tem dificuldade para se concentrar?", 0),
            ("Percebe que está se movimentando mais devagar ou mais agitado do que o normal?", 0),
            ("Já pensou em se machucar ou que preferia não estar vivo?", 0)
        ]

        self.questoes_ansiedade = [
            ("Você sente preocupação excessiva com várias coisas?", 0),
            ("Tem dificuldade em controlar as preocupações?", 0),
            ("Sente-se frequentemente nervoso ou assustado?", 0),
            ("Tem dificuldade para relaxar?", 0),
            ("Tem se irritado com facilidade ou se sentido impaciente?", 0),
            ("Sente que algo ruim pode acontecer sem motivo claro?", 0)
        ]

        self.total_depressao = 0
        self.total_ansiedade = 0

        self.respostas_validas = {
            "nada": 0,
            "um pouco": 1,
            "moderadamente": 2,
            "muito": 3,
            "extremamente": 3,
        }

    def normalizar_texto(self, texto):
        texto = texto.strip().lower()
        texto = unicodedata.normalize("NFD", texto)
        return ''.join([c for c in texto if unicodedata.category(c) != 'Mn'])

    def obter_resposta(self, pergunta):
        while True:
            print(f"{pergunta}\nComo você avaliaria a intensidade ou quantidade disso nos últimos dias?")
            print("Responda com: nada | um pouco | moderadamente | muito | extremamente")
            resposta = input("> ")
            resposta_normalizada = self.normalizar_texto(resposta)
            if resposta_normalizada in self.respostas_validas:
                return self.respostas_validas[resposta_normalizada]
            else:
                print("Resposta inválida. Tente usar uma das opções sugeridas.")

    def aplicar_questionario(self):
        print("=== Avaliação de Saúde Mental ===\n")
        print("--- Sintomas de Depressão ---")
        for i, (pergunta, _) in enumerate(self.questoes_depressao):
            resposta_valor = self.obter_resposta(f"{i+1}. {pergunta}")
            self.questoes_depressao[i] = (pergunta, resposta_valor)
            self.total_depressao += resposta_valor

        print("\n--- Sintomas de Ansiedade ---")
        for i, (pergunta, _) in enumerate(self.questoes_ansiedade):
            resposta_valor = self.obter_resposta(f"{i+1}. {pergunta}")
            self.questoes_ansiedade[i] = (pergunta, resposta_valor)
            self.total_ansiedade += resposta_valor

    def interpretar_resultado(self):
        print("\n=== Resultado ===")

        print(f"Pontuação Total - Depressão: {self.total_depressao}")
        if self.total_depressao <= 4:
            print("Sintomas de Depressão: Mínimos")
        elif self.total_depressao <= 9:
            print("Sintomas de Depressão: Leves")
        elif self.total_depressao <= 14:
            print("Sintomas de Depressão: Moderados")
        elif self.total_depressao <= 19:
            print("Sintomas de Depressão: Moderadamente graves")
        else:
            print("Sintomas de Depressão: Graves")

        print(f"\nPontuação Total - Ansiedade: {self.total_ansiedade}")
        if self.total_ansiedade <= 4:
            print("Sintomas de Ansiedade: Mínimos")
        elif self.total_ansiedade <= 8:
            print("Sintomas de Ansiedade: Leves")
        elif self.total_ansiedade <= 12:
            print("Sintomas de Ansiedade: Moderados")
        else:
            print("Sintomas de Ansiedade: Graves")

        print("\n--- Recomendações sem uso de medicamentos ---")
        print("- Exercite-se regularmente")
        print("- Tenha uma boa higiene do sono")
        print("- Pratique meditação, oração ou respiração consciente")
        print("- Converse com amigos ou participe de grupos de apoio")
        print("- Reduza estímulos digitais e conecte-se com a natureza")
        print("- Escreva diariamente sentimentos e gratidão")

        if self.total_depressao >= 15 or self.total_ansiedade >= 13:
            print("\n⚠️ Recomendação importante: Busque apoio profissional com psicólogo ou terapeuta.")

def main():
    avaliador = AvaliadorSaudeMental()
    avaliador.aplicar_questionario()
    avaliador.interpretar_resultado()

if __name__ == "__main__":
    main()
