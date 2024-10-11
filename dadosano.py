import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import tkinter as tk
from tkinter import messagebox, filedialog

# Função para carregar e listar os países
def listar_paises(dados):
    paises_unicos = dados['pais'].unique()  # Obter países únicos
    # Limpar o campo de texto antes de adicionar novos países
    lista_paises_text.delete(1.0, tk.END)
    for pais in paises_unicos:
        lista_paises_text.insert(tk.END, f"{pais}\n")  # Inserir cada país em uma nova linha

# Função para carregar e processar os dados
def processar_dados():
    caminho_arquivo = caminho_entrada.get()  # Caminho do arquivo CSV

    if not os.path.exists(caminho_arquivo):
        messagebox.showerror("Erro", "O arquivo não foi encontrado. Verifique o caminho.")
        return

    try:
        # Carregar os dados
        dados = pd.read_csv(caminho_arquivo)

        # Listar os países
        listar_paises(dados)

        # Filtrar os dados pelos anos especificados
        ano_inicio = int(ano_inicio_entrada.get())
        ano_fim = int(ano_fim_entrada.get())
        dados = dados[(dados['ano'] >= ano_inicio) & (dados['ano'] <= ano_fim)]

        # Tratamento de valores ausentes e outliers
        dados = dados.dropna()

        def remove_outliers(df, column):
            Q1 = df[column].quantile(0.25)
            Q3 = df[column].quantile(0.75)
            IQR = Q3 - Q1
            return df[(df[column] >= (Q1 - 1.5 * IQR)) & (df[column] <= (Q3 + 1.5 * IQR))]

        dados = remove_outliers(dados, 'altura')
        dados = remove_outliers(dados, 'peso')

        # Estatísticas descritivas
        media_altura = dados['altura'].mean()
        desvio_padrao_altura = dados['altura'].std()
        media_peso = dados['peso'].mean()
        desvio_padrao_peso = dados['peso'].std()

        # Exibir resultados
        resultados.set(f'Média Altura: {media_altura:.2f} cm, Desvio Padrão Altura: {desvio_padrao_altura:.2f} cm\n'
                       f'Média Peso: {media_peso:.2f} kg, Desvio Padrão Peso: {desvio_padrao_peso:.2f} kg')

        # Plotar os gráficos
        sns.set(style='whitegrid')
        fig, axes = plt.subplots(2, 2, figsize=(20, 15))

        # Gráfico 1: Distribuição da Altura dos Atletas
        sns.histplot(dados['altura'], bins=30, kde=True, color='skyblue', stat='density', ax=axes[0, 0])
        axes[0, 0].set_title('Distribuição da Altura dos Atletas', fontsize=16)
        axes[0, 0].set_xlabel('Altura (cm)', fontsize=14)
        axes[0, 0].set_ylabel('Densidade', fontsize=14)
        axes[0, 0].axvline(media_altura, color='red', linestyle='--', label='Média: {:.2f} cm'.format(media_altura))
        axes[0, 0].axvline(media_altura + desvio_padrao_altura, color='orange', linestyle='--', label='Desvio Padrão: {:.2f} cm'.format(desvio_padrao_altura))
        axes[0, 0].axvline(media_altura - desvio_padrao_altura, color='orange', linestyle='--')
        axes[0, 0].legend()

        # Gráfico 2: Relação entre Peso e Altura dos Atletas
        sns.scatterplot(x='peso', y='altura', data=dados, hue='sexo', style='medalha', palette='deep', s=100, ax=axes[0, 1])
        axes[0, 1].set_title('Relação entre Peso e Altura dos Atletas', fontsize=16)
        axes[0, 1].set_xlabel('Peso (kg)', fontsize=14)
        axes[0, 1].set_ylabel('Altura (cm)', fontsize=14)

        # Gráfico 3: Número de Medalhas por País
        sns.countplot(data=dados, x='pais', order=dados['pais'].value_counts().index, palette='viridis', ax=axes[1, 0])
        axes[1, 0].set_title('Número de Medalhas por País', fontsize=16)
        axes[1, 0].set_xlabel('País', fontsize=14)
        axes[1, 0].set_ylabel('Número de Medalhas', fontsize=14)
        axes[1, 0].tick_params(axis='x', rotation=90)

        # Gráfico 4: Matriz de Correlação
        colunas_numericas = dados.select_dtypes(include='number')
        correlation_matrix = colunas_numericas.corr()
        sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='coolwarm', square=True, linewidths=0.5, ax=axes[1, 1])
        axes[1, 1].set_title('Matriz de Correlação', fontsize=16)

        plt.tight_layout()
        plt.show()

    except Exception as e:
        messagebox.showerror("Erro", str(e))

# Função para selecionar o arquivo CSV
def selecionar_arquivo():
    caminho = filedialog.askopenfilename(filetypes=[("Arquivo CSV", "*.csv")])
    caminho_entrada.delete(0, tk.END)  # Limpa o campo de entrada
    caminho_entrada.insert(0, caminho)  # Insere o caminho selecionado

# Configuração da Interface Gráfica com Tkinter
janela = tk.Tk()
janela.title("Análise de Dados das Olimpíadas")

# Labels e Entradas
tk.Label(janela, text="Caminho do arquivo CSV:").grid(row=0, column=0, padx=10, pady=5)
caminho_entrada = tk.Entry(janela, width=50)
caminho_entrada.grid(row=0, column=1, padx=10, pady=5)

# Botão para selecionar o arquivo
tk.Button(janela, text="Selecionar Arquivo", command=selecionar_arquivo).grid(row=0, column=2, padx=10, pady=5)

tk.Label(janela, text="Ano de início:").grid(row=1, column=0, padx=10, pady=5)
ano_inicio_entrada = tk.Entry(janela)
ano_inicio_entrada.grid(row=1, column=1, padx=10, pady=5)

tk.Label(janela, text="Ano de fim:").grid(row=2, column=0, padx=10, pady=5)
ano_fim_entrada = tk.Entry(janela)
ano_fim_entrada.grid(row=2, column=1, padx=10, pady=5)

# Botão para processar os dados
tk.Button(janela, text="Processar Dados", command=processar_dados).grid(row=3, column=0, columnspan=2, pady=20)

# Label para exibir os resultados
resultados = tk.StringVar()
tk.Label(janela, textvariable=resultados).grid(row=4, column=0, columnspan=2, padx=10, pady=10)

# Criação do widget Text para exibir a lista de países
tk.Label(janela, text="Lista de Países:").grid(row=5, column=0, padx=10, pady=5)
lista_paises_frame = tk.Frame(janela)
lista_paises_frame.grid(row=6, column=0, columnspan=2, padx=10, pady=5)

# Criar o widget Text com scrollbar
lista_paises_text = tk.Text(lista_paises_frame, height=10, width=50)
lista_paises_text.pack(side=tk.LEFT, fill=tk.BOTH)

scrollbar = tk.Scrollbar(lista_paises_frame, command=lista_paises_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

lista_paises_text.config(yscrollcommand=scrollbar.set)

# Executar a interface gráfica
janela.mainloop()
