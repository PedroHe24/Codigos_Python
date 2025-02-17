class Retangulo:
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura

    def calcular_area(self):
        return self.largura * self.altura

    def calcular_perimetro(self):
        return 2 * (self.largura + self.altura)

# Teste
retangulo = Retangulo(5, 10)
print(f"Área: {retangulo.calcular_area()}")
print(f"Perímetro: {retangulo.calcular_perimetro()}")
