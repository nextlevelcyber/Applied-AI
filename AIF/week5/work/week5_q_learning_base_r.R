states <- c("start", "middle", "goal")
actions <- c("left", "right")
q <- matrix(0, nrow = length(states), ncol = length(actions), dimnames = list(states, actions))

transition <- function(state, action) {
  if (state == "goal") return(list(next_state = "goal", reward = 0, done = TRUE))
  if (state == "start") {
    if (action == "right") return(list(next_state = "middle", reward = -1, done = FALSE))
    return(list(next_state = "start", reward = -2, done = FALSE))
  }
  if (state == "middle") {
    if (action == "right") return(list(next_state = "goal", reward = 10, done = TRUE))
    return(list(next_state = "start", reward = -1, done = FALSE))
  }
}

set.seed(42)
alpha <- 0.2
gamma <- 0.9
epsilon <- 0.15
rewards <- c()

for (episode in 1:300) {
  state <- "start"
  total <- 0
  for (step in 1:10) {
    if (runif(1) < epsilon) {
      action <- sample(actions, 1)
    } else {
      action <- names(which.max(q[state, ]))
    }
    tr <- transition(state, action)
    q[state, action] <- q[state, action] + alpha * (tr$reward + gamma * max(q[tr$next_state, ]) - q[state, action])
    total <- total + tr$reward
    state <- tr$next_state
    if (tr$done) break
  }
  rewards <- c(rewards, total)
}

args <- commandArgs(trailingOnly = FALSE)
script_arg <- grep("^--file=", args, value = TRUE)
script_path <- normalizePath(sub("^--file=", "", script_arg))
results_dir <- file.path(dirname(dirname(script_path)), "results")
dir.create(results_dir, showWarnings = FALSE)
sink(file.path(results_dir, "week5_r_q_learning_output.txt"))
cat("Q-table\n")
print(round(q, 3))
cat("\nLearned policy\n")
print(apply(q, 1, function(row) names(which.max(row))))
cat("\nAverage reward last 25 episodes:", mean(tail(rewards, 25)), "\n")
sink()
