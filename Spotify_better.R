# ====================================
# A comprehensive analysis of Spotify's most streamed songs in 2023

# Package Installation and Loading
# ================================

# Install required packages if not already installed
#install.packages(c("ggplot2", "corrplot", "dplyr", "tidyr", "corrgram", "readr", "janitor", "viridis", "plotly", "knitr", "scales", "gridExtra", "RColorBrewer", "stringr"))

# Load all libraries
library(ggplot2)
library(corrplot)
library(dplyr)
library(tidyr)
library(corrgram)
library(readr)
library(janitor)
library(viridis)
library(plotly)
library(knitr)
library(scales)
library(gridExtra)
library(RColorBrewer)
library(stringr)

# Set global theme for ggplot
theme_set(theme_minimal() +
            theme(plot.title = element_text(hjust = 0.5, size = 14, face = "bold"),
                  plot.subtitle = element_text(hjust = 0.5, size = 12)))

# Data Loading and Initial Exploration
# ====================================

cat("🎵 SPOTIFY 2023 DATA ANALYSIS\n")
cat("============================\n\n")

# Load the data with error handling
tryCatch({
  spotify_data <- read_csv(
    'spotify-2023.csv',
    locale = locale(encoding = "UTF-8"),
    na = c("", "NA", "N/A", "null", "BPM110KeyAModeMajorDanceability53Valence75Energy69Acousticness7Instrumentalness0Liveness17Speechiness3")
  )
  cat("✅ Data loaded successfully!\n")
}, error = function(e) {
  # Try alternative file names/paths
  possible_files <- c(
    'spotify_2023.csv',
    'Spotify_2023.csv'
  )
  
  for (file in possible_files) {
    tryCatch({
      spotify_data <<- read_csv(file, locale = locale(encoding = "UTF-8"))
      cat(paste("✅ Data loaded from:", file, "\n"))
      break
    }, error = function(e) {
      cat("❌ Error loading file:", file, "\n")
      cat("Message:", e$message, "\n")
    })
  }
})

# Check if data was loaded
if (!exists("spotify_data")) {
  stop("❌ Could not load the Spotify dataset. Please check the file path and try again.")
}

# Display initial data info
cat("\n📊 INITIAL DATA OVERVIEW\n")
cat("------------------------\n")
cat("Dimensions:", paste(dim(spotify_data), collapse = " x "), "\n")
cat("Columns:", ncol(spotify_data), "\n")
cat("Rows:", nrow(spotify_data), "\n\n")

# Display column names
cat("Column Names:\n")
print(colnames(spotify_data))

# Data Cleaning and Preprocessing
# ===============================

cat("\n🧹 DATA CLEANING\n")
cat("----------------\n")

# Clean column names and handle data types
spotify_clean <- spotify_data %>%
  clean_names() %>%
  mutate(
    # Clean streams column (remove any non-numeric characters)
    streams = as.numeric(str_extract(as.character(streams), "\\d+")),
    # Clean playlist columns
    in_spotify_playlists = as.numeric(str_extract(as.character(in_spotify_playlists), "\\d+")),
    in_apple_playlists = as.numeric(str_extract(as.character(in_apple_playlists), "\\d+")),
    in_deezer_playlists = as.numeric(str_extract(as.character(in_deezer_playlists), "\\d+")),
    # Clean chart columns
    in_spotify_charts = as.numeric(str_extract(as.character(in_spotify_charts), "\\d+")),
    in_apple_charts = as.numeric(str_extract(as.character(in_apple_charts), "\\d+")),
    in_deezer_charts = as.numeric(str_extract(as.character(in_deezer_charts), "\\d+")),
    in_shazam_charts = as.numeric(str_extract(as.character(in_shazam_charts), "\\d+")),
    # Clean audio features (handle percentage columns)
    danceability_percent = as.numeric(str_extract(as.character(danceability_percent), "\\d+")),
    valence_percent = as.numeric(str_extract(as.character(valence_percent), "\\d+")),
    energy_percent = as.numeric(str_extract(as.character(energy_percent), "\\d+")),
    acousticness_percent = as.numeric(str_extract(as.character(acousticness_percent), "\\d+")),
    instrumentalness_percent = as.numeric(str_extract(as.character(instrumentalness_percent), "\\d+")),
    liveness_percent = as.numeric(str_extract(as.character(liveness_percent), "\\d+")),
    speechiness_percent = as.numeric(str_extract(as.character(speechiness_percent), "\\d+")),
    # Clean BPM
    bpm = as.numeric(str_extract(as.character(bpm), "\\d+")),
    # Convert categorical variables
    key = as.factor(key),
    mode = as.factor(mode),
    track_name = as.factor(track_name),
    artist_s_name = as.factor(artist_s_name),
    # Handle date columns
    released_year = as.numeric(released_year),
    released_month = as.numeric(released_month),
    released_day = as.numeric(released_day)
  ) %>%
  # Remove rows with critical missing data
  filter(!is.na(streams), !is.na(track_name), !is.na(artist_s_name))

cat("✅ Data cleaning completed!\n")
cat("Final dimensions:", paste(dim(spotify_clean), collapse = " x "), "\n")

# Data Quality Assessment
# ======================

cat("\n🔍 DATA QUALITY ASSESSMENT\n")
cat("--------------------------\n")

# Missing values analysis
missing_summary <- spotify_clean %>%
  summarise_all(~sum(is.na(.))) %>%
  pivot_longer(everything(), names_to = "column", values_to = "missing_count") %>%
  mutate(missing_percent = round((missing_count / nrow(spotify_clean)) * 100, 2)) %>%
  filter(missing_count > 0) %>%
  arrange(desc(missing_count))

if (nrow(missing_summary) > 0) {
  cat("Missing Values Summary:\n")
  print(missing_summary)
} else {
  cat("✅ No missing values found in critical columns!\n")
}

# Basic statistics
cat("\n📈 DESCRIPTIVE STATISTICS\n")
cat("-------------------------\n")
summary(select_if(spotify_clean, is.numeric))

# Exploratory Data Analysis
# =========================

cat("\n📊 EXPLORATORY DATA ANALYSIS\n")
cat("-----------------------------\n")

# 1. Top 10 most streamed songs
top_songs <- spotify_clean %>%
  arrange(desc(streams)) %>%
  head(10) %>%
  select(track_name, artist_s_name, streams, released_year)

cat("🎵 TOP 10 MOST STREAMED SONGS:\n")
print(top_songs)

# 2. Top artists by total streams
top_artists <- spotify_clean %>%
  group_by(artist_s_name) %>%
  summarise(
    total_streams = sum(streams, na.rm = TRUE),
    song_count = n(),
    avg_streams = mean(streams, na.rm = TRUE)
  ) %>%
  arrange(desc(total_streams)) %>%
  head(10)

cat("\n🎤 TOP 10 ARTISTS BY TOTAL STREAMS:\n")
print(top_artists)

# Data Visualization
# ==================

cat("\n📈 CREATING VISUALIZATIONS\n")
cat("--------------------------\n")

# 1. Distribution of Streams
p1 <- ggplot(spotify_clean, aes(x = streams)) +
  geom_histogram(bins = 50, fill = "#1DB954", alpha = 0.7) +
  scale_x_continuous(labels = scales::comma) +
  labs(title = "Distribution of Streams",
       subtitle = "Most songs have relatively low stream counts",
       x = "Number of Streams",
       y = "Frequency") +
  theme_minimal()

print(p1)

# 2. Streams by Release Year
p2 <- spotify_clean %>%
  filter(!is.na(released_year), released_year >= 2000) %>%
  group_by(released_year) %>%
  summarise(avg_streams = mean(streams, na.rm = TRUE), .groups = 'drop') %>%
  ggplot(aes(x = released_year, y = avg_streams)) +
  geom_line(color = "#1DB954", size = 1.2) +
  geom_point(color = "#1DB954", size = 2) +
  scale_y_continuous(labels = scales::comma) +
  labs(title = "Average Streams by Release Year",
       subtitle = "Trends in song popularity over time",
       x = "Release Year",
       y = "Average Streams") +
  theme_minimal()

print(p2)

# 3. Audio Features Distribution
audio_features <- c("danceability_percent", "valence_percent", "energy_percent",
                    "acousticness_percent", "instrumentalness_percent",
                    "liveness_percent", "speechiness_percent")

# Check which audio features exist in our cleaned data
existing_features <- audio_features[audio_features %in% colnames(spotify_clean)]

if (length(existing_features) > 0) {
  audio_data <- spotify_clean %>%
    select(all_of(existing_features)) %>%
    pivot_longer(everything(), names_to = "feature", values_to = "value") %>%
    filter(!is.na(value))
  
  p3 <- ggplot(audio_data, aes(x = feature, y = value, fill = feature)) +
    geom_boxplot(alpha = 0.7) +
    scale_fill_viridis_d() +
    labs(title = "Distribution of Audio Features",
         subtitle = "Box plots showing the spread of audio characteristics",
         x = "Audio Feature",
         y = "Value (%)") +
    theme_minimal() +
    theme(axis.text.x = element_text(angle = 45, hjust = 1),
          legend.position = "none")
  
  print(p3)
}

# 4. Mode and Key Analysis
if ("mode" %in% colnames(spotify_clean) && "key" %in% colnames(spotify_clean)) {
  p4 <- spotify_clean %>%
    filter(!is.na(mode), !is.na(key)) %>%
    group_by(mode, key) %>%
    summarise(count = n(), avg_streams = mean(streams, na.rm = TRUE), .groups = 'drop') %>%
    ggplot(aes(x = key, y = count, fill = mode)) +
    geom_col(position = "dodge", alpha = 0.8) +
    scale_fill_manual(values = c("#1DB954", "#FF6B6B")) +
    labs(title = "Song Distribution by Key and Mode",
         subtitle = "Popular keys and modes in 2023",
         x = "Key",
         y = "Number of Songs",
         fill = "Mode") +
    theme_minimal() +
    theme(axis.text.x = element_text(angle = 45, hjust = 1))
  
  print(p4)
}

# Correlation Analysis
# ===================

cat("\n🔗 CORRELATION ANALYSIS\n")
cat("-----------------------\n")

# Get all numeric columns for correlation
numeric_cols <- spotify_clean %>%
  select_if(is.numeric) %>%
  select(-released_year, -released_month, -released_day) %>%
  colnames()

cat("Numeric columns for correlation analysis:\n")
print(numeric_cols)

# Calculate correlation matrix
if (length(numeric_cols) > 1) {
  correlation_matrix <- spotify_clean %>%
    select(all_of(numeric_cols)) %>%
    cor(use = "complete.obs")
  
  # Display correlation matrix
  cat("\nCorrelation Matrix:\n")
  print(round(correlation_matrix, 3))
  
  # Create correlation plot
  corrplot(correlation_matrix,
           method = "color",
           type = "upper",
           order = "hclust",
           tl.cex = 0.8,
           tl.col = "black",
           title = "Spotify Data Correlation Matrix",
           mar = c(0, 0, 2, 0),
           col = colorRampPalette(c("#FF6B6B", "white", "#1DB954"))(100))
}

# Key Insights and Summary
# ========================

cat("\n📋 KEY INSIGHTS SUMMARY\n")
cat("=======================\n")

# Calculate some key metrics
total_songs <- nrow(spotify_clean)
total_streams <- sum(spotify_clean$streams, na.rm = TRUE)
avg_streams <- mean(spotify_clean$streams, na.rm = TRUE)
unique_artists <- length(unique(spotify_clean$artist_s_name))

cat(sprintf("📊 Dataset contains %s songs from %s unique artists\n",
            format(total_songs, big.mark = ","),
            format(unique_artists, big.mark = ",")))

cat(sprintf("🎵 Total streams across all songs: %s billion\n",
            format(round(total_streams / 1e9, 2), big.mark = ",")))

cat(sprintf("📈 Average streams per song: %s million\n",
            format(round(avg_streams / 1e6, 2), big.mark = ",")))

# Most popular features
if (length(existing_features) > 0) {
  feature_averages <- spotify_clean %>%
    select(all_of(existing_features)) %>%
    summarise_all(~mean(.x, na.rm = TRUE)) %>%
    pivot_longer(everything(), names_to = "feature", values_to = "avg_value") %>%
    arrange(desc(avg_value))
  
  cat("\n🎼 Audio Feature Averages (highest to lowest):\n")
  print(feature_averages)
}

# Export cleaned data option
cat("\n💾 DATA EXPORT\n")
cat("---------------\n")
cat("The cleaned dataset is stored in the variable 'spotify_clean'\n")
cat("To export to CSV: write_csv(spotify_clean, 'spotify_2023_cleaned.csv')\n")

# Final message
cat("\n✨ ANALYSIS COMPLETE!\n")
cat("=====================\n")
cat("The Spotify 2023 dataset has been thoroughly analyzed.\n")
cat("All visualizations and insights are now available.\n")
cat("Use 'spotify_clean' for further custom analysis.\n\n")

# Display final structure
cat("Final dataset structure:\n")
str(spotify_clean)

