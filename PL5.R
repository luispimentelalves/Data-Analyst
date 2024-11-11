install.packages("factoextra")
library(factoextra)
library(corrgram)
library(dplyr)

#a.Considere o ficheiro fornecido (casas), crie uma tabela normalizada (scaled).

casas <- data.frame(read.csv("C:/Users/miglp/OneDrive - CESAE/DATA ANALYST/R/PL3/PL3/casas.csv", sep = ';'))

casas.numeric<-subset(casas, select = -c(id,date))#remoção das colunas id e date para poder escalar o dataset

#scaled
casas.scaled<-as.data.frame(scale(casas.numeric))

corrgram(casas.scaled)

#b.Crie o gráfico cotovelo segundo método silhouette

nclust<-fviz_nbclust(casas.scaled, kmeans, method="silhouette")

#c.Garde numa variável o número de cluster ideais.

nclust<-nclust$data #reduz a informacao que aparece abaixo
n_clusters<-as.numeric(nclust$clusters[which.max(nclust$y)]) #valor mais alto

#d.Execute a classificação em clusters usando o Kmeans
km <- kmeans(casas.scaled, centers = n_clusters,iter.max = 100, nstart = 25)

#e.Cria um gráfico com a representação visual dos clusters
fviz_cluster(km,data=casas.scaled)

#f.Adiciona o número do cluster ao dataset original

casas <- casas |> mutate(cluster=km$cluster)
corrgram(casas)

#g.Produza um gráfico de dispersão com base nos clusters e tente classificar os grupos gerados
pairs(casas[3:8], pch = 21, bg = c("red","green","cyan")[unclass(casas.scaled$Cluster)])

########################################################################################
#2-a.Gere os clusters e classifique os grupos de acordo com os clusters gerados
# Carregar as bibliotecas necessárias

library(readr)  # Para ler o arquivo de dados
library(dplyr)  # Para manipulação de dados
library(tidyr)  # Para trabalhar com dados arrumados
library(ggplot2)  # Para visualização

# Carregar o conjunto de dados
bank_clients <- read_csv("caminho/para/o/seu/arquivo/bank_clients.csv")

# Pré-processamento de dados, se necessário
# Isso pode incluir tratar valores ausentes, converter variáveis categóricas em numéricas, etc.

# Exemplo: Tratamento de valores ausentes
bank_clients <- bank_clients %>%
  na.omit()  # Remover linhas com valores ausentes

# Executar o algoritmo K-means
# Defina o número de clusters desejado (nclust)
nclust <- 4  # Altere conforme necessário

# Selecionar apenas as variáveis numéricas relevantes para o algoritmo K-means
bank_clients_numeric <- bank_clients %>%
  select_if(is.numeric)

# Executar o algoritmo K-means
km <- kmeans(bank_clients_numeric, centers = nclust, iter.max = 100, nstart = 25)

# Adicionar as atribuições de cluster aos dados originais
bank_clients <- bank_clients %>%
  mutate(cluster = km$cluster)

# Visualizar os clusters (opcional)
# Por exemplo, um gráfico de dispersão das duas primeiras variáveis numéricas com cores representando clusters
ggplot(bank_clients, aes(x = var1, y = var2, color = as.factor(cluster))) +
  geom_point() +
  labs(title = "Gráfico de Dispersão com Clusters",
       x = "Variável 1",
       y = "Variável 2",
       color = "Cluster") +
  theme_minimal()


