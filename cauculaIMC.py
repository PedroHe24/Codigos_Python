def calcula_imc (peso, altura):
    return peso * 100 / (altura * 2)

peso = eval (input('digite o peso em quilos'))
altura = eval (input('digite a altura em centimetros'))
calcula_imc(peso, altura)
imc = calcula_imc(peso, altura)
print ('imc = ', imc)
