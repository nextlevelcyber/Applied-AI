# MSc Applied Artificial Intelligence

This repository is my working directory for the **Teesside University MSc Applied Artificial Intelligence** programme, May 2026 intake.

It is used to keep course materials, assessment briefs, notes, datasets, code, dashboards, and personal study outputs in one place.

## Courses

| Course | Code | Folder | Focus |
| --- | --- | --- | --- |
| Artificial Intelligence Foundations | CIS4049-N | `AIF/` | AI foundations, intelligent agents, ML, LLMs, reinforcement learning, and ICA work |
| Big Data and Business Intelligence | CIS4008-N | `BDBI/` | Big data, BI reporting, Power BI dashboards, and assessment work |
| Software for Digital Innovation | CIS4044-N | `SDI/` | Python, SQLite, OpenMeteo assessment work, and software development practice |

## Repository Structure

```text
.
├── BDBI/        # Big Data and Business Intelligence materials
├── AIF/         # Artificial Intelligence Foundations materials
├── SDI/         # Software for Digital Innovation materials and assessment code
├── Course.txt   # Term 1 timetable and class access notes
└── README.md    # Project overview
```

## Current Materials

### Big Data and Business Intelligence

- ICA brief, report template, sample reports, and sample Power BI dashboards are saved under `BDBI/`.
- The confirmed Blackboard ICA deadline is `2026-07-29 23:59 (UTC+8)`.
- Current work is tracked in `BDBI/tasks.md`.

### Software for Digital Innovation

- Lecture materials and student notes
- Python and SQLite exercises
- OpenMeteo assessment specification
- ICA project code split into phases
- SQLite database files used for coursework

### Artificial Intelligence Foundations

- Module guide, teaching schedule, and ICA specification are saved under `AIF/`.
- The confirmed Blackboard ICA deadline is `2026-07-27 04:00 (UTC+8)`.
- Current work is tracked in `AIF/tasks.md`.

## Suggested Working Convention

- Keep official briefs, lecture files, and provided datasets unchanged.
- Put personal notes in a clearly named `notes/` folder inside each course.
- Put assessment drafts and final submissions in an `assessment/` folder inside each course.
- Put experiments, scripts, notebooks, and generated outputs in a `work/` or `src/` folder.
- Avoid committing temporary files such as `.DS_Store`, Office lock files, exported caches, and local environment folders.

## Setup Notes

Some coursework uses Python and SQLite. When working on those projects, use the environment instructions from the relevant module folder or assessment brief.

Power BI files require Power BI Desktop or a compatible viewer.

## To Organise Next

- [x] Add an `AIF/` folder for CIS4049-N Artificial Intelligence Foundations.
- [x] Remove references to the deleted `CIS/` folder.
- [x] Add per-course README files once each course folder structure settles.
- [ ] Move personal assessment drafts away from official source materials.
- [ ] Review `.gitignore` for macOS, Office, Python, database, and Power BI temporary files.
