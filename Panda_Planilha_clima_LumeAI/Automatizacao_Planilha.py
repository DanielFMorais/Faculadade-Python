import pandas as pd  # Importa a biblioteca pandas, usada para manipulação e análise de dados

# Caminho do arquivo de entrada (o arquivo Excel com os dados originais)
arquivo_entrada = "dados_2024.xlsx" #Troque pelo nome do seu arquivo

# Caminho do arquivo de saída (onde será salvo o arquivo com médias diárias)
arquivo_saida = "dados_2024_media_diaria_corrigida.xlsx" #Troque pelo nome desejado para o arquivo de saída

# Lê a planilha Excel e transforma em um DataFrame do pandas
# DataFrame é como uma tabela em memória, que facilita cálculos e manipulação
df = pd.read_excel(arquivo_entrada)

# Substitui valores especiais que indicam "dados ausentes" (-9999) por NaN (Not a Number)
# Também substitui zeros por NaN, caso queira ignorá-los nos cálculos
# pd.NA é usado para representar valores ausentes de forma consistente
df.replace(-9999, pd.NA, inplace=True)
df.replace(0, pd.NA, inplace=True)

# Converte a coluna 'DATA' para o tipo datetime
# Isso permite manipular datas corretamente (como extrair dia, mês, ano)
# 'errors="coerce"' transforma datas inválidas em NaT (Not a Time)
df['DATA'] = pd.to_datetime(df['DATA'], errors='coerce')

# Cria uma nova coluna 'DIA' apenas com a parte da data (sem hora)
# Isso é útil para agrupar os dados por dia inteiro
df['DIA'] = df['DATA'].dt.date

# Seleciona todas as colunas que serão usadas para calcular a média diária
# Excluímos 'DATA' e 'DIA' porque não faz sentido calcular média de datas
colunas_para_media = [col for col in df.columns if col not in ['DATA', 'DIA']]

# Agrupa os dados por 'DIA' e calcula a média de cada coluna numérica
# Valores NaN são ignorados automaticamente no cálculo da média
df_media = df.groupby('DIA')[colunas_para_media].mean().reset_index()
# reset_index() transforma o índice (que era a coluna 'DIA') em uma coluna normal

# O DataFrame final será apenas as médias diárias
# Se houver outras colunas não numéricas que queira manter, precisaríamos incluí-las manualmente
df_final = df_media

# Salva o DataFrame final em um arquivo Excel
# index=False evita que o pandas adicione uma coluna extra de índice
df_final.to_excel(arquivo_saida, index=False)

# Mensagem de confirmação de que o arquivo foi gerado com sucesso
print("✅ Arquivo gerado com sucesso:", arquivo_saida)
