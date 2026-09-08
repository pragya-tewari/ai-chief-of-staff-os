# Install

Five minutes. A script sets up the folders and config; then a short conversation
with your assistant fills in who you are.

## Before you start

You need:
- This repo, cloned to your machine.
- An AI assistant that can read files in a folder (see
  [../docs/supported-assistants.md](../docs/supported-assistants.md)).
- macOS or Linux. On Windows, use WSL or a compatible Bash environment; there is
  no native PowerShell installer in v0.1.
- Git, if you want local history for undo (recommended). A git repository is not
  an off-device backup until you add and push to a private remote.

## Steps

1. **Clone this repo**, e.g. to `~/ai-chief-of-staff-os`:

   ```
   git clone https://github.com/pragya-tewari/ai-chief-of-staff-os.git ~/ai-chief-of-staff-os
   ```

2. **Run the installer:**

   ```
   bash setup/install.sh
   ```

   It asks three things — where your workspace should live (default:
   folder `~/chief-of-staff-workspace`), which assistant you use, and your
   timezone — then it:
   - creates your workspace from the template (never overwriting an existing one),
   - writes `cos-os.yaml` with an absolute path linking the two folders,
   - optionally initialises the workspace as its own git repo with a first commit,
   - runs the doctor to confirm the wiring,
   - prints your first demo command.

   It resolves `..` and symlinks before checking the boundary. It refuses custom
   paths inside the product folder. Passing `--inside` uses exactly the protected,
   git-ignored path `<product>/workspace`; no other inside path is allowed.

3. **Fill in your profile.** Ask your assistant: "set up my profile." It reads
   `rules/about-me.template.md` and asks these nine questions, then proposes your
   completed `workspace/profile/about-me.md` for confirmation:

   1. Your name.
   2. Your title and what you're accountable for.
   3. Your company or organisation.
   4. Who you report to.
   5. Who reports to you, and who you work with most.
   6. How you like your writing to sound (short? plain? any words you avoid?).
   7. What you always want to see in an output.
   8. What you never want to see.
   9. Your top two or three priorities right now.

4. **Point your assistant at the system.** The repo ships a root `CLAUDE.md` and
   `AGENTS.md` — most assistants read one of them on their own. If yours doesn't,
   paste [adapters/generic-prompt.md](../adapters/generic-prompt.md) to start.

## What you now have

```
~/ai-chief-of-staff-os/          the system — you pull updates here
~/chief-of-staff-workspace/      your private data — separate by default
```

Updating the system later is `git pull` in the repo folder. It never touches your
workspace.

## The simplest alternative

If two folders feels like too much, run `bash setup/install.sh --inside`. This
does not ask for a path: it uses the fixed folder `workspace/` inside the product
repo and verifies that git ignores it. Simpler to hold in your head, weaker
protection (a forced git add could still stage private files). The two-folder
default is safer.

## Next

Don't feed it your real data yet. Go to [first-week.md](first-week.md) — its demo
script creates an isolated sample workspace without replacing your live config.
