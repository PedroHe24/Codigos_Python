from classes.Cliente import Cliente
from classes.Conta import Conta
from classes.ContaRemuneradaPooupanca import ContaRemuneradaPoupanca


# Criando clientes
cliente1 = Cliente(cpf = "123", nome = "João", endereco ="Rua X")
cliente2 = Cliente(cpf = "321", nome = "Maria", endereco ="Rua Y")
cliente3 = Cliente(cpf = "456", nome = "Zezinho", endereco ="Rua Z")

# Criando contas
conta1 = Conta(cliente=cliente1, numero =1, saldo=2000)
conta2 = Conta(cliente=cliente2, numero =2, saldo=2000)



# Operações bancárias
conta1.depositar(300)
conta1.transferir_valor(conta2, valor=500)
conta2.sacar(700)
conta3.depositar(800)

# Gerando extratos
conta1.extrato.gerar_extrato(conta1)
conta2.extrato.gerar_extrato(conta2)
conta3.extrato.gerar_extrato(conta3)
