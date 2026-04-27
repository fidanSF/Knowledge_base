---
tags: [meta, protocol]
---

# Memory Compression Protocol

Run this monthly (or when `memory/log/` has 10+ sessions).

---

## Why Compress?

Raw session logs grow unboundedly. Compression extracts durable facts into core files,  
then archives the raw log. Result: core memory stays small and fast to read; nothing is lost.

---

## Step 1 — Identify What to Compress

Read all entries in `memory/log/YYYY-MM.md` for the target month.  
Group entries by theme:

- Repeated user preferences → `core/working_style.md`
- Biographical facts → `core/user_profile.md`  
- Project milestones → `memory/projects/<project>.md`
- Domain knowledge → `memory/knowledge/<topic>.md`
- One-off decisions → keep in log (do not compress)

---

## Step 2 — Write Distilled Facts

For each group, add a bullet to the relevant core file:

```markdown
**YYYY-MM (compressed):** <distilled fact, max 1-2 sentences>
```

Use the label `(compressed)` instead of a specific date to indicate this is a summary.

---

## Step 3 — Archive the Raw Log

```bash
mv memory/log/YYYY-MM.md memory/archive/YYYY-MM.md
```

Update `memory/00_INDEX.md`: move the entry from "Session Logs" to "Archive".

---

## Step 4 — Commit

```bash
git add -A
git commit -m "memory: compress YYYY-MM logs"
git push -u origin main
```

---

## Compression Rules

1. **Never delete without extracting** — if a log entry has no home in core files, it stays in the archive, not in the trash
2. **Preserve dates** — always note the original date range of compressed entries
3. **Compress facts, not events** — "user prefers concise answers" is a fact; "we debugged auth for 2 hours" is an event (keep in archive)
4. **Keep "Do Not Forget" section untouched** — never compress `user_profile.md#do-not-forget`

---

## Emergency Memory Recovery

If memory is lost or corrupted:

```bash
git log --all --oneline memory/    # see all historical commits
git show <commit>:memory/core/user_profile.md  # read old version
git checkout <commit> -- memory/   # restore entire memory folder
```
