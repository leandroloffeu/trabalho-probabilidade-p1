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

# Função para processar os dados e gerar gráficos
def processar_dados():
    caminho_arquivo = caminho_entrada.get()
    
    # Verificar se o arquivo existe
    if not os.path.exists(caminho_arquivo):
        messagebox.showerror("Erro", "O arquivo não foi encontrado. Verifique o caminho.")
        return

    try:
        # Carregar os dados do arquivo CSV
        dados = pd.read_csv(caminho_arquivo)

        # Compreensão Inicial dos Dados
        info_texto = dados.info()
        print(info_texto)
        
        # Tratamento de Valores Ausentes
        dados = dados.dropna()

        # Remover outliers nas colunas 'altura' e 'peso'
        dados = remove_outliers(dados, 'altura')
        dados = remove_outliers(dados, 'peso')

        # Estatísticas Descritivas
        media_altura = dados['altura'].mean()
        desvio_padrao_altura = dados['altura'].std()
        media_peso = dados['peso'].mean()
        desvio_padrao_peso = dados['peso'].std()
        
        # Atualizar a caixa de texto com as estatísticas
        resultado_stats.set(f'Média Altura: {media_altura:.2f} cm\n'
                            f'Desvio Padrão Altura: {desvio_padrao_altura:.2f} cm\n'
                            f'Média Peso: {media_peso:.2f} kg\n'
                            f'Desvio Padrão Peso: {desvio_padrao_peso:.2f} kg')

        # Estilo do Seaborn
        sns.set(style='whitegrid')

        # Gráfico de Distribuição da Altura
        plt.figure(figsize=(10, 6))
        sns.histplot(dados['altura'], bins=30, kde=True, color='skyblue', stat='density')
        plt.title('Distribuição da Altura dos Atletas', fontsize=16)
        plt.xlabel('Altura (cm)', fontsize=14)
        plt.ylabel('Densidade', fontsize=14)
        plt.axvline(media_altura, color='red', linestyle='--', label='Média: {:.2f} cm'.format(media_altura))
        plt.axvline(media_altura + desvio_padrao_altura, color='orange', linestyle='--', label='Desvio Padrão: {:.2f} cm'.format(desvio_padrao_altura))
        plt.axvline(media_altura - desvio_padrao_altura, color='orange', linestyle='--')
        plt.legend()
        plt.show()

        # Gráfico de Dispersão entre Peso e Altura
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x='peso', y='altura', data=dados, hue='sexo', style='medalha', palette='deep', s=100)
        plt.title('Relação entre Peso e Altura dos Atletas', fontsize=16)
        plt.xlabel('Peso (kg)', fontsize=14)
        plt.ylabel('Altura (cm)', fontsize=14)
        plt.grid(True)
        plt.legend(title='Sexo / Medalha')
        plt.show()

        # Gráfico de Contagem do Número de Medalhas por País
        plt.figure(figsize=(12, 6))
        sns.countplot(data=dados, x='pais', order=dados['pais'].value_counts().index, palette='viridis')
        plt.xticks(rotation=90)
        plt.title('Número de Medalhas por País', fontsize=16)
        plt.xlabel('País', fontsize=14)
        plt.ylabel('Número de Medalhas', fontsize=14)
        plt.grid(axis='y')
        plt.show()

        # Matriz de Correlação
        plt.figure(figsize=(12, 8))
        correlation_matrix = dados.corr()
        sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='coolwarm', square=True, linewidths=0.5)
        plt.title('Matriz de Correlação', fontsize=16)
        plt.show()

        # Salvar dados processados
        dados.to_csv('dados_limpos.csv', index=False)
        messagebox.showinfo("Sucesso", "Dados processados e salvos como 'dados_limpos.csv'.")

    except Exception as e:
        messagebox.showerror("Erro", str(e))

# Função para listar países
def listar_paises():
    caminho_arquivo = caminho_entrada.get()
    
    # Verificar se o arquivo existe
    if not os.path.exists(caminho_arquivo):
        messagebox.showerror("Erro", "O arquivo não foi encontrado. Verifique o caminho.")
        return

    try:
        # Carregar os dados do arquivo CSV
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
janela.title("Análise de Dados Olímpicos")

# Labels e Entradas
tk.Label(janela, text="Caminho do arquivo CSV:").grid(row=0, column=0, padx=10, pady=5)
caminho_entrada = tk.Entry(janela, width=50)
caminho_entrada.grid(row=0, column=1, padx=10, pady=5)

# Botão para selecionar o arquivo
tk.Button(janela, text="Selecionar Arquivo", command=selecionar_arquivo).grid(row=0, column=2, padx=10, pady=5)

# Botão para processar os dados
tk.Button(janela, text="Analisar Dados", command=processar_dados).grid(row=1, column=0, columnspan=3, pady=20)

# Botão para listar países
tk.Button(janela, text="Listar Países", command=listar_paises).grid(row=2, column=0, columnspan=3, pady=5)

# Caixa de texto para exibir a lista de países
lista_paises = tk.Text(janela, height=10, width=60)
lista_paises.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

# Label para exibir as estatísticas
resultado_stats = tk.StringVar()
tk.Label(janela, textvariable=resultado_stats, justify='left').grid(row=4, column=0, columnspan=3, padx=10, pady=10)

# Executar a interface gráfica
janela.mainloop()
