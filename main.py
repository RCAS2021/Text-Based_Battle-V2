# Personagem
# Herói: Controlado pelo usuario
# Inimigo: Adversario do usuario
import json
import os

class Personagem:
    def __init__(self, nome, vida, nivel):
        self.__nome = nome
        self.__vida = vida
        self.__nivel = nivel

    def get_nome(self):
        return self.__nome

    def get_vida(self):
        return self.__vida

    def get_nivel(self):
        return self.__nivel

    def exibir_detalhes(self):
        return f"Nome: {self.get_nome()}\nVida: {self.get_vida()}\nNível: {self.get_nivel()}"
    
    def to_dict(self):
        return {
            'nome': self.__nome,
            'vida': self.__vida,
            'nivel': self.__nivel
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(data['nome'], data['vida'], data['nivel'])
    
    def atacar(self, alvo):
        dano = self.__nivel * 100
        print(f"{self.__nome} atacou {alvo.get_nome()} e causou {dano} de dano")
        alvo.receber_dano(dano)

    def receber_dano(self, dano):
        self.__vida -= dano

        if self.__vida <= 0:
            self.__vida = 0

class Heroi(Personagem):
    def __init__(self, nome, vida, nivel, item, habilidade):
        super().__init__(nome, vida, nivel)
        self.__item = item
        self.__habilidade = habilidade

    def get_item(self):
        return self.__item

    def get_habilidade(self):
        return self.__habilidade

    def exibir_detalhes(self):
        return f"{super().exibir_detalhes()}\nHabilidade: {self.get_habilidade()}\nItem: {self.get_item()}\n"

    def to_dict(self):
        data = super().to_dict()
        data.update({
            'item': self.__item,
            'habilidade': self.__habilidade
        })
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(data['nome'], data['vida'], data['nivel'], data['item'], data['habilidade'])

class Inimigo(Personagem):
    def __init__(self, nome, vida, nivel, tipo):
        super().__init__(nome, vida, nivel)
        self.__tipo = tipo

    def get_tipo(self):
        return self.__tipo 

    def exibir_detalhes(self):
        return f"{super().exibir_detalhes()}\nTipo: {self.get_tipo()}"

    def to_dict(self):
        data = super().to_dict()
        data.update({
            'tipo': self.__tipo
        })
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(data['nome'], data['vida'], data['nivel'], data['tipo'])

class Jogo:
    """ Classe orquestradora do jogo """
    def __init__(self, filename='save.json'):
        self.heroi = None
        self.inimigo = None
        self.filename = filename
        self.carregar_jogo()

    def criar_heroi(self, nome, vida, nivel, item, habilidade):
        self.heroi = Heroi(nome, vida, nivel, item, habilidade)

    def criar_inimigo(self, nome, vida, nivel, tipo):
        self.inimigo = Inimigo(nome, vida, nivel, tipo)

    def exibir_status(self):
        if self.heroi:
            print("Herói:")
            print(self.heroi.exibir_detalhes())
        if self.inimigo:
            print("Inimigo:")
            print(self.inimigo.exibir_detalhes())

    def salvar_jogo(self, filename):
        jogo_estado = {
            "heroi": self.heroi.to_dict() if self.heroi else None,
            "inimigo": self.inimigo.to_dict() if self.inimigo and self.inimigo.get_vida() > 0 else None
        }

        with open(filename, 'w') as f:
            json.dump(jogo_estado, f, indent=4)
        filename, _ = os.path.splitext(filename)
        print(f'Jogo salvo em {filename}')

    def carregar_jogo(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                jogo_estado = json.load(f)
            if jogo_estado['heroi']:
                self.heroi = Heroi.from_dict(jogo_estado['heroi'])
            else:
                # Criar um herói padrão se não existir no JSON
                print("Nenhum herói encontrado no arquivo. Criando um herói padrão.")
                self.criar_heroi("Herói Padrão", 100, 1, "Espada", "Corte")
            if jogo_estado['inimigo']:
                self.inimigo = Inimigo.from_dict(jogo_estado['inimigo'])
            else:
                self.criar_inimigo("Inimigo", 5, 1, "Água")
            print(f"Jogo carregado de {self.filename}")
        else:
            print(f"Arquivo {self.filename} não encontrado. Criando um novo jogo.")
            # Criar um herói padrão se o arquivo não existir
            self.criar_heroi("Herói Padrão", 100, 1, "Espada", "Corte")
            self.criar_inimigo("Inimigo", 5, 1, "Água")

    def iniciar_batalha(self):
        while self.heroi.get_vida() > 0 and self.inimigo.get_vida() > 0:
            print(self.exibir_status())

            escolha = input("1- Atacar\n2- Habilidade\n3- Item\n4- Sair\n")
            if escolha == '1':
                self.heroi.atacar(self.inimigo)
            if escolha == "4":
                self.salvar_jogo('save.json')
                exit()
            else:
                print("Escolha inválida")

        if self.heroi.get_vida() > 0:
            print("Inimigo derrotado. Salvando o jogo")
            self.salvar_jogo('save.json')

        if self.inimigo.get_vida() > 0:
            print("Derrota")

if __name__ == "__main__":
    jogo = Jogo()
    jogo.carregar_jogo()

    jogo.iniciar_batalha()
