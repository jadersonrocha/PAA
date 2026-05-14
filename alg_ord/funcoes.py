
from tkinter import messagebox

# Bubble Sort 
def bubbleSort(lista): 
    comparacoes = 0 # conta o numero de comprações
    n = len(lista)

    for i in range(n):
        for j in range(0, n - i - 1): # Percorremos a lista com j sendo o índice do elemento atual
            comparacoes += 1
            if lista[j] > lista[j + 1]: # Se o elemento atual é maior que o próximo elemento
                lista[j], lista[j + 1] = lista[j + 1], lista[j] # Trocamos os elementos de lugar.

    return lista, comparacoes

#Insertion Sort 
def insertionSort(lista):         
    comparacoes = 0

    for j in range(1, len(lista)):
        chave = lista[j]
        i = j - 1        
        # Compara a chave com elementos anteriores
        while i >= 0 and chave < lista[i]:
            comparacoes += 1
            lista[i + 1] = lista[i]
            i -= 1
        lista[i + 1] = chave

    return lista, comparacoes

# mergeSort
def mergeSort(lista):
    comparacoes = 0

    def ordenar(valores):  
        nonlocal comparacoes

        if len(valores) <= 1:
            return valores

        meio = len(valores) // 2
        esquerda = ordenar(valores[:meio])
        direita = ordenar(valores[meio:])

        resultado = []
        i = 0
        j = 0

        while i < len(esquerda) and j < len(direita):
            comparacoes += 1
            if esquerda[i] < direita[j]:
                resultado.append(esquerda[i])
                i += 1
            else:
                resultado.append(direita[j])
                j += 1

        resultado.extend(esquerda[i:])
        resultado.extend(direita[j:])
        return resultado

    return ordenar(lista), comparacoes


def lista_crescente(tamanho):
    return list(range(1, tamanho + 1))


def lista_decrescente(tamanho):
    return list(range(tamanho, 0, -1))

def lista_aleatoria(tamanho):
    import random
    return [random.randint(1, 100) for _ in range(tamanho)]



# Geração e Análise

def gerar_lista(tipo_lista, tamanho=None, entrada_custom=None):
    """
    Gera uma lista de acordo com as opções especificadas.   
   
    """
    
    # Verificar se há entrada personalizada
    if entrada_custom and entrada_custom.strip():
        try:
            lista = [int(x.strip()) for x in entrada_custom.split(",")]
            return lista, None
        except ValueError:
            return None, "Entrada personalizada inválida! Use números separados por vírgula."
    
    # Validar tamanho
    if tamanho is None:
        return None, "Tamanho não especificado!"
    
    try:
        tamanho = int(tamanho)
        if tamanho <= 0:
            return None, "O tamanho deve ser maior que 0!"
    except (ValueError, TypeError):
        return None, "Tamanho inválido!"
    
    # Gerar lista baseado no tipo
    if tipo_lista == "crescente":
        return lista_crescente(tamanho), None
    elif tipo_lista == "decrescente":
        return lista_decrescente(tamanho), None
    else:  # aleatoria
        return lista_aleatoria(tamanho), None


def executar_comparacao(lista, executar_bubble=True, executar_insertion=True, executar_mergesort = True):
    """
    Executa a comparação entre algoritmos de ordenação. 
    
    """
    import time
    
    resultados = {}
    
    if executar_bubble:
        inicio = time.time()
        lista_copia = lista.copy()
        resultado_bubble, comparacoes_bubble = bubbleSort(lista_copia)
        tempo_bubble = time.time() - inicio
        
        resultados['bubble'] = {
            'resultado': resultado_bubble,
            'tempo': tempo_bubble,
            'comparacoes': comparacoes_bubble
        }
    
    if executar_insertion:
        inicio = time.time()
        lista_copia = lista.copy()
        resultado_insertion, comparacoes_insertion = insertionSort(lista_copia)
        tempo_insertion = time.time() - inicio
        
        resultados['insertion'] = {
            'resultado': resultado_insertion,
            'tempo': tempo_insertion,
            'comparacoes': comparacoes_insertion
        }
    
    if executar_mergesort:
        inicio = time.time()
        lista_copia = lista.copy()
        resultado_mergesort, comparacoes_mergesort_real = mergeSort(lista_copia)
        tempo_mergesort = time.time() - inicio
        comparacoes_mergesort = len(lista) * (len(lista).bit_length() - 1) # comparações aproximadas para Merge Sort: n log n, onde log n é o número de níveis na recursão (bit_length - 1)
        
        resultados['mergesort'] = {
            'resultado': resultado_mergesort,
            'tempo': tempo_mergesort,
            'comparacoes': comparacoes_mergesort_real
        }
    
    return resultados


def calcular_desempenho(tempo_bubble, tempo_insertion, tempo_merge):
    """
    Calcula a análise comparativa de desempenho entre dois algoritmos.
    
    """
    if tempo_bubble < tempo_insertion and tempo_bubble < tempo_merge:
        diferenca = tempo_insertion - tempo_bubble
        percentual = (diferenca / tempo_insertion) * 100
        vencedor = "Bubble Sort"
        mais_rapido = True

    elif tempo_merge < tempo_bubble and tempo_merge < tempo_insertion:
        diferenca_bubble = tempo_bubble - tempo_merge
        diferenca_insertion = tempo_insertion - tempo_merge
        percentual_bubble = (diferenca_bubble / tempo_bubble) * 100
        percentual_insertion = (diferenca_insertion / tempo_insertion) * 100
        
        vencedor = "Merge Sort"
        mais_rapido = True
        return {
            'vencedor': vencedor,
            'diferenca_bubble': diferenca_bubble,
            'percentual_bubble': percentual_bubble,
            'diferenca_insertion': diferenca_insertion,
            'percentual_insertion': percentual_insertion,
            'merge_mais_rapido': True
        }

    else:
        diferenca = tempo_bubble - tempo_insertion
        percentual = (diferenca / tempo_bubble) * 100
        vencedor = "Insertion Sort"
        mais_rapido = False
    
    return {
        'vencedor': vencedor,
        'diferenca': diferenca,
        'percentual': percentual,
        'bubble_mais_rapido': mais_rapido
    }




def formatar_resultado(lista, tipo_lista, tamanho, resultados):
    """
    Formata os resultados da comparação em texto estruturado.
    """
    
    texto = "=" * 80 + "\n"
    texto += "ANÁLISE COMPARATIVA DE ALGORITMOS DE ORDENAÇÃO\n"
    texto += "=" * 80 + "\n\n"
    
    texto += f"Tipo de Lista: {tipo_lista.upper()}\n"
    texto += f"Tamanho: {tamanho} elementos\n"
    
    if tamanho <= 20:
        texto += f"Lista: {lista}\n"
    else:
        texto += f"Lista: {lista[:10]}... ({tamanho} elementos)\n"
    
    texto += "\n" + "=" * 80 + "\n\n"
    
    # Bubble Sort
    if 'bubble' in resultados:
        bubble = resultados['bubble']
        texto += "BUBBLE SORT\n"
        texto += "-" * 80 + "\n"
        
        if tamanho <= 20:
            texto += f"Resultado: {bubble['resultado']}\n"
        else:
            texto += f"Resultado: {bubble['resultado'][:10]}...\n"
        
        texto += f"Tempo de Execução: {bubble['tempo']:.6f} segundos\n"
        texto += f"Comparações realizadas: {bubble['comparacoes']}\n"
        texto += "\n"
    
    # Insertion Sort
    if 'insertion' in resultados:
        insertion = resultados['insertion']
        texto += "INSERTION SORT\n"
        texto += "-" * 80 + "\n"
        
        if tamanho <= 20:
            texto += f"Resultado: {insertion['resultado']}\n"
        else:
            texto += f"Resultado: {insertion['resultado'][:10]}...\n"
        
            texto += f"Tempo de Execução: {insertion['tempo']:.6f} segundos\n"
            texto += f"Comparações realizadas: {insertion['comparacoes']}\n"
            texto += "\n"    # Merge Sort
    if 'mergesort' in resultados:
        mergesort = resultados['mergesort']
        texto += "MERGE SORT\n"
        texto += "-" * 80 + "\n"

        if tamanho <= 20:
            texto += f"Resultado: {mergesort['resultado']}\n"
        else:
            texto += f"Resultado: {mergesort['resultado'][:10]}...\n"
            texto += f"Tempo de Execução: {mergesort['tempo']:.6f} segundos\n"
            texto += f"Comparações realizadas: {mergesort['comparacoes']}\n"
            texto += "\n"
    
    # Comparação (2 ou 3 algoritmos)
    tempos_disponiveis = {
        'bubble': resultados.get('bubble', {}).get('tempo'),
        'insertion': resultados.get('insertion', {}).get('tempo'),
        'mergesort': resultados.get('mergesort', {}).get('tempo')
    }
    
    # Filtrar apenas os algoritmos que foram executados
    tempos_filtrados = {k: v for k, v in tempos_disponiveis.items() if v is not None}

      # Se há 2 ou mais algoritmos, fazer comparação
    if len(tempos_filtrados) >= 2:
        texto += "=" * 80 + "\n"
        texto += "AVALIAÇÃO DE DESEMPENHO DOS ALGORITMOS\n"
        texto += "=" * 80 + "\n"
        
        # Encontrar o mais rápido
        algoritmo_mais_rapido = min(tempos_filtrados, key=tempos_filtrados.get)
        melhor_tempo = tempos_filtrados[algoritmo_mais_rapido]
        
        nm_algoritmo = {
            'bubble': 'Bubble Sort',
            'insertion': 'Insertion Sort',
            'mergesort': 'Merge Sort'
        }

        texto += f"O {nm_algoritmo[algoritmo_mais_rapido]} foi o algoritmo mais eficiente!\n"
        texto += f"Com um tempo de execução igual a: {melhor_tempo:.6f} segundos\n\n"
        
        # Comparar com os outros
        for algoritmo, tempo in tempos_filtrados.items():# Comparar cada algoritmo com o mais rápido
            if algoritmo != algoritmo_mais_rapido:
                diferenca = tempo - melhor_tempo
                percentual = (diferenca / melhor_tempo) * 100
                texto += f"{nm_algoritmo[algoritmo]}: {percentual:.2f}% mais lento ({tempo:.6f}s)\n"

        texto += "\n" + "=" * 80 + "\n"
    
    return texto





