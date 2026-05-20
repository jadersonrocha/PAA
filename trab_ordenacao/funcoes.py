import random
import time

# Bubble Sort 
def bubbleSort(lista): 
    comparacoes = 0 # conta o numero de comprações
    trocas = 0
    n = len(lista)

    for i in range(n):
        for j in range(0, n - i - 1): # Percorremos a lista com j sendo o índice do elemento atual
            comparacoes += 1
            if lista[j] > lista[j + 1]: # Se o elemento atual é maior que o próximo elemento
                lista[j], lista[j + 1] = lista[j + 1], lista[j] # Trocamos os elementos de lugar.
                trocas += 1

    return lista, comparacoes, trocas

#Insertion Sort 
def insertionSort(lista):         
    comparacoes = 0
    trocas = 0

    for j in range(1, len(lista)):
        chave = lista[j]
        i = j - 1        
        # Compara a chave com elementos anteriores
        while i >= 0:
            comparacoes += 1 # contagem das comparações
            if chave < lista[i]:
                lista[i + 1] = lista[i]
                trocas += 1
                i -= 1
            else:
                break
        lista[i + 1] = chave

    return lista, comparacoes, trocas

# mergeSort
def mergeSort(lista):
    comparacoes = 0
    trocas = 0

    def ordenar(valores):  
        nonlocal comparacoes, trocas

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
            trocas += 1

        resultado.extend(esquerda[i:])
        trocas += len(esquerda) - i
        resultado.extend(direita[j:])
        trocas += len(direita) - j
        return resultado

    return ordenar(lista), comparacoes, trocas

# função usada pela heapsort
def heapify(lista, n, i, comparacoes, trocas):
    maior_elemento = i
    ld_esq = 2 * i + 1 # índice do filho da esquerda
    ld_dir = 2 * i + 2 # índice do filho da direita
    
    # verificar o filho da esquerda
    if ld_esq < n:
        comparacoes[0] += 1
        if lista[ld_esq] > lista[maior_elemento]:
            maior_elemento = ld_esq

    # verificar o filho da direita
    if ld_dir < n:
        comparacoes[0] += 1
        if lista[ld_dir] > lista[maior_elemento]:
            maior_elemento = ld_dir

    # caso o maior elemento nao seja a raiz
    if maior_elemento != i:
        lista[i], lista[maior_elemento] = lista[maior_elemento], lista[i] #realizar a troca 
        trocas[0] += 1
        heapify(lista, n, maior_elemento, comparacoes, trocas) # realiza a recursão

def heapSort(lista):
    n = len(lista)
    comparacoes = [0]
    trocas = [0]

    for i in range(n // 2 - 1, -1, -1): # Construir o heap
        heapify(lista, n, i, comparacoes, trocas) # Realizar a ordenação

    for i in range(n - 1, 0, -1): # Extrair elementos do heap
        lista[0], lista[i] = lista[i], lista[0] # Troca o maior elemento com o ultimo elemento  do heap
        trocas[0] += 1
        heapify(lista, i, 0, comparacoes, trocas) # 
    
    return lista, comparacoes[0], trocas[0]    # Geração de Listas

def quick_sort(vetor):
    comparacoes = [0]
    trocas = [0]

    def trocar(i, j):
        if i != j:
            vetor[i], vetor[j] = vetor[j], vetor[i]
            trocas[0] += 1

    def particionar(inicio, fim):
        # Escolhe pivô aleatório e coloca no fim
        indice_pivo = random.randint(inicio, fim)
        trocar(indice_pivo, fim)

        pivo = vetor[fim]
        i = inicio - 1

        for j in range(inicio, fim):
            comparacoes[0] += 1
            if vetor[j] <= pivo:
                i += 1
                trocar(i, j)

        trocar(i + 1, fim)
        return i + 1

    def quicksort_rec(inicio, fim):
        if inicio < fim:
            posicao_pivo = particionar(inicio, fim)
            quicksort_rec(inicio, posicao_pivo - 1)
            quicksort_rec(posicao_pivo + 1, fim)

    quicksort_rec(0, len(vetor) - 1)
    return vetor, comparacoes[0], trocas[0]


def algoritmo_hibrido(lista): 
   
    comparacoes = [0]
    trocas = [0]
    limite_troca = 32
    arr = lista  
    
    def insertion_sort_parcial(a, esq, dir):
        """Insertion Sort para sublistas pequenas"""
        for j in range(esq + 1, dir + 1):
            chave = a[j]
            i = j - 1
            while i >= esq:
                comparacoes[0] += 1
                if a[i] > chave:
                    a[i + 1] = a[i] 
                    trocas[0] += 1
                    i -= 1
                else:
                    break
            a[i + 1] = chave

    def quick_sort_hibrido(esq, dir):
        if dir - esq + 1 <= limite_troca:
            insertion_sort_parcial(arr, esq, dir)
        elif esq < dir:
            # Escolher pivô aleatório
            pivot_index = random.randint(esq, dir)
            arr[pivot_index], arr[dir] = arr[dir], arr[pivot_index]
            pivot = arr[dir]
            i = esq - 1
            for j in range(esq, dir):
                comparacoes[0] += 1
                if arr[j] <= pivot:
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]
                    trocas[0] += 1
            arr[i + 1], arr[dir] = arr[dir], arr[i + 1]
            trocas[0] += 1
            p = i + 1
            quick_sort_hibrido(esq, p - 1)
            quick_sort_hibrido(p + 1, dir)

    quick_sort_hibrido(0, len(arr) - 1)
    return arr, comparacoes[0], trocas[0]

def lista_crescente(tamanho):
    return list(range(1, tamanho + 1))


def lista_decrescente(tamanho):
    return list(range(tamanho, 0, -1))

def lista_aleatoria(tamanho):
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


def executar_comparacao(lista, executar_bubble=True, executar_insertion=True, executar_mergesort=True, executar_heapsort=True, executar_quicksort=True):
    """
    Executa a comparação entre algoritmos de ordenação. 
    
    """
   
    
    resultados = {}
    
    if executar_bubble:
        lista_copia = lista.copy()
        inicio = time.perf_counter() # medindo o tempo de execução
        resultado_bubble, comparacoes_bubble, trocas_bubble = bubbleSort(lista_copia)
        tempo_bubble = time.perf_counter() - inicio
        
        resultados['bubble'] = {
            'resultado': resultado_bubble,
            'tempo': tempo_bubble,
            'comparacoes': comparacoes_bubble,
            'trocas': trocas_bubble
        }
    
    if executar_insertion:
        lista_copia = lista.copy()
        inicio = time.perf_counter() # medindo o tempo de execução
        resultado_insertion, comparacoes_insertion, trocas_insertion = insertionSort(lista_copia)
        tempo_insertion = time.perf_counter() - inicio
        
        resultados['insertion'] = {
            'resultado': resultado_insertion,
            'tempo': tempo_insertion,
            'comparacoes': comparacoes_insertion,
            'trocas': trocas_insertion
        }
    
    if executar_mergesort:
        lista_copia = lista.copy()
        inicio = time.perf_counter()
        resultado_mergesort, comparacoes_mergesort, trocas_mergesort = mergeSort(lista_copia)
        tempo_mergesort = time.perf_counter() - inicio
        
        resultados['mergesort'] = {
            'resultado': resultado_mergesort,
            'tempo': tempo_mergesort,
            'comparacoes': comparacoes_mergesort,
            'trocas': trocas_mergesort
        }

    if executar_heapsort:
        lista_copia = lista.copy()
        inicio = time.perf_counter()
        resultado_heapsort, comparacoes_heapsort, trocas_heapsort = heapSort(lista_copia)
        tempo_heapsort = time.perf_counter() - inicio
        
        resultados['heapsort'] = {
            'resultado': resultado_heapsort,
            'tempo': tempo_heapsort,
            'comparacoes': comparacoes_heapsort,
            'trocas': trocas_heapsort
        } 

    if executar_quicksort:
        lista_copia = lista.copy()
        inicio = time.perf_counter()
        resultado_quicksort, comparacoes_quicksort, trocas_quicksort = quick_sort(lista_copia)
        tempo_quicksort = time.perf_counter() - inicio
        
        resultados['quicksort'] = {
            'resultado': resultado_quicksort,
            'tempo': tempo_quicksort,
            'comparacoes': comparacoes_quicksort,
            'trocas': trocas_quicksort
        }           
    
    return resultados



def avaliacao_comparacao(lista, num_repeticoes=3, executar_bubble=True, executar_insertion=True, executar_mergesort=True, executar_heapsort=True, executar_quicksort=True, executar_hibrido=True):
    
    # Executa os algoritmos de ordenação 3 vezes e calcula a média. 
    # Retorna um dicionário com os resultados de cada algoritmo, incluindo o resultado ordenado, 
    # tempo médio, tempos individuais, número de comparações e trocas.     
    
    resultados = {}
    
    if executar_bubble:
        tempos_bubble = []
        comparacoes_bubble = 0
        trocas_bubble = 0
        
        for _ in range(num_repeticoes): # Executa o algoritmo varias vezes (3x) para efetuar a media
            lista_copia = lista.copy()
            inicio = time.perf_counter()
            resultado_bubble, comp, troc = bubbleSort(lista_copia) # Retorna o resultado da ordenação
            tempo = time.perf_counter() - inicio # calcula o tempo de ordenação da lista
            tempos_bubble.append(tempo) # Recebe o tempo de cada ordenação, para calculo da média.
            comparacoes_bubble = comp  # São iguais em todas as repetições
            trocas_bubble = troc
        
        tempo_medio = sum(tempos_bubble) / num_repeticoes # calcula o tempo médio de ordenacao
        resultados['bubble'] = {
            'resultado': resultado_bubble,
            'tempo_medio': tempo_medio,
            'tempos': tempos_bubble,
            'comparacoes': comparacoes_bubble,
            'trocas': trocas_bubble
        }
    
    if executar_insertion:
        tempos_insertion = []
        comparacoes_insertion = 0
        trocas_insertion = 0
        
        for _ in range(num_repeticoes):
            lista_copia = lista.copy()
            inicio = time.perf_counter()
            resultado_insertion, comp, troc = insertionSort(lista_copia)
            tempo = time.perf_counter() - inicio
            tempos_insertion.append(tempo)
            comparacoes_insertion = comp
            trocas_insertion = troc
        
        tempo_medio = sum(tempos_insertion) / num_repeticoes
        resultados['insertion'] = {
            'resultado': resultado_insertion,
            'tempo_medio': tempo_medio,
            'tempos': tempos_insertion,
            'comparacoes': comparacoes_insertion,
            'trocas': trocas_insertion
        }
    
    if executar_mergesort:
        tempos_mergesort = []
        comparacoes_mergesort = 0
        trocas_mergesort = 0
        
        for _ in range(num_repeticoes):
            lista_copia = lista.copy()
            inicio = time.perf_counter()
            resultado_mergesort, comp, troc = mergeSort(lista_copia)
            tempo = time.perf_counter() - inicio
            tempos_mergesort.append(tempo)
            comparacoes_mergesort = comp
            trocas_mergesort = troc
        
        tempo_medio = sum(tempos_mergesort) / num_repeticoes
        resultados['mergesort'] = {
            'resultado': resultado_mergesort,
            'tempo_medio': tempo_medio,
            'tempos': tempos_mergesort,
            'comparacoes': comparacoes_mergesort,
            'trocas': trocas_mergesort
        }

    if executar_heapsort:
        tempos_heapsort = []
        comparacoes_heapsort = 0
        trocas_heapsort = 0
        
        for _ in range(num_repeticoes):
            lista_copia = lista.copy()
            inicio = time.perf_counter()
            resultado_heapsort, comp, troc = heapSort(lista_copia)
            tempo = time.perf_counter() - inicio
            tempos_heapsort.append(tempo)
            comparacoes_heapsort = comp
            trocas_heapsort = troc
        
        tempo_medio = sum(tempos_heapsort) / num_repeticoes
        resultados['heapsort'] = {
            'resultado': resultado_heapsort,
            'tempo_medio': tempo_medio,
            'tempos': tempos_heapsort,
            'comparacoes': comparacoes_heapsort,            'trocas': trocas_heapsort
        }

    if executar_quicksort:
        tempos_quicksort = []
        comparacoes_quicksort = 0
        trocas_quicksort = 0
        
        for _ in range(num_repeticoes):
            lista_copia = lista.copy()
            inicio = time.perf_counter()
            resultado_quicksort, comp, troc = quick_sort(lista_copia)
            tempo = time.perf_counter() - inicio
            tempos_quicksort.append(tempo)
            comparacoes_quicksort = comp
            trocas_quicksort = troc
        
        tempo_medio = sum(tempos_quicksort) / num_repeticoes
        resultados['quicksort'] = {
            'resultado': resultado_quicksort,
            'tempo_medio': tempo_medio,
            'tempos': tempos_quicksort,
            'comparacoes': comparacoes_quicksort,
            'trocas': trocas_quicksort
        }

    if executar_hibrido:
        tempos_hibrido = []
        comparacoes_hibrido = 0
        trocas_hibrido = 0
        
        for _ in range(num_repeticoes):
            lista_copia = lista.copy()
            inicio = time.perf_counter()
            resultado_hibrido, comp, troc = algoritmo_hibrido(lista_copia)
            tempo = time.perf_counter() - inicio
            tempos_hibrido.append(tempo)
            comparacoes_hibrido = comp
            trocas_hibrido = troc
        
        tempo_medio = sum(tempos_hibrido) / num_repeticoes
        resultados['algoritmo_hibrido'] = {
            'resultado': resultado_hibrido,
            'tempo_medio': tempo_medio,
            'tempos': tempos_hibrido,
            'comparacoes': comparacoes_hibrido,
            'trocas': trocas_hibrido
        }
    
    return resultados

