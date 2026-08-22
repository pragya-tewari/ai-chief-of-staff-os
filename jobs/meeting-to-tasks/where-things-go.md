# Where things go

| Output | Goes to | Needs a yes |
|---|---|---|
| The meeting note (evidence) | `workspace/meetings/` | no |
| Register row | `workspace/registers/meetings.md` | no |
| Unclear items | `workspace/registers/uncertain.md` | no |
| A person's factual commitments and role updates | `workspace/people/<name>.md` | no |
| Interpretive working-style observations about a person | `workspace/private/` | **yes** |
| Tasks, when the internal list is live | `workspace/tasks.md` | no |
| Tasks, when an external tool is live | the external tool | **yes** |
| Telling anyone about their task | chat / mail | **yes** |
| Project status change | `workspace/projects/<project>/` | no |
| Open questions | `workspace/registers/questions.md` | no |
| A decision record | `workspace/decisions/` | **yes** |
| A message to the team | chat / mail | **yes** |

## The line that resolves the tricky case

A **factual update about a person** — what they now own, what they committed to —
files itself. An **interpretation of a person** — how they behave, how they
handle pressure — waits, and lives in `private/`. Claims about what was decided,
and anything another human will see, always wait.
