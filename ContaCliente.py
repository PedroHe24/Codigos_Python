class ContaCliente:
    def __init__(self, numero, IDF, IR, valor_investido, taxa_rendimento):
        self.numero = numero  # Número da conta
        self.IDF = IDF  # Imposto sobre o rendimento
        self.IR = IR  # Imposto de Renda sobre o rendimento
        self.valor_investido = valor_investido  # Valor inicial investido
        self.taxa_rendimento = taxa_rendimento  # Taxa de rendimento mensal
        self.saldo = valor_investido  # Saldo da conta (inicia como valor investido)

    def calcular_rendimento(self):
        # Cálculo do rendimento bruto
        rendimento_bruto = self.valor_investido * self.taxa_rendimento
        # Aplicação dos impostos
        impostos = rendimento_bruto * (self.IDF + self.IR)
        rendimento_liquido = rendimento_bruto - impostos
        # Atualiza o saldo com o rendimento líquido
        self.saldo += rendimento_liquido
        return rendimento_liquido

    def __str__(self):
        return f"Conta {self.numero}: Saldo = {self.saldo:.2f}, Valor Investido = {self.valor_investido:.2f}"
