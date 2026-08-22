# FAQ

**Is this an app I install?**
No. It's plain Markdown files and an AI assistant you already use. There's no
server, no account, no database.

**Do I need to be technical?**
No. You need to be able to clone a repo, copy a folder, and talk to an AI
assistant. Every file is written to be read by a person.

**What assistant does it work with?**
Any capable file-aware assistant for full runs; a paste-in chat assistant works
for drafting and dry-runs. Claude Code is the reference setup. See
[supported-assistants.md](supported-assistants.md).

**Where does my data live?**
By default, in a separate sibling folder on your machine:
`chief-of-staff-workspace`. A weaker `--inside` installation uses only the fixed,
git-ignored `product/workspace` path. You are responsible for a private backup.

**Will it send things without asking?**
No. Writing into your own notes is free. Anything that reaches another person — a
message, a task on their board — waits for your explicit yes. See
[../rules/what-needs-my-approval.md](../rules/what-needs-my-approval.md). Note that
content you have the assistant read *is* processed by your AI provider; "nothing
leaves" means nothing is sent to a person or an external tool without your yes,
not that content never reaches your model.

**I don't have Asana or Jira. Can I still use it?**
Yes. It has a built-in task list — a plain table in your workspace. Only one task
source is ever live at a time. See
[../connections/built-in-tasks.md](../connections/built-in-tasks.md).

**I do have Asana. Can I use that instead?**
Yes — if your assistant has a real connection to it (a connection file here is
documentation, not integration). Jobs check the connection's declared
capabilities before every external action and stop when one is missing. Only one
task source is ever live at a time. See [../connections/](../connections/).

**Why doesn't it do my email and calendar like other tools?**
On purpose. Personal-assistant work is what every other project in this space
does. This one helps you track, coordinate and follow up on work across the
organisation — the chief-of-staff half of the job.

**How does it get better over time?**
You correct it, and the corrections that repeat become rules. See
[how-it-compounds.md](how-it-compounds.md).

**Can I add my own jobs?**
Yes. Copy an existing job folder and keep the same files. See
[../CONTRIBUTING.md](../CONTRIBUTING.md).

**Is it safe to give it sensitive information?**
Read [../rules/safety.md](../rules/safety.md) and [threat-model.md](threat-model.md)
first. The short version: private material stays in `private/` and is never put
into a message, shared document or other external-facing artifact; reading
sensitive sources needs explicit scope; and instruction files reduce risk but
aren't a hard boundary. Your AI provider still processes what the assistant
reads under your account settings, so your own review and provider choice are
part of the system.
