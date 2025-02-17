def taximetro(distancia):
    def calculaMulti(distancia):
        if distancia < 5:
            return 1.2
        else:
            return 1.0
    
    # Valores fixos
    largada = 3  # Custo inicial
    km_rodado = 2  # Custo por Km

    multiplicador = calculaMulti(distancia)
    valor = (largada + distancia * km_rodado) * multiplicador
    return valor

def main():
    try:
        dist = float(input("Entre com a distância a ser percorrida em Km: "))
        if dist < 0:
            print("A distância não pode ser negativa.")
            return
        
        pagamento = taximetro(dist)
        print(f'O valor a pagar é R$ {pagamento:.2f}')
    
    except ValueError:
        print("Por favor, insira um número válido.")

if __name__ == "__main__":
    main()
