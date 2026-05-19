import tkinter as tk
from tkinter import ttk, messagebox
#from funcoes import gerar_lista, executar_comparacao
from funcoes import gerar_lista, avaliacao_comparacao, algoritmo_hibrido
from ui import (
    configurar_estilos,
    criar_interface_principal,
    criar_titulo,
    FrameConfiguracao,
    FrameAlgoritmos,
    FrameResultados
)


class App:
    ENTRADAS = [10000, 30000] # listas com as entradas para teste
    TIPOS_ORDENACAO = ["crescente", "decrescente", "aleatoria"]
    NOMES_ALGORITMOS = {
        "bubble": "Bubble Sort",
        "insertion": "Insertion Sort",
        "mergesort": "Merge Sort",
        "heapsort": "Heap Sort",
        "quicksort": "Quick Sort",
        "algoritmo_hibrido": "Algoritmo Híbrido",
    }

    def __init__(self, root): # Inicializar a aplicação
        self.root = root
        self.cor_primaria = "#2c3e50"
        
        # Configurar janela
        self.root.title("Comparador de Algoritmos de Ordenacao")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        self.root.configure(bg="#f0f0f0")
        self.root.protocol("WM_DELETE_WINDOW", self.sair_aplicacao)
        
        # Configurar estilos
        configurar_estilos()
        
        # Criar interface
        self.criar_interface()
    
    def criar_interface(self):
        # Frame principal com scroll
        main_frame = criar_interface_principal(self.root)
        criar_titulo(main_frame, self.cor_primaria)
        
        # Frames de configuração
        self.config_frame = FrameConfiguracao(main_frame, self.ENTRADAS)
        self.config_frame.pack(fill=tk.X, pady=10)
        
        self.algo_frame = FrameAlgoritmos(main_frame)
        self.algo_frame.pack(fill=tk.X, pady=10)
        
        # Botão executar
        botoes_frame = ttk.Frame(main_frame)
        botoes_frame.pack(fill=tk.X, pady=15)

        ttk.Button(
            botoes_frame,
            text="Executar Testes Automaticos",
            command=self.avaliacao_comparativa
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            botoes_frame,
            text="Limpar Resultados",
            command=self.limpar_resultados
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            botoes_frame,
            text="SAIR",
            command=self.sair_aplicacao
        ).pack(side=tk.RIGHT, padx=5)
        
        # Frame de resultados
        self.resultado_frame = FrameResultados(main_frame)
        self.resultado_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
      
    
    
    
    # Obtem os algoritmos selecionados pelo usuário
    def algoritmos_selecionados(self):
        return {
            "bubble": self.algo_frame.bubble_var.get(),
            "insertion": self.algo_frame.insertion_var.get(),
            "mergesort": self.algo_frame.merge_var.get(),
            "heapsort": self.algo_frame.heapsort_var.get(),
            "quicksort": self.algo_frame.quicksort_var.get(),
            "algoritmo_hibrido": self.algo_frame.aoh_var.get(),
        }
    
    # Avaliação comparativa dos algoritmos selecionados
    def avaliacao_comparativa(self):
        self.resultado_frame.limpar() # Limpar resultados anteriores

        algoritmos = self.algoritmos_selecionados()
        if not any(algoritmos.values()):
            messagebox.showwarning("Aviso", "Selecione pelo menos um algoritmo!")
            return

        resultados_automaticos = []
        self.resultado_frame.inserir("Executando testes automaticos...\n")
        self.resultado_frame.inserir(f"Entradas: {', '.join(str(t) for t in self.ENTRADAS)}\n")
        self.resultado_frame.inserir("Tipos de lista: crescente, decrescente e aleatoria\n\n")
        self.root.update_idletasks()

        for tamanho in self.ENTRADAS: # Para cada entrada, gerar as listas e executar os algoritmos selecionados
            resultado_por_tamanho = {
                "tamanho": tamanho,
                "tipos": {},
            }

            self.resultado_frame.inserir(f"Processando entrada {tamanho}...\n") 
            self.root.update_idletasks()

            for tipo_lista in self.TIPOS_ORDENACAO:
                lista, erro = gerar_lista(tipo_lista, tamanho)
                if erro:
                    messagebox.showerror("Erro", erro)
                    return

                resultados = avaliacao_comparacao(
                    lista,
                    executar_bubble=algoritmos["bubble"],
                    executar_insertion=algoritmos["insertion"],
                    executar_mergesort=algoritmos["mergesort"],
                    executar_heapsort=algoritmos["heapsort"],
                    executar_quicksort=algoritmos["quicksort"],
                    executar_hibrido=algoritmos["algoritmo_hibrido"],
                )
                resultado_por_tamanho["tipos"][tipo_lista] = resultados

            resultados_automaticos.append(resultado_por_tamanho)

        self.resultado_frame.limpar()
        self.resultado_frame.inserir(self.formatar_resultados(resultados_automaticos, algoritmos))

    # Função de apresentação dos resultados
    def formatar_resultados(self, resultados_automaticos, algoritmos):
        largura = 122
        texto = "=" * largura + "\n"
        texto += "AVALIAÇÃO DOS ALGORITMOS DE ORDENACAO\n"
        texto += "=" * largura + "\n\n"
        texto += f"Entradas testadas: {', '.join(str(t) for t in self.ENTRADAS)}\n"
        texto += "Tipos de lista: Crescente, Decrescente e Aleatoria\n"
        texto += "Comp.: numero de comparacoes realizadas. Trocas: numero de trocas ou movimentacoes realizadas.\n\n"

        for resultado_tamanho in resultados_automaticos:
            tamanho = resultado_tamanho["tamanho"]
            texto += "=" * largura + "\n"
            texto += f"VETOR [{tamanho}]\n"
            texto += "=" * largura + "\n"
            texto += (
                f"{'Lista':<16}"
                f"{'Ordem Crescente':^35}"
                f"{'Ordem Decrescente':^35}"
                f"{'Ordem Aleatoria':^35}\n"
            )
            texto += (
                f"{'Algoritmo':<16}"
                f"{'Tempo(s)':>12}{'Comp.':>11}{'Trocas':>12}"
                f"{'Tempo(s)':>12}{'Comp.':>11}{'Trocas':>12}"
                f"{'Tempo(s)':>12}{'Comp.':>11}{'Trocas':>12}\n"
            )
            texto += "-" * largura + "\n"

            for algoritmo, executar in algoritmos.items():
                if not executar:
                    continue

                metricas = {}
                for tipo in self.TIPOS_ORDENACAO:
                    resultado_algoritmo = resultado_tamanho["tipos"][tipo].get(algoritmo)
                    metricas[tipo] = resultado_algoritmo

                texto += (
                    f"{self.NOMES_ALGORITMOS[algoritmo]:<16}"
                    f"{self.formatar_metricas(metricas['crescente'])}"
                    f"{self.formatar_metricas(metricas['decrescente'])}"
                    f"{self.formatar_metricas(metricas['aleatoria'])}\n"
                )

            texto += "\n"

        return texto

    @staticmethod
    def formatar_tempo(tempo):
        if tempo is None:
            return "-"
        return f"{tempo:.6f}"

    @classmethod
    def formatar_metricas(cls, resultado):
        if resultado is None:
            return f"{'-':>12}{'-':>11}{'-':>12}"

        return (
            f"{cls.formatar_tempo(resultado['tempo_medio']):>12}"
            f"{cls.formatar_numero(resultado['comparacoes']):>11}"
            f"{cls.formatar_numero(resultado['trocas']):>12}"
        )

    @staticmethod
    def formatar_numero(numero):
        return str(numero)
    
    def limpar_resultados(self):
        self.resultado_frame.limpar()
        self.config_frame.limpar_entrada_custom()
    
    def sair_aplicacao(self):
        for janela in self.root.winfo_children():
            if isinstance(janela, tk.Toplevel):
                try:
                    janela.destroy()
                except tk.TclError:
                    pass

        self.root.quit()
        self.root.destroy()


def inicializar():
    root = tk.Tk()# Criar a janela principal
    App(root) # Inicializar a aplicação
    root.mainloop() # Iniciar o loop principal da interface


if __name__ == "__main__":
    inicializar() #
