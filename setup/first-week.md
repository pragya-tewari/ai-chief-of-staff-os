# Your first week

An empty workspace gives generic answers, and that's where people quit. This is a
dated path from empty to genuinely useful. It starts on the sample company, as a
dry-run, so you see the system work before you touch your own data.

| Day | Do this | What you get |
|---|---|---|
| 1 | Run `bash setup/demo.sh`. It copies the sample to an isolated temporary workspace, prints prompts for file-aware assistants, and creates an attachable bundle for paste-in assistants | You see the plan, routing and approvals without reading or writing your configured workspace |
| 2 | Read [doctor.md](doctor.md) and your workspace's one-page privacy boundary (`README.md` in the workspace). Decide what will live in `private/` | You know what the system will and won't surface before you feed it anything real |
| 3 | Fill in your own `org/portfolio-map.md` and `org/cadence.md` | The assistant knows what exists and when things happen |
| 4 | Write one file per person you work with — five lines each, named by a stable id (`per-ravi.md`). Then run `meeting-to-tasks` on a real recent meeting | The assistant knows your people first, so the meeting's tasks attach to real ids instead of invented ones |
| 5 | Now ask "what does <name> owe me" (it filters the tasks you just created into `reports/`). Then run `write-an-update` and **correct it hard** | Your first useful views — and the corrections that start the system compounding |

## Why the order matters

- **Sample company first, as a dry-run**, so you learn the system on data that
  can't be touched or leaked.
- **Privacy check second**, so you decide the boundary before real data goes in.
- **Your data third** — and people files come *before* the first real meeting
  run, so its tasks attach to real person ids. Tasks then exist (day 4) before
  you ask "who owes me what" (day 5), because that view is a filter of your
  tasks, not your person files.

## Want to see a full run, with writes, on the sample?

Create a throwaway sample and print a full-run prompt:

```
bash setup/demo.sh --full
```

The script does not replace `cos-os.yaml`. Its prompt explicitly overrides the
workspace for that run only. It prints the exact temporary path and cleanup
command. A paste-in assistant cannot write local files, so its bundled demo stays
a dry-run even when `--full` is selected. Review the proposed writes before
approving them, even in the demo.

## After week one

- Run `run-a-sweep` weekly to catch what's slipping.
- Run `review-the-system` weekly to keep the OS itself healthy.
- Correct it every time it's wrong. See [../rules/how-you-learn.md](../rules/how-you-learn.md).
