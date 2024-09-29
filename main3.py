import random
import json  # Usar JSON para manipular os dados de forma estruturada

usuarios = {}
usuario_atual = None  # Variável global para armazenar o usuário logado
arquivo_usuarios = "usuarios.txt"  # Nome do arquivo para armazenar os dados

# --------------------------------------------------------------------------------------

def salvar_usuarios():
    """Salva os dados dos usuários no arquivo .txt"""
    with open(arquivo_usuarios, 'w') as f:
        json.dump(usuarios, f)
    print("\nDados dos usuários salvos com sucesso!\n")

def carregar_usuarios():
    """Carrega os dados dos usuários do arquivo .txt"""
    global usuarios
    try:
        with open(arquivo_usuarios, 'r') as f:
            conteudo = f.read().strip()
            if conteudo:  # Verifica se o arquivo não está vazio
                usuarios = json.loads(conteudo)
            else:
                usuarios = {}  # Se o arquivo estiver vazio, inicializa um dicionário vazio
        print("\nDados dos usuários carregados com sucesso!\n")
    except FileNotFoundError:
        print("\nNenhum dado de usuário encontrado, começando do zero.\n")
        usuarios = {}  # Inicializa um dicionário vazio se o arquivo não for encontrado


# --------------------------------------------------------------------------------------

def main():
    carregar_usuarios()  # Carregar dados ao iniciar o programa
    while True:
        if usuario_atual is None:
            print("""
>>> MENU RÁPIDO <<<

- Digite o número do sistema que você deseja acessar!

1 - Registro
2 - Login
3 - Finalizar Programa
""")
            opcao = int(input('Escolha uma opção: '))
            match opcao:
                case 1:
                    registro()
                case 2:
                    if login():
                        continue  # Volta para o loop principal, já que o login foi bem-sucedido
                case 3:
                    salvar_usuarios()  # Salvar dados antes de finalizar
                    print("""
Programa Finalizado
""")
                    break
                case _:
                    print('\nOpção inválida')
        else:
            print("""
----------------------------------------------------

- Tudo o que você fizer aqui ficará
salvo na sua conta.

--------------------------------------------------------
    >>> JOGOS <<<

1 - Corrida
2 - Apostar

--------------------------------------------------------
    >>> EXTRAS <<<

3 - Minha Conta
4 - Logout
5 - Terminar Programa

--------------------------------------------------------

    >>> LOJINHA <<<

6 - Mais 5% de sorte de aparecer um Quiz
   ↳ Custo: (1) Moedas

--------------------------------------------------------
""")
            opcao = int(input('Escolha uma opção: '))
            match opcao:
                case 1:
                    corrida()
                case 2:
                    apostar()
                case 3:
                    conta()
                case 4:
                    print("""
Você saiu da sua conta.
""")
                    logout()
                    break
                case 5:
                    salvar_usuarios()  # Salvar dados ao terminar
                    print("Programa Finalizado")
                    break
                case 6:
                    compra1()
                case _:
                    print('Opção inválida')

# --------------------------------------------------------------------------------------

def voltar():
    input(f'Clique ENTER para voltar: ')

def continuar():
    input(f'Clique ENTER para continuar: ')

def logout():
    global usuario_atual
    usuario_atual = None
    continuar()

def voltar_quiz():
    quiz = random.randint(1, 100)
    quiz += usuarios[usuario_atual]['sorte']
    if quiz > 95:
        input(f'Clique ENTER para continuar: ')
        print(f'\nVOCÊ ENCONTROU UMA PERGUNTA MISTERIOSA\n(Raridade: {usuarios[usuario_atual]["sorte"]}% ) | (Padrão: 5%)\n')
        input(f'Clique ENTER para continuar: ')
        pergunta()
    else:
        voltar()

# --------------------------------------------------------------------------------------

def corrida():
    print("\nAinda não há uma integração direta com o nosso site para jogar esse mini-game... \nPorém aqui estão algumas moedas para você adquirir algo na loja.")
    recompensa = random.randint(1, 10)
    print(f"\nVocê recebeu {recompensa} moedas.\n")
    usuarios[usuario_atual]['moedas'] += recompensa
    voltar_quiz()

def apostar():
    print(f"""
--------------------------------------------------------

    >>> NESSE MINI-GAME DE APOSTAS VOCÊ TERÁ: <<<

- 10% de chance de ganhar 10x o valor apostado!
- 40% de chance de ganhar 2x o valor apostado!
- 50% de chance de perder o valor apostado!
""")
    print(f'Você tem {usuarios[usuario_atual]["moedas"]} moedas para apostar!\n')

    quantia = int(input("Sua aposta: "))

    if quantia > usuarios[usuario_atual]['moedas']:
        print("\nVocê não tem todas essas moedas!\n")
        voltar()
    else:
        usuarios[usuario_atual]['moedas'] -= quantia
        aposta = random.randint(1, 10)
        if aposta == 1:
            print("\nVOCÊ GANHOU 10X!!!")
            usuarios[usuario_atual]['moedas'] += quantia * 10
        elif aposta > 1 and aposta < 6:
            print("\nVocê duplicou sua aposta!!!")
            usuarios[usuario_atual]['moedas'] += quantia * 2
        else:
            print("\nVocê não teve sorte dessa vez...")
        print("\n")
    voltar()

# --------------------------------------------------------------------------------------

def pergunta():
    perguntas = [
        ("\nQual equipe venceu a primeira corrida da Fórmula E?\n", "b", ["a) Mahindra Racing", "b) Audi Sport ABT", "c) Nissan e.dams\n"]),
        ("\nQuem foi o primeiro campeão da Fórmula E?\n", "c", ["a) Sebastien Buemi", "b) Lucas di Grassi", "c) Nelson Piquet Jr.\n"]),
        ("\nEm qual cidade ocorreu a primeira corrida da Fórmula E?\n", "a", ["a) Pequim", "b) Nova Iorque", "c) Londres\n"]),
        # Adicione mais perguntas conforme necessário
    ]

    pergunta, resposta_correta, opcoes = random.choice(perguntas)

    print("""
----------------------------------------------------
              
RESPONDA UTILIZANDO "a", "b" ou "c" """)
    print(pergunta)
    for opcao in opcoes:
        print(opcao)
    resposta = input("Escolha a resposta correta: ")
    if resposta == resposta_correta:
        print("\nResposta correta!\n")
        recompensa = random.randint(1, 10)
        print(f"Você recebeu {recompensa} moedas.\n")
        usuarios[usuario_atual]['moedas'] += recompensa
    else:
        print("\nResposta incorreta!\n")
    voltar()

# --------------------------------------------------------------------------------------

def registro():
    print("\n\n>>> Registro <<<")
    while True:
        usuario = input("\nDigite um nome de usuário: ").strip()
        if usuario in usuarios:
            print("\nEsse nome já foi cadastrado. Tente outro.\n")
        else:
            break
    senha = input("\nDigite uma senha: ").strip()
    usuarios[usuario] = {'senha': senha, 'moedas': 100, 'sorte': 5}
    print(f"\nUsuário {usuario} registrado com sucesso!\n")
    voltar()

def login():
    global usuario_atual
    print("\n\n>>> Login <<<")
    usuario = input("\nDigite seu nome de usuário: ").strip()
    if usuario not in usuarios:
        print("\nNome de usuário não encontrado.\n")
        voltar()
        return False

    senha = input("\nDigite sua senha: ").strip()
    if usuarios[usuario]['senha'] == senha:
        usuario_atual = usuario
        print(f"\nBem-vindo, {usuario}!\n")
        return True
    else:
        print("\nSenha incorreta.\n")
        voltar()
        return False

# --------------------------------------------------------------------------------------

def conta():
    print("\n>>> MINHA CONTA <<<")
    usuario = usuario_atual
    senha = usuarios[usuario_atual]['senha']
    moedas = usuarios[usuario_atual]['moedas']
    sorte = usuarios[usuario_atual]['sorte']

    # Exibir informações da conta
    print(f"\nUsuário: {usuario}")
    print(f"Senha: {'*' * len(senha)}")
    print(f"\nVocê tem: {moedas} Moedas!" if moedas > 0 else "Hmm... Parece que você não tem nenhuma moeda!")
    print(f"Sua Chance de aparecer um Quiz: {sorte}%\n" if sorte > 5 else "Sua Chance de aparecer um Quiz: 5% (Padrão)\n")

    voltar()

# --------------------------------------------------------------------------------------

def compra1():
    if usuarios[usuario_atual]['moedas'] < 1:
        print("\nVocê não tem moedas suficientes.\n")
        voltar()
    else:
        if usuarios[usuario_atual]['sorte'] > 95:
            print("\nSeu nível de sorte já está no máximo.\n")
            voltar()
        else:
            usuarios[usuario_atual]['sorte'] += 5
            usuarios[usuario_atual]['moedas'] -= 1
            print("\nCompra Efetuada com Sucesso!\n")
            voltar()

# --------------------------------------------------------------------------------------

main()
