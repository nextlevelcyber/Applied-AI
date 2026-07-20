CIS4049-N  Artificial Intelligence Foundations — In-Course Assessment (ICA)
AI Solution: Autonomous Grid Navigation (Reinforcement Learning vs Search)

Student : CUI JIANGKUN
Student No : F5743005

------------------------------------------------------------------------
CONTENTS
------------------------------------------------------------------------
  F5743005_CUI_JIANGKUN_AI_solution_report.pdf   Written report (~4,000 words)
  F5743005_CUI_JIANGKUN_solution.ipynb           Jupyter notebook (executed, with outputs)
  F5743005_CUI_JIANGKUN_solution.py              Same solution as a plain Python script
  F5743005_CUI_JIANGKUN_slides.pptx              Slides for the walkthrough video
  F5743005_CUI_JIANGKUN_video_script.pdf         Timed narration script (~2 min 50 s)
  figures/                                       Figures produced by the experiments
  README.txt                                     This file

  >>> Before final submission, record the 2-3 minute voice-over walkthrough
      video (using the slides + script above) and add it to the zip as
      F5743005_CUI_JIANGKUN_video.<mp4/mov>.

------------------------------------------------------------------------
WHAT THE SOLUTION DOES
------------------------------------------------------------------------
A warehouse delivery robot must travel from a depot (S) to a drop-off (G)
across a grid containing obstacles and slow, congested aisles, taking the
CHEAPEST route (not simply the fewest steps). The identical task is solved
two ways and compared:

  * Reinforcement Learning — tabular Q-learning (Weeks 5-6): learns the
    route by trial and error, with no map.
  * Classical search (Weeks 7-9): BFS, Uniform-Cost Search / Dijkstra and
    A* plan the route directly from a known map.

Key result: BFS is step-optimal but 55% more expensive (cost 34); UCS and
A* are cost-optimal (cost 22) with A* expanding ~half the nodes of UCS;
and Q-learning independently learns the same optimal route (cost 22).

------------------------------------------------------------------------
HOW TO RUN
------------------------------------------------------------------------
Requirements: Python 3.10+, with numpy, pandas and matplotlib.
    pip install numpy pandas matplotlib

Run the script:
    python F5743005_CUI_JIANGKUN_solution.py

Or open the notebook and run all cells:
    jupyter notebook F5743005_CUI_JIANGKUN_solution.ipynb

The code is self-contained — it needs no external dataset and no
reinforcement-learning library (the environment is written from scratch).
A fixed random seed (42) makes every run reproducible; the notebook ends
with automatic validation checks that all pass.
