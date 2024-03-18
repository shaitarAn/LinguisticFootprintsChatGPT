# empty environment
rm(list=ls())
dev.off()
# install.packages("data.table")
# install.packages("ggplot2")
# install.packages("effsize")
# install.packages("stringr")
# install.packages("cowplot")
library(data.table)
library(ggplot2)
library(effsize)
library(stringr)
library(cowplot)

# Define the list of languages and domains
languages <- c("german")
# domains <- c("news", "science", "clinical")

# create domain dictionary
domain_dict <- c("news" = "Journalistic",
                 "science" = "Scientific",
                 "clinical" = "Clinical")

# German:
  #  "news" = c('alpha_ratio', 'pos_prop_PUNCT', 'mean_word_length', 'proportion_unique_tokens'),
  #  "science" = c('pos_prop_VERB', 'sentence_length_std', 'proportion_unique_tokens', 'TTR'),
  #  "clinical" = c('pos_prop_VERB', 'pos_prop_PUNCT', 'first_order_coherence', 'MTLD')

# English:
#    "news" = c('mean_word_length', 'MTLD', 'Yules', 'token_length_mean'),
#    "science" = c('mean_word_length', 'MTLD', 'pos_prop_VERB', 'coleman_liau_index'),
#    "clinical" = c('mean_word_length', 'flesch_reading_ease', 'lix', 'coleman_liau_index')

# Loop through languages and domains
# Create an empty list to store language plots
language_plots <- list()

# Loop through languages
for (language in languages) {
  # Create an empty list to store domain plots
  domain_plots <- list()
  
  # Loop through domain keys
  for (domain in names(domain_dict)) {
    # Define feature list based on domain
    feature_list <- switch(domain,
   "news" = c('alpha_ratio', 'pos_prop_PUNCT', 'mean_word_length', 'proportion_unique_tokens'),
   "science" = c('pos_prop_VERB', 'sentence_length_std', 'proportion_unique_tokens', 'TTR'),
   "clinical" = c('pos_prop_VERB', 'pos_prop_PUNCT', 'first_order_coherence', 'MTLD')
    )

  # Sample feature dictionary (replace with your actual dictionary)
      feat_dict <- c("coleman_liau_index" = "Coleman-Liau",
              "flesch_reading_ease" = "FRE",
              "lix" = "LIX",
              "mean_word_length" = "Mean Word Len",
              "MTLD" = "MTLD",
              "pos_prop_PUNCT" = "PUNCT",
              "pos_prop_VERB" = "VERB",
              "proportion_unique_tokens" = "Unique Tokens",
              "sentence_length_std" = "Sent Len Std",
              "TTR" = "TTR",
              "alpha_ratio" = "Alpha Ratio",
              "first_order_coherence" = "1 Ord Coherence",
              "Yules" = "Yule's K",
              "token_length_mean" = "Token Len Mean")
    
    # Create an empty list to store feature plots
    feature_plots <- list()
    
    # Iterate over the list of features and calculate Cohen's d for each feature
    for (feature in feature_list) {
      # Create an empty dataframe to store the results for this feature
      feature_results_df <- data.frame(Feature = character(),
                                       System = character(),
                                       Cohen_d = numeric(),
                                       stringsAsFactors = FALSE)
      
      # Load the data for this feature
      lang_df <- fread(
        paste0("../../feature_extraction/results/per_domain/", domain, "/", language, "/", feature,
               ".csv")
      )
      
      # Function to calculate Cohen's d
      calculate_cohens_d <- function(lang_df, feature) {
        systems <- unique(c("continue", "explain", "create"))
        results_list <- list()
        
        for (sys in systems) {
          cohens_d <- cohen.d(lang_df[[sys]], lang_df$human, hedges.correction = FALSE)
          d_estimate <- cohens_d$estimate
          
          result_df <- data.frame(Feature = feature,
                                  System = sys,
                                  Cohen_d = d_estimate,
                                  stringsAsFactors = FALSE)
          results_list[[sys]] <- result_df
        }
        
        # Combine results for this feature
        feature_results_df <<- do.call(rbind, results_list)
      }
      
      # Calculate Cohen's d for this feature
      calculate_cohens_d(lang_df, feature)
      
      # Plot with specified order
# Add geom_hline for zero line
zero_line_color <- "red"
# impose order on the x-axis
feature_results_df$System <- factor(feature_results_df$System, levels = c("continue", "explain", "create"))
p <- ggplot(feature_results_df, aes(x = System, y = Cohen_d, fill = System)) +
        geom_hline(yintercept = 0, linetype = "dashed", color = zero_line_color) +  # Add zero line
        geom_col(position = position_dodge2(width = 0.9)) +
        facet_wrap(~Feature, scales = "free", strip.position = "bottom", labeller = labeller(Feature = as_labeller(feat_dict))) + # Placing strip text at the bottom
        theme_minimal() +
        theme(axis.text.x = element_blank(),  # Remove x-axis labels
              axis.title.x = element_blank(), # Remove x-axis title
              plot.title.position = "plot", # Title position at the bottom
              plot.title = element_text(hjust = 0.5), # Center the title
              legend.position = "none") +
        labs(title = NULL,  # No title for individual subplots
             x = NULL,
             y = NULL,
             caption = NULL) +
        theme(plot.title = element_text(hjust = 0.5),
              strip.text = element_text(size = 10)) + # Adjust strip text appearance
        scale_fill_manual(values = c("continue" = "#A6CEE3", "explain" = "cadetblue", "create" = "darkseagreen4")) +
        scale_color_manual(values = zero_line_color) +  # Set color for zero line
        scale_x_discrete(labels = function(x) feat_dict[x]) # Rep

      
      # Append plot to list
      feature_plots[[feature]] <- p
    }
    
    # Combine feature plots into one row for this domain
    combined_domain_plot <- plot_grid(plotlist = feature_plots, nrow = 1)
    
title <- paste(str_to_title(domain_dict[domain]))
combined_domain_plot <- cowplot::ggdraw(combined_domain_plot) +
  cowplot::draw_label(label = title, x = 0.18, y = 1, vjust = 1, hjust = 1, size = 12, angle = 30, lineheight = 1.9, color = "#7d0303", fontface = "bold")  

    
    # Append the combined plot to the list of domain plots
    domain_plots[[domain]] <- combined_domain_plot
  }
  
  # Combine domain plots into one column for this language
  combined_language_plot <- plot_grid(plotlist = domain_plots, ncol = 1)
  
  # Add title to the combined plot for this language
#   title <- paste(str_to_title(language), "Language")
  combined_language_plot <- cowplot::ggdraw(combined_language_plot) +
    cowplot::draw_label(label = NULL, x = 0.5, y = 1, vjust = 1, hjust = 0.5, size = 12)
  
  # Add the combined plot for this language to the list of language plots
  language_plots[[language]] <- combined_language_plot
}

# Save the language plots to separate files
for (language in languages) {
  ggsave(paste0("../../viz/effect_size/cohen_d_", language, "_language.pdf"),
         plot = language_plots[[language]],
         width = 6, height = 5, units = "in")
}

# close device
dev.off()
