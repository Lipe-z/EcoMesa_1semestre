# Projeto ExpoTech - 3 ponto
# PROJETO EcoMesa
# CRUD completo (Usuarios e Doações)
# Entrega - dia 23/05/2026


# USUARIOS

def criar_usuario():
    # Exercicio 1: cadastrar um novo usuario na tabela tbl_usuarios (tipo, entidade, nome, email, senha).
    return


def listar_usuarios():
    # Exercicio 2: listar todos os usuarios cadastrados com id, nome, email, tipo e entidade.
    return


def atualizar_usuario():
    # Exercicio 3: atualizar nome e/ou email de um usuario existente por id.
    return


def excluir_usuario():
    # Exercicio 4: excluir um usuario por id, tratando dependencias em tbl_pessoa_fisica e tbl_estabelecimentos.
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