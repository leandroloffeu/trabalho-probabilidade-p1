import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import tkinter as tk
from tkinter import filedialog, messagebox

# Função para remover outliers
def remove_outliers(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    return df[(df[column] >= (Q1 - 1.5 * IQR)) & (df[column] <= (Q3 + 1.5 * IQR))]

# Função para listar os países do arquivo CSV
def listar_paises():
    caminho_arquivo = caminho_entrada.get()

    if not os.path.exists(caminho_arquivo):
        messagebox.showerror("Erro", "O arquivo não foi encontrado. Verifique o caminho.")
        return

    try:
        # Carregar os dados do arquivo CSV
        dados = pd.read_csv(caminho_arquivo)
        paises_unicos = dados['pais'].unique()  # Obter países únicos

        # Limpar o campo de texto antes de adicionar novos países
        lista_paises_text.delete(1.0, tk.END)
        for pais in paises_unicos:
            lista_paises_text.insert(tk.END, f"{pais}\n")  # Inserir cada país em uma nova linha

    except Exception as e:
        messagebox.showerror("Erro", str(e))

# Função para processar os dados e gerar os gráficos
def processar_dados():
    caminho_arquivo = caminho_entrada.get()
    
    # Verificar se o arquivo existe
    if not os.path.exists(caminho_arquivo):
        messagebox.showerror("Erro", "O arquivo não foi encontrado. Verifique o caminho.")
        return

    try:
        # Carregar os dados do arquivo CSV
        dados = pd.read_csv(caminho_arquivo)
        
        # Solicitar ano de início, fim e país
        ano_inicio = int(ano_inicio_entrada.get())
        ano_fim = int(ano_fim_entrada.get())
        pais_selecionado = pais_entrada.get()

        # Filtrar os dados pelos anos e pelo país especificado
        dados_filtrados = dados[(dados['ano'] >= ano_inicio) & (dados['ano'] <= ano_fim) & (dados['pais'] == pais_selecionado)]

        # Tratamento de Valores Ausentes e Outliers
        dados_filtrados = dados_filtrados.dropna()
        dados_filtrados = remove_outliers(dados_filtrados, 'altura')
        dados_filtrados = remove_outliers(dados_filtrados, 'peso')

        # Estatísticas Descritivas
        media_altura = dados_filtrados['altura'].mean()
        desvio_padrao_altura = dados_filtrados['altura'].std()
        media_peso = dados_filtrados['peso'].mean()
        desvio_padrao_peso = dados_filtrados['peso'].std()

        resultado_stats.set(f'Média Altura: {media_altura:.2f} cm, Desvio Padrão Altura: {desvio_padrao_altura:.2f} cm\n'
                            f'Média Peso: {media_peso:.2f} kg, Desvio Padrão Peso: {desvio_padrao_peso:.2f} kg')

        # Estilo do Seaborn
        sns.set(style='whitegrid')

        # Criar dashboard com subplots
        fig, axes = plt.subplots(2, 2, figsize=(20, 15))

        # Gráfico 1: Distribuição da Altura
        sns.histplot(dados_filtrados['altura'], bins=30, kde=True, color='skyblue', stat='density', ax=axes[0, 0])
        axes[0, 0].set_title(f'Distribuição da Altura dos Atletas ({pais_selecionado})', fontsize=16)
        axes[0, 0].set_xlabel('Altura (cm)', fontsize=14)
        axes[0, 0].set_ylabel('Densidade', fontsize=14)
        axes[0, 0].axvline(media_altura, color='red', linestyle='--', label='Média: {:.2f} cm'.format(media_altura))
        axes[0, 0].axvline(media_altura + desvio_padrao_altura, color='orange', linestyle='--', label='Desvio Padrão: {:.2f} cm'.format(desvio_padrao_altura))
        axes[0, 0].axvline(media_altura - desvio_padrao_altura, color='orange', linestyle='--')
        axes[0, 0].legend()

        # Gráfico 2: Relação entre Peso e Altura
        sns.scatterplot(x='peso', y='altura', data=dados_filtrados, hue='sexo', style='medalha', palette='deep', s=100, ax=axes[0, 1])
        axes[0, 1].set_title(f'Relação entre Peso e Altura ({pais_selecionado})', fontsize=16)
        axes[0, 1].set_xlabel('Peso (kg)', fontsize=14)
        axes[0, 1].set_ylabel('Altura (cm)', fontsize=14)

        # Gráfico 3: Número de Medalhas por País
        sns.countplot(data=dados_filtrados, x='pais', hue='pais', order=dados_filtrados['pais'].value_counts().index, palette='viridis', ax=axes[1, 0])
        axes[1, 0].set_title(f'Número de Medalhas por País ({pais_selecionado})', fontsize=16)
        axes[1, 0].set_xlabel('País', fontsize=14)
        axes[1, 0].set_ylabel('Número de Medalhas', fontsize=14)
        axes[1, 0].tick_params(axis='x', rotation=90)

        # Gráfico 4: Matriz de Correlação (somente colunas numéricas)
        colunas_numericas = dados_filtrados.select_dtypes(include='number')
        correlation_matrix = colunas_numericas.corr()
        sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='coolwarm', square=True, linewidths=0.5, ax=axes[1, 1])
        axes[1, 1].set_title(f'Matriz de Correlação ({pais_selecionado})', fontsize=16)

        # Ajustar layout
        plt.tight_layout()
        plt.show()

        # Salvar dados processados
        dados_filtrados.to_csv(f'dados_limpos_{pais_selecionado}.csv', index=False)
        messagebox.showinfo("Sucesso", f'Dados salvos como dados_limpos_{pais_selecionado}.csv')

    except Exception as e:
        messagebox.showerror("Erro", str(e))

# Função para selecionar o arquivo
def selecionar_arquivo():
    caminho = filedialog.askopenfilename(filetypes=[("Arquivo CSV", "*.csv")])
    caminho_entrada.set(caminho)

# Configuração da interface gráfica
janela = tk.Tk()
janela.title("Análise de Dados Olímpicos")

# Labels e Entradas
tk.Label(janela, text="Caminho do arquivo CSV:").grid(row=0, column=0, padx=10, pady=5)
caminho_entrada = tk.StringVar()
tk.Entry(janela, textvariable=caminho_entrada, width=50).grid(row=0, column=1, padx=10, pady=5)
tk.Button(janela, text="Selecionar Arquivo", command=selecionar_arquivo).grid(row=0, column=2, padx=10, pady=5)

# Botão para listar os países
tk.Button(janela, text="Listar Países", command=listar_paises).grid(row=0, column=3, padx=10, pady=5)

tk.Label(janela, text="Ano de início:").grid(row=1, column=0, padx=10, pady=5)
ano_inicio_entrada = tk.Entry(janela)
ano_inicio_entrada.grid(row=1, column=1, padx=10, pady=5)

tk.Label(janela, text="Ano de fim:").grid(row=2, column=0, padx=10, pady=5)
ano_fim_entrada = tk.Entry(janela)
ano_fim_entrada.grid(row=2, column=1, padx=10, pady=5)

tk.Label(janela, text="País:").grid(row=3, column=0, padx=10, pady=5)
pais_entrada = tk.Entry(janela)
pais_entrada.grid(row=3, column=1, padx=10, pady=5)

# Label para exibir a lista de países
tk.Label(janela, text="Lista de Países:").grid(row=4, column=0, padx=10, pady=5)
lista_paises_text = tk.Text(janela, height=10, width=40)
lista_paises_text.grid(row=4, column=1, padx=10, pady=5)

# Variável para armazenar o resultado das estatísticas
resultado_stats = tk.StringVar()
tk.Label(janela, textvariable=resultado_stats, justify=tk.LEFT).grid(row=5, column=0, columnspan=4, padx=10, pady=5)

# Botão para processar os dados
tk.Button(janela, text="Processar Dados", command=processar_dados).grid(row=6, column=0, columnspan=4, padx=10, pady=5)

# Iniciar o loop da interface gráfica
janela.mainloop()
