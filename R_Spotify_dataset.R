
install.packages("ggplot2")   
install.packages("corrplot")  
install.packages("plyr")       
install.packages("dplyr")      
install.packages("tidyr")  
install.packages("corrgram")

library(ggplot2)
library(corrplot)
library(plyr)
library(dplyr)
library(tidyr)
library(corrgram)


spotify_data <- read.csv('C:/Users/miglp/OneDrive - CESAE/DATA ANALYST/R/spotify_2023/spotify-2023.csv', sep = ',', header = TRUE, stringsAsFactors = FALSE)
spotify_data <- data.frame(read.csv('C:/Users/miglp/OneDrive - CESAE/DATA ANALYST/R/spotify_2023/spotify-2023.csv', sep = ',', header = TRUE, stringsAsFactors = FALSE))
spotify_data <- apply(spotify_data, 2, as.numeric)
head(spotify_data)

#passar para fatorial


# Convert specific columns to factors
spotify_data$track_name <- factor(spotify_data$track_name)
spotify_data$artist.s._name <- factor(spotify_data$artist.s._name)
spotify_data$mode <- factor(spotify_data$mode)


# Convert non-numeric columns to numeric
numeric_columns <- sapply(spotify_data, is.numeric)
spotify_data[, numeric_columns] <- lapply(spotify_data[, numeric_columns], as.numeric)

# Print the resulting data frame
print(spotify_data)


head(spotify_data)

summary(spotify_data)

str(spotify_data)

colSums(is.na(spotify_data))

colnames(spotify_data)

dim(spotify_data)

correlation_matrix <- cor(select(spotify_data, streams, in_spotify_playlists, in_apple_playlists, in_deezer_playlists, bpm, `danceability_%`, `valence_%`, `energy_%`, `acousticness_%`))
print(correlation_matrix)


#relevant_columns <- c("streams", "in_spotify_playlists", "in_apple_playlists", "in_deezer_playlists", "bpm", "danceability_%", "valence_%", "energy_%", "acousticness_%", "instrumentalness_%", "liveness_%", "speechiness_%")
relevant_columns <- c("streams", "in_spotify_playlists", "in_apple_playlists", "in_deezer_playlists", "bpm")
correlation_matrix <- cor(select(spotify_data, relevant_columns))
print(correlation_matrix)


correlation_matrix <- cor(select(spotify_data, relevant_columns))
print(correlation_matrix)

cor_matrix <- cor(spotify_data[, c("danceability_%", "valence_%", "energy_%", "acousticness_%", "in_spotify_playlists", "in_apple_playlists", "in_deezer_playlists")])
print(cor_matrix)



