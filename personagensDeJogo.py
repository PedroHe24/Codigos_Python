class Personagem:
    def __init__(self, nome, vida, ataque, defesa):
        self.nome = nome
        self.vida = vida
        self.ataque = ataque
        self.defesa = defesa
    
    def atacar(self, outro_personagem):
        dano = max(self.ataque - outro_personagem.defesa, 0)
        outro_personagem.vida -= dano
        print(f"{self.nome} atacou {outro_personagem.nome} causando {dano} de dano!")
    
    def exibir_status(self):
        print(f"{self.nome}: Vida = {self.vida}, Ataque = {self.ataque}, Defesa = {self.defesa}")

class Guerreiro(Personagem):
    def __init__(self, nome):
        super().__init__(nome, vida=120, ataque=15, defesa=10)
        self.defesa += 5  # Bônus de defesa

class Mago(Personagem):
    def __init__(self, nome):
        super().__init__(nome, vida=80, ataque=20, defesa=5)
    
    def lançar_magia(self, outro_personagem):
        dano_magia = self.ataque * 1.5
        outro_personagem.vida -= dano_magia
        print(f"{self.nome} lançou uma magia em {outro_personagem.nome} causando {dano_magia:.0f} de dano!")

# Criando os personagens
guerreiro = Guerreiro("Arthur")
mago = Mago("Merlin")

# Exibindo status antes da luta
guerreiro.exibir_status()
mago.exibir_status()

# Simulando combate
guerreiro.atacar(mago)
mago.lançar_magia(guerreiro)

# Exibindo status depois da luta
guerreiro.exibir_status()
mago.exibir_status()
