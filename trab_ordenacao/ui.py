"""Módulo de interface gráfica"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class FrameConfiguracao:
    """Frame para configuração da lista"""
    
    def __init__(self, parent, entradas_teste=None):
        self.entradas_teste = entradas_teste or []
        self.frame = ttk.LabelFrame(parent, text="Configuração da Lista", padding="10")
        self.criar_widgets()
    
    def criar_widgets(self):
        # Tipo de lista
        ttk.Label(self.frame, text="Tipos de Lista Executados:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.tipo_lista = tk.StringVar(value="aleatoria")
        self.crescente_var = tk.BooleanVar(value=True)
        self.decrescente_var = tk.BooleanVar(value=True)
        self.aleatoria_var = tk.BooleanVar(value=True)
        
        opcoes_frame = ttk.Frame(self.frame)
        opcoes_frame.grid(row=0, column=1, sticky="w", padx=5)
        
        ttk.Checkbutton(opcoes_frame, text="Crescente", variable=self.crescente_var,
                        state=tk.DISABLED).pack(side=tk.LEFT, padx=5)
        ttk.Checkbutton(opcoes_frame, text="Decrescente", variable=self.decrescente_var,
                        state=tk.DISABLED).pack(side=tk.LEFT, padx=5)
        ttk.Checkbutton(opcoes_frame, text="Aleatória", variable=self.aleatoria_var,
                        state=tk.DISABLED).pack(side=tk.LEFT, padx=5)
        
        # Tamanho da lista
        ttk.Label(self.frame, text="Tamanho da Lista:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        entradas_texto = ", ".join(str(entrada) for entrada in self.entradas_teste)
        self.tamanho_var = tk.StringVar(value=entradas_texto)
        tamanho_spinbox = ttk.Spinbox(self.frame, from_=1, to=10000, textvariable=self.tamanho_var, 
                                      width=30, state=tk.DISABLED)
        tamanho_spinbox.grid(row=1, column=1, sticky="w", padx=5)
        
        # Entrada personalizada
        ttk.Label(self.frame, text="Ou Digite Números (separados por vírgula):").grid(row=2, column=0, 
                                                                                         sticky="nw", padx=5, pady=5)
        self.entrada_custom = tk.Text(self.frame, height=3, width=50, state=tk.DISABLED)
        self.entrada_custom.grid(row=2, column=1, padx=5, pady=5)

    def limpar_entrada_custom(self):
        self.entrada_custom.config(state=tk.NORMAL)
        self.entrada_custom.delete("1.0", tk.END)
        self.entrada_custom.config(state=tk.DISABLED)
    
    def pack(self, **kwargs):
        self.frame.pack(**kwargs)


class FrameAlgoritmos:
    """Frame para seleção de algoritmos"""
    
    def __init__(self, parent):
        self.frame = ttk.LabelFrame(parent, text="Selecione o Algoritmo para Simulação", padding="10")
        self.criar_widgets()
    
    def criar_widgets(self):
        self.bubble_var = tk.BooleanVar(value=True)
        self.insertion_var = tk.BooleanVar(value=True)
        self.merge_var = tk.BooleanVar(value=True)
        self.heapsort_var = tk.BooleanVar(value=True)
        self.quicksort_var = tk.BooleanVar(value=True)

        ttk.Checkbutton(self.frame, text="Bubble Sort", variable=self.bubble_var).pack(anchor=tk.W, padx=5)
        ttk.Checkbutton(self.frame, text="Insertion Sort", variable=self.insertion_var).pack(anchor=tk.W, padx=5)
        ttk.Checkbutton(self.frame, text="Merge Sort", variable=self.merge_var).pack(anchor=tk.W, padx=5)
        ttk.Checkbutton(self.frame, text="Heap Sort", variable=self.heapsort_var).pack(anchor=tk.W, padx=5)
        ttk.Checkbutton(self.frame, text="Quick Sort", variable=self.quicksort_var).pack(anchor=tk.W, padx=5)

    def pack(self, **kwargs):
        self.frame.pack(**kwargs)


class FrameResultados:
    """Frame para exibição de resultados"""
    
    def __init__(self, parent):
        self.frame = ttk.LabelFrame(parent, text="Resultados", padding="10")
        self.criar_widgets()
    
    def criar_widgets(self):
        # Text widget para resultados
        self.resultado_text = tk.Text(self.frame, height=15, width=100, 
                                      font=("Courier", 9), bg="white")
        self.resultado_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, 
                                 command=self.resultado_text.yview)
        self.resultado_text.config(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def pack(self, **kwargs):
        self.frame.pack(**kwargs)
    
    def limpar(self):
        """Limpa o texto de resultados"""
        self.resultado_text.delete("1.0", tk.END)
    
    def inserir(self, texto):
        """Insere texto nos resultados"""
        self.resultado_text.insert(tk.END, texto)


class FrameAcoes:
    """Frame para botões de ação"""
    
    def __init__(self, parent, cmd_limpar, cmd_sair):
        self.frame = ttk.Frame(parent)
        self.criar_widgets(cmd_limpar, cmd_sair)
    
    def criar_widgets(self, cmd_limpar, cmd_sair):
        ttk.Button(self.frame, text="Limpar Resultados", 
                  command=cmd_limpar).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.frame, text="SAIR", 
                  command=cmd_sair).pack(side=tk.RIGHT, padx=5)
    
    def pack(self, **kwargs):
        self.frame.pack(**kwargs)


class JanelaGrafico:
    """Janela para exibição de gráficos"""
    
    def __init__(self, parent=None, resultados=None, lista=None):
        if parent is None or resultados is None or lista is None:
            raise ValueError("parent, resultados e lista são obrigatórios")
        
        self.janela = tk.Toplevel(parent)
        self.janela.title("Gráfico de Desempenho")
        self.janela.geometry("900x600")
        self.janela.resizable(True, True)
        self.resultados = resultados
        self.lista = lista
        
        self.fig = self.criar_graficos()
        self.incorporar_grafico()
        self.criar_botoes()
        
        # Trazer a janela para frente
        self.janela.lift()
        self.janela.attributes('-topmost', True)
        self.janela.after_idle(self.janela.attributes, '-topmost', False)
    
    def criar_graficos(self):
        """Cria os gráficos de comparação"""
        # Determinar quantos algoritmos foram executados
        num_algoritmos = len(self.resultados)
        
        if num_algoritmos == 1:
            # Se apenas 1 algoritmo, mostrar apenas informações
            return self.criar_grafico_unico()
        else:
            # Se 2 ou mais, mostrar comparação
            return self.criar_grafico_comparacao()
    
    def criar_grafico_unico(self):
        """Cria gráfico quando apenas 1 algoritmo é executado"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        
        # Informações do algoritmo executado
        algoritmo = list(self.resultados.keys())[0]
        tempo = self.resultados[algoritmo]['tempo']
        
        nomes_algoritmos = {
            'bubble': 'Bubble Sort',
            'insertion': 'Insertion Sort',
            'mergesort': 'Merge Sort',
            'heapsort': 'Heap Sort',
             'quicksort': 'Quick Sort'
        }
        
        nome_algo = nomes_algoritmos.get(algoritmo, algoritmo.upper())
        cores_algoritmos = {
            'bubble': '#e74c3c',
            'insertion': '#27ae60',
            'mergesort': '#3498db',
            'heapsort': '#8e44ad',
            'quicksort': '#000000'
        }
        cor = cores_algoritmos.get(algoritmo, '#2c3e50')
        comparacoes = self.resultados[algoritmo]['comparacoes']

        barra = ax1.bar([nome_algo], [tempo], color=cor, alpha=0.85,
                        edgecolor='black', linewidth=2)

        ax1.set_title(f'Tempo de Execucao - {nome_algo}', fontsize=13, fontweight='bold')
        ax1.set_ylabel('Tempo de Execucao (segundos)', fontsize=11, fontweight='bold')
        ax1.grid(True, alpha=0.3, linestyle='--', axis='y')

        limite_superior = tempo * 1.35 if tempo > 0 else 0.001
        ax1.set_ylim(0, limite_superior)
        ax1.bar_label(
            barra,
            labels=[f'{tempo:.6f}s\n{comparacoes:,} comp.'.replace(',', '.')],
            padding=6,
            fontsize=9,
            fontweight='bold'
        )

        resumo = (
            f'Tamanho da lista: {len(self.lista)} elementos'
        )
        ax1.text(0.5, 0.88, resumo, transform=ax1.transAxes, ha='center',
                 va='top', fontsize=10,
                 bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
                           edgecolor='#bdc3c7', alpha=0.9))

        tamanho = len(self.lista)
        inicio_teste = 1 if tamanho < 10 else 10
        tamanhos_teste = list(range(inicio_teste, tamanho + 1, max(1, tamanho // 20)))

        if algoritmo == 'bubble':
            operacoes = [(t * (t - 1) // 2) for t in tamanhos_teste]
            marcador = 'o'
        elif algoritmo == 'insertion':
            operacoes = [(t ** 2 // 4) for t in tamanhos_teste]
            marcador = 's'
        else:
            operacoes = [t * __import__('math').log(t) if t > 0 else 0 for t in tamanhos_teste]
            marcador = '^'

        max_operacoes = max(operacoes) if operacoes else 1
        tempos_estimados = [
            op / max_operacoes * tempo if max_operacoes > 0 else 0
            for op in operacoes
        ]

        ax2.plot(tamanhos_teste, tempos_estimados, marker=marcador, linewidth=2.5,
                 markersize=6, label=nome_algo, color=cor, alpha=0.8)
        ax2.set_xlabel('Tamanho da Lista', fontsize=11, fontweight='bold')
        ax2.set_ylabel('Tempo Estimado (segundos)', fontsize=11, fontweight='bold')
        ax2.set_title('Analise de Complexidade', fontsize=13, fontweight='bold')
        ax2.legend(loc='upper left', fontsize=10, framealpha=0.9)
        ax2.grid(True, alpha=0.3, linestyle='--')

        plt.tight_layout()
        return fig
        
        ax.text(0.5, 0.7, nome_algo, fontsize=24, fontweight='bold', 
                ha='center', transform=ax.transAxes)
        ax.text(0.5, 0.5, f'Tempo de Execução', fontsize=14, 
                ha='center', transform=ax.transAxes)
        ax.text(0.5, 0.35, f'{tempo:.6f} segundos', fontsize=18, fontweight='bold',
                color='#2c3e50', ha='center', transform=ax.transAxes)
        ax.text(0.5, 0.15, f'Tamanho da lista: {len(self.lista)} elementos', fontsize=11,
                ha='center', transform=ax.transAxes, style='italic')
        
        ax.axis('off')
        plt.tight_layout()
        return fig
    
    def criar_grafico_comparacao(self):
        """Cria gráfico comparativo quando 2 ou mais algoritmos são executados"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        
        # Preparar dados
        nomes_mapa = {
            'bubble': 'Bubble Sort',
            'insertion': 'Insertion Sort',
            'mergesort': 'Merge Sort',
            'heapsort': 'Heap Sort',
            'quicksort': 'Quick Sort'
        }
        
        cores_mapa = {
            'bubble': '#e74c3c',
            'insertion': '#27ae60',
            'mergesort': '#3498db',
            'heapsort': '#8e44ad',
            'quicksort': '#000000'
        }

        nomes = [nomes_mapa[k] for k in self.resultados.keys()]
        tempos = [self.resultados[k]['tempo'] for k in self.resultados.keys()]
        comparacoes = [self.resultados[k]['comparacoes'] for k in self.resultados.keys()]
        cores = [cores_mapa[k] for k in self.resultados.keys()]
        
        # Gráfico 1: Comparação de tempos (Barras)
        x_pos = range(len(nomes))
        barras_tempo = ax1.bar(x_pos, tempos, color=cores, alpha=0.8,
                               edgecolor='black', linewidth=2)
        
        ax1.set_ylabel('Tempo de Execução (segundos)', fontsize=11, fontweight='bold')
        ax1.set_title('Comparação de Tempos de Execução', fontsize=13, fontweight='bold')
        ax1.set_xticks(x_pos)
        ax1.set_xticklabels(nomes, rotation=15, ha='right')
        ax1.grid(True, alpha=0.3, linestyle='--', axis='y')
        
        limite_tempo = max(tempos) * 1.35 if max(tempos) > 0 else 0.001
        ax1.set_ylim(0, limite_tempo)
        ax1.bar_label(
            barras_tempo,
            labels=[
                f'{tempo:.6f}s\n{comparacao:,} comp.'.replace(',', '.')
                for tempo, comparacao in zip(tempos, comparacoes)
            ],
            padding=6,
            fontsize=9,
            fontweight='bold'
        )

        ax1.text(0.5, 0.88, f'Tamanho da lista: {len(self.lista)} elementos',
                 transform=ax1.transAxes, ha='center', va='top', fontsize=10,
                 bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
                           edgecolor='#bdc3c7', alpha=0.9))
        
        # Gráfico 2: Evolução com diferentes tamanhos (Linhas)
        tamanho = len(self.lista)
        tamanhos_teste = list(range(10, tamanho + 1, max(1, tamanho // 20)))
        
        # Calcular complexidade teórica normalizada
        bubble_ops = [(t * (t - 1) // 2) for t in tamanhos_teste]
        insertion_ops = [(t ** 2 // 4) for t in tamanhos_teste]
        merge_ops = [t * __import__('math').log(t) if t > 0 else 0 for t in tamanhos_teste]
        heapsort_ops = [t * __import__('math').log(t) if t > 0 else 0 for t in tamanhos_teste]
        
        # Normalizar para escala de tempo estimada
        max_ops = max(max(bubble_ops), max(insertion_ops), max(merge_ops), max(heapsort_ops)) if (bubble_ops and insertion_ops and merge_ops and heapsort_ops) else 1

        # Plotar linhas conforme disponibilidade
        if 'bubble' in self.resultados:
            bubble_tempo_est = [op / max_ops * self.resultados['bubble']['tempo'] for op in bubble_ops]
            ax2.plot(tamanhos_teste, bubble_tempo_est, marker='o', linewidth=2.5, 
                    markersize=6, label='Bubble Sort', color='#e74c3c', alpha=0.8)
        
        if 'insertion' in self.resultados:
            insertion_tempo_est = [op / max_ops * self.resultados['insertion']['tempo'] for op in insertion_ops]
            ax2.plot(tamanhos_teste, insertion_tempo_est, marker='s', linewidth=2.5, 
                    markersize=6, label='Insertion Sort', color='#27ae60', alpha=0.8)
        
        if 'mergesort' in self.resultados:
            merge_tempo_est = [(op / max_ops * self.resultados['mergesort']['tempo']) for op in merge_ops]
            ax2.plot(tamanhos_teste, merge_tempo_est, marker='^', linewidth=2.5, 
                    markersize=6, label='Merge Sort', color='#3498db', alpha=0.8)

        if 'heapsort' in self.resultados:
            heapsort_tempo_est = [(op / max_ops * self.resultados['heapsort']['tempo']) for op in heapsort_ops]
            ax2.plot(tamanhos_teste, heapsort_tempo_est, marker='d', linewidth=2.5,
                     markersize=6, label='Heap Sort', color='#8e44ad', alpha=0.8)

        if 'quicksort' in self.resultados:
            quicksort_tempo_est = [(op / max_ops * self.resultados['quicksort']['tempo']) for op in heapsort_ops]
            ax2.plot(tamanhos_teste, quicksort_tempo_est, marker='d', linewidth=2.5,
                     markersize=6, label='Heap Sort', color='#000000', alpha=0.8)    

        ax2.set_xlabel('Tamanho da Lista', fontsize=11, fontweight='bold')
        ax2.set_ylabel('Tempo Estimado (segundos)', fontsize=11, fontweight='bold')
        ax2.set_title('Análise de Complexidade', fontsize=13, fontweight='bold')
        ax2.legend(loc='upper left', fontsize=10, framealpha=0.9)
        ax2.grid(True, alpha=0.3, linestyle='--')
        
        plt.tight_layout()
        return fig
    
    def incorporar_grafico(self):
        
        """Incorpora o gráfico na janela Tkinter"""
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.janela)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def criar_botoes(self):
        """Cria os botões de ação"""
        btn_frame = ttk.Frame(self.janela)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(btn_frame, text=" Salvar Gráfico", 
                  command=self.salvar).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Fechar", 
                  command=self.fechar).pack(side=tk.RIGHT, padx=5)

        self.janela.protocol("WM_DELETE_WINDOW", self.fechar)

    def fechar(self):
        """Fecha a janela do grafico e libera a figura do Matplotlib."""
        plt.close(self.fig)
        self.janela.destroy()
    
    def salvar(self):
        """Salva o gráfico como imagem"""
        arquivo = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        
        if arquivo:
            self.fig.savefig(arquivo, dpi=300, bbox_inches='tight')
            messagebox.showinfo("Sucesso", f"Gráfico salvo em:\n{arquivo}")


def criar_interface_principal(root):
    """Cria a interface principal com scroll"""
    # Frame principal com Canvas para scroll
    canvas = tk.Canvas(root, bg="#f0f0f0", highlightthickness=0)
    scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas, padding="10")
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    # Permitir scroll com roda do mouse
    def on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    canvas.bind_all("<MouseWheel>", on_mousewheel)
    
    return scrollable_frame


def criar_titulo(parent, cor_primaria):
    """Cria o título da aplicação"""
    titulo = ttk.Label(parent, text="PAA - Análise dos Algoritmos de Ordenação", 
                      style="Title.TLabel", foreground=cor_primaria)
    titulo.pack(pady=10)


def configurar_estilos():
    """Configura os estilos da aplicação"""
    style = ttk.Style()
    style.theme_use('clam')
    
    style.configure("TFrame", background="#f0f0f0")
    style.configure("TLabel", background="#f0f0f0", font=("Helvetica", 10))
    style.configure("Title.TLabel", background="#f0f0f0", font=("Helvetica", 14, "bold"))
    style.configure("TButton", font=("Helvetica", 10))
