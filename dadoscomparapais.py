import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog  # Importar filedialog

# Função para listar os países do arquivo CSV
def listar_paises():
    caminho_arquivo = caminho_entrada.get()

    if not os.path.exists(caminho_arquivo):
        messagebox.showerror("Erro", "O arquivo não foi encontrado. Verifique o caminho.")
        return

    try:
        # Carregar os dados
        dados = pd.read_csv(caminho_arquivo)
        paises_unicos = dados['pais'].unique()  # Obter países únicos

        # Limpar o campo de texto antes de adicionar novos países
        lista_paises_text.delete(1.0, tk.END)
        for pais in paises_unicos:
            lista_paises_text.insert(tk.END, f"{pais}\n")  # Inserir cada país em uma nova linha

    except Exception as e:
        messagebox.showerror("Erro", str(e))

# Função para processar e comparar dados dos dois países
def processar_dados():
    caminho_arquivo = caminho_entrada.get()

    if not os.path.exists(caminho_arquivo):
        messagebox.showerror("Erro", "O arquivo não foi encontrado. Verifique o caminho.")
        return

    try:
        # Carregar os dados
        dados = pd.read_csv(caminho_arquivo)

        # Solicitar ano de início e fim e os países
        ano_inicio = int(ano_inicio_entrada.get())
        ano_fim = int(ano_fim_entrada.get())
        pais_1 = pais_1_entrada.get()
        pais_2 = pais_2_entrada.get()

        # Filtrar os dados pelos anos e pelos países especificados
        dados_pais_1 = dados[(dados['ano'] >= ano_inicio) & (dados['ano'] <= ano_fim) & (dados['pais'] == pais_1)]
        dados_pais_2 = dados[(dados['ano'] >= ano_inicio) & (dados['ano'] <= ano_fim) & (dados['pais'] == pais_2)]

        # Tratamento de valores ausentes
        dados_pais_1 = dados_pais_1.dropna(subset=['altura', 'peso'])
        dados_pais_2 = dados_pais_2.dropna(subset=['altura', 'peso'])

        # Estatísticas descritivas para os dois países
        if not dados_pais_1.empty:
            media_altura_1 = dados_pais_1['altura'].mean()
            desvio_padrao_altura_1 = dados_pais_1['altura'].std()
            media_peso_1 = dados_pais_1['peso'].mean()
            desvio_padrao_peso_1 = dados_pais_1['peso'].std()

            resultados_pais_1.set(f'{pais_1} - Média Altura: {media_altura_1:.2f} cm, Desvio Padrão Altura: {desvio_padrao_altura_1:.2f} cm\n'
                                  f'{pais_1} - Média Peso: {media_peso_1:.2f} kg, Desvio Padrão Peso: {desvio_padrao_peso_1:.2f} kg')
        else:
            resultados_pais_1.set(f'{pais_1} - Não há dados disponíveis para o período selecionado.')

        if not dados_pais_2.empty:
            media_altura_2 = dados_pais_2['altura'].mean()
            desvio_padrao_altura_2 = dados_pais_2['altura'].std()
            media_peso_2 = dados_pais_2['peso'].mean()
            desvio_padrao_peso_2 = dados_pais_2['peso'].std()

            resultados_pais_2.set(f'{pais_2} - Média Altura: {media_altura_2:.2f} cm, Desvio Padrão Altura: {desvio_padrao_altura_2:.2f} cm\n'
                                  f'{pais_2} - Média Peso: {media_peso_2:.2f} kg, Desvio Padrão Peso: {desvio_padrao_peso_2:.2f} kg')
        else:
            resultados_pais_2.set(f'{pais_2} - Não há dados disponíveis para o período selecionado.')

        # Criar gráficos somente se houver dados para ambos os países
        if not dados_pais_1.empty and not dados_pais_2.empty:
            sns.set(style='whitegrid')

            # Criar dashboard comparativo com subplots
            fig, axes = plt.subplots(2, 2, figsize=(20, 15))

            # Gráfico 1: Comparação da distribuição de altura
            sns.histplot(dados_pais_1['altura'], bins=30, kde=True, color='skyblue', stat='density', label=pais_1, ax=axes[0, 0])
            sns.histplot(dados_pais_2['altura'], bins=30, kde=True, color='green', stat='density', label=pais_2, ax=axes[0, 0])
            axes[0, 0].set_title(f'Distribuição da Altura ({pais_1} vs {pais_2})', fontsize=16)
            axes[0, 0].set_xlabel('Altura (cm)', fontsize=14)
            axes[0, 0].set_ylabel('Densidade', fontsize=14)
            axes[0, 0].legend()

            # Gráfico 2: Comparação da relação entre peso e altura
            sns.scatterplot(x='peso', y='altura', data=dados_pais_1, hue='sexo', style='medalha', palette='deep', s=100, ax=axes[0, 1])
            sns.scatterplot(x='peso', y='altura', data=dados_pais_2, hue='sexo', style='medalha', palette='dark', s=100, ax=axes[0, 1])
            axes[0, 1].set_title(f'Relação entre Peso e Altura ({pais_1} vs {pais_2})', fontsize=16)
            axes[0, 1].set_xlabel('Peso (kg)', fontsize=14)
            axes[0, 1].set_ylabel('Altura (cm)', fontsize=14)

            # Gráfico 3: Contagem de medalhas por sexo
            sns.countplot(x='sexo', hue='pais', data=dados[(dados['pais'] == pais_1) | (dados['pais'] == pais_2)], palette='viridis', ax=axes[1, 0])
            axes[1, 0].set_title(f'Número de Medalhas por Sexo ({pais_1} vs {pais_2})', fontsize=16)
            axes[1, 0].set_xlabel('Sexo', fontsize=14)
            axes[1, 0].set_ylabel('Número de Medalhas', fontsize=14)

            # Ajustar layout
            plt.tight_layout()
            plt.show()
        else:
            messagebox.showinfo("Informação", "Não há dados suficientes para gerar os gráficos.")

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
janela.title("Comparação de Atletas Olímpicos entre Países")

# Labels e Entradas
tk.Label(janela, text="Caminho do arquivo CSV:").grid(row=0, column=0, padx=10, pady=5)
caminho_entrada = tk.Entry(janela, width=50)
caminho_entrada.grid(row=0, column=1, padx=10, pady=5)

# Botão para selecionar o arquivo
tk.Button(janela, text="Selecionar Arquivo", command=selecionar_arquivo).grid(row=0, column=2, padx=10, pady=5)

# Botão para listar os países
tk.Button(janela, text="Listar Países", command=listar_paises).grid(row=0, column=3, padx=10, pady=5)

tk.Label(janela, text="Ano de início:").grid(row=1, column=0, padx=10, pady=5)
ano_inicio_entrada = tk.Entry(janela)
ano_inicio_entrada.grid(row=1, column=1, padx=10, pady=5)

tk.Label(janela, text="Ano de fim:").grid(row=2, column=0, padx=10, pady=5)
ano_fim_entrada = tk.Entry(janela)
ano_fim_entrada.grid(row=2, column=1, padx=10, pady=5)

tk.Label(janela, text="País 1:").grid(row=3, column=0, padx=10, pady=5)
pais_1_entrada = tk.Entry(janela)
pais_1_entrada.grid(row=3, column=1, padx=10, pady=5)

tk.Label(janela, text="País 2:").grid(row=4, column=0, padx=10, pady=5)
pais_2_entrada = tk.Entry(janela)
pais_2_entrada.grid(row=4, column=1, padx=10, pady=5)

# Botão para processar os dados
tk.Button(janela, text="Comparar Países", command=processar_dados).grid(row=5, column=0, columnspan=3, pady=20)

# Label para exibir a lista de países
tk.Label(janela, text="Lista de Países:").grid(row=6, column=0, padx=10, pady=5, columnspan=2)
lista_paises_text = tk.Text(janela, height=10, width=40)
lista_paises_text.grid(row=7, column=0, columnspan=4, padx=10, pady=5)

# Labels para exibir os resultados
resultados_pais_1 = tk.StringVar()
tk.Label(janela, textvariable=resultados_pais_1).grid(row=8, column=0, columnspan=3, padx=10, pady=5)

resultados_pais_2 = tk.StringVar()
tk.Label(janela, textvariable=resultados_pais_2).grid(row=9, column=0, columnspan=3, padx=10, pady=5)

# Iniciar a interface gráfica
janela.mainloop()
