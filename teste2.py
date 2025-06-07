import threading
import time
import random
import os

# -- Variáveis de Diálogo --
g = "Guanabara: "
vc = "Você: " 
d = "Desconhecido: "

def tela_reset():
    os.system('cls' if os.name == 'nt' else 'clear')

class Hero:
    def __init__(self):
        self.nome = ""
        self.hp = 0
        self.mana = 0
        self.nivel = 1
        self.c_critico = 0
        
    def introducao_e_criacao(self):
        tela_reset()
        print(f"{d}Olá, pequeno gafanhoto.")
        print(f"{d}Que bom que você acordou, estávamos preocupados.")
        time.sleep(6)
        print(f"{d}Ops, acho que tem alguém me chamando, vai se virando aí, mais tarde venho falar com você.")
        time.sleep(3)
        print(f"{vc}Hm? Como assim? Do que você está falando? Espera, quem é você?")
        print(f"{d}Como assim quem sou eu? Você tá brincando comigo?")
        time.sleep(5)
        print(f"{d}Karalho, só pode ser brincadeira, isso não pode tá acontecendo agora.")
        print(f"{vc}Você não tá falando coisa com coisa... Espera, você tá sangrando?")
        time.sleep(6)
        print(f"{g}Me chamo Guanabara, cuidado por aí. Vou deixar uns itens em cima da mesa. Fica e espera a Leticia, ela vai te ajudar. Se cuida!")
        input("\nPressione Enter para continuar...")
        
        tela_reset()
        print(f"{vc}Espera! Droga, não consigo ir atrás dele, estou com muita dor.")
        print(f"{vc}O que será que rolou, afinal de contas?")
        print(f"Quem karalho e Leticia ?")
        input("\nPressione Enter para continuar...") 
        
        tela_reset()
        self.nome = input("Qual será seu nome de herói? ")
        self.hp = 100  
        self.mana = 50
        self.c_critico = 5
        self.nivel = 1
        print(f"\nSeja bem-vindo(a) a KN City, {self.nome}!")
        time.sleep(5)
        
    def exibir_atributos_hero(self):
        print(f"--- ATRIBUTOS DO HERÓI ---")
        print(f"Nome: {self.nome} | Nível: {self.nivel}")
        print(f"HP: {self.hp}/100 | Mana: {self.mana}/50")
        print(f"--------------------------")
    
    def attack(self):
        return random.randint(5, 15)
    
    def magic(self):
        if self.mana >= 20:
            self.mana -= 20
            return random.randint(10, 20)
        return 0
    
    # def regenerate_mana(self):
    #     if self.mana < 50:
    #         self.mana = min(50, self.mana + 10)
    #         return True
    #     return False

class Monster:
    def __init__(self):
        self.hp = 80
    
    def attack(self):
        return random.randint(5, 10)

class Game:
    def __init__(self):
        self.hero = Hero()
        self.monster = Monster()
        self.game_over = False
        
        #semáforos 
        self.turn_lock = threading.Semaphore(1)   
        self.hero_hp_lock = threading.Semaphore(1)
        self.hero_mana_lock = threading.Semaphore(1) 

    # Thread para o ataque do monstro
    def monster_attack(self):
        while not self.game_over:
            time.sleep(random.randint(3, 6)) 
            
            if self.game_over: break 
                
            self.turn_lock.acquire() # Monstro tenta pegar o controle do turno
            try: 
                if self.monster.hp > 0 and self.hero.hp > 0:
                    damage = self.monster.attack()
                    
                    with self.hero_hp_lock: # Protege a alteração do HP do herói
                        self.hero.hp = max(0, self.hero.hp - damage)
                    
                    print(f"\n\n>> O Monstro atacou! Causou {damage} de dano. Vida do herói: {self.hero.hp} <<\n")
                    
                    if self.hero.hp <= 0:
                        self.game_over = True
                        print(">> Você foi derrotado! <<")
            finally:
                self.turn_lock.release() # Monstro libera o turno para o jogador

    # Thread para a regeneracao de mana
    def mana_regeneration(self):
        while not self.game_over:
            time.sleep(5)
            if self.game_over: break

            with self.hero_mana_lock: #semáforo de mana
                if self.hero.regenerate_mana():
                    print(f"\n\n>> Mana regenerada! Mana atual: {self.hero.mana} <<\n")
    
    def run(self):
        # Primeiro, cria o personagem
        self.hero.introducao_e_criacao()
        self.hero.exibir_atributos_hero()
        print("\nUm monstro feroz aparece na sua frente! A batalha começa!\n")
        time.sleep(2)

        # Inicia as threads
        monster_thread = threading.Thread(target=self.monster_attack)
        mana_thread = threading.Thread(target=self.mana_regeneration)
        
        monster_thread.start()
        mana_thread.start()
        
        # Loop principal do jogo (turno do jogador)
        while not self.game_over:
            self.turn_lock.acquire() # Jogador pega o controle do turno
            try:
                if self.game_over: break # Verifica de novo caso o monstro tenha finalizado o jogo

                ## MELHORADO: Menu de ação movido para dentro do lock de turno
                print(f"--- SEU TURNO ---")
                print(f"Sua Vida: {self.hero.hp} | Sua Mana: {self.hero.mana} | Vida do Monstro: {self.monster.hp}")
                print("1 - Atacar (dano 5-15)")
                print("2 - Usar Magia (custa 20 mana, dano 10-20)")
                action = input("Escolha sua ação (1 ou 2): ")
                
                if action == "1":
                    damage = self.hero.attack()
                    self.monster.hp = max(0, self.monster.hp - damage)
                    print(f"\n>> Você atacou! Causou {damage} de dano. Vida do monstro: {self.monster.hp} <<")
                elif action == "2":
                    with self.hero_mana_lock: # Protege o acesso à mana durante o uso
                        damage = self.hero.magic()
                    
                    if damage > 0:
                        self.monster.hp = max(0, self.monster.hp - damage)
                        print(f"\n>> Você usou magia! Causou {damage} de dano. Vida do monstro: {self.monster.hp} <<")
                    else:
                        print("\n>> Mana insuficiente! <<")
                else:
                    print("\n>> Ação inválida! Você perdeu sua vez. <<")
                
                if self.monster.hp <= 0:
                    self.game_over = True
                    print("\n>> PARABÉNS! Você venceu! O monstro foi derrotado! <<")
            
            finally:
                self.turn_lock.release() # Jogador libera o turno para o monstro
            
            time.sleep(2) 
            
        # Espera as threads terminarem antes de encerrar o programa
        monster_thread.join()
        mana_thread.join()
        print("\n--- FIM DE JOGO ---")

# Inicia o jogo
if __name__ == "__main__":
    print("Bem vindo ao KN City")
    print("Desenvolvido por Grupo 7")
    time.sleep(5)
    tela_reset()
    game = Game()
    game.run()