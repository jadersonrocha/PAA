"""Módulo de interface gráfica"""

import tkinter as tk
from tkinter import ttk


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
        self.aoh_var = tk.BooleanVar(value=True)

        ttk.Checkbutton(self.frame, text="Bubble Sort", variable=self.bubble_var).pack(anchor=tk.W, padx=5)
        ttk.Checkbutton(self.frame, text="Insertion Sort", variable=self.insertion_var).pack(anchor=tk.W, padx=5)
        ttk.Checkbutton(self.frame, text="Merge Sort", variable=self.merge_var).pack(anchor=tk.W, padx=5)
        ttk.Checkbutton(self.frame, text="Heap Sort", variable=self.heapsort_var).pack(anchor=tk.W, padx=5)
        ttk.Checkbutton(self.frame, text="Quick Sort", variable=self.quicksort_var).pack(anchor=tk.W, padx=5)
        ttk.Checkbutton(self.frame, text="Algoritmo Híbrido", variable=self.aoh_var).pack(anchor=tk.W, padx=5)

    def pack(self, **kwargs):
        self.frame.pack(**kwargs)


class FrameResultados:
    """Frame para exibição de resultados"""
    
    def __init__(self, parent):
        self.frame = ttk.LabelFrame(parent, text="Resultados", padding="10")
        self.criar_widgets()
    
    def criar_widgets(self):
        # Text widget para resultados
        self.resultado_text = tk.Text(
            self.frame,
            height=15,
            width=140,
            font=("Courier", 9),
            bg="white",
            wrap=tk.NONE
        )
        
        scrollbar_y = ttk.Scrollbar(
            self.frame,
            orient=tk.VERTICAL,
            command=self.resultado_text.yview
        )
        scrollbar_x = ttk.Scrollbar(
            self.frame,
            orient=tk.HORIZONTAL,
            command=self.resultado_text.xview
        )

        self.resultado_text.config(
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set
        )

        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.resultado_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def pack(self, **kwargs):
        self.frame.pack(**kwargs)
    
    def limpar(self):
        """Limpa o texto de resultados"""
        self.resultado_text.delete("1.0", tk.END)
    
    def inserir(self, texto):
        """Insere texto nos resultados"""
        self.resultado_text.insert(tk.END, texto)


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
