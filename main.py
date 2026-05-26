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
        nome = input(f"{bcolors.CYAN}Digite seu nome de usuário: {bcolors.ENDC}")
        if nome.strip():
            break
        else:
            print(f"{bcolors.RED}❌ Nome de usuário não pode ser vazio. Tente novamente.{bcolors.ENDC}")

    while True:
        email = input(f"{bcolors.CYAN}Digite seu email: {bcolors.ENDC}")
        if email.strip():
            break
        else:
            print(f"{bcolors.RED}❌ Email não pode ser vazio. Tente novamente.{bcolors.ENDC}")

    while True:
        senha = input(f"{bcolors.CYAN}Digite sua senha: {bcolors.ENDC}")
        if senha.strip():
            break
        else:
            print(f"{bcolors.RED}❌ Senha não pode ser vazia. Tente novamente.{bcolors.ENDC}")

    while True:
        telefone = input(f"{bcolors.CYAN}Digite seu telefone (apenas numeros): {bcolors.ENDC}")
        if telefone.isdigit() and len(telefone) == 11:
            break
        else:
            print(f"{bcolors.RED}❌ Telefone inválido. Digite apenas números.{bcolors.ENDC}")

    while True:
        endereco = input(f"{bcolors.CYAN}Digite seu endereço: {bcolors.ENDC}")
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
            cpf = input(f"{bcolors.CYAN}Digite seu CPF (apenas numeros): {bcolors.ENDC}")
            if cpf.isdigit() and len(cpf) == 11:
                break
            else:
                print(f"{bcolors.RED}❌ CPF inválido. Digite um número de 11 dígitos.{bcolors.ENDC}")
        cursor.execute("""INSERT INTO tbl_pessoa_fisica (nome_pessoa, cpf_pessoa, telefone_pessoa, endereco_pessoa, fk_usuario_pessoa) VALUES (%s, %s, %s, %s, %s)""",
                        (nome, cpf, telefone, endereco, id_novo_usuario))

    elif entidade == 2: #(Estabelecimento)
        while True:
            cnpj = input(f"{bcolors.CYAN}Digite seu CNPJ (apenas numeros): {bcolors.ENDC}")
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
            atualizar_usuario = int(input(f"\n{bcolors.CYAN}Digite o ID do usuário que deseja atualizar: {bcolors.ENDC}"))
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
        novo_nome = input(f"{bcolors.CYAN}Digite o novo nome do usuário (deixe em branco para manter o atual): {bcolors.ENDC}")
        if novo_nome.strip() or novo_nome == "":
            break

    while True:
        novo_email = input(f"{bcolors.CYAN}Digite o novo email do usuário (deixe em branco para manter o atual): {bcolors.ENDC}")
        if novo_email.strip() or novo_email == "":
            break

    while True:
        nova_senha = input(f"{bcolors.CYAN}Digite a nova senha do usuário (deixe em branco para manter a atual): {bcolors.ENDC}")
        if nova_senha.strip() or nova_senha == "":
            break

    while True:
        novo_telefone = input(f"{bcolors.CYAN}Digite o novo telefone do usuário (deixe em branco para manter o atual): {bcolors.ENDC}")
        if novo_telefone.strip() == "" or (novo_telefone.isdigit() and len(novo_telefone) == 11):
            break
        else:
            print(f"{bcolors.RED}❌ Telefone inválido. Digite apenas números ou deixe em branco para manter o atual.{bcolors.ENDC}")

    while True:
        novo_endereco = input(f"{bcolors.CYAN}Digite o novo endereço do usuário (deixe em branco para manter o atual): {bcolors.ENDC}")
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
    cursor = conexao.cursor()

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
        else:
            print(f"{bcolors.YELLOW}⚠️  Exclusão cancelada.{bcolors.ENDC}")
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


# DOAÇÕES

def criar_doacao():
    # Exercicio 5: criar uma doacao e inserir itens na tabela tbl_itens_doacoes com descricao, quantidade e validade.
    conexao = conectar()
    cursor = conexao.cursor()

    listar_usuarios()
    while True:
        try:
            id_usuario = int(input(f"{bcolors.CYAN}\nDigite o ID do usuário que está realizando a doação: {bcolors.ENDC}"))
            break
        except ValueError:
            print(f"{bcolors.RED}❌ ID inválido. Digite um número inteiro.{bcolors.ENDC}")

    while True:
        cursor.execute("""SELECT id_usuario FROM tbl_usuarios WHERE id_usuario = %s""", (id_usuario,))
        if cursor.fetchone():
            break
        else:
            print(f"{bcolors.RED}❌ ID não encontrado. Tente novamente.{bcolors.ENDC}")
            return
        
    while True:
        data_doacao = input(f"{bcolors.CYAN}Digite a data em que a doação foi postada (formato YYYY-MM-DD): {bcolors.ENDC}")
        try:
            datetime.strptime(data_doacao, "%Y-%m-%d")
            break
        except ValueError:
            print(f"{bcolors.RED}❌ Data de doação inválida. Use o formato YYYY-MM-DD.{bcolors.ENDC}")    
    
    itens = []
    while True:   
        while True:
            descricao = input(f"{bcolors.CYAN}Digite a descrição do item a ser doado: {bcolors.ENDC}")
            if descricao.strip():
                break
            else:
                print(f"{bcolors.RED}❌ Descrição não pode ser vazia. Tente novamente.{bcolors.ENDC}")

        while True:
                quantidade = input(f"{bcolors.CYAN}Digite a quantidade do item a ser doado: {bcolors.ENDC}")
                if quantidade.strip():
                    break
                else:
                    print(f"{bcolors.RED}❌ Quantidade não pode ser vazia. Tente novamente.{bcolors.ENDC}")

        while True:
            validade = input(f"{bcolors.CYAN}Digite a data de validade do item (formato YYYY-MM-DD): {bcolors.ENDC}")
            try:
                datetime.strptime(validade, "%Y-%m-%d")
                break
            except ValueError:
                print(f"{bcolors.RED}❌ Data de validade inválida. Use o formato YYYY-MM-DD.{bcolors.ENDC}")

        itens.append((descricao, quantidade, validade))
        while True:
            continuar = input(f"{bcolors.CYAN}Deseja adicionar outro item? (s/n): {bcolors.ENDC}").strip().lower()
            if continuar in ["s", "n"]:
                break
            else:
                print(f"{bcolors.RED}❌ Opção inválida. Digite s ou n.{bcolors.ENDC}")
        if continuar == "n":
            break
        
    cursor.execute("""INSERT INTO tbl_doacoes (id_doacao, fk_usuario_doacao, data_doacao) VALUES (DEFAULT, %s, %s)""",
                    (id_usuario, data_doacao))
    
    id_doacao = cursor.lastrowid
    for item in itens:
        cursor.execute("""INSERT INTO tbl_itens_doacoes (descricao_item, quantidade_item, validade_item, fk_doacao_itens) VALUES (%s, %s, %s, %s)""",
                        (item[0], item[1], item[2], id_doacao))
            
    conexao.commit()
    print(f"{bcolors.GREEN}✅ Doação criada com sucesso!{bcolors.ENDC}")
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
    
    maior_id = max(len(str(doacao[0])) for doacao in doacoes)
    maior_doador = max(len(doacao[1]) for doacao in doacoes)
    maior_descricao = max(len(doacao[2]) for doacao in doacoes)
    maior_quantidade = max(len(str(doacao[3])) for doacao in doacoes)
    print("""\n=== DOAÇÕES CADASTRADAS ===""")
    for doacao in doacoes:
        print(f"{bcolors.BLUE}ID Doação:{bcolors.ENDC} {doacao[0]:{maior_id}} {bcolors.CYAN}| Doador: {bcolors.ENDC}{doacao[1]:{maior_doador}} {bcolors.GREEN}| Descrição: {bcolors.ENDC}{doacao[2]:{maior_descricao}} {bcolors.YELLOW}| Quantidade: {bcolors.ENDC}{doacao[3]:{maior_quantidade}} {bcolors.PINK}| Validade: {bcolors.ENDC}{doacao[4]}")
    
    cursor.close()
    fechar_conexao(conexao)
    return

def listar_itens_doacao(id_doacao):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""SELECT id_item, descricao_item, quantidade_item, validade_item FROM tbl_itens_doacoes WHERE fk_doacao_itens = %s""", (id_doacao,))
    itens = cursor.fetchall()
    
    maior_id = max(len(str(item[0])) for item in itens)
    maior_descricao = max(len(item[1]) for item in itens)
    maior_quantidade = max(len(str(item[2])) for item in itens)
    print("\n=== ITENS DA DOAÇÃO SELECIONADA ===")
    for item in itens:
        print(f"{bcolors.BLUE}ID:{bcolors.ENDC} {item[0]:{maior_id}} {bcolors.GREEN}| Descricao:{bcolors.ENDC} {item[1]:{maior_descricao}} {bcolors.YELLOW}| Quantidade: {bcolors.ENDC}{item[2]:{maior_quantidade}} {bcolors.PINK}| Validade: {bcolors.ENDC}{item[3]}")

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
            atualizar_doacao = int(input(f"{bcolors.CYAN}\nDigite o ID da doação que deseja atualizar: {bcolors.ENDC}"))
            break
        except ValueError:
            print(f"{bcolors.RED}❌ ID inválido. Digite um número inteiro.{bcolors.ENDC}")

    while True:
        cursor.execute("""SELECT id_doacao FROM tbl_doacoes WHERE id_doacao = %s""", (atualizar_doacao,))
        if cursor.fetchone():
            break
        else:
            print(f"{bcolors.RED}❌ ID não encontrado. Tente novamente.{bcolors.ENDC}")
            return
        
    while True:
        try:
            atualizar_data = input(f"{bcolors.CYAN}Digite a nova data da doação (formato YYYY-MM-DD, deixe em branco para manter a atual): {bcolors.ENDC}")
            if atualizar_data.strip() == "":
                break
            datetime.strptime(atualizar_data, "%Y-%m-%d")
            break
        except ValueError:
            print(f"{bcolors.RED}❌ Data de doação inválida. Use o formato YYYY-MM-DD ou deixe em branco para manter a atual.{bcolors.ENDC}")
        
    while True:
        try:
            atualizar_itens = input(f"{bcolors.CYAN}Deseja atualizar os itens da doação? (s/n): {bcolors.ENDC}").strip().lower()
            if atualizar_itens in ["s", "n"]:
                break
            else:
                print(f"{bcolors.RED}❌ Opção inválida. Digite s ou n.{bcolors.ENDC}")
        except ValueError:
            print(f"{bcolors.RED}❌ Entrada inválida. Digite s ou n.{bcolors.ENDC}")
    if atualizar_itens == "s":
        while True:
            listar_itens_doacao(atualizar_doacao)

            while True:
                try:
                    escolha_item = input(f"{bcolors.CYAN}Qual item deseja atualizar? (digite o ID): {bcolors.ENDC}")
                    break
                except ValueError:
                    print(f"{bcolors.RED}❌ ID inválido. Digite um número inteiro.{bcolors.ENDC}")

            cursor.execute("""SELECT id_item FROM tbl_itens_doacoes WHERE id_item = %s AND fk_doacao_itens = %s""", (escolha_item, atualizar_doacao))
            if not cursor.fetchone():
                print(f"{bcolors.RED}❌ ID do item não encontrado para essa doação. Tente novamente.{bcolors.ENDC}")
                return
                   
            while True:
                    descricao = input(f"{bcolors.CYAN}Digite a descrição do item a ser doado{bcolors.ENDC} {bcolors.YELLOW}(deixe em branco para manter a atual): {bcolors.ENDC}")
                    if descricao.strip() or descricao == "":
                        break

            while True:
                    quantidade = input(f"{bcolors.CYAN}Digite a quantidade do item a ser doado{bcolors.ENDC} {bcolors.YELLOW}(deixe em branco para manter a atual): {bcolors.ENDC}")
                    if quantidade.strip() or quantidade == "":
                        break

            while True:
                validade = input(f"{bcolors.CYAN}Digite a data de validade do item (formato YYYY-MM-DD){bcolors.ENDC} {bcolors.YELLOW}(deixe em branco para manter a atual): {bcolors.ENDC}")
                if validade.strip() == "":
                    break
                try:
                    datetime.strptime(validade, "%Y-%m-%d")
                    break
                except ValueError:
                    print(f"{bcolors.RED}❌ Data de validade inválida. Use o formato YYYY-MM-DD.{bcolors.ENDC}")

            # cursor.execute("""UPDATE tbl_itens_doacoes SET descricao_item = %s, quantidade_item = %s, validade_item = %s WHERE id_item = %s""",
            #                 (descricao, quantidade, validade, escolha_item))

            cursor.execute("""SELECT descricao_item, quantidade_item, validade_item FROM tbl_itens_doacoes WHERE id_item = %s""", (escolha_item,))
            atual_item = cursor.fetchone()

            descricao = descricao if descricao.strip() else atual_item[0]
            quantidade = quantidade if quantidade.strip() else atual_item[1]
            validade = validade if validade.strip() else atual_item[2]

            cursor.execute("""UPDATE tbl_itens_doacoes SET descricao_item = %s, quantidade_item = %s, validade_item = %s WHERE id_item = %s""",
                            (descricao, quantidade, validade, escolha_item))

            while True:
                continuar = input(f"{bcolors.CYAN}Deseja atualizar outro item? (s/n): {bcolors.ENDC}").strip().lower()
                if continuar in ["s", "n"]:
                    break
                else:
                    print(f"{bcolors.RED}❌ Opção inválida. Digite s ou n.{bcolors.ENDC}")
            if continuar == "n":
                break

    if atualizar_data.strip():
        cursor.execute("""UPDATE tbl_doacoes SET data_doacao = %s WHERE id_doacao = %s""",
                    (atualizar_data, atualizar_doacao))
    
    conexao.commit()
    print(f"{bcolors.GREEN}✅ Doação atualizada com sucesso!{bcolors.ENDC}")
    cursor.close()
    fechar_conexao(conexao)
    return


def excluir_doacao():
    # Exercicio 8: excluir uma doacao por id, removendo primeiro os itens de tbl_itens_doacoes.
    conexao = conectar()
    cursor = conexao.cursor()

    listar_doacoes()
    while True:
        try:
            id_doacao = int(input(f"\n{bcolors.CYAN}Digite o ID da doação que deseja excluir: {bcolors.ENDC}"))
            break
        except ValueError:
            print(f"{bcolors.RED}❌ ID inválido. Digite um número inteiro.{bcolors.ENDC}")

    while True:
        cursor.execute("""SELECT id_doacao FROM tbl_doacoes WHERE id_doacao = %s""", (id_doacao,))
        if cursor.fetchone():
            break
        else:
            print(f"{bcolors.RED}❌ ID não encontrado. Tente novamente.{bcolors.ENDC}")
            return
        
    cursor.execute("""DELETE FROM tbl_itens_doacoes WHERE fk_doacao_itens = %s""", (id_doacao,))
    cursor.execute("""DELETE FROM tbl_doacoes WHERE id_doacao = %s""", (id_doacao,))

    conexao.commit()
    print(f"{bcolors.GREEN}✅ Doação excluída com sucesso!{bcolors.ENDC}")
    cursor.close()
    fechar_conexao(conexao)
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
        print("\n=== MENU EcoMesa ===")
        for codigo, (descricao, _) in opcoes.items():
            if int(codigo) <= 4:                      #Diferenciar as opções de usuário e doação por cor
                cor = bcolors.CYAN                    # 🟦 = Ciano para usuários
            else:
                cor = bcolors.GREEN                   # 🟩 = Verde para doações
            print(f"{cor}{codigo} - {descricao}{bcolors.ENDC}")
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


menu()