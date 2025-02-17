from classes import Conta
import datetime

class ContaEspecial(Conta):
    def __init__(self, clientes, numero, saldo, limite):
        super().__init__(clientes, numero, saldo)
        self.limite = limite  # Adiciona um limite especial à conta

    def sacar(self, valor):
        if (self.saldo + self.limite) < valor:
            print(f"Saldo insuficiente. Conta número {self.numero}, cliente {self.clientes[0].cpf}")
            return False
        else:
            self.saldo -= valor
            if self.saldo < 0:
                self.limite += self.saldo  # Atualiza o limite com o valor negativo do saldo
            self.extrato.transações.append(["SAQUE", valor, datetime.datetime.today()])
            return True
