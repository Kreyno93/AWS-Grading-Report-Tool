# AWS re/Start – Student Grading Reports

A small Python tool that turns the grades export from the **AWS re/Start Portal** into **one individual report per student**.
Each report lists the student's Knowledge Check (KC) and Lab results and highlights every module that has not been scored yet, so you can send each student a quick overview of their progress.

> [!WARNING]
> **Reports contain personal grading data. Never share them publicly** (no group channels, no public repos, no shared drives).
> Send each report **only to the student it belongs to, via direct message (DM) on Discord**.

---

## Requirements

- Python **3.8 or newer** (no extra packages needed, only the standard library)
- A grades export (`.csv`) from the AWS re/Start Portal

Check your Python version:

```bash
python3 --version
```

---

## Step-by-step guide

### 1. Download the current grades from the AWS re/Start Portal

1. Log in to the **AWS re/Start Portal** and open your class.
2. Go to **Grades**.
3. *(Optional, but recommended)* **Filter by module** so the export only contains the module(s) you want to report on. This keeps the reports short and focused.
4. Click **Export** and download the grades as a **`.csv` file**
   (e.g. `2026-10-05T1143_Grades-DEHAM38.csv`).

> [!TIP]
> Always export a **fresh** file right before creating the reports, so the students get their current status.

### 2. Place the CSV next to the program

Copy the downloaded `.csv` file into the **same directory** as `generate_student_reports.py`:

```
GradingPythonTool/
├── generate_student_reports.py
└── 2026-10-05T1143_Grades-DEHAM38.csv   ← your export
```

### 3. Run the program

Open a terminal in that directory and run:

```bash
python3 generate_student_reports.py <GRADES_FILE>.csv
```

Example:

```bash
python3 generate_student_reports.py 2026-10-05T1143_Grades-DEHAM38.csv
```

> On Windows, use `python` or `py` instead of `python3` if `python3` is not available.

When it finishes, you will see something like:

```
Created 18 student report(s) in student_reports.
```

#### Optional: choose a different output folder

```bash
python3 generate_student_reports.py <GRADES_FILE>.csv -o reports_module_3
```

| Option | Description | Default |
| --- | --- | --- |
| `<GRADES_FILE>.csv` | Path to the exported grades CSV (required) | – |
| `-o`, `--output-directory` | Folder where the reports are written | `student_reports` |

### 4. Share the reports – individually!

The program creates one Markdown file per student in the `student_reports/` folder, named `<Last>_<First>_<StudentID>.md`.

Send each file **only to the matching student via Discord DM**. 🔒

---

## What a report contains

Each report includes:

- **Student name and ID**
- **Current Score** and **Final Score**
  *(note: the Final Score counts all modules of the full curriculum, including modules not covered yet)*
- **Modules Not Scored (Not Completed)**: a list of every KC and Lab without a grade
- **KC Results**: table with module, score and status
- **Lab Results**: table with module, score and status

Example (shortened):

```markdown
# Student Report: Doe, Jane

- **ID:** 123456
- **Current Score:** 87.5
- **Final Score:** 42.1

## Modules Not Scored (Not Completed)
- [Lab] [Linux] Lab - Working with Files

## KC Results

| Module | Score | Status |
| --- | ---: | --- |
| KC - Linux Fundamentals | 100 | Completed |
```

The program automatically skips the *Points Possible* row and the *Test Student* account.

---

## Privacy & data protection

- `*.csv` exports and the `student_reports/` folder are listed in `.gitignore`, so they are **not committed** to Git. Keep it that way.
- Do **not** upload exports or reports anywhere public.
- Share reports **only one-to-one via Discord DM**.
- Delete old exports and reports when you no longer need them.

---

## Troubleshooting

| Problem | Solution |
| --- | --- |
| `error: the following arguments are required: input_csv` | Add the CSV filename to the command (see step 3). |
| `FileNotFoundError` | Check that the CSV is in the same folder and the filename is spelled correctly. |
| `The CSV file contains no KC or Lab module columns.` | The export (or your module filter) contains no KCs/Labs. Export again with a different filter. |
| `python3: command not found` (Windows) | Use `python` or `py` instead. |
