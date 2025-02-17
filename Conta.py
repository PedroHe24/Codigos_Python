import datetime

class Extrato:
    def __init__(self):
        self.transacoes = []

class Conta:
    def __init__(self, clientes, numero, saldo):
        self.clientes = clientes  # Lista de clientes ou objeto cliente
        self.numero = numero
        self.saldo = saldo
        self.data_abertura = datetime.datetime.today()
        self.extrato = Extrato()

    def depositar(self, valor):
        self.saldo += valor
        self.extrato.transacoes.append(["Depósito", valor, datetime.datetime.today()])

    def sacar(self, valor):
        if self.saldo < valor:
            print(f"Não existe saldo suficiente na conta {self.numero} do cliente {self.clientes}.")
            return False
        else:
            self.saldo -= valor
            self.extrato.transacoes.append(["Saque", valor, datetime.datetime.today()])
            return True

    def transfere_valor(self, conta_destino, valor):
        if self.saldo < valor:
            return "Não existe saldo suficiente!"
        else:
            self.sacar(valor)
            conta_destino.depositar(valor)
            self.extrato.transacoes.append(["Transferência", valor, datetime.datetime.today()])
            return "Transferência realizada!"

    def gerar_saldo(self):
        print(f"Conta: {self.numero}\nSaldo: R${self.saldo:10.2f}")
