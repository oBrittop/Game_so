import threading
import time
import random
import os
import sys

# --- Dados do Jogo ---

# Armazena nome da arma: (preco, bonus_ataque)
Armas_na_Loja = {
    "Espada_Aco": (30, 10),
    "Adaga_Envenenada": (50, 25),
    "Machado_Pesado": (100, 50)
}
# Armazena nome da pocao: quantidade_cura
Pocoes_na_Loja = {
    "Pocao_vida": 50,
    "Super_pocao_vida": 100
}

# --- Variaveis de Dialogo ---
g = "Guanabara: "
vc = "Você: "
d = "Desconhecido: "
l = "Leticia: "

def tela_reset():
    """Limpa a tela do console."""
    os.system('cls' if os.name == 'nt' else 'clear')

def menu_principal():
    """Exibe o menu principal e lida com a entrada do usuario."""
    tela_reset()
    print("----------------------------")
    print("Bem-vindo à KN City \n".upper())
    print("1. Iniciar Novo Jogo")
    print("2. Sair")
    print("----------------------------")

    while True:
        opcao = input(">>>> ")
        if opcao == "1":
            return "novo_jogo"
        elif opcao == "2":
            sys.exit()
        else:
            print("Opção inválida. Por favor, digite 1 ou 2.")

def introducao_novo_jogo(heroi):
    """Lida com o dialogo de introducao e criacao do nome do heroi."""
    tela_reset()
    print(f"{d}Olá, pequeno gafanhoto.")
    print(f"{d}Que bom que você acordou, estávamos preocupados.")
    time.sleep(4)

    print(f"{d}Ops, acho que tem alguém me chamando, vai se virando aí, mais tarde venho falar com você.")
    time.sleep(4)
    tela_reset()
    print(f"{vc}Hm? Como assim? Do que você está falando? Espera, quem é você?")
    print(f"{d}Como assim quem sou eu? Você tá brincando comigo?")
    time.sleep(4)

    print(f"{d}Caramba, só pode ser brincadeira, isso não pode 'tá' acontecendo agora.")
    print(f"{vc}Você não 'tá' falando coisa com coisa... Espera, você 'tá' sangrando?")
    time.sleep(4)

    print(f"{g}Me chamo Guanabara, cuidado por aí. Vou deixar uns itens em cima da mesa. Fica e espera a Leticia, ela vai te ajudar. Se cuida!")
    input("\nPressione Enter para continuar...")
    tela_reset()

    print(f"{vc}Espera! Droga, não consigo ir atrás dele, estou com muita dor.")
    time.sleep(1)
    print(f"{vc}O que será que rolou, afinal de contas?")
    time.sleep(2)
    print(f"{vc}Quem caramba é Leticia?")
    time.sleep(2)
    input("\nPressione Enter para continuar...")
    tela_reset()

    heroi.nome = input("Qual será seu nome de herói? ")
    print(f"\nSeja bem-vindo(a) a KN City, {heroi.nome}!")
    time.sleep(6)

def loja(heroi):
    """Gerencia a loja do jogo para armas e pocoes."""
    while True:
        tela_reset()
        print("-----------------------------")
        print("Bem vindo jogador!!!")
        print("Aqui você pode aumentar seu poder e adquirir novas poções!!!")
        print("\nO que você gostaria de comprar?\n")
        print("1. Armas")
        print("2. Poções")
        print("3. Voltar ao Menu Principal")
        print(f"Suas Moedas: ${heroi.moedas}")
        print("-----------------------------")

        opcao = input(">>>> ")

        if opcao == "1":
            tela_reset()
            print("--- Armas Disponíveis ---")
            print("Arma               Preço   Dano Adicional")
            print("------------------------------------------")
            for i, (nome_arma, (preco, bonus_dano)) in enumerate(Armas_na_Loja.items()):
                print(f"{i}. {nome_arma:<17} ${preco:<6} +{bonus_dano}")
            print("------------------------------------------")
            print("4. Voltar")

            while True:
                try:
                    escolha_str = input("Digite o número da arma que você quer comprar (ou 4 para voltar): ")
                    escolha = int(escolha_str)
                    if 0 <= escolha < len(Armas_na_Loja):
                        nome_arma = list(Armas_na_Loja.keys())[escolha]
                        preco, bonus_dano = Armas_na_Loja[nome_arma]
                        if heroi.moedas >= preco:
                            heroi.moedas -= preco
                            heroi.armas.add(nome_arma)
                            print(f"Você comprou {nome_arma} por ${preco}.")
                            equipar_agora = input(f"Deseja equipar {nome_arma} agora? (s/n): ").lower()
                            if equipar_agora == 's':
                                heroi.arma_atual = nome_arma
                                print(f"{nome_arma} equipada!")
                            else:
                                print(f"{nome_arma} adicionada ao seu inventário.")
                        else:
                            print("Você não tem moedas suficientes!")
                        input("\nPressione Enter para continuar...")
                        break
                    elif escolha == 4:
                        break
                    else:
                        print("Escolha inválida. Por favor, digite um número da lista.")
                except ValueError:
                    print("Entrada inválida. Digite um número.")

        elif opcao == "2":
            tela_reset()
            print("--- Poções Disponíveis ---")
            print("Poção              Preço   Cura")
            print("------------------------------------")
            for i, (nome_pocao, quantidade_cura) in enumerate(Pocoes_na_Loja.items()):
                # O preço da poção é o seu valor de cura na loja
                print(f"{i}. {nome_pocao:<17} ${Pocoes_na_Loja[nome_pocao]:<6} +{quantidade_cura}") 
            print("------------------------------------")
            print("2. Voltar")

            while True:
                try:
                    escolha_str = input("Digite o número da poção que você quer comprar (ou 2 para voltar): ")
                    escolha = int(escolha_str)
                    if 0 <= escolha < len(Pocoes_na_Loja):
                        nome_pocao = list(Pocoes_na_Loja.keys())[escolha]
                        preco = Pocoes_na_Loja[nome_pocao] 
                        if heroi.moedas >= preco:
                            heroi.moedas -= preco
                            heroi.pocoes[nome_pocao] = heroi.pocoes.get(nome_pocao, 0) + 1
                            print(f"Você comprou {nome_pocao} por ${preco}.")
                        else:
                            print("Você não tem moedas suficientes!")
                        input("\nPressione Enter para continuar...")
                        break
                    elif escolha == 2:
                        break
                    else:
                        print("Escolha inválida. Por favor, digite um número da lista.")
                except ValueError:
                    print("Entrada inválida. Digite um número.")

        elif opcao == "3":
            break
        else:
            print("Opção inválida. Por favor, escolha 1, 2 ou 3.")
            input("\nPressione Enter para continuar...")


class Heroi:
    def __init__(self, nome="Herói"):
        self.nome = nome
        self.hp_max = 100
        self.hp = self.hp_max
        self.mana_max = 50
        self.mana = self.mana_max
        self.ataque_base = 15  # Ataque base desarmado
        self.nivel = 1
        self.moedas = 25  # Moedas iniciais
        self.pocoes = {"Pocao_vida": 2, "Super_pocao_vida": 0}
        self.armas = {"Punhos"}
        self.arma_atual = "Punhos" # Arma padrao

    def atacar(self):
        """Calcula o dano de ataque do heroi com base na arma atual."""
        dano = self.ataque_base + random.randint(5, 15) # Dano base aleatorio

        if self.arma_atual != "Punhos":
            if self.arma_atual in Armas_na_Loja:
                dano += Armas_na_Loja[self.arma_atual][1]  # Adiciona bonus de dano da arma
            else:
                print(f"Aviso: Arma '{self.arma_atual}' não encontrada na loja de armas. Usando ataque básico.")
        return dano

    def usar_pocao(self):
        """Permite ao heroi usar uma pocao de seu inventario."""
        if self.pocoes["Super_pocao_vida"] > 0:
            self.hp = min(self.hp_max, self.hp + Pocoes_na_Loja["Super_pocao_vida"])
            self.pocoes["Super_pocao_vida"] -= 1
            print(f"Você usou uma Super Poção! HP atual: {self.hp}/{self.hp_max}")
        elif self.pocoes["Pocao_vida"] > 0:
            self.hp = min(self.hp_max, self.hp + Pocoes_na_Loja["Pocao_vida"])
            self.pocoes["Pocao_vida"] -= 1
            print(f"Você usou uma Poção de Vida! HP atual: {self.hp}/{self.hp_max}")
        else:
            print("Você não tem poções para usar!")
        input("\nPressione Enter para continuar...")

    def exibir_atributos(self):
        """Exibe os atributos atuais do heroi."""
        print("--- ATRIBUTOS DO HERÓI ---")
        print(f"Nome: {self.nome} | Nível: {self.nivel}")
        print(f"HP: {self.hp}/{self.hp_max} | Mana: {self.mana}/{self.mana_max}")
        print(f"Moedas: ${self.moedas}")
        print(f"Arma Atual: {self.arma_atual}")
        print(f"Poções: {', '.join(f'{k}: {v}' for k, v in self.pocoes.items())}")
        print("--------------------------")
        input("\nPressione Enter para continuar...")

    def magia(self):
        """Realiza um ataque magico se houver mana suficiente."""
        if self.mana >= 20:
            self.mana -= 20
            return random.randint(10, 20)
        return 0

    def regenerar_mana(self):
        """Regenera uma pequena quantidade de mana ao longo do tempo."""
        if self.mana < self.mana_max:
            self.mana = min(self.mana_max, self.mana + 5) # Regenera 5 de mana
            return True
        return False

class Monstro:
    def __init__(self, nome, hp_maximo, ataque_monstro, moedas):
        self.nome = nome
        self.hp_maximo = hp_maximo
        self.hp = hp_maximo # Monstro começa com HP total
        self.ataque_monstro = ataque_monstro
        self.moedas = moedas

    def atacar(self):
        """Calcula o dano de ataque do monstro."""
        return random.randint(self.ataque_monstro - 5, self.ataque_monstro + 5) # Aleatoriza ligeiramente o ataque do monstro

# --- Definições dos Monstros (São modelos, instâncias serão criadas) ---
ZUMBI_NORMAL_ESTATS = {"nome": "Zumbie Normal", "hp_maximo": 60, "ataque_monstro": 15, "moedas": 20}
ZUMBI_POLICIAL_ESTATS = {"nome": "Zumbie Policial", "hp_maximo": 90, "ataque_monstro": 25, "moedas": 50}
ZUMBI_MUTANTE_ESTATS = {"nome": "Zumbie Mutante", "hp_maximo": 150, "ataque_monstro": 35, "moedas": 100}


class Jogo:
    def __init__(self):
        self.heroi = Heroi() # Objeto Heroi é criado aqui
        self.monstro = None # Monstro será definido quando uma batalha começar
        self.jogo_finalizado = False
        self.zumbis_derrotados = 0 # Contador para zumbis derrotados

        # Semáforos para sincronizacao de threads
        self.trava_turno = threading.Semaphore(1)
        self.trava_hp_heroi = threading.Semaphore(1)
        self.trava_mana_heroi = threading.Semaphore(1)

    def thread_ataque_monstro(self):
        """Funcao da thread para os ataques autonomos do monstro."""
        while not self.jogo_finalizado:
            time.sleep(random.randint(3, 6)) # Monstro ataca a cada 3-6 segundos

            if self.jogo_finalizado: break # Sai se o jogo terminar enquanto espera

            self.trava_turno.acquire() # Monstro tenta adquirir o controle do turno
            try:
                if self.monstro and self.monstro.hp > 0 and self.heroi.hp > 0:
                    dano = self.monstro.atacar()

                    with self.trava_hp_heroi: # Protege a modificacao do HP do heroi
                        self.heroi.hp = max(0, self.heroi.hp - dano)

                    print(f"\n--- LOG DA BATALHA ---")
                    print(f">> {self.monstro.nome} atacou! Causou {dano} de dano. Vida do {self.heroi.nome}: {self.heroi.hp}/{self.heroi.hp_max} <<")
                    print("----------------------")

                    if self.heroi.hp <= 0:
                        self.jogo_finalizado = True
                        print("\n>> Você foi derrotado! Fim de jogo. <<")
            finally:
                if self.trava_turno._value == 0: # Apenas libera se o monstro adquiriu
                    self.trava_turno.release()

    def thread_regeneracao_mana(self):
        """Funcao da thread para a regeneracao automatica de mana."""
        while not self.jogo_finalizado:
            time.sleep(5)
            if self.jogo_finalizado: break

            with self.trava_mana_heroi: # Protege o acesso à mana durante a regeneracao
                if self.heroi.regenerar_mana():
                    print(f"\n--- LOG DA BATALHA ---")
                    print(f">> Mana regenerada! Mana atual: {self.heroi.mana}/{self.heroi.mana_max} <<")
                    print("----------------------")

    def batalha(self, tipo_monstro):
        """Gerencia a sequencia de combate entre o heroi e um monstro."""
        # Cria uma nova instancia de Monstro para cada batalha
        self.monstro = Monstro(tipo_monstro["nome"], tipo_monstro["hp_maximo"], tipo_monstro["ataque_monstro"], tipo_monstro["moedas"])

        print(f"\nUm {self.monstro.nome} feroz aparece na sua frente! A batalha começa!\n")
        time.sleep(2)

        thread_monstro = threading.Thread(target=self.thread_ataque_monstro)
        thread_mana = threading.Thread(target=self.thread_regeneracao_mana)

        thread_monstro.start()
        thread_mana.start()

        rodada_batalha = 1
        while not self.jogo_finalizado:
            tela_reset()
            self.trava_turno.acquire() # Jogador adquire o controle do turno
            try:
                if self.jogo_finalizado: break # Verifica novamente caso o monstro tenha finalizado o jogo

                print(f"--- BATALHA - Rodada {rodada_batalha} ---")
                print(f"{self.heroi.nome} HP: {self.heroi.hp}/{self.heroi.hp_max} | Mana: {self.heroi.mana}/{self.heroi.mana_max}")
                print(f"{self.monstro.nome} HP: {self.monstro.hp}/{self.monstro.hp_maximo}")
                print("1. Atacar")
                print("2. Usar Magia (Custa 20 mana)")
                print("3. Usar Poção")
                print("4. Abrir Inventário (para equipar armas ou ver poções)")
                print("5. Fugir (50% de chance de sucesso)")
                print("-----------------------------")

                acao = input("Escolha sua ação: ")

                print("\n--- LOG DA BATALHA ---")
                if acao == "1":
                    dano = self.heroi.atacar()
                    self.monstro.hp = max(0, self.monstro.hp - dano)
                    print(f">> Você atacou! Causou {dano} de dano. Vida do {self.monstro.nome}: {self.monstro.hp}/{self.monstro.hp_maximo} <<")
                elif acao == "2":
                    with self.trava_mana_heroi: # Protege o acesso à mana durante o uso
                        dano = self.heroi.magia()
                    if dano > 0:
                        self.monstro.hp = max(0, self.monstro.hp - dano)
                        print(f">> Você usou magia! Causou {dano} de dano. Vida do {self.monstro.nome}: {self.monstro.hp}/{self.monstro.hp_maximo} <<")
                    else:
                        print(">> Mana insuficiente para usar magia! <<")
                elif acao == "3":
                    self.heroi.usar_pocao() # Isso ja tem suas proprias mensagens
                    input("\nPressione Enter para continuar...") # Adicionado para pausar apos o uso da pocao
                elif acao == "4":
                    self.abrir_inventario_batalha()
                elif acao == "5":
                    if random.random() < 0.5: # 50% de chance de escapar
                        print(">> Você conseguiu fugir da batalha! <<")
                        self.jogo_finalizado = True
                    else:
                        print(">> Você falhou em fugir! <<")
                else:
                    print(">> Ação inválida! Você perdeu sua vez. <<")
                print("----------------------")
                time.sleep(1.5) # Pausa para ler o log da batalha

                if self.monstro.hp <= 0:
                    print(f"\n>> PARABÉNS! Você venceu! O {self.monstro.nome} foi derrotado! <<")
                    self.heroi.moedas += self.monstro.moedas
                    print(f"Você ganhou {self.monstro.moedas} moedas! Total: ${self.heroi.moedas}")
                    self.zumbis_derrotados += 1 # Incrementa o contador de zumbis derrotados
                    print(f"Zumbis derrotados: {self.zumbis_derrotados}/5")
                    self.jogo_finalizado = True
                
                rodada_batalha += 1

            finally:
                if self.trava_turno._value == 0: # Apenas libera se o jogador adquiriu
                    self.trava_turno.release()
            
            # Pequeno atraso apos o turno do jogador para permitir que a thread do monstro possa ser executada
            time.sleep(1)

        # Garante que as threads terminem graciosamente
        thread_monstro.join()
        thread_mana.join()
        print("\n--- FIM DA BATALHA ---")
        # Reinicia jogo_finalizado para a proxima batalha potencial, mas apenas se o jogo nao tiver terminado completamente
        if self.zumbis_derrotados < 5 and self.heroi.hp > 0:
            self.jogo_finalizado = False
        self.monstro = None # Limpa o monstro apos a batalha

    def abrir_inventario_batalha(self):
        """Permite ao heroi gerenciar o inventario durante a batalha."""
        tela_reset()
        print("--- SEU INVENTÁRIO ---")
        self.heroi.exibir_atributos() # Isso ja pausa com input()
        
        # Opcao para equipar arma
        if len(self.heroi.armas) > 1: # Se tiver mais do que apenas "Punhos"
            print("\nVocê tem as seguintes armas:")
            for i, arma in enumerate(list(self.heroi.armas)): # Converte set para lista para acesso indexado
                print(f"{i}. {arma}")
            
            while True:
                escolha_equipar = input("Digite o número da arma para equipar (ou 'v' para voltar): ").lower()
                if escolha_equipar == 'v':
                    break
                try:
                    indice = int(escolha_equipar)
                    lista_armas = list(self.heroi.armas)
                    if 0 <= indice < len(lista_armas):
                        arma_selecionada = lista_armas[indice]
                        self.heroi.arma_atual = arma_selecionada
                        print(f"Você equipou: {arma_selecionada}")
                        input("\nPressione Enter para continuar...")
                        break
                    else:
                        print("Escolha inválida.")
                except ValueError:
                    print("Entrada inválida. Digite um número ou 'v'.")
        else:
            print("Você não tem outras armas para equipar.")
            input("\nPressione Enter para continuar...")


    def executar_jogo(self):
        """Loop principal do jogo e progressao."""
        acao = menu_principal()
        
        if acao == "novo_jogo":
            introducao_novo_jogo(self.heroi)
            
            while self.heroi.hp > 0 and self.zumbis_derrotados < 5: # O jogo continua ate o heroi morrer ou 5 zumbis serem derrotados
                tela_reset()
                print("--- KN CITY ---")
                print(f"Zumbis Derrotados: {self.zumbis_derrotados}/5")
                print("O que você gostaria de fazer agora?")
                print("1. Explorar (Encontrar um monstro)")
                print("2. Visitar a Loja")
                print("3. Ver Atributos do Herói")
                print("4. Sair do Jogo")
                print("-----------------------------")
                
                escolha = input(">>>> ")

                if escolha == "1":
                    # Determina qual monstro deve aparecer com base na contagem de zumbis_derrotados
                    if self.zumbis_derrotados == 0 or self.zumbis_derrotados == 1:
                        estats_monstro_escolhido = ZUMBI_NORMAL_ESTATS
                    elif self.zumbis_derrotados == 2 or self.zumbis_derrotados == 3:
                        estats_monstro_escolhido = ZUMBI_POLICIAL_ESTATS
                    elif self.zumbis_derrotados == 4: # O 5º zumbi (indice 4)
                        estats_monstro_escolhido = ZUMBI_MUTANTE_ESTATS
                    else: # Fallback, nao deve acontecer se a logica estiver correta
                        estats_monstro_escolhido = ZUMBI_NORMAL_ESTATS 
                        
                    self.batalha(estats_monstro_escolhido)

                elif escolha == "2":
                    loja(self.heroi)
                elif escolha == "3":
                    self.heroi.exibir_atributos()
                elif escolha == "4":
                    print("\nObrigado por jogar KN City! Até a próxima!")
                    sys.exit()
                else:
                    print("\nOpção inválida. Por favor, tente novamente.")
                    input("\nPressione Enter para continuar...")
            
            if self.zumbis_derrotados >= 5:
                tela_reset()
                print("--------------------------------------------------")
                print(f"{l}Olá, {self.heroi.nome}! Você conseguiu! Eu sabia que você era forte!")
                time.sleep(4)
                print(f"{vc}Leticia? Você é a Leticia que o Guanabara mencionou?")
                time.sleep(4)
                print(f"{l}Isso mesmo. E você veio na hora certa. Os zumbis mais fortes estavam vindo para cá.")
                time.sleep(4)
                print(f"{l}Graças a você, a cidade está segura por enquanto. Venha, vou te levar para um lugar onde você estará realmente protegido.")
                time.sleep(5)
                print("\nCom a ajuda de Leticia, você encontra um santuário seguro, longe do perigo dos zumbis. A cidade de KN City tem uma nova esperança.")
                print("\n--- FIM DE JOGO: VITÓRIA! ---")
                input("\nPressione Enter para sair...")
                sys.exit()
            elif self.heroi.hp <= 0:
                print("\n>> Seu herói foi derrotado. Fim de jogo. <<")
                input("\nPressione Enter para sair...")
                sys.exit()

if __name__ == "__main__":
    print("Bem vindo ao KN City")
    print("Desenvolvido por Grupo 7")
    jogo = Jogo()
    jogo.executar_jogo()