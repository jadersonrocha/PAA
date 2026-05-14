import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from funcoes import gerar_lista, executar_comparacao, formatar_resultado
from ui import (
    configurar_estilos,
    criar_interface_principal,
    criar_titulo,
    FrameConfiguracao,
    FrameAlgoritmos,
    FrameResultados,
    JanelaGrafico
)


class App:
    def __init__(self, root):
        self.root = root
        self.cor_primaria = "#2c3e50"
        self.janela_grafico = None
        
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
        self.config_frame = FrameConfiguracao(main_frame)
        self.config_frame.pack(fill=tk.X, pady=10)
        
        self.algo_frame = FrameAlgoritmos(main_frame)
        self.algo_frame.pack(fill=tk.X, pady=10)
        
        # Botão executar
        botoes_frame = ttk.Frame(main_frame)
        botoes_frame.pack(fill=tk.X, pady=15)

        ttk.Button(
            botoes_frame,
            text="Executar Comparacao",
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
        
        # Frame de ações
    
    def obter_lista_usuario(self): # Obter o vetor do usuário, seja gerada ou personalizada
        entrada_custom = self.config_frame.entrada_custom.get("1.0", tk.END).strip()
        tamanho = self.config_frame.tamanho_var.get()
        tipo = self.config_frame.tipo_lista.get()
        
        lista, erro = gerar_lista(tipo, tamanho, entrada_custom)
        if erro:
            messagebox.showerror("Erro", erro)
            return None
        
        return lista
    
    def avaliacao_comparativa(self):# Avaliação comparativa dos algoritmos selecionados
        self.resultado_frame.limpar() # Limpar resultados anteriores
        
        lista = self.obter_lista_usuario() # Obter o vetor do usuário, seja gerada ou personalizada
        if lista is None:
            return
        
        if not self.algo_frame.bubble_var.get() and not self.algo_frame.insertion_var.get() and not self.algo_frame.merge_var.get():
            messagebox.showwarning("Aviso", "Selecione pelo menos um algoritmo!")
            return
        
        # Executar comparação e obter resultados
        
        resultados = executar_comparacao(
            lista,
            executar_bubble=self.algo_frame.bubble_var.get(),
            executar_insertion=self.algo_frame.insertion_var.get(),            
            executar_mergesort=self.algo_frame.merge_var.get()
        )
        
        tipo_lista = self.config_frame.tipo_lista.get() # Obter o tipo da lista para exibir no resultado
        tamanho = len(lista) # Obter o tamanho da lista para exibir no resultado
        texto_resultado = formatar_resultado(lista, tipo_lista, tamanho, resultados) # Gerar o texto formatado do resultado
        self.resultado_frame.inserir(texto_resultado)
        
        self.root.update()
        
        # Abrir gráfico se há 1 ou mais algoritmos selecionados
        if len(resultados) >= 1:
            try:
                self.janela_grafico = JanelaGrafico(
                    parent=self.root,
                    resultados=resultados,
                    lista=lista
                )
                # Aguardar a janela ficar visível
                self.janela_grafico.janela.wait_visibility()
                self.janela_grafico.janela.grab_set()
            except Exception as e:
                messagebox.showerror("Erro ao Abrir Gráfico", f"Erro: {str(e)}")
    
    def limpar_resultados(self):
        self.resultado_frame.limpar()
        self.config_frame.entrada_custom.delete("1.0", tk.END)
    
    def sair_aplicacao(self):
        if self.janela_grafico is not None:
            try:
                self.janela_grafico.fechar()
            except tk.TclError:
                pass
            self.janela_grafico = None

        for janela in self.root.winfo_children():
            if isinstance(janela, tk.Toplevel):
                try:
                    janela.destroy()
                except tk.TclError:
                    pass

        plt.close("all")
        self.root.quit()
        self.root.destroy()


def inicializar():
    root = tk.Tk()# Criar a janela principal
    app = App(root) # Inicializar a aplicação
    root.mainloop() # Iniciar o loop principal da interface


if __name__ == "__main__":
    inicializar() 
