import matplotlib.pyplot as plt
import networkx as nx
from itertools import combinations
from matplotlib.patches import Patch


def domina_tudo(mapa, salas_escolhidas):
    salas_cobertas = set()

    for sala in salas_escolhidas:
        salas_cobertas.add(sala)
        salas_cobertas.update(mapa[sala])

    return salas_cobertas == set(mapa.keys())


def achar_melhor_conjunto(mapa):
    salas = list(mapa.keys())

    for tam_grupo in range(1, len(salas) + 1):
        for grupo in combinations(salas, tam_grupo):
            if domina_tudo(mapa, grupo):
                return set(grupo)

    return set(salas)


def pedir_total_de_salas():
    while True:
        try:
            total = int(input("Digite a quantidade de comodos: ").strip())
            if total > 0:
                return total
            print("A quantidade precisa ser maior que zero.")
        except ValueError:
            print("Digite um numero inteiro.")


def pedir_nomes_das_salas(total):
    salas = []

    print("\nAgora informe o nome de cada comodo.")
    for posicao in range(total):
        while True:
            nome_sala = input(f"Comodo {posicao + 1}: ").strip()

            if not nome_sala:
                print("Esse campo nao pode ficar vazio.")
                continue

            if nome_sala in salas:
                print("Esse comodo ja foi cadastrado.")
                continue

            salas.append(nome_sala)
            break

    return salas


def pedir_conexoes(salas):
    mapa = {}

    print("\nDigite os vizinhos de cada comodo.")
    print("Se houver mais de um, separe por virgula.")
    print("Se um comodo nao tiver vizinhos, digite nenhum.")

    for sala_atual in salas:
        while True:
            texto = input(f"Vizinhos de {sala_atual}: ").strip()

            if not texto:
                print("Informe os vizinhos ou escreva nenhum.")
                continue

            if texto.lower() == "nenhum":
                mapa[sala_atual] = []
                break

            vizinhos = [nome.strip() for nome in texto.split(",") if nome.strip()]
            vizinhos_invalidos = [nome for nome in vizinhos if nome not in salas or nome == sala_atual]

            if vizinhos_invalidos:
                print("Tem nome invalido na lista. Use apenas comodos ja cadastrados.")
                continue

            mapa[sala_atual] = list(dict.fromkeys(vizinhos))
            break

    return mapa


def descobrir_cobertura(mapa, roteadores):
    cobertura = set()

    for sala in roteadores:
        cobertura.add(sala)
        cobertura.update(mapa[sala])

    return cobertura


def mostrar_resultado(salas, mapa, roteadores):
    cobertura = descobrir_cobertura(mapa, roteadores)
    taxa = (len(roteadores) / len(salas)) * 100

    print("\nResultado final")
    print("-" * 50)
    print("Comodos escolhidos para instalar roteador:", ", ".join(sorted(roteadores)))
    print("Quantidade de roteadores:", len(roteadores))
    print("Comodos cobertos:", ", ".join(sorted(cobertura)))
    print(f"Taxa de cobertura com roteador instalado: {taxa:.1f}%")


def mostrar_grafo(mapa, roteadores):
    rede = nx.Graph()

    for sala in mapa:
        rede.add_node(sala)

    for sala, vizinhos in mapa.items():
        for vizinho in vizinhos:
            rede.add_edge(sala, vizinho)

    cores = ["crimson" if sala in roteadores else "skyblue" for sala in rede.nodes()]

    plt.figure(figsize=(11, 7))
    posicoes = nx.spring_layout(rede, seed=9)

    nx.draw_networkx_nodes(rede, posicoes, node_color=cores, node_size=2200)
    nx.draw_networkx_edges(rede, posicoes, width=2, alpha=0.7)
    nx.draw_networkx_labels(rede, posicoes, font_size=10, font_weight="bold")

    legenda = [
        Patch(facecolor="crimson", label="Comodo com roteador"),
        Patch(facecolor="skyblue", label="Comodo sem roteador"),
    ]

    plt.legend(handles=legenda, loc="upper left")
    plt.title("Representacao do conjunto dominante minimo")
    plt.axis("off")
    plt.tight_layout()
    plt.show()


def main():
    print("TRABALHO - CONJUNTO DOMINANTE")
    print("Aplicacao para distribuir roteadores no ambiente")
    print("=" * 50)

    total_salas = pedir_total_de_salas()
    salas = pedir_nomes_das_salas(total_salas)
    mapa = pedir_conexoes(salas)

    roteadores = achar_melhor_conjunto(mapa)
    mostrar_resultado(salas, mapa, roteadores)

    print("\nGerando o grafo da solucao...")
    mostrar_grafo(mapa, roteadores)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nPrograma encerrado pelo usuario.")
    except Exception as erro:
        print(f"\nOcorreu um erro na execucao: {erro}")
