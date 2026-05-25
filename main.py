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
    conexao = conectar()
    cursor = conexao.cursor()

    while True:
        try:
            tipo = int(input("Digite o tipo de usuário: \n1 - Doador \n2 - Receptor \n: "))
            if tipo in [1, 2]:
                break
            print("Tipo inválido. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Digite um número inteiro.")

    while True:
        try:
            entidade = int(input("Digite a entidade \n1 - Pessoa Fisica, \n2 - Estabelecimento \n: "))
            if entidade in [1, 2]:
                break
            print("Entidade inválida. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Digite um número inteiro.")

    while True:
        nome = input("Digite seu nome de usuário: ")
        if nome.strip():
            break
        else:
            print("Nome de usuário não pode ser vazio. Tente novamente.")

    while True:
        email = input("Digite seu email: ")
        if email.strip():
            break
        else:
            print("Email não pode ser vazio. Tente novamente.")

    while True:
        senha = input("Digite sua senha: ")
        if senha.strip():
            break
        else:
            print("Senha não pode ser vazia. Tente novamente.")

    while True:
        telefone = input("Digite seu telefone (apenas numeros): ")
        if telefone.isdigit() and len(telefone) == 11:
            break
        else:
            print("Telefone inválido. Digite apenas números.")

    while True:
        endereco = input("Digite seu endereço: ")
        if endereco.strip():
            break
        else:
            print("Endereço não pode ser vazio. Tente novamente.")

    

    cursor.execute("""INSERT INTO tbl_usuarios (tipo_usuario, tipo_entidade, nome_usuario, email_usuario,
                    senha_usuario) VALUES (%s, %s, %s, %s, %s)""", 
                    (tipo, entidade, nome, email, senha))
    
    # Validações adicionais para Pessoa Fisica e Estabelecimento 
    if entidade == 1: #(Pessoa Fisica)
        while True:
            cpf = input("Digite seu CPF (apenas numeros): ")
            if cpf.isdigit() and len(cpf) == 11:
                break
            else:
                print("CPF invalido. Digite um numero de 11 digitos.")
        cursor.execute("""INSERT INTO tbl_pessoa_fisica (nome_pessoa, cpf_pessoa, telefone_pessoa, endereco_pessoa, fk_usuario_pessoa) VALUES (%s, %s, %s, %s, %s)""",
                        (nome, cpf, telefone, endereco, cursor.lastrowid))

    elif entidade == 2: #(Estabelecimento)
        while True:
            cnpj = input("Digite seu CNPJ (apenas numeros): ")
            if cnpj.isdigit() and len(cnpj) == 14:
                break
            else:
                print("CNPJ invalido. Digite um numero de 14 digitos.")
        cursor.execute("""INSERT INTO tbl_estabelecimentos (nome_estabelecimento, cnpj_estabelecimento, telefone_estabelecimento, endereco_estabelecimento, fk_usuario_estabelecimento) VALUES (%s, %s, %s, %s, %s)""",
                    (nome, cnpj, telefone, endereco, cursor.lastrowid))

    conexao.commit()
    print("Usuario criado com sucesso!")
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
        print(f"{bcolors.BLUE}ID:{bcolors.ENDC} {usuario[0]:<2} | {bcolors.CYAN}Nome:{bcolors.ENDC} {usuario[1]:<{maior_nome}} | {bcolors.GREEN}Email: {bcolors.ENDC}{usuario[2]:<{maior_email}} | {bcolors.YELLOW}Tipo: {bcolors.ENDC}{usuario[3]:<2} | {bcolors.PINK}Entidade: {bcolors.ENDC}{usuario[4]}")

    cursor.close()
    fechar_conexao(conexao)
    return


def atualizar_usuario():
    conexao = conectar()
    cursor = conexao.cursor()

    listar_usuarios()
    while True:
        try:
            atualizar_usuario = int(input("\nDigite o ID do usuário que deseja atualizar: "))
            break
        except ValueError:
            print("ID inválido. Digite um número inteiro.")

    while True:
        cursor.execute("""SELECT id_usuario FROM tbl_usuarios WHERE id_usuario = %s""", (atualizar_usuario,))
        if cursor.fetchone():
            break
        else:
            print("ID não encontrado. Tente novamente.")
            return
    while True:
        novo_nome = input("Digite o novo nome do usuário (deixe em branco para manter o atual): ")
        if novo_nome.strip() or novo_nome == "":
            break

    while True:
        novo_email = input("Digite o novo email do usuário (deixe em branco para manter o atual): ")
        if novo_email.strip() or novo_email == "":
            break

    while True:
        nova_senha = input("Digite a nova senha do usuário (deixe em branco para manter a atual): ")
        if nova_senha.strip() or nova_senha == "":
            break

    while True:
        novo_telefone = input("Digite o novo telefone do usuário (deixe em branco para manter o atual): ")
        if novo_telefone.strip() == "" or (novo_telefone.isdigit() and len(novo_telefone) == 11):
            break
        else:
            print("Telefone inválido. Digite apenas números ou deixe em branco para manter o atual.")

    while True:
        novo_endereco = input("Digite o novo endereço do usuário (deixe em branco para manter o atual): ")
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
    print("Usuário atualizado com sucesso!")
    cursor.close()
    fechar_conexao(conexao)
    return


def excluir_usuario():
    conexao = conectar()
    cursor = conexao.cursor()

    listar_usuarios()
    while True:
        try:
            excluir_usuario = int(input("\nDigite o ID do usuário que deseja excluir: "))
            break
        except ValueError:
            print("ID inválido. Digite um número inteiro.")

    while True:
        cursor.execute("""SELECT id_usuario FROM tbl_usuarios WHERE id_usuario = %s""", (excluir_usuario,))
        if cursor.fetchone():
            break
        else:
            print("ID não encontrado. Tente novamente.")
            return
    
    cursor.execute("""SELECT fk_usuario_doacao
                    FROM tbl_doacoes
                    WHERE fk_usuario_doacao = %s""", (excluir_usuario,))
    resultado = cursor.fetchone()
    if resultado:
        print("Usuário possui doações vinculadas. Deseja excluir o usuário e todas as doações associadas? (s/n)")
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
            print("Usuário excluído com sucesso!") 
        else:
            print("Exclusão cancelada.")
    else:
        # Excluir dependencias em tbl_pessoa_fisica e tbl_estabelecimentos
        cursor.execute("""DELETE FROM tbl_pessoa_fisica WHERE fk_usuario_pessoa = %s""", (excluir_usuario,))
        cursor.execute("""DELETE FROM tbl_estabelecimentos WHERE fk_usuario_estabelecimento = %s""", (excluir_usuario,))
        # Excluir usuario
        cursor.execute("""DELETE FROM tbl_usuarios WHERE id_usuario = %s""", (excluir_usuario,))
        conexao.commit()
        print("Usuário excluído com sucesso!")



    cursor.close()
    fechar_conexao(conexao)
    return


# DOAÇÕES

def criar_doacao():
    # Exercicio 5: criar uma doacao e inserir itens na tabela tbl_itens_doacoes com descricao, quantidade e validade.
    conexao = conectar()
    cursor = conexao.cursor()

    listar_usuarios()
    while True:
        try:
            id_usuario = int(input("\nDigite o ID do usuário que está realizando a doação: "))
            break
        except ValueError:
            print("ID inválido. Digite um número inteiro.")

    while True:
        cursor.execute("""SELECT id_usuario FROM tbl_usuarios WHERE id_usuario = %s""", (id_usuario,))
        if cursor.fetchone():
            break
        else:
            print("ID não encontrado. Tente novamente.")
            return
        
    while True:
        data_doacao = input("Digite a data em que a doação foi postada (formato YYYY-MM-DD): ")
        try:
            datetime.strptime(data_doacao, "%Y-%m-%d")
            break
        except ValueError:
            print("Data de doação inválida. Use o formato YYYY-MM-DD.")    
    
    itens = []
    while True:   
        while True:
            descricao = input("Digite a descrição do item a ser doado: ")
            if descricao.strip():
                break
            else:
                print("Descrição não pode ser vazia. Tente novamente.")

        while True:
                quantidade = input("Digite a quantidade do item a ser doado: ")
                if quantidade.strip():
                    break
                else:
                    print("Quantidade não pode ser vazia. Tente novamente.")

        while True:
            validade = input("Digite a data de validade do item (formato YYYY-MM-DD): ")
            try:
                datetime.strptime(validade, "%Y-%m-%d")
                break
            except ValueError:
                print("Data de validade inválida. Use o formato YYYY-MM-DD.")

        itens.append((descricao, quantidade, validade))
        while True:
            continuar = input("Deseja adicionar outro item? (s/n): ").strip().lower()
            if continuar in ["s", "n"]:
                break
            else:
                print("Opcao inválida. Digite s ou n.")
        if continuar == "n":
            break
        
    cursor.execute("""INSERT INTO tbl_doacoes (id_doacao, fk_usuario_doacao, data_doacao) VALUES (DEFAULT, %s, %s)""",
                    (id_usuario, data_doacao))
    
    id_doacao = cursor.lastrowid
    for item in itens:
        cursor.execute("""INSERT INTO tbl_itens_doacoes (descricao_item, quantidade_item, validade_item, fk_doacao_itens) VALUES (%s, %s, %s, %s)""",
                        (item[0], item[1], item[2], id_doacao))
            
    conexao.commit()
    print("Doação criada com sucesso!")
    cursor.close()
    fechar_conexao(conexao)
    return


def listar_doacoes():
    # Exercicio 6: listar todas as doacoes com o nome do doador e seus itens (descricao, quantidade, validade).
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""SELECT tbl_doacoes.id_doacao, tbl_usuarios.nome_usuario, tbl_itens_doacoes.descricao_item, tbl_itens_doacoes.quantidade_item, tbl_itens_doacoes.validade_item
                    FROM tbl_doacoes
                    JOIN tbl_usuarios ON tbl_doacoes.fk_usuario_doacao = tbl_usuarios.id_usuario
                    JOIN tbl_itens_doacoes ON tbl_itens_doacoes.fk_doacao_itens = tbl_doacoes.id_doacao
                    ORDER BY tbl_doacoes.id_doacao""")
    
    doacoes = cursor.fetchall()
    print("""\n=== DOAÇÕES CADASTRADAS ===""")
    for doacao in doacoes:
        print(f"{bcolors.BLUE}ID Doação:{bcolors.ENDC} {doacao[0]:<2} | {bcolors.GREEN}Doador: {bcolors.ENDC}{doacao[1]:<20} | {bcolors.YELLOW}Descrição: {bcolors.ENDC}{doacao[2]:<30} | {bcolors.CYAN}Quantidade: {bcolors.ENDC}{doacao[3]:<5} | {bcolors.PINK}Validade: {bcolors.ENDC}{doacao[4]}")
    
    cursor.close()
    fechar_conexao(conexao)
    return

def listar_itens_doacao(id_doacao):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""SELECT id_item, descricao_item, quantidade_item, validade_item FROM tbl_itens_doacoes WHERE fk_doacao_itens = %s""", (id_doacao,))
    itens = cursor.fetchall()
    for item in itens:
        print(f"ID: {bcolors.BLUE}{item[0]}{bcolors.ENDC} | {bcolors.YELLOW}Descricao: {bcolors.ENDC}{item[1]:<30} | {bcolors.CYAN}Quantidade: {bcolors.ENDC}{item[2]:<5} | {bcolors.PINK}Validade: {bcolors.ENDC}{item[3]}")

    cursor.close()
    fechar_conexao(conexao)
    return

def atualizar_doacao():
    # Exercicio 7: atualizar a data, itens vinculados, validade e/ou quantidade de uma doacao por id.
    conexao = conectar()
    cursor = conexao.cursor(buffered=True)
    
    listar_doacoes()
    while True:
        try:
            atualizar_doacao = int(input("\nDigite o ID da doação que deseja atualizar: "))
            break
        except ValueError:
            print("ID inválido. Digite um número inteiro.")

    while True:
        cursor.execute("""SELECT id_doacao FROM tbl_doacoes WHERE id_doacao = %s""", (atualizar_doacao,))
        if cursor.fetchone():
            break
        else:
            print("ID não encontrado. Tente novamente.")
            return
        
    while True:
        try:
            atualizar_data = input("Digite a nova data da doação (formato YYYY-MM-DD, deixe em branco para manter a atual): ")
            if atualizar_data.strip() == "":
                break
            datetime.strptime(atualizar_data, "%Y-%m-%d")
            break
        except ValueError:
            print("Data de doação inválida. Use o formato YYYY-MM-DD ou deixe em branco para manter a atual.")
        
    while True:
        try:
            atualizar_itens = input("Deseja atualizar os itens da doação? (s/n): ").strip().lower()
            if atualizar_itens in ["s", "n"]:
                break
            else:
                print("Opção inválida. Digite s ou n.")
        except ValueError:
            print("Entrada inválida. Digite s ou n.")
    if atualizar_itens == "s":
        while True:
            listar_itens_doacao(atualizar_doacao)

            while True:
                try:
                    escolha_item = input("Qual item deseja atualizar? (digite o ID): ")
                    break
                except ValueError:
                    print("ID inválido. Digite um número inteiro.")

            cursor.execute("""SELECT id_item FROM tbl_itens_doacoes WHERE id_item = %s AND fk_doacao_itens = %s""", (escolha_item, atualizar_doacao))
            if not cursor.fetchone():
                print("ID do item não encontrado para essa doação. Tente novamente.")
                return

                    
            cursor.execute("""SELECT descricao_item, quantidade_item, validade_item FROM tbl_itens_doacoes WHERE fk_doacao_itens = %s""", (atualizar_doacao,))
            while True:
                    descricao = input("Digite a descrição do item a ser doado: ")
                    if descricao.strip():
                        break
                    else:
                            print("Descrição não pode ser vazia. Tente novamente.")

            while True:
                    quantidade = input("Digite a quantidade do item a ser doado: ")
                    if quantidade.strip():
                        break
                    else:
                        print("Quantidade não pode ser vazia. Tente novamente.")

            while True:
                validade = input("Digite a data de validade do item (formato YYYY-MM-DD): ")
                try:
                    datetime.strptime(validade, "%Y-%m-%d")
                    break
                except ValueError:
                    print("Data de validade invalida. Use o formato YYYY-MM-DD.")

            cursor.execute("""UPDATE tbl_itens_doacoes SET descricao_item = %s, quantidade_item = %s, validade_item = %s WHERE id_item = %s""",
                            (descricao, quantidade, validade, escolha_item))

            while True:
                continuar = input("Deseja atualizar outro item? (s/n): ").strip().lower()
                if continuar in ["s", "n"]:
                    break
                else:
                    print("Opção invalida. Digite s ou n.")
            if continuar == "n":
                break

    if atualizar_data.strip():
        cursor.execute("""UPDATE tbl_doacoes SET data_doacao = %s WHERE id_doacao = %s""",
                    (atualizar_data, atualizar_doacao))
    
    conexao.commit()
    print("Doação atualizada com sucesso!")
    cursor.close()
    fechar_conexao(conexao)
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