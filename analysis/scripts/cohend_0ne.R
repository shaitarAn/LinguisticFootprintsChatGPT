# empty environment
rm(list=ls())

library(effsize)
library(see)
library(data.table)
library(ggplot2)

language <- "english"
feature <- "proportion_unique_tokens"

# Load the data for this feature
# lang_df <- fread(
#     paste0("../../feature_extraction/results/per_language/", language, "/", feature, ".csv")
# )
lang_df <- fread(
    paste0("test_full_", feature, ".csv")
)

systems <- unique(c("continue", "explain", "create"))

# Initialize a data frame to store Cohen's d results
results <- data.frame(
    system = character(),
    estimate = numeric(),
    conf.low = numeric(),
    conf.high = numeric(),
    stringsAsFactors = FALSE
)

for (sys in systems) {
    cohens_d <- cohen.d(lang_df[[sys]], lang_df$human, hedges.correction = FALSE)
    d_estimate <- cohens_d$estimate
    conf.low <- cohens_d$conf.int[1]
    conf.high <- cohens_d$conf.int[2]

    # Append results to the data frame
    results <- rbind(results, data.frame(
        system = sys,
        estimate = d_estimate,
        conf.low = conf.low,
        conf.high = conf.high
    ))

    print("-------------------------------")
    print(sys)
    print(cohens_d)
    print(interpret_cohens_d(d_estimate))
}

# Plot the effect size with confidence intervals
ggplot(results, aes(x = system, y = estimate)) +
    geom_point(size = 5) +
    geom_errorbar(aes(ymin = conf.low, ymax = conf.high), width = 0.2) +
    labs(title = paste("Cohen's d for", feature, "by System"),
         x = "System",
         y = "Cohen's d") +
    theme_minimal() +
    theme(
        text = element_text(size = 15),
        plot.title = element_text(size = 20, face = "bold")
    )
