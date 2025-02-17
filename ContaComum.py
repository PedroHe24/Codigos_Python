from classes.ContaCliente import ContaCliente
pass


class ContaComum (ContaCliente):

    def __init__(self, numero, IDF, IR, valor_investido, taxa_rendimento):
        super().__init__(numero, IDF, IR, valor_investido, taxa_rendimento)

def calcula_rendimento(self):
    remuneracao = self.valor_investido * self.taxa_rendimento
    valorIDF = remuneracao * self.IDF
    self.valor_investido += remuneracao - valorIDF   
      