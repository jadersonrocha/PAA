
"""
Módulo para gerar gráficos de análise dos algoritmos de ordenação
Apresenta:
- Tempo médio de execução por algoritmo 
- Número de comparações por algoritmo 
Cada métrica é apresentada em 3 gráficos de linha (um para cada tipo de lista).
"""

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')  # Backend para Tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk
from tkinter import ttk

class GeradorGraficos:
    """Classe responsável por gerar e exibir gráficos de análise"""
    
    def __init__(self):
        self.cores = {
            'bubble': '#FF6B6B',
            'insertion': '#FFA500',
            'mergesort': '#4ECDC4',
            'heapsort': '#45B7D1',
            'quicksort': '#96CEB4',
            'algoritmo_hibrido': '#FFEAA7',
            'algoritmo_hibrido_insercao': '#DDA0DD'
        }
        
        self.nomes_display = {
            'bubble': 'Bubble Sort',
            'insertion': 'Insertion Sort',
            'mergesort': 'Merge Sort',
            'heapsort': 'Heap Sort',
            'quicksort': 'Quick Sort',
            'algoritmo_hibrido': 'Híbrido (LOMUTO)',
            'algoritmo_hibrido_insercao': 'Híbrido (HOARE)'
        }
        
        self.tipos_lista = ['crescente', 'decrescente', 'aleatoria']
        self.nomes_tipos = {
            'crescente': 'Lista Crescente',
            'decrescente': 'Lista Decrescente',
            'aleatoria': 'Lista Aleatória'
        }
    
    def criar_janela_graficos(self, resultados_automaticos, root=None):
        """
        Cria uma janela com os gráficos de análise      
        """
        if root is None:
            root = tk.Tk()
            root.title("Gráficos de Análise - Algoritmos de Ordenação")
            root.geometry("1600x900")
        
        # Frame principal com abas
        notebook = ttk.Notebook(root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Aba: Tempo de Execução
        frame_tempo = ttk.Frame(notebook)
        notebook.add(frame_tempo, text="Tempo de Execução")
        self.criar_graficos_tempo(frame_tempo, resultados_automaticos)
        
        # Aba: Comparações
        frame_comparacoes = ttk.Frame(notebook)
        notebook.add(frame_comparacoes, text="Comparações")
        self.criar_graficos_comparacoes(frame_comparacoes, resultados_automaticos)
        
        return root
    
    def criar_graficos_tempo(self, parent, resultados_automaticos):
        """
        Cria 3 gráficos de linha para tempo de execução        
        resultados_automaticos: Lista com resultados de múltiplos tamanhos
        """
        fig = Figure(figsize=(16, 5), dpi=100)
        
        # Criar um subplot para cada tipo de lista
        for idx, tipo in enumerate(self.tipos_lista, 1):
            ax = fig.add_subplot(1, 3, idx)
            
            # Organizar dados por algoritmo
            dados_por_algoritmo = {}
            for resultado_tamanho in resultados_automaticos:
                tamanho = resultado_tamanho["tamanho"]
                resultados_algos = resultado_tamanho["resultados"]
                
                for algoritmo, dados_algo in resultados_algos.items():
                    if algoritmo not in dados_por_algoritmo:
                        dados_por_algoritmo[algoritmo] = {
                            'tamanhos': [],
                            'tempos': []
                        }
                    
                    tempo_medio = dados_algo['por_tipo'][tipo]['tempo_medio']
                    dados_por_algoritmo[algoritmo]['tamanhos'].append(tamanho)
                    dados_por_algoritmo[algoritmo]['tempos'].append(tempo_medio)
            
            # Plotar uma linha para cada algoritmo
            for algoritmo, dados in dados_por_algoritmo.items():
                ax.plot(
                    dados['tempos'],
                    dados['tamanhos'],
                    marker='o',
                    color=self.cores[algoritmo],
                    linewidth=2.5,
                    markersize=8,
                    label=self.nomes_display[algoritmo],
                    zorder=3
                )
            
            ax.set_xlabel('Tempo de Execução (s)', fontsize=11, fontweight='bold')
            ax.set_ylabel('Tamanho da Entrada', fontsize=11, fontweight='bold')
            ax.set_title(self.nomes_tipos[tipo], fontsize=12, fontweight='bold')
            ax.grid(True, alpha=0.3, linestyle='--')
            ax.legend(loc='best', fontsize=9)
        
        fig.suptitle('Tempo Médio de Execução por Tipo de Lista', 
                     fontsize=14, fontweight='bold', y=1.02)
        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def criar_graficos_comparacoes(self, parent, resultados_automaticos):
        """
        Cria 3 gráficos de linha para número de comparações
        Eixo X: Número de comparações
        Eixo Y: Tamanho da entrada       
        resultados_automaticos: Lista com resultados de múltiplos tamanhos
        """
        fig = Figure(figsize=(16, 5), dpi=100)
        
        # Criar um subplot para cada tipo de lista
        for idx, tipo in enumerate(self.tipos_lista, 1):
            ax = fig.add_subplot(1, 3, idx)
            
            # Organizar dados por algoritmo
            dados_por_algoritmo = {}
            for resultado_tamanho in resultados_automaticos:
                tamanho = resultado_tamanho["tamanho"]
                resultados_algos = resultado_tamanho["resultados"]
                
                for algoritmo, dados_algo in resultados_algos.items():
                    if algoritmo not in dados_por_algoritmo:
                        dados_por_algoritmo[algoritmo] = {
                            'tamanhos': [],
                            'comparacoes': []
                        }
                    
                    comparacoes = dados_algo['por_tipo'][tipo]['comparacoes']
                    dados_por_algoritmo[algoritmo]['tamanhos'].append(tamanho)
                    dados_por_algoritmo[algoritmo]['comparacoes'].append(comparacoes)
            
            # Plotar uma linha para cada algoritmo
            for algoritmo, dados in dados_por_algoritmo.items():
                ax.plot(
                    dados['comparacoes'],
                    dados['tamanhos'],
                    marker='o',
                    color=self.cores[algoritmo],
                    linewidth=2.5,
                    markersize=8,
                    label=self.nomes_display[algoritmo],
                    zorder=3
                )
            
            ax.set_xlabel('Número de Comparações', fontsize=11, fontweight='bold')
            ax.set_ylabel('Tamanho da Entrada', fontsize=11, fontweight='bold')
            ax.set_title(self.nomes_tipos[tipo], fontsize=12, fontweight='bold')
            ax.grid(True, alpha=0.3, linestyle='--')
            ax.legend(loc='best', fontsize=9)
        
        fig.suptitle('Número de Comparações por Tipo de Lista', 
                     fontsize=14, fontweight='bold', y=1.02)
        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


def testar_graficos():
    """Função para testar os gráficos com dados de exemplo"""
    from funcoes import avaliacao_comparacao
    
    # Gerar dados de teste para MÚLTIPLOS tamanhos
    print("Gerando dados de teste para múltiplos tamanhos...")
    tamanhos = [1000, 5000, 10000]
    resultados_automaticos = []
    
    for tamanho in tamanhos:
        print(f"  Processando tamanho: {tamanho}")
        resultados = avaliacao_comparacao(
            tamanho=tamanho,
            num_repeticoes=2,
            executar_bubble=True,
            executar_insertion=True,
            executar_mergesort=True,
            executar_heapsort=True,
            executar_quicksort=True,
            executar_hibrido=True,
            executar_hibrido_insercao=True
        )
        
        resultados_automaticos.append({
            "tamanho": tamanho,
            "resultados": resultados
        })
    
    # Criar gráficos
    print("Criando gráficos...")
    root = tk.Tk()
    gerador = GeradorGraficos()
    gerador.criar_janela_graficos(resultados_automaticos, root)
    
    print("Exibindo janela...")
    root.mainloop()


if __name__ == "__main__":
    testar_graficos()
