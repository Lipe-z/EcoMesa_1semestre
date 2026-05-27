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

import CRUD_usuarios
import CRUD_doacoes

def menu_principal():
    while True:
        print("\n========== PROJETO ECOMESA ==========")
        print(f"{bcolors.CYAN}1 - CRUD de Usuários{bcolors.ENDC}")
        print(f"{bcolors.GREEN}2 - CRUD de Doações{bcolors.ENDC}")
        print(f"{bcolors.RED}0 - Sair{bcolors.ENDC}")

        opcao = input("Escolha uma opcao: ").strip()

        if opcao == "1":
            CRUD_usuarios.menu()
        elif opcao == "2":
            CRUD_doacoes.menu()
        elif opcao == "0":
            print("Encerrando o sistema.")
            break
        else:
            print("Opcao invalida. Tente novamente.")


if __name__ == "__main__":
    menu_principal()

