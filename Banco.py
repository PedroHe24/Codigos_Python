class Banco:
    def __init__(self, codigo, nome):
        self.codigo = codigo  # Código do banco
        self.nome = nome  # Nome do banco
        self.contas = []  # Lista de contas vinculadas ao banco

    def adiciona_conta(self, conta):
        # Adiciona uma conta à lista de contas do banco
        self.contas.append(conta)

    def calcular_rendimento_mensal(self):
        # Calcula o rendimento de todas as contas no banco
        for conta in self.contas:
            rendimento = conta.calcular_rendimento()
            print(f"Conta {conta.numero}: Rendimento do mês = {rendimento:.2f}")

    def imprime_saldo_contas(self):
        # Imprime o saldo de todas as contas no banco
        print(f"Banco {self.nome} - Código {self.codigo}")
        for conta in self.contas:
            print(conta)
