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


def algoritmo_hibrido_insercao(lista):
    """ Algoritmo híbrido que combina Quick Sort com Insertion Sort para sublistas pequenas. """
    comparacoes = [0]
    trocas = [0]
    limite_troca = 32
    arr = lista  
    
    def insertion_sort_parcial(a, esq, dir):
        """Insertion Sort para sublistas pequenas """
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

    def partition_hoare(esq, dir):
        """Partição usando o método de Hoare      
        """
        # Selecionar pivô aleatório
        pivot_index = random.randint(esq, dir)
        arr[pivot_index], arr[esq] = arr[esq], arr[pivot_index]
        
        pivot = arr[esq]
        i = esq - 1
        j = dir + 1
        
        while True:
            # Encontrar elemento >= pivot da direita para esquerda
            j -= 1
            while j >= esq:
                comparacoes[0] += 1
                if arr[j] <= pivot:
                    break
                j -= 1
            
            # Encontrar elemento <= pivot da esquerda para direita
            i += 1
            while i <= dir:
                comparacoes[0] += 1
                if arr[i] >= pivot:
                    break
                i += 1
            
            # Se os índices se cruzaram, sair
            if i < j:
                # Trocar elementos
                arr[i], arr[j] = arr[j], arr[i]
                trocas[0] += 1
            else:
                return j + 1

    def quick_sort_hibrido(esq, dir):
        """algoritmo HOARE """
        while esq < dir:
            #  troca para InsertionSort quando sublista <= 32 elementos
            if dir - esq + 1 <= limite_troca: 
                insertion_sort_parcial(arr, esq, dir)
                break
            else:
                # retorna posição de partição
                p = partition_hoare(esq, dir)
                
                # Recursivamente ordenar a parte menor primeiro                
                if p - esq < dir - p:
                    quick_sort_hibrido(esq, p - 1) # Ordena a parte menor primeiro
                    esq = p  
                else:
                    quick_sort_hibrido(p, dir) # Ordena a parte menor primeiro
                    dir = p - 1 

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
    """Executa a comparação entre algoritmos de ordenação.  """  
    
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



def avaliacao_comparacao(tamanho, num_repeticoes=3, executar_bubble=True, executar_insertion=True, executar_mergesort=True, executar_heapsort=True, executar_quicksort=True, executar_hibrido=True, executar_hibrido_insercao=True):
    
    # Executa os algoritmos de ordenação 3 vezes para CADA tipo de lista     
    
    tipos_lista = ['crescente', 'decrescente', 'aleatoria']
    resultados = {}
      # Gerar listas para cada tipo
    listas = {}
    for tipo in tipos_lista:
        listas[tipo], _ = gerar_lista(tipo, tamanho)
    
    def algoritmo(algoritmo_func, nome_algoritmo):
        """Executa cada algoritmo selecionado 3 vezes para cada tipo de lista"""
        resultados_algo = {}
        tempos_totais = []
        comparacoes_totais = []
        trocas_totais = []
        resultado_final = None
        
        for tipo in tipos_lista:
            tempos_tipo = []
            comparacoes_tipo_lista = []
            trocas_tipo_lista = []
            
            for _ in range(num_repeticoes):
                lista_copia = listas[tipo].copy()
                inicio = time.perf_counter()
                resultado, comp, troc = algoritmo_func(lista_copia)
                tempo = time.perf_counter() - inicio
                
                tempos_tipo.append(tempo)
                tempos_totais.append(tempo)
                comparacoes_tipo_lista.append(comp)
                trocas_tipo_lista.append(troc)
                comparacoes_totais.append(comp)
                trocas_totais.append(troc)
                resultado_final = resultado
            
            # Médias por tipo de lista
            resultados_algo[tipo] = {
                'tempo_medio': sum(tempos_tipo) / len(tempos_tipo),
                'tempos': tempos_tipo,
                'comparacoes': sum(comparacoes_tipo_lista) / len(comparacoes_tipo_lista),
                'trocas': sum(trocas_tipo_lista) / len(trocas_tipo_lista)
            }
        
        # Resultados
        return {
            'tempo_medio_geral': sum(tempos_totais) / len(tempos_totais),
            'resultado': resultado_final,
            'por_tipo': resultados_algo,
            'comparacoes_media': sum(comparacoes_totais) / len(comparacoes_totais),
            'trocas_media': sum(trocas_totais) / len(trocas_totais)
        }
      # Executar cada algoritmo
    if executar_bubble:
        resultados['bubble'] = algoritmo(bubbleSort, 'Bubble Sort')
    
    if executar_insertion:
        resultados['insertion'] = algoritmo(insertionSort, 'Insertion Sort')
    
    if executar_mergesort:
        resultados['mergesort'] = algoritmo(mergeSort, 'Merge Sort')

    if executar_heapsort:
        resultados['heapsort'] = algoritmo(heapSort, 'Heap Sort')

    if executar_quicksort:
        resultados['quicksort'] = algoritmo(quick_sort, 'Quick Sort')

    if executar_hibrido:
        resultados['algoritmo_hibrido'] = algoritmo(algoritmo_hibrido, 'Híbrido (LOMUTO)')

    if executar_hibrido_insercao:
        resultados['algoritmo_hibrido_insercao'] = algoritmo(algoritmo_hibrido_insercao, 'Híbrido (HOARE)')
    
    return resultados

