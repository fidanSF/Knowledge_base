# Claude Memory Protocol

This repository is Claude's persistent memory, stored on GitHub and compatible with Obsidian.

## Session Start — Read This First

At the beginning of every session, read these files in order:

1. `memory/00_INDEX.md` — master index, tells you what exists
2. `memory/core/user_profile.md` — who the user is, key facts
3. `memory/core/working_style.md` — how the user likes to work
4. `memory/core/ongoing_context.md` — current projects, open threads, recent decisions

Then scan `memory/projects/` for any project files relevant to the current task.

**Command to do this quickly:**
```
Read memory/00_INDEX.md → follow links to relevant sections
```

## Session End — Write Back

Before ending every session, update memory if anything changed:

1. **New facts about user** → append to `memory/core/user_profile.md`
2. **New preferences/style** → append to `memory/core/working_style.md`
3. **Project progress** → update or create file in `memory/projects/`
4. **Knowledge learned** → create entry in `memory/knowledge/`
5. **Session summary** → append entry to `memory/log/YYYY-MM.md`
6. **Update index** → reflect any new files in `memory/00_INDEX.md`

Then commit with message: `memory: update <date> — <one-line summary>`

## Memory Hierarchy

```
WORKING MEMORY  (this session's context window)
      ↕  read/write
LONG-TERM MEMORY  (files in this repo)
      ↕  git push/pull
GITHUB  (source of truth, accessible from all devices)
```

## Memory Compression (monthly)

When `memory/log/` accumulates more than 10 entries per month:
1. Summarize recurring themes into `memory/core/`
2. Archive raw logs to `memory/archive/`
3. Delete compressed entries from log

See `memory/COMPRESSION_PROTOCOL.md` for details.

## File Naming Conventions

- Core files: `memory/core/<topic>.md`
- Projects: `memory/projects/<slug>.md`
- Knowledge: `memory/knowledge/<topic>.md`
- Logs: `memory/log/YYYY-MM.md`
- Archive: `memory/archive/YYYY-MM.md`

## Writing Style for Memory Entries

- Use bullet points, not paragraphs
- Date every entry: `**2026-04-27:** ...`
- Be specific and concrete, not vague
- Prefer facts over interpretations
- Use Obsidian `[[wikilinks]]` to connect related notes
- Tag entries with `#tags` for filtering in Obsidian
