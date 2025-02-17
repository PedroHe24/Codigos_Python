# Classe Computador
# Marca, Memória RAM, Placa de vídeo
class Computador:
    def __init__(self, marca, memoria_ram, placa_de_video):
        self.marca = marca
        self.memoria_ram = memoria_ram
        self.placa_de_video = placa_de_video

    def ligar(self):
        print("Estou ligando")

    def desligar(self):
        print("Estou desligando")

    def exibir_informacoes_deste_computador(self):
        print(f"Marca: {self.marca}, Memoria RAM: {self.memoria_ram}, Placa de Vídeo: {self.placa_de_video}")


# Instanciando e utilizando a classe
computador1 = Computador("Acer", "4GB", "GeForce RTX")
computador1.ligar()
computador1.desligar()
computador1.exibir_informacoes_deste_computador()
