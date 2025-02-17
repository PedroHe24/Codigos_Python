
from classes.Conta import Conta
from classes.Poupanca import Poupanca
pass


class ContaRemuneradaPoupanca(Conta, Poupanca):

    def __init__(self, clientes, numero, saldo, taxa_remuneracao):
        # Inicializando a classe Conta
        Conta.__init__(self, clientes, numero, saldo)
        # Inicializando a classe Poupanca
        Poupanca.__init__(self, taxa_remuneracao)

    def remuneraConta(self):
        # Calcula a remuneração da conta
        self.saldo += self.saldo * (self.taxa_remuneracao / 30)
