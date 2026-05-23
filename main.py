# Projeto ExpoTech - 3 pontos
# PROJETO EcoMesa
# CRUD completo (Usuarios e Doações)
# Entrega - dia 31/05/2026

class bcolors:
    PINK = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

from datetime import datetime
from Banco_de_dados.conexao import conectar, fechar_conexao

# USUARIOS

def criar_usuario():
    # Exercicio 1: cadastrar um novo usuario na tabela tbl_usuarios (tipo, entidade, nome, email, senha).
    conexao = conectar()
    cursor = conexao.cursor()

    while True:
        try:
            tipo = int(input("Digite o tipo de usuario: \n1 - Doador \n2 - Receptor \n: "))
            if tipo in [1, 2]:
                break
            print("Tipo invalido. Tente novamente.")
        except ValueError:
            print("Entrada invalida. Digite um numero inteiro.")

    while True:
        try:
            entidade = int(input("Digite a entidade \n1 - Pessoa Fisica, \n2 - Estabelecimento \n: "))
            if entidade in [1, 2]:
                break
            print("Entidade invalida. Tente novamente.")
        except ValueError:
            print("Entrada invalida. Digite um numero inteiro.")

    while True:
        nome = input("Digite seu nome de usuario: ")
        if nome.strip():
            break
        else:
            print("Nome de usuario nao pode ser vazio. Tente novamente.")

    while True:
        email = input("Digite seu email: ")
        if email.strip():
            break
        else:
            print("Email nao pode ser vazio. Tente novamente.")

    while True:
        senha = input("Digite sua senha: ")
        if senha.strip():
            break
        else:
            print("Senha nao pode ser vazia. Tente novamente.")

    cursor.execute("""INSERT INTO tbl_usuarios (tipo_usuario, tipo_entidade, nome_usuario, email_usuario,
                    senha_usuario) VALUES (%s, %s, %s, %s, %s)""", 
                    (tipo, entidade, nome, email, senha))

    conexao.commit()
    print("Usuario criado com sucesso!")
    cursor.close()
    fechar_conexao(conexao)
    return


def listar_usuarios():
    # Exercicio 2: listar todos os usuarios cadastrados com id, nome, email, tipo e entidade.
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""SELECT id_usuario, nome_usuario, email_usuario, tbl_tipo_usuario.tipo, tbl_tipo_entidade.entidade
                    FROM tbl_usuarios
                    JOIN tbl_tipo_usuario ON tbl_usuarios.tipo_usuario = tbl_tipo_usuario.id_tipo
                    JOIN tbl_tipo_entidade ON tbl_usuarios.tipo_entidade = tbl_tipo_entidade.id_entidade
                    ORDER BY id_usuario""")
    usuarios = cursor.fetchall()

    maior_nome = max(len(usuario[1]) for usuario in usuarios)
    maior_email = max(len(usuario[2]) for usuario in usuarios)
    print("""\n=== USUARIOS CADASTRADOS ===""")
    for usuario in usuarios:
        print(f"{bcolors.BLUE}ID:{bcolors.ENDC} {usuario[0]:<2} | {bcolors.CYAN}Nome:{bcolors.ENDC} {usuario[1]:<{maior_nome}} | {bcolors.GREEN}Email: {bcolors.ENDC}{usuario[2]:<{maior_email}} | {bcolors.YELLOW}Tipo: {bcolors.ENDC}{usuario[3]:<2} | {bcolors.PINK}Entidade: {bcolors.ENDC}{usuario[4]}")

    cursor.close()
    fechar_conexao(conexao)
    return


def atualizar_usuario():
    # Exercicio 3: atualizar nome e/ou email de um usuario existente por id.
    conexao = conectar()
    cursor = conexao.cursor()

    listar_usuarios()
    while True:
        try:
            atualizar_usuario = int(input("\nDigite o ID do usuario que deseja atualizar: "))
            break
        except ValueError:
            print("ID invalido. Digite um numero inteiro.")

    while True:
        cursor.execute("""SELECT id_usuario FROM tbl_usuarios WHERE id_usuario = %s""", (atualizar_usuario,))
        if cursor.fetchone():
            break
        else:
            print("ID nao encontrado. Tente novamente.")
            return
    while True:
        novo_nome = input("Digite o novo nome do usuario (deixe em branco para manter o atual): ")
        if novo_nome.strip() or novo_nome == "":
            break

    while True:
        novo_email = input("Digite o novo email do usuario (deixe em branco para manter o atual): ")
        if novo_email.strip() or novo_email == "":
            break

    while True:
        nova_senha = input("Digite a nova senha do usuario (deixe em branco para manter a atual): ")
        if nova_senha.strip() or nova_senha == "":
            break

    cursor.execute("""SELECT nome_usuario, email_usuario, senha_usuario FROM tbl_usuarios WHERE id_usuario = %s""", (atualizar_usuario,))
    atual = cursor.fetchone()

    novo_nome = novo_nome if novo_nome.strip() else atual[0]
    novo_email = novo_email if novo_email.strip() else atual[1]
    nova_senha = nova_senha if nova_senha.strip() else atual[2]

    cursor.execute("""UPDATE tbl_usuarios SET nome_usuario = %s, email_usuario = %s, senha_usuario = %s WHERE id_usuario = %s""", 
                    (novo_nome, novo_email, nova_senha, atualizar_usuario))
    conexao.commit()
    print("Usuario atualizado com sucesso!")
    cursor.close()
    fechar_conexao(conexao)
    return


def excluir_usuario():
    # Exercicio 4: excluir um usuario por id, tratando dependencias em tbl_pessoa_fisica e tbl_estabelecimentos.
    conexao = conectar()
    cursor = conexao.cursor()

    listar_usuarios()
    while True:
        try:
            excluir_usuario = int(input("\nDigite o ID do usuario que deseja excluir: "))
            break
        except ValueError:
            print("ID invalido. Digite um numero inteiro.")

    while True:
        cursor.execute("""SELECT id_usuario FROM tbl_usuarios WHERE id_usuario = %s""", (excluir_usuario,))
        if cursor.fetchone():
            break
        else:
            print("ID nao encontrado. Tente novamente.")
            return
    
    cursor.execute("""SELECT fk_usuario_doacao
                    FROM tbl_doacoes
                    WHERE fk_usuario_doacao = %s""", (excluir_usuario,))
    resultado = cursor.fetchone()
    if resultado:
        print("Usuario possui doacoes vinculadas. Deseja excluir o usuario e todas as doacoes associadas? (s/n)")
        opcao = input().strip().lower()
        if opcao == "s":
            # Excluir doacoes associadas
            cursor.execute("""DELETE FROM tbl_itens_doacoes WHERE fk_doacao_itens IN (SELECT id_doacao FROM tbl_doacoes WHERE fk_usuario_doacao = %s)""", (excluir_usuario,))
            cursor.execute("""DELETE FROM tbl_doacoes WHERE fk_usuario_doacao = %s""", (excluir_usuario,))
            #excluir dependencias em tbl_pessoa_fisica e tbl_estabelecimentos
            cursor.execute("""DELETE FROM tbl_pessoa_fisica WHERE fk_usuario_pessoa = %s""", (excluir_usuario,))
            cursor.execute("""DELETE FROM tbl_estabelecimentos WHERE fk_usuario_estabelecimento = %s""", (excluir_usuario,))
            # Excluir usuario
            cursor.execute("""DELETE FROM tbl_usuarios WHERE id_usuario = %s""", (excluir_usuario,))       
            conexao.commit()
            print("Usuario excluido com sucesso!") 
        else:
            print("Exclusao cancelada.")
    else:
        # Excluir dependencias em tbl_pessoa_fisica e tbl_estabelecimentos
        cursor.execute("""DELETE FROM tbl_pessoa_fisica WHERE fk_usuario_pessoa = %s""", (excluir_usuario,))
        cursor.execute("""DELETE FROM tbl_estabelecimentos WHERE fk_usuario_estabelecimento = %s""", (excluir_usuario,))
        # Excluir usuario
        cursor.execute("""DELETE FROM tbl_usuarios WHERE id_usuario = %s""", (excluir_usuario,))
        conexao.commit()
        print("Usuario excluido com sucesso!")
    


    cursor.close()
    fechar_conexao(conexao)
    return


# DOAÇÕES

def criar_doacao():
    # Exercicio 5: criar uma doacao e inserir itens na tabela tbl_itens_doacoes com descricao, quantidade e validade.
    return


def listar_doacoes():
    # Exercicio 6: listar todas as doacoes com o nome do doador e seus itens (descricao, quantidade, validade).
    return


def atualizar_doacao():
    # Exercicio 7: atualizar a data de uma doacao e/ou os itens vinculados a ela por id.
    return


def excluir_doacao():
    # Exercicio 8: excluir uma doacao por id, removendo primeiro os itens de tbl_itens_doacoes.
    return


def menu():
    opcoes = {
        "1": ("Criar usuario", criar_usuario),
        "2": ("Listar usuarios", listar_usuarios),
        "3": ("Atualizar usuario", atualizar_usuario),
        "4": ("Excluir usuario", excluir_usuario),
        "5": ("Criar doacao com itens", criar_doacao),
        "6": ("Listar doacoes completas", listar_doacoes),
        "7": ("Atualizar doacao e itens", atualizar_doacao),
        "8": ("Excluir doacao", excluir_doacao),
    }

    while True:
        print("\n=== MENU EcoMesa - CRUD COMPLETO ===")
        for codigo, (descricao, _) in opcoes.items():
            print(f"{codigo} - {descricao}")
        print("0 - Sair")

        escolha = input("Escolha uma opcao: ").strip()

        if escolha == "0":
            print("Saindo do sistema.")
            break

        if escolha in opcoes:
            descricao, funcao = opcoes[escolha]
            print(f"\nSelecionado: {descricao}")
            funcao()
            print("Exercicio em estrutura base (return vazio).")
        else:
            print("Opcao invalida. Tente novamente.")


menu()