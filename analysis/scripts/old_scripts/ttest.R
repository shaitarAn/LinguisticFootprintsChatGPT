#############################
# Unpaired t-test
#############################

# Read (open) data
alpha <- read.csv("../../feature_extraction/results/per_language/english/alpha_ratio.csv", header = TRUE, stringsAsFactors = TRUE)

attach(alpha)

# Info
summary(dataRate)
View(dataRate)

hist(human)
hist(continue)
hist(explain)
hist(create)

#Boxplot
boxplot(human, continue, explain, create, main="Boxplot of human, continue, explain and create", xlab="Type", ylab="Value")

# Have a look at the distribution of both groups:
# Is the the distribution in both groups more or less normal?
# Is the variability in both groups more a less similar?

# Test the normal distribution of the two groups (H0 = normal distribution)
shapiro.test(human)
shapiro.test(explain)

# iterate over files in a directory
for (i in list.files(path = "../../feature_extraction/results/per_language/english/")) {
  print(i)
  # Read (open) data
  filer <- read.csv(paste("../../feature_extraction/results/per_language/english/", i, sep = ""), header = TRUE, stringsAsFactors = TRUE)
  attach(filer)
  # shapiro.test(human)
  # plot the data in human column with name of the file
  hist(human, main=i)
  # hist(human)
  
}
