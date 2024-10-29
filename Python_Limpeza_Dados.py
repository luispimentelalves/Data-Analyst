
import beaupy
import os
import datetime
import mysql.connector
import json
from datetime import datetime

def wipe_terminal(): 
    if os.name == "nt": _ = os.system("cls")
wipe_terminal()

   
def validar_data(date_text):
    while True:
        try:
            datetime.strptime(date_text, "%Y-%m-%d")
            return True
        except ValueError:
            print("Formato de data incorreto, deve ser YYYY-MM-DD")
            date_text = input("Insira a data novamente: ")

def inserirCurso():#nome,data_inicio,data_fim):#

    while True:
        nome = input("Insira o nome do curso: ")
        data_inicio = input("Insira a data de início do curso (YYYY-MM-DD): ")
        data_fim = input("Insira a data de término do curso (YYYY-MM-DD): ")

        if validar_data(data_inicio) and validar_data(data_fim):
            break
        else:
            print("Erro: Formato de data incorreto, deve ser YYYY-MM-DD. Tente novamente.")

    conn = mysql.connector.connect(user="root", host="localhost", database='pl1', port=3306, autocommit=True)
    cursorObject=conn.cursor()
    query="INSERT INTO curso (nome, data_inicio, data_fim) VALUES (%s, %s,%s)"
    val=(nome,data_inicio, data_fim)
    cursorObject.execute(query,val)
    print(f"\nRegistos inseridos: {cursorObject.rowcount}\n")
    conn.close()

#inserirCurso()


def inserirformando():#(nome,nif):

    while True:
        nome = input("Insira o nome do formando: ")
        nif = int(input("Insira o nif: "))
        

        if (nome) and (nif):
            break
        else:
            print("Erro: Tente novamente.")

    
    conn = mysql.connector.connect(user="root", host="localhost", database='pl1', port=3306, autocommit=True)
    cursorObject=conn.cursor()
    query="INSERT INTO formando (nome,nif) VALUES (%s,%s)"
    val=(nome,nif)
    cursorObject.execute(query,val)
    print(f"\nRegistos inseridos: {cursorObject.rowcount}\n")
    conn.close()

#inserirformando()

        
import mysql.connector
import json

def verCursos():
    lista_de_cursos = []

    try:
        conn = mysql.connector.connect(user="root", host='localhost', database='pl1', autocommit=True)
        cursorObject = conn.cursor()
        query = "SELECT id, nome, data_inicio, data_fim FROM curso"
        cursorObject.execute(query)
        cursos = cursorObject.fetchall()

        if cursos:
            print("Cursos Disponíveis:")
            for curso in cursos:
                curso_info = {'id': curso[0], 'nome': curso[1], 'data_inicio': curso[2].strftime("%Y-%m-%d"), 'data_fim': curso[3].strftime("%Y-%m-%d")}
                print(f"Nome: {curso_info['nome']}, Data de Inicio: {curso_info['data_inicio']}, Data de Fim: {curso_info['data_fim']}")
                lista_de_cursos.append(curso_info)
        else:
            print("Não há cursos disponíveis.")
    except mysql.connector.Error as err:
        print(f"\nErro de conexão: {err}")
    finally:
        if conn.is_connected():
            cursorObject.close()
            conn.close()

    return lista_de_cursos

def gravar_em_json(dados, nome_arquivo):
    with open(nome_arquivo, 'w') as file:
        json.dump(dados, file, indent=4)


def verFormandos():
    lista_de_formandos = []

    try:
        conn = mysql.connector.connect(user="root", host='localhost', database='pl1', autocommit=True)
        cursorObject = conn.cursor()
        query = "SELECT id, nome, nif FROM formando"
        cursorObject.execute(query)
        formandos = cursorObject.fetchall()

        if formandos:
            print("Formandos registados:")
            for formando in formandos:
                formando_info = {'id': formando[0], 'nome': formando[1], 'nif': formando[2]}
                print(f"id: {formando_info['id']} Nome: {formando_info['nome']}, NIF: {formando_info['nif']}")
                lista_de_formandos.append(formando_info)
        else:
            print("Não há formandos disponíveis.")
    except mysql.connector.Error as err:
        print(f"\nErro de conexão: {err}")
    finally:
        if conn.is_connected():
            cursorObject.close()
            conn.close()

    return lista_de_formandos

def gravar_em_json(dados, nome_arquivo):
    with open(nome_arquivo, 'w') as file:
        json.dump(dados, file, indent=4)


def inserir_matricular_formando():
    try:
        conn = mysql.connector.connect(user="root", host='localhost', database='pl1', autocommit=True)
        cursor = conn.cursor()
 
        
        hoje = datetime.now().date()
        cursor.execute("SELECT id, nome FROM curso WHERE data_inicio > %s", (hoje,))
        cursos = cursor.fetchall()
        if not cursos:
            print("Não há cursos disponíveis neste momento.")
            return
        print("Cursos disponíveis:")
        for curso in cursos:
            print(f"Nome: {curso[0]}")
       
        while True:
            nif = input("Introduza o NIF: ")
            if len(nif) != 9:
                print("NIF inválido. Deve conter 9 dígitos.")
            else:
                break
       
 
       
        cursor.execute("SELECT id FROM formando WHERE nif = %s", (nif,))
        formando = cursor.fetchone()
        if formando:
            print("NIF já inscrito nos nossos cursos. Não é possivel fazer uma nova inscrição.")
            return
       
        print("Formando não encontrado.")
 
       
        nome_formando = input("Introduza o nome do formando: ")
        cursor.execute("INSERT INTO formando (nome, nif) VALUES (%s, %s)", (nome_formando, nif))
        conn.commit()
 
        
        cursor.execute("SELECT id FROM formando WHERE nif = %s", (nif,))
        formando = cursor.fetchone()
       
        curso_nome = input("Qual o curso que pretende inscrever?: ")
        curso_nome = curso_nome.lower()
       
        
        cursor.execute("SELECT id FROM curso WHERE LOWER(nome) = %s AND data_inicio > %s", (curso_nome, hoje))
        curso = cursor.fetchone()
        if not curso:
            print("Curso não encontrado, ou já iniciado.")
            return
 

        cursor.execute("INSERT INTO matricula (formando_id, curso_id) VALUES (%s, %s)", (formando[0], curso[0]))
        print("Matrícula realizada com sucesso!")
 
    except :
        print(f"Erro ao matricular formando")
    else:
        cursor.close()
        conn.close()

#inserir_matricular_formando()
        

def pesquisar_curso_por_nome(nome):
    try:
        conn = mysql.connector.connect(user="root", host="localhost", database='pl1', port=3306, autocommit=True)
        cursorObject = conn.cursor()

        query = "SELECT * FROM curso WHERE nome = %s"
        cursorObject.execute(query, (nome,))
        
        cursos_encontrados = cursorObject.fetchall()

        if cursos_encontrados:
            print("Cursos encontrados:")
            for curso in cursos_encontrados:
                print(f"ID: {curso[0]}, Nome: {curso[1]}, Data de Início: {curso[2]}, Data de Fim: {curso[3]}")
        else:
            print("Nenhum curso encontrado com esse nome.")

    except mysql.connector.Error as err:
        print(f"Erro ao conectar ao banco de dados: {err}")

    finally:
        if conn.is_connected():
            cursorObject.close()
            conn.close()


def pesquisar_formando_por_nome(nome):
    try:
        conn = mysql.connector.connect(user="root", host="localhost", database='pl1', port=3306, autocommit=True)
        cursorObject = conn.cursor()

        query = "SELECT * FROM formando WHERE nome = %s"
        cursorObject.execute(query, (nome,))
        
        formandos_encontrados = cursorObject.fetchall()

        if formandos_encontrados:
            print("Formandos encontrados:")
            for formando in formandos_encontrados:
                print(f"ID: {formando[0]}, Nome: {formando[1]}, NIF: {formando[2]}")
        else:
            print("Nenhum formando/a encontrado com esse nome.")

    except mysql.connector.Error as err:
        print(f"Erro ao conectar ao banco de dados: {err}")

    finally:
        if conn.is_connected():
            cursorObject.close()
            conn.close()


def subMenuCursos():

    print("\n")
    print("-"*30)
    print("Gestão de Cursos:")
    print("-"*30)

    subMenuCursos = ["a) - Ver cursos", "b) - Inserir Curso", "c) - Voltar ao menu principal"]

    while True:
        
        op2 = beaupy.select(subMenuCursos, cursor="🢧", cursor_style="cyan", return_index=True)+1
        if op2==1:
            verCursos()
        if op2==2:
            inserirCurso()
        if op2==3:
            cursos = verCursos()
            if cursos:
             gravar_em_json(cursos, 'bd_cursos.json')
            break           

def subMenuFormandos():

    print("\n")
    print("-"*30)
    print("Gestão de Formandos:")
    print("-"*30)

    subMenuFormandos = ["a) - Ver formandos", "b) - Inserir/Matricular formando", "c) - Voltar ao menu principal"]

    while True:
        
        op2 = beaupy.select(subMenuFormandos, cursor="🢧", cursor_style="cyan", return_index=True)+1
        if op2==1:
            verFormandos()
        if op2==2:
            inserir_matricular_formando()
        if op2==3:
            formandos = verFormandos()
            if formandos:
             gravar_em_json(formandos, 'bd_formandos.json')
            
        break

def menuPrincipal():
    
    while True:

        print("-"*30)
        print("MENU PRINCIPAL:")
        print("-"*30)

        menuPrincipal = ["1 - Gestão de Cursos", "2 - Gestão de Formandos", "3 - Pesquisa de Curso","4 - Pesquisa de Formando", "5 - Sair"]

        op = beaupy.select(menuPrincipal, cursor="😎",return_index=True)+1
        if op==1:
            subMenuCursos()
        if op==2:
            subMenuFormandos()
        if op==3:
            nome_pesquisa = input("Insira o nome do curso a pesquisar: ")
            pesquisar_curso_por_nome(nome_pesquisa)
            
        if op==4:
            nome_pesquisa = input("Insira o nome do formando a pesquisar: ")
            pesquisar_formando_por_nome(nome_pesquisa) 

        if op==5:
            break

menuPrincipal()








































# #----------------------------------------INSERIR MATRICULA(4 FUNÇÕES)------------------------------------
# def obter_id_curso(nome):
#     try:
#         conn = mysql.connector.connect(user = "root", host='localhost', database='pl1', port=3306, autocommit=True)
#     except:
#         print("\nErro de conexão\n")
#     else:
#         cursorObject = conn.cursor()
#         query = "SELECT id FROM curso WHERE nome=%s"
#         val = (nome,)
#         cursorObject.execute(query, val)
#         myResult = cursorObject.fetchone()
#         conn.close()
#         if myResult:
#             return myResult[0]
#     return None

# # ver=obter_id_curso(input("Nome do curso:"))
# # print(ver)

# def obter_id_formando(nome):
#     try:
#         conn = mysql.connector.connect(user = "root", host='localhost', database='pl1', port=3306, autocommit=True)
#     except:
#         print("\nErro de conexão\n")
#     else:
#         cursorObject = conn.cursor()
#         query = "SELECT id FROM formando WHERE nome=%s"
#         val = (nome,) 
#         cursorObject.execute(query, val)
#         myResult = cursorObject.fetchone()
#         conn.close()
#         if myResult:
#             return myResult[0]
#     return None
# # ver = obter_id_formando(input("Nome do formando:"))
# # print(ver)


# #-------------------------------------------------------------------------------------------------------------------
# def inserir_matricula_bd(formando_id,curso_id):
#     print("\nPor favor indique o nome do aluno:\n")
#     nome = input("Nome: ")
  
#     try:
#         conn = mysql.connector.connect(user = "root", host='localhost', database='pl1', port=3306, autocommit=True)
#     except:
#         print("\nErro de conexão\n")
#     else:
#         cursorObject = conn.cursor()
#         query = "INSERT INTO matricula (formando_id,curso_id) VALUES (%s, %s)"
#         val = (formando_id,curso_id) 
#         cursorObject.execute(query, val)
#         print(f"\nRegistos inseridos: {cursorObject.rowcount}\n")
#         conn.close()   

# # ver = inserir_matricula_bd(input("Nome do formando:"))
# # print(ver)

# def inserir_matricula():
#     print("\nPor favor indique o nome do formando e do Curso:\n")
#     while True:
#         formando_id = obter_id_formando(input("Nome do formando: "))
#         curso_id = obter_id_curso(input("Nome do curso: "))
#         if formando_id:
#             if curso_id:
#              inserir_matricula_bd(formando_id,curso_id)
#             break
#         print("\nErro: dados inválidos!\n")

# #inserir_matricula()
# #---------------------------------------------------------------------------------------------------------------------     

#
#----------------------------------------------------------



# def save(filename, lista):     
#     try:
#         with open(filename, "w") as f:
#             json.dump(lista, f, indent=4)
#     except:
#         print("\nErro: impossível operar sobre o ficheiro!\n")
 
# def load(filename):
#     try:
#         with open(filename, "r") as f:
#             data = json.load(f)
#     except:
#         return []  # RETORNA UMA LISTA VAZIA EM VEZ DE UM none, PARA NÃO DAR ERR0
#     else:
#         return data

# # PARA GUARDAR A TABELA CURSOS NO FICHEIRO JSON:
# file_cursos = "bd_cursos.json"
# lista_de_cursos=verCursos()
# save(file_cursos,lista_de_cursos)







