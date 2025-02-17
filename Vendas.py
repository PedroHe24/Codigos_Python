class Vendedor():
    def __init__(self, nome):
        self.nome = nome
        self.vendas = 0

    def vendeu(self, vendas):
        self.vendas = vendas

    def bateu_meta(self, meta):
        if self.vendas >= meta:  # Se as vendas forem maiores ou iguais à meta
            print(self.nome, "Bateu a meta")
        else:
            print(self.nome, "não bateu a meta")

# Testando com dois vendedores
Vendedor1 = Vendedor("Pedro")
Vendedor1.vendeu(1050)
Vendedor1.bateu_meta(600)

Vendedor2 = Vendedor("Luiz")
Vendedor2.vendeu(1000)
Vendedor2.bateu_meta(600)
