# Week 5 - Reinforcement Learning

## Learning Focus

Week 5 introduces reinforcement learning in Python and R. The lab covers agents, environments, rewards, policies, Q-values, epsilon-greedy exploration, and model-free learning.

## Key Concepts

- Reinforcement learning trains an agent through interaction with an environment.
- The agent observes states, chooses actions, receives rewards, and updates behavior.
- A policy maps states to actions.
- Q-learning estimates the value of taking an action in a state.
- Epsilon-greedy action selection balances exploration and exploitation.
- The R workbook uses the `ReinforcementLearning` package; the completed local practice also includes a base R implementation to avoid package dependency issues.

## Official Materials

Lab files:

- `lab/AI Foundations - Week 5 - Lab Introduction.pdf`
- `lab/Week 5 - Lab session Material.docx`
- `lab/Lab_5_AI_Python_Reinforcement_Learning.pdf`
- `lab/Lab_5_AI_R_Reinforcement Learning.pdf`

The Week 5 lecture page on Blackboard contained Panopto recording links but no downloadable lecture slide file was visible during this pass.

## Lab Completed

Completed practical work:

- Implemented a small three-state reinforcement learning environment.
- Implemented Q-learning in Python.
- Implemented a base R Q-learning version.
- Trained for 300 episodes.
- Saved the learned Q-table, policy, and reward summary.

## Results

Results are saved in `results/`:

- `week5_q_learning_results.json`
- `week5_r_q_learning_output.txt`

Key Python output:

- Learned policy: start -> right, middle -> right.
- Average reward over the final 25 episodes: `8.76`.

Key R output:

- Learned policy: start -> right, middle -> right.
- Average reward over the final 25 episodes: `8.6`.

## ICA Connection

This week is a strong candidate for an ICA topic if you want to implement and evaluate an AI technique. A small RL project can be extended into a real-world case study by defining a meaningful environment, reward function, evaluation metrics, and commercial/ethical risks.
