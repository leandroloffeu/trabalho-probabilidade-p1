import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
import os  # Importar a biblioteca os para verificar a existência de arquivos

# Função para listar países na base de dados
def listar_paises():
    caminho_arquivo = caminho_entrada.get()
    
    if not os.path.exists(caminho_arquivo):
        messagebox.showerror("Erro", "O arquivo não foi encontrado. Verifique o caminho.")
        return

    try:
        # Carregar os dados
        dados = pd.read_csv(caminho_arquivo)

        # Verificar se a coluna 'pais' existe
        if 'pais' in dados.columns:
            paises_unicos = dados['pais'].unique()
            lista_paises.delete(1.0, tk.END)  # Limpar a caixa de texto
            for pais in paises_unicos:
                lista_paises.insert(tk.END, pais + '\n')  # Adicionar cada país na caixa de texto
        else:
            messagebox.showerror("Erro", "A coluna 'pais' não foi encontrada no arquivo.")

    except Exception as e:
        messagebox.showerror("Erro", str(e))

# Função para selecionar o arquivo CSV
def selecionar_arquivo():
    arquivo = filedialog.askopenfilename(title="Selecione um arquivo CSV", filetypes=[("CSV files", "*.csv")])
    if arquivo:
        caminho_entrada.delete(0, tk.END)  # Limpar a entrada
        caminho_entrada.insert(0, arquivo)  # Inserir o caminho do arquivo selecionado

# Configuração da interface gráfica com Tkinter
janela = tk.Tk()
janela.title("Listar Países a partir de um CSV")

# Labels e Entradas
tk.Label(janela, text="Caminho do arquivo CSV:").grid(row=0, column=0, padx=10, pady=5)
caminho_entrada = tk.Entry(janela, width=50)
caminho_entrada.grid(row=0, column=1, padx=10, pady=5)

# Botão para selecionar o arquivo
tk.Button(janela, text="Selecionar Arquivo", command=selecionar_arquivo).grid(row=0, column=2, padx=10, pady=5)

# Botão para listar países
tk.Button(janela, text="Listar Países", command=listar_paises).grid(row=1, column=0, columnspan=3, pady=20)

# Caixa de texto para exibir os países
lista_paises = tk.Text(janela, height=15, width=60)
lista_paises.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

# Adicionando uma barra de rolagem à caixa de texto
scrollbar = tk.Scrollbar(janela, command=lista_paises.yview)
scrollbar.grid(row=2, column=3, sticky='ns')  # Posição da barra de rolagem

lista_paises.config(yscrollcommand=scrollbar.set)  # Conectar a barra de rolagem à caixa de texto

# Executar a interface gráfica
janela.mainloop()
