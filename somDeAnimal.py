# Classe base Animal
class Animal:
    def __init__(self, nome):
        self.nome = nome

    def som(self):
        raise NotImplementedError("Subclasses devem implementar o método 'som'.")

# Classe Vaca que herda de Animal
class Vaca(Animal):
    def som(self):
        return f"A {self.nome} faz muu."

# Classe Cachorro que herda de Animal
class Cachorro(Animal):
    def som(self):
        return f"O {self.nome} faz au au."

# Classe Gato que herda de Animal
class Gato(Animal):
    def som(self):
        return f"O {self.nome} faz miau."

# Testando as classes
vaca = Vaca("Vaca")
cachorro = Cachorro("Cachorro")
gato = Gato("Gato")

# Exibindo os sons
print(vaca.som())       # A Vaca faz muu.
print(cachorro.som())   # O Cachorro faz au au.
print(gato.som())       # O Gato faz miau.
