def taximetro(distancia, multiplicador=1):
    largada = 3
    km_rodado = 2
    valor = (largada + distancia * km_rodado) 
    return valor

pagamento = taximetro (3.5, 2)
print (pagamento)