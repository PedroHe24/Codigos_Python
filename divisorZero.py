try:
    num1 = int(input("Digite o numerador: "))
    num2 = int(input("Digite o denominador: "))
    result = num1 /num2
except ValueError:
    print("Entrada Inválida.")
except ZeroDivisionError:
    print("Não é possivel dividir por zero. ")

