global listagemOuvintes
import random
listagemOuvintes = []

#preenchimento de ouvintes inicial para teste
def fillInitialValues(listagemOuvintes):
# função [eval] verifica que as linhas do ficheiro TXT não são uma simples STRING mas sim, uma funcao de python, neste caso, um dicionario
#   https://www.w3schools.com/python/ref_func_eval.asp
#   https://realpython.com/python-eval-function/
    
    f = open('ouvintes.txt', 'rt')
    linhas = f.readlines()
    for linha in linhas:
        linhaAvaliada = eval(linha.strip()) 
        listagemOuvintes.append(linhaAvaliada)
    f.close
fillInitialValues(listagemOuvintes)

# função para validar ficheiro/BD ao arranque do programa e fazer as devidas diligencias caso o mesmo se encontre vazio
def validarInicio():

    f = open('ouvintes.txt', 'rt')
    linhas = f.readlines()
    if linhas == []:
        print("\n! Erro: Base de dados vazia, por favor crie os registos antes de continuar!")
        return menu()
    f.close()

# função para validar ficheiro/BD a quando da execução da função "Jogar" e fazer as devidas diligencias caso o mesmo se encontre vazio
def validarJogo():
    
    contador = 0
    f = open('ouvintes.txt', 'rt')
    
    for _ in f:
        contador += 1
    
    if contador < 2 :
        print("\n! Erro: Necessário pelo menos 2 ouvintes para jogar. Por favor crie os registos !\n")
        return menu()
    f.close()

#Função para criar novo ouvinte, necessário adicionar valores para todos os campos, "Nome", "Numero de Participacoes" e "Numero de Vitorias"
def criarOuvinte():

#A função any() é uma função em Python que retorna True se pelo menos um dos elementos em um iterável for verdadeiro.
# No contexto em que está a ser utilizada:, any(ouvinte["Nome"] == nome for ouvinte in listagemOuvintes)
#   verifica se existe algum ouvinte na lista listagemOuvintes cujo nome seja igual ao nome inserido.

    global listagemOuvintes

    continuar = 1
    while continuar != 0:

        while True:
            try:
                nome = input("\nQual o nome do novo ouvinte ?\n")
            except:
                print(f"\nErro: Algo inesperado aconteceu, por favor reinicie o programa!")    
            else:
                if any(ouvinte["Nome"] == nome for ouvinte in listagemOuvintes):
                    print(f"\nErro: Já existe um jogador registado com esse nome, escolha outro!\n") 
                else:
                    break

        while True:
            try:
                participacoes = int(input(f"\nQuantas participações teve @ {nome} no programa: \n"))  
            except:
                print(f"\nErro: Por favor insira um número inteiro maior que zero (0)\n")    
            else:
                if participacoes < 0:
                    print(f"\nErro: Por favor insira um número inteiro maior que zero (0)\n") 
                else:
                    break

        while True:
            try:
                vitorias = int(input(f"Quantas vitórias teve o {nome} no programa: \n"))
            except:
                print(f"\nErro: Por favor insira um número inteiro maior que zero (0)\n")    
            else:
                if vitorias < 0:
                    print(f"\nErro: Por favor insira um numero inteiro maior que zero (0)\n")
                elif vitorias > participacoes:
                    print(f"\nErro: O número de Vitórias não pode ser maior que o numero de Participações\n") 
                else:
                    ouvinte = {
                    "Nome": nome,
                    "Participacoes": participacoes,
                    "Vitorias": vitorias
                }
                                            
                    print(f"\nO ouvinte {nome} foi adicionado com sucesso\n")
                    listagemOuvintes.append(ouvinte)
                                            
                    f = open('ouvintes.txt', 'rt')
                    if f.read() == "":
                        f.close()
                        f = open('ouvintes.txt', 'at')
                        f.write(str(ouvinte))
                    else:
                        f.close()
                        f = open('ouvintes.txt', 'at')
                        f.write('\n'+str(ouvinte))
                    f.close()

                    break
                                
        
        while True:
            try:
                continuar = int(input('\nPretende inserir mais algum ouvinte? \n1 - Sim\n0 - Não\n'))
            except:
                print("\nERRO: Valor inválido, por favor insira apenas 1 (Sim) ou 0 (não)\n")    
            else:
                if continuar<0 or continuar>1:
                    print("\nERRO: Valor inválido, por favor insira apenas 1 (Sim) ou 0 (não)\n")    
                else:
                    break

#função para atualização do ficheiro e "limpeza" da ultima linha
def updateFile():

    f = open('ouvintes.txt', 'wt')
    
    for i, ouvinte in enumerate(listagemOuvintes):
        if i != len(listagemOuvintes)-1:    # verifica se não é a ultima linha da listagem
            f.write(str(ouvinte)+'\n')      # não sendo a ultima, quebra de linha
        else:                               # sendo a ultima
            f.write(str(ouvinte))           # não quebra a linha (não cria uma ultima linha vazia)
    f.close

#editar ouvintes já criados, necessário indicar qual o campo de cada ouvinte a editar e o respectivo "novo" valor desse campo
def editarOuvinte():

    validarInicio()

    global listagemOuvintes

    print("-"*70)
    print("Listagem atual de ouvintes:")
    verDadosOuvinte()
    print("-"*70)

    op=1
    while op!=0:

        while True:
            try:
                ouvintEdit = int(input(f"\nQual o ouvinte que pretende editar? [1 - {len(listagemOuvintes)}]\n"))
            except:
                print(f"\nErro: introduza um número de jogador válido! (valor inteiro [1 - {len(listagemOuvintes)}])")    
            else:
                if ouvintEdit <=0 or ouvintEdit > len(listagemOuvintes):
                    print(f"\nErro: introduza um numero de jogador válido! (valor inteiro [1 - {len(listagemOuvintes)}])") 
                else:
                    print("\n??   Nome  ||  Participacoes  ||  Vitorias   ??")
                    
                    while True:
                        try:
                            campoEdit = input("Qual o campo da informação do ouvinte que pretende editar?\n")
                        except:
                            print(f"\nErro: introduza um campo válido! ( Nome || Participacoes || Vitorias )\n")    
                        else:
                            if campoEdit not in ["Nome", "Participacoes", "Vitorias"]:
                                print(f"\nErro: introduza um campo válido! ( Nome || Participacoes || Vitorias )\n") 
                            else:
                                
                                while True:
                                    try:
                                        valorEdit = input(f"Qual o novo valor do campo '{campoEdit}':\n")
                                    except:
                                        print(f"\nErro: introduza um campo válido!")    
                                    else:
                                        if campoEdit ==  "Vitorias" and int(valorEdit) > int(listagemOuvintes[ouvintEdit-1]["Participacoes"]):
                                            print(f"\nErro: o número de vitórias não pode ser maior que o nº de participações!\n")
                                        elif campoEdit ==  "Vitorias" and int(valorEdit) <0:
                                            print("\nErro: Introduza um valor válido: Inteiro, maior ou igual a zero (0) e menor ou igual ao numero de participações!\n")
                                        elif campoEdit ==  "Participacoes" and int(valorEdit) < int(listagemOuvintes[ouvintEdit-1]["Vitorias"]):
                                            print(f"\nErro: o nº de Participações não pode ser negativo nem menor que o nº de Vitórias!\n")
                                        elif campoEdit == "Nome" and valorEdit in [ouvinte["Nome"] for ouvinte in listagemOuvintes]:
                                            print("\nErro: Já existe um ouvinte registado com esse nome!\n")
                                        else:
                                            
                                            listagemOuvintes[ouvintEdit-1][campoEdit]=valorEdit
                                            updateFile()
                                            break
                        break
                
                while True:
                    try:
                        op = int(input('\nPretende editar mais algum ouvinte? \n1 - Sim\n0 - Não\n'))
                    except:
                        print("\nERRO: Valor inválido, por favor insira apenas 1 (Sim) ou 0 (não)\n")    
                    else:
                        if op<0 or op>1:
                            print("\nERRO: Valor inválido, por favor insira apenas 1 (Sim) ou 0 (não)\n")    
                        else:
                            break
            
            break

    print("-"*60)
    print("Listagem atualizada de ouvintes após alterações:")
    verDadosOuvinte()
    print("-"*60)

#eliminar um ouvinte da listagem de ouvintes existentes
def eliminarOuvinte():

    validarInicio()

    global listagemOuvintes

    print("-"*60)
    print("Listagem atual de ouvintes:")
    verDadosOuvinte()
    print("-"*60)

    op=1
    while op!=0:

        while True:
            try:
                ouvintEdit = int(input(f"\nQual o ouvinte que pretende eliminar? [1 - {len(listagemOuvintes)}] "))
            except:
                print(f"\nErro: introduza um número de jogador válido! (valor inteiro [1 - {len(listagemOuvintes)}])")    
            else:
                if ouvintEdit <=0 or ouvintEdit > len(listagemOuvintes):
                    print(f"\nErro: introduza um número de jogador válido! (valor inteiro [1 - {len(listagemOuvintes)}])") 
                else:
                    listagemOuvintes.pop(ouvintEdit-1)
                    updateFile()



                    while True:
                        try:
                            op = int(input('\nPretende eliminar mais algum ouvinte? \n1 - Sim\n0 - Não\n'))
                        except:
                            print("\nERRO: Valor inválido, por favor insira apenas 1 (Sim) ou 0 (não)\n")    
                        else:
                            if op<0 or op>1:
                                print("\nERRO: Valor inválido, por favor insira apenas 1 (Sim) ou 0 (não)\n")    
                            else:
                                break
            break

    print("-"*60)
    print("Listagem atualizada de ouvintes após eleminação de registos:")
    verDadosOuvinte()
    print("-"*60)

#submenu para a gestão da listagem de ouvintes (Criar, editar e eliminiar)
def gerirOuvintes():

    op = 1
    while op != 0:
        print("-"*60)
        print('\n**** GESTAO BD DE OUVINTES ****')
        print('Escolha uma das seguintes opções')
        print('1 - Criar novo Ouvinte')
        print('2 - Editar Ouvinte existente')
        print('3 - Eliminar Ouvinte')
        print('0 - Menu anterior')
        print("-"*60)
        op = int(input())

        match op:
            case 0: break
            case 1: criarOuvinte()
            case 2: editarOuvinte()
            case 3: eliminarOuvinte()
            case _: print('Opção inválida')

#funcao global de visualizacao da listagem de ouvintes
def verDadosOuvinte():

    global listagemOuvintes
    for i, ouvinte in enumerate(listagemOuvintes, start=1):
        print(f"{i} - {ouvinte}")

# função para ordenar a lista de participantes primeiro por numero de vitorias (descendente "-")
# e depois (em caso de numero igual de vitorias) por numero de participacoes (ascendente)
def verRankingOuvintes():

    validarInicio()

    global listagemOuvintes
    
    print("\n")
    print("-"*60)
    print("\t"*3, 'R A N K I N G')
    print("\n")
    ranking = sorted(listagemOuvintes, key=lambda x: (-int(x['Vitorias']), int(x['Participacoes'])))
    
    maxParticipacoes = max(int(ouvinte['Participacoes']) for ouvinte in listagemOuvintes)
    
    #   A função lambda tem um único argumento, que é x. Esta função lambda retorna uma tupla com dois elementos:
    #       -int(x['Vitorias']): Este é o primeiro elemento da tupla.
    #   Converte o valor da chave 'Vitorias' do dicionário x para um inteiro
    #       int(x['Participacoes']): Este é o segundo elemento da tupla. 
    #   Converte o valor da chave 'Participacoes' do dicionário x para um inteiro
    #   A função lambda está a ser usada como um argumento para a função sorted().
    #   A função sorted() ordena os elementos da lista "listagemOuvintes" de acordo com os critérios especificados pela função lambda.
    #       Neste caso, a lista esta ordenada primeiro pelo número de vitórias (em ordem decrescente, devido ao sinal negativo) e,
    #   de seguida (em caso de empate de vitórias), pelo número de participações (em ordem crescente).
    #   Resumindo: os ouvintes são classificados com base no número de vitórias,
    #       e se dois ou mais ouvintes tiverem o mesmo número de vitórias, serão classificados com base no número de participações.
    print("Posição/Nome:\t Participações:\t Vitórias:\t Ratio:")
    print("-"*12,"\t","-"*12,"\t","-"*10,"\t","-"*9)
    for i, user in enumerate(ranking, start=1):
        print(f"{i}º - {user["Nome"]}\t {user["Participacoes"]}\t\t {user["Vitorias"]}\t\t  {int(user['Vitorias'])/maxParticipacoes :.2f} ")
    print("-"*60)

# Função para mostrar os detalhes (nº participações e nº vitorias) de todos os participantes/ouvintes registados no programa
# Inicialmente são apresentados os Nomes de todos os participantes
#   e de seguida o utilizador deve escolher sobre qual dos participantes/ouvintes pretende ver os detalhes
def verDadosPorOuvinte():

    validarInicio()

    global listagemOuvintes
    
    print("\nListagem de todos os ouvintes registados no programa:")
    for i, ouvinte in enumerate(listagemOuvintes, start=1):
        print(f"{i} - {ouvinte['Nome']}")

    op=1
    while op!=0:

        while True:
            try:
                ouvinteVer = int(input(f"\nQual o ouvinte que pretende verificar os detalhes [1 - {len(listagemOuvintes)}] ?"))
            except:
                print(f"\nErro: introduza um número de jogador válido! (valor inteiro [1 - {len(listagemOuvintes)}])")    
            else:
                if ouvinteVer <=0 or ouvinteVer > len(listagemOuvintes):
                    print(f"\nErro: introduza um número de jogador válido! (valor inteiro [1 - {len(listagemOuvintes)}])") 
                else:
                    print("\n")
                    print("-"*60)
                    print(f"Seguem os detalhes d@ {listagemOuvintes[ouvinteVer-1]['Nome']}: ")
                    print(f"Participações: {listagemOuvintes[ouvinteVer-1]['Participacoes']}")
                    print(f"Vitórias: {listagemOuvintes[ouvinteVer-1]['Vitorias']}")
                    print("-"*60)
                    
                    
                    
                    while True:
                        try:
                            op = int(input('\nPretende consultar mais algum ouvinte? \n1 - Sim\n0 - Não\n'))
                        except:
                            print("\nERRO: Valor inválido, por favor insira apenas 1 (Sim) ou 0 (não)")    
                        else:
                            if op<0 or op>1:
                                print("\nERRO: Valor inválido, por favor insira apenas 1 (Sim) ou 0 (não)")    
                            else:
                                break
            break

#Função para jogar
def jogar():

    validarJogo()

    global listagemOuvintes
    jogadores =[]
    apostas = []
    diferencas = []
    vencedoresAprox = []

    # seleccao da quantidade de ouvintes que vão a jogo (minimo=2, maximo=total de ouvintes registados)
    numJogadores = random.randint(2,len(listagemOuvintes))
    
    #preenchimento da lista "jogadores" com os numeros dos ouvintes registados na listagem de ouvintes
    while len(jogadores) < numJogadores:
        qualJogador = random.randint(1,len(listagemOuvintes))
        if qualJogador not in jogadores:
            jogadores.append(qualJogador)

    # Geração aleatoria de um dos limites.
    # Obtenção do limite complementar mediante tolerancia de 150g.
    # Geração aleatoria do peso certo do saco entre os limites gerados anteriormente 
    qualLimite = random.randint(1,2)
    if qualLimite == 1:
        limiteInferior = random.randint(1000,5000)
        limiteSuperior = limiteInferior+150
        pesoSaco = random.randint(limiteInferior, limiteSuperior)
    else:
        limiteSuperior = random.randint(1000,5000)
        limiteInferior = limiteSuperior-150
        pesoSaco = random.randint(limiteInferior, limiteSuperior)

    # geração aleatoria das apostas unicas para cada um dos jogadores seleccionados
    # preenchimento da lista de apostas
    while len(apostas) < numJogadores:
        apostaJogador = random.randint(limiteInferior, limiteSuperior)
        if apostaJogador not in apostas:
            apostas.append(apostaJogador)

    #impressão dos jogadores seleccionados por ordem de participação
    #incremento de +1 participação na BS dos participantes
    #atualização do ficheiro TXT com a listagem de artigos atualizada com o numero de participações
    print("-"*60)
    print("Listagem de jogadores e respectivas apostas")
    print("ordenados por ordem de participação:")
    for i, jogador in enumerate(jogadores, start=1):
        print(f'{i}º - {listagemOuvintes[jogador-1]["Nome"]} - Aposta:  {apostas[i-1]} ')
        listagemOuvintes[jogador-1]["Participacoes"] = int(listagemOuvintes[jogador-1]["Participacoes"]) + 1                   
    updateFile()
    print("-"*60)

    
    # retirar "#" para ajudar a validar o programa
    #   print("*"*60)
    #   print(qualLimite)
    #   print(f"peso: {pesoSaco}")
    #   print(limiteSuperior)
    #   print(limiteInferior)
    #   print(jogadores)
    #   print(apostas)
    #   print("*"*60)

    #   verificação do vencedor com o palpite exato e atualização do numero de vitórias
    contador = 0
    for i, jogador in enumerate(jogadores, start=1):
        if pesoSaco == apostas[i-1]:
            print(f'O vencedor é @ {listagemOuvintes[jogador-1]["Nome"]} com o seu palpite certeiro de {apostas[i-1]}g')
            listagemOuvintes[jogador-1]["Vitorias"] = int(listagemOuvintes[jogador-1]["Vitorias"]) + 1
            updateFile()
            contador +=1
            if contador>0:
                return
    
    # não havendo vencedor com palpite exato verifica o(s) vencedor(es) por aproximação
    if contador == 0:
        for jogador, aposta in zip(jogadores, apostas):
            diferenca = abs(aposta-pesoSaco)
            diferencas.append(diferenca)

        for jogador, diferenca in zip(jogadores, diferencas):
            if diferenca == min(diferencas):
                vencedoresAprox.append(listagemOuvintes[jogador-1]["Nome"])
                listagemOuvintes[jogador-1]["Vitorias"] = int(listagemOuvintes[jogador-1]["Vitorias"]) + 1
        
        if len(vencedoresAprox) == 1:
            print(f"O vencedor por aproximação foi @ {vencedoresAprox[0]} e o peso do saco era {pesoSaco}")
            updateFile()

        elif len(vencedoresAprox) == 2:
            print(f"Os vencedores por aproximação foram @ {vencedoresAprox[0]} e @ {vencedoresAprox[1]} e o peso do saco era {pesoSaco}")
            updateFile()

#menu principal do jogo
def menu():

    op = 1
    while op != 0:

        print("\n")
        print("-"*35)
        print("###      MENU PRINCIPAL      ###")
        print('Escolha uma das seguintes opções:')
        print('1 - Gerir BD ouvintes')
        print('2 - Ver dados por ouvinte')
        print('3 - Ver ranking ouvintes')
        print('4 - \u2618\u2618  Jogar  \u2618\u2618')
        print('0-Sair')
        print("-"*35)
        op = int(input())

        match op:
            case 0: break
            case 1: gerirOuvintes()
            case 2: verDadosPorOuvinte()
            case 3: verRankingOuvintes()
            case 4: jogar()
            case _: print('Opção inválida')
menu()