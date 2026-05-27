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
    conexao = conectar()
    cursor = conexao.cursor()

    while True:
        try:
            print(f"{bcolors.BLUE}1-{bcolors.ENDC} Doador\n{bcolors.BLUE}2-{bcolors.ENDC} Receptor")
            tipo = int(input(f"{bcolors.CYAN}Digite o tipo de usuário: {bcolors.ENDC}"))
            if tipo in [1, 2]:
                break
            print(f"{bcolors.RED}❌ Tipo inválido. Tente novamente.{bcolors.ENDC}")
        except ValueError:
            print(f"{bcolors.RED}❌ Entrada inválida. Digite um número inteiro.{bcolors.ENDC}")

    while True:
        try:
            print(f"{bcolors.BLUE}1-{bcolors.ENDC} Pessoa Física\n{bcolors.BLUE}2-{bcolors.ENDC} Estabelecimento")
            entidade = int(input(f"{bcolors.CYAN}Digite a o tipo de entidade: {bcolors.ENDC}"))
            if entidade in [1, 2]:
                break
            print(f"{bcolors.RED}❌ Entidade inválida. Tente novamente.{bcolors.ENDC}")
        except ValueError:
            print(f"{bcolors.RED}❌ Entrada inválida. Digite um número inteiro.{bcolors.ENDC}")

    while True:
        nome = input(f"{bcolors.CYAN}\nDigite seu nome de usuário: {bcolors.ENDC}")
        if nome.strip():
            break
        else:
            print(f"{bcolors.RED}❌ Nome de usuário não pode ser vazio. Tente novamente.{bcolors.ENDC}")

    while True:
        email = input(f"{bcolors.CYAN}\nDigite seu email: {bcolors.ENDC}")
        if email.strip():
            break
        else:
            print(f"{bcolors.RED}❌ Email não pode ser vazio. Tente novamente.{bcolors.ENDC}")

    while True:
        senha = input(f"{bcolors.CYAN}\nDigite sua senha: {bcolors.ENDC}")
        if senha.strip():
            break
        else:
            print(f"{bcolors.RED}❌ Senha não pode ser vazia. Tente novamente.{bcolors.ENDC}")

    while True:
        telefone = input(f"{bcolors.CYAN}\nDigite seu telefone (apenas numeros): {bcolors.ENDC}")
        if telefone.isdigit() and len(telefone) == 11:
            break
        else:
            print(f"{bcolors.RED}❌ Telefone inválido. Digite apenas números.{bcolors.ENDC}")

    while True:
        endereco = input(f"{bcolors.CYAN}\nDigite seu endereço: {bcolors.ENDC}")
        if endereco.strip():
            break
        else:
            print(f"{bcolors.RED}❌ Endereço não pode ser vazio. Tente novamente.{bcolors.ENDC}")

    cursor.execute("""INSERT INTO tbl_usuarios (tipo_usuario, tipo_entidade, nome_usuario, email_usuario,
                    senha_usuario) VALUES (%s, %s, %s, %s, %s)""", 
                    (tipo, entidade, nome, email, senha))
    
    # Validações adicionais para Pessoa Fisica e Estabelecimento 
    id_novo_usuario = cursor.lastrowid
    if entidade == 1: #(Pessoa Fisica)
        while True:
            cpf = input(f"{bcolors.CYAN}\nDigite seu CPF (apenas numeros): {bcolors.ENDC}")
            if cpf.isdigit() and len(cpf) == 11:
                break
            else:
                print(f"{bcolors.RED}❌ CPF inválido. Digite um número de 11 dígitos.{bcolors.ENDC}")
        cursor.execute("""INSERT INTO tbl_pessoa_fisica (nome_pessoa, cpf_pessoa, telefone_pessoa, endereco_pessoa, fk_usuario_pessoa) VALUES (%s, %s, %s, %s, %s)""",
                        (nome, cpf, telefone, endereco, id_novo_usuario))

    elif entidade == 2: #(Estabelecimento)
        while True:
            cnpj = input(f"{bcolors.CYAN}\nDigite seu CNPJ (apenas numeros): {bcolors.ENDC}")
            if cnpj.isdigit() and len(cnpj) == 14:
                break
            else:
                print(f"{bcolors.RED}❌ CNPJ inválido. Digite um número de 14 dígitos.{bcolors.ENDC}")
        cursor.execute("""INSERT INTO tbl_estabelecimentos (nome_estabelecimento, cnpj_estabelecimento, telefone_estabelecimento, endereco_estabelecimento, fk_usuario_estabelecimento) VALUES (%s, %s, %s, %s, %s)""",
                    (nome, cnpj, telefone, endereco, id_novo_usuario))

    conexao.commit()
    print(f"{bcolors.GREEN}✅ Usuario criado com sucesso!{bcolors.ENDC}")
    cursor.close()
    fechar_conexao(conexao)
    return


def listar_usuarios():
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
    print("""\n=== USUÁRIOS CADASTRADOS ===""")
    for usuario in usuarios:
        print(f"{bcolors.BLUE}ID:{bcolors.ENDC} {usuario[0]:<2} {bcolors.CYAN}| Nome:{bcolors.ENDC} {usuario[1]:<{maior_nome}} {bcolors.GREEN}| Email: {bcolors.ENDC}{usuario[2]:<{maior_email}} {bcolors.YELLOW}| Tipo: {bcolors.ENDC}{usuario[3]:<8} {bcolors.PINK}| Entidade: {bcolors.ENDC}{usuario[4]}")

    cursor.close()
    fechar_conexao(conexao)
    return


def atualizar_usuario():
    conexao = conectar()
    cursor = conexao.cursor()

    listar_usuarios()
    while True:
        try:
            atualizar_usuario = int(input(f"\n{bcolors.CYAN}Ryu, The RunnerDigite o ID do usuário que deseja atualizar: {bcolors.ENDC}"))
            break
        except ValueError:
            print(f"{bcolors.RED}❌ ID inválido. Digite um número inteiro.{bcolors.ENDC}")

    while True:
        cursor.execute("""SELECT id_usuario FROM tbl_usuarios WHERE id_usuario = %s""", (atualizar_usuario,))
        if cursor.fetchone():
            break
        else:
            print(f"{bcolors.RED}❌ ID não encontrado. Tente novamente.{bcolors.ENDC}")
            return
    while True:
        novo_nome = input(f"{bcolors.CYAN}\nDigite o novo nome do usuário (deixe em branco para manter o atual): {bcolors.ENDC}")
        if novo_nome.strip() or novo_nome == "":
            break

    while True:
        novo_email = input(f"{bcolors.CYAN}\nDigite o novo email do usuário (deixe em branco para manter o atual): {bcolors.ENDC}")
        if novo_email.strip() or novo_email == "":
            break

    while True:
        nova_senha = input(f"{bcolors.CYAN}\nDigite a nova senha do usuário (deixe em branco para manter a atual): {bcolors.ENDC}")
        if nova_senha.strip() or nova_senha == "":
            break

    while True:
        novo_telefone = input(f"{bcolors.CYAN}\nDigite o novo telefone do usuário (deixe em branco para manter o atual): {bcolors.ENDC}")
        if novo_telefone.strip() == "" or (novo_telefone.isdigit() and len(novo_telefone) == 11):
            break
        else:
            print(f"{bcolors.RED}❌ Telefone inválido. Digite apenas números (11 dígitos) ou deixe em branco para manter o atual.{bcolors.ENDC}")

    while True:
        novo_endereco = input(f"{bcolors.CYAN}\nDigite o novo endereço do usuário (deixe em branco para manter o atual): {bcolors.ENDC}")
        if novo_endereco.strip() or novo_endereco == "":
            break

    cursor.execute("""SELECT nome_usuario, email_usuario, senha_usuario FROM tbl_usuarios WHERE id_usuario = %s""", (atualizar_usuario,))
    atual = cursor.fetchone()

    cursor.execute("""SELECT tipo_entidade FROM tbl_usuarios WHERE id_usuario = %s""", (atualizar_usuario,))
    entidade = cursor.fetchone()[0]

    novo_nome = novo_nome if novo_nome.strip() else atual[0]
    novo_email = novo_email if novo_email.strip() else atual[1]
    nova_senha = nova_senha if nova_senha.strip() else atual[2]

    cursor.execute("""UPDATE tbl_usuarios SET nome_usuario = %s, email_usuario = %s, senha_usuario = %s WHERE id_usuario = %s""", 
                    (novo_nome, novo_email, nova_senha, atualizar_usuario))
    
    if entidade == 1: #(Pessoa Fisica)
        cursor.execute("""SELECT telefone_pessoa, endereco_pessoa FROM tbl_pessoa_fisica WHERE fk_usuario_pessoa = %s""", (atualizar_usuario,))
        atual_pf = cursor.fetchone()
        novo_telefone = novo_telefone if novo_telefone.strip() else atual_pf[0]
        novo_endereco = novo_endereco if novo_endereco.strip() else atual_pf[1]
        cursor.execute("""UPDATE tbl_pessoa_fisica SET nome_pessoa = %s, telefone_pessoa = %s, endereco_pessoa = %s WHERE fk_usuario_pessoa = %s""", 
                       (novo_nome, novo_telefone, novo_endereco, atualizar_usuario))
        
    elif entidade == 2: #(Estabelecimento)
        cursor.execute("""SELECT telefone_estabelecimento, endereco_estabelecimento FROM tbl_estabelecimentos WHERE fk_usuario_estabelecimento = %s""", (atualizar_usuario,))
        atual_estab = cursor.fetchone()
        novo_telefone = novo_telefone if novo_telefone.strip() else atual_estab[0]
        novo_endereco = novo_endereco if novo_endereco.strip() else atual_estab[1]
        cursor.execute("""UPDATE tbl_estabelecimentos SET nome_estabelecimento = %s, telefone_estabelecimento = %s, endereco_estabelecimento = %s WHERE fk_usuario_estabelecimento = %s""", 
                       (novo_nome, novo_telefone, novo_endereco, atualizar_usuario))

    conexao.commit()
    print(f"{bcolors.GREEN}✅ Usuário atualizado com sucesso!{bcolors.ENDC}")
    cursor.close()
    fechar_conexao(conexao)
    return


def excluir_usuario():
    conexao = conectar()
    cursor = conexao.cursor(buffered=True)

    listar_usuarios()
    while True:
        try:
            excluir_usuario = int(input(f"{bcolors.CYAN}\nDigite o ID do usuário que deseja excluir: {bcolors.ENDC}"))
            break
        except ValueError:
            print(f"{bcolors.RED}❌ ID inválido. Digite um número inteiro.{bcolors.ENDC}")

    while True:
        cursor.execute("""SELECT id_usuario FROM tbl_usuarios WHERE id_usuario = %s""", (excluir_usuario,))
        if cursor.fetchone():
            break
        else:
            print(f"{bcolors.RED}❌ ID não encontrado. Tente novamente.{bcolors.ENDC}")
            return
    
    cursor.execute("""SELECT fk_usuario_doacao
                    FROM tbl_doacoes
                    WHERE fk_usuario_doacao = %s""", (excluir_usuario,))
    resultado = cursor.fetchone()
    if resultado:
        print(f"{bcolors.RED}❌ Usuário possui doações vinculadas. Deseja excluir o usuário e todas as doações associadas? (s/n){bcolors.ENDC}")
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
            print(f"{bcolors.GREEN}✅ Usuário excluído com sucesso!{bcolors.ENDC}") 
        elif opcao == "n":
            print(f"{bcolors.YELLOW}⚠️  Exclusão cancelada.{bcolors.ENDC}")
        else:
            print(f"{bcolors.RED}❌ Opção inválida. Digite 's' ou 'n'.{bcolors.ENDC}")
    else:
        # Excluir dependencias em tbl_pessoa_fisica e tbl_estabelecimentos
        cursor.execute("""DELETE FROM tbl_pessoa_fisica WHERE fk_usuario_pessoa = %s""", (excluir_usuario,))
        cursor.execute("""DELETE FROM tbl_estabelecimentos WHERE fk_usuario_estabelecimento = %s""", (excluir_usuario,))
        # Excluir usuario
        cursor.execute("""DELETE FROM tbl_usuarios WHERE id_usuario = %s""", (excluir_usuario,))
        conexao.commit()
        print(f"{bcolors.GREEN}✅ Usuário excluído com sucesso!{bcolors.ENDC}")



    cursor.close()
    fechar_conexao(conexao)
    return


def menu():
    opcoes = {
        "1": ("Criar usuário", criar_usuario),
        "2": ("Listar usuários", listar_usuarios),
        "3": ("Atualizar usuário", atualizar_usuario),
        "4": ("Excluir usuário", excluir_usuario),
    }

    while True:
        print("\n=== MENU USUÁRIOS ===")
        for codigo, (descricao, _) in opcoes.items():
            print(f"{bcolors.CYAN}{codigo} - {descricao}{bcolors.ENDC}")
        print(f"{bcolors.RED}0 - Sair{bcolors.ENDC}")

        escolha = input("Escolha uma opcao: ").strip()

        if escolha == "0":
            print(f"{bcolors.YELLOW}⚠️  Saindo do sistema.{bcolors.ENDC}")
            break

        if escolha in opcoes:
            descricao, funcao = opcoes[escolha]
            print(f"{bcolors.BOLD}\nSelecionado: {descricao}{bcolors.ENDC}")
            funcao()
        else:
            print(f"{bcolors.RED}❌ Opcao invalida. Tente novamente.{bcolors.ENDC}")