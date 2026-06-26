args <- commandArgs(trailingOnly = FALSE)
script_arg <- grep("^--file=", args, value = TRUE)
script_path <- normalizePath(sub("^--file=", "", script_arg))
base_dir <- normalizePath(file.path(dirname(script_path), ".."))
lab_dir <- file.path(base_dir, "lab")
results_dir <- file.path(base_dir, "results")
dir.create(results_dir, showWarnings = FALSE)

order <- read.csv(file.path(lab_dir, "OrderData.csv"), stringsAsFactors = FALSE)
order$Total <- ifelse(is.na(order$Total) | order$Total == "", order$Units * order$Unit.Cost, order$Total)
region_summary <- aggregate(cbind(Units, Total) ~ Region, data = order, FUN = sum)
write.csv(region_summary, file.path(results_dir, "week1_r_order_region_summary.csv"), row.names = FALSE)

iris_data <- read.csv(file.path(lab_dir, "Iris.csv"), stringsAsFactors = FALSE)
species_means <- aggregate(
  cbind(SepalLengthCm, SepalWidthCm, PetalLengthCm, PetalWidthCm) ~ Species,
  data = iris_data,
  FUN = mean
)
write.csv(species_means, file.path(results_dir, "week1_r_iris_species_means.csv"), row.names = FALSE)

sink(file.path(results_dir, "week1_r_console_output.txt"))
cat("Week 1 R basics completed\n")
cat("Objects created: order, region_summary, iris_data, species_means\n\n")
print(region_summary)
cat("\n")
print(species_means)
sink()
