import threading
import time
import random
import os

g = "Guanabara: "
vc = "Você: "
d = "Desconhecido"

def tela_reset():
    os.system("clear")

class Hero:
    def __init__(self,nome:str, hp:int, mana:int, nivel:int, c_critico:int):
        self.nome = nome
        self.hp = hp 
        self.mana = mana  
        self.nivel = nivel
        self.c_critico = c_critico
        
    
    def cria_jogador(self):
        print(f"{d}Olá, pequeno garfanhoto.")
        print(f"{d}Que bom que você acordou, estavamos preocupados")
        print(f"{d}Ops, acho que tem alguem me chamando, vai se virando ai, mais tarde venho falar com você")
        print(f"{vc}Hm?, como assim do que voce falando Espera quem e você ?")
        print(f"{d}Como assim quem sou eu?, você ta bricando comigo?")
        print(f"{d}Karalho so pode ser brincadeira, isso não pode ta acontecendo agora,")
        print(f"{vc}Voê não ta falando coisa com coisa, espera vc ta sangrando?")
        print(f"{g}Me chamdo Guanabara, cuidado por ai, vou deixar uns itens em cima da mesa, fica e espera a Leticia ela vai te ajudar.\nSe cuida !")
        input("Press Ent...")
        tela_reset()
        print(f"{vc}Espera !\nDroga não consigo ir atras dele, estou com muita dor.\n Oque sera que rolou afinal de contas?")
        int("Press Ent...")
        tela_reset()
        self.hp = 30
        self.mana = 50
        self.c_critico = 0
        self.nivel = 1
        self.nome = input("Qual sera seu nome ?")
        print(f"Seja bem vindo a KN city {self.nome}!!!")
        
    def exibir_atributos_hero(self):
        print("Atributos")
    
    def attack(self):
        return random.randint(5, 15)  # Dano de ataque (5-15)
    
    def magic(self):
        if self.mana >= 20:
            self.mana -= 20
            return random.randint(10, 20)  # Dano de magia (10-20)
        return 0  # Sem mana suficiente
    
    # def regenerate_mana(self):
    #     if self.mana < 50:
    #         self.mana = min(50, self.mana + 10)  # Regenera 10 de mana
    #         return True
    #     return False

# Classe para o Monstro
class Monster:
    def __init__(self):
        self.hp = 80  # Vida inicial
    
    def attack(self):
        return random.randint(5, 10)  # Dano de ataque (5-10)

# Classe para o Jogo
class Game:
    def __init__(self):
        self.hero = Hero()
        self.monster = Monster()
        self.game_over = False


            #SEMAFOROS
        self.hp_lock = threading.Semaphore(1) 
        self.turn_lock = threading.Semaphore(1)  
        self.hero_mana_lock = threading.Semaphore(1)
    
    # Thread para ataque do monstro
    def monster_attack(self):
        while self.hero.hp > 0 and self.monster.hp > 0 and not self.game_over:
            time.sleep(3)  # roda a dunção em 3segundos
            with self.turn_lock:# thread entra no bloco de código indentado e "tranca" o semáforo.
                if self.hero.hp > 0 and self.monster.hp > 0:
                    damage = self.monster.attack()
                    with self.hp_lock:
                        self.hero.hp = max(0, self.hero.hp - damage)
                    print(f"Monstro atacou! Causou {damage} de dano. Vida do herói: {self.hero.hp}")
                    if self.hero.hp <= 0:
                        self.game_over = True
                        print("Você foi derrotado!")
    

    # Thread para regeneracao de mana
    def mana_regeneration(self):
        while not self.game_over:
            time.sleep(5)
            if self.game_over: break

            with self.hero_mana_lock: #Usando o semáforo de mana
                if self.hero.regenerate_mana():
                    print(f"\n\n>> Mana regenerada! Mana atual: {self.hero.mana} <<\n")

    # Loop principal do jogo
    def run(self):
        # Inicia as threads
        monster_thread = threading.Thread(target=self.monster_attack)
        mana_thread = threading.Thread(target=self.mana_regeneration)
        monster_thread.start()
        mana_thread.start()
        
        # Loop do jogo
        while not self.game_over:
            print(f"\nSua vez! Vida: {self.hero.hp} Mana: {self.hero.mana} Vida do monstro: {self.monster.hp}")
            print("1 - Atacar (dano 5-15)")
            print("2 - Usar magia (custa 20 mana, dano 10-20)")
            action = input("Escolha (1 ou 2): ")
            
            with self.turn_lock:
                if action == "1":
                    damage = self.hero.attack()
                    self.monster.hp = max(0, self.monster.hp - damage)
                    print(f"Você atacou! Causou {damage} de dano. Vida do monstro: {self.monster.hp}")
                elif action == "2":
                    damage = self.hero.magic()
                    if damage > 0:
                        self.monster.hp = max(0, self.monster.hp - damage)
                        print(f"Você usou magia! Causou {damage} de dano. Vida do monstro: {self.monster.hp}")
                    else:
                        print("Mana insuficiente!")
                else:
                    print("Ação inválida!")
                
                # Verifica fim do jogo
                if self.monster.hp <= 0:
                    self.game_over = True
                    print("Você venceu! O monstro foi derrotado!")
                if self.hero.hp <= 0:
                    self.game_over = True
                    print("Você foi derrotado!")
        
        # Espera as threads terminarem
        monster_thread.join()
        mana_thread.join()

# Inicia o jogo
if __name__ == "__main__":
    game = Game()
    game.run()
    