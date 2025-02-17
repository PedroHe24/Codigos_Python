# Função recursiva
def regressiva(x):
    print(x)
    if x > 0:
        regressiva(x - 1)
    else:
        print('acabou')

# Chamar a função recursiva
regressiva(10)

# Loop não recursivo
for y in range(10, -1, -1):
    print(y)
print('acabou')
