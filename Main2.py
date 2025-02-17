from classes.ContaCliente import ContaCliente
from classes.Banco import Banco 
pass

# Instância do banco
banco1 = Banco(codigo=999, nome="Teste")

# Instância de uma conta cliente
conta_cliente1 = ContaCliente(
    numero=1, 
    IDF=0.01, 
    IR=0.1, 
    valor_investido=2000, 
    taxa_rendimento=0.05
)

# Adicionar a conta ao banco
banco1.adiciona_conta(conta_cliente1)

# Calcular rendimento mensal e imprimir saldo
banco1.calcular_rendimento_mensal()
banco1.imprime_saldo_contas()
