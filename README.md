# Claude Memory — Knowledge Base

Persistent memory for Claude AI, based on Andrej Karpathy's external memory method.  
Stored on GitHub → accessible from any device. Compatible with Obsidian for visual navigation.

---

## How It Works

```
┌─────────────────────────────────────────────────────────┐
│                     GITHUB (cloud)                       │
│                  fidanSF/knowledge_base                  │
│                                                          │
│  memory/core/          ← permanent facts & preferences   │
│  memory/projects/      ← per-project state               │
│  memory/knowledge/     ← domain knowledge Claude learns  │
│  memory/log/           ← session-by-session diary        │
│  memory/archive/       ← compressed old logs             │
└─────────────────────────────────────────────────────────┘
         ↑ git pull                    git push ↓
┌─────────────────────────────────────────────────────────┐
│                  CLAUDE CODE SESSION                     │
│  reads CLAUDE.md → loads memory → works → writes back   │
└─────────────────────────────────────────────────────────┘
         ↑ open vault                  sync ↓
┌─────────────────────────────────────────────────────────┐
│                     OBSIDIAN                             │
│  visual graph, search, backlinks, tags, mobile app       │
└─────────────────────────────────────────────────────────┘
```

---

## Quick Start

### 1. Clone the repo on any device

```bash
git clone https://github.com/fidanSF/knowledge_base.git
cd knowledge_base
```

### 2. Open as Obsidian vault

1. Open Obsidian → "Open folder as vault"
2. Select the cloned `knowledge_base/` folder
3. Trust the `.obsidian/` config (already set up)

### 3. Sync from any device

```bash
git pull origin main        # get latest memory
# ... use Claude ...
git push origin main        # push Claude's updates
```

### 4. Mobile (Obsidian + Working Copy on iOS / MGit on Android)

- Install **Obsidian** + **Working Copy** (iOS) or **MGit** (Android)
- Clone this repo in Working Copy/MGit
- Open the folder in Obsidian
- Set up auto-sync shortcut

---

## Repository Structure

```
knowledge_base/
├── CLAUDE.md                    ← Claude reads this first every session
├── README.md                    ← this file
│
├── memory/
│   ├── 00_INDEX.md              ← master map of all memory
│   ├── COMPRESSION_PROTOCOL.md ← how to compress old logs
│   │
│   ├── core/
│   │   ├── user_profile.md      ← facts about the user
│   │   ├── working_style.md     ← user's preferences with Claude
│   │   └── ongoing_context.md   ← current projects, open threads
│   │
│   ├── projects/
│   │   └── _template.md         ← copy this for new projects
│   │
│   ├── knowledge/
│   │   └── _template.md         ← copy this for new knowledge entries
│   │
│   ├── log/
│   │   └── _template.md         ← session log format
│   │
│   └── archive/                 ← compressed old logs live here
│
└── .obsidian/                   ← Obsidian vault settings
```

---

## Karpathy Memory Method

Based on Andrej Karpathy's approach to LLM memory:

1. **External storage beats in-context**: facts in files persist forever; context window is temporary
2. **The AI owns its memory**: Claude reads AND writes to keep memory accurate
3. **Human-readable first**: all files are plain markdown — you can read/edit directly
4. **Compression prevents bloat**: raw logs get summarized monthly into core facts
5. **Git is the backbone**: version history means no memory is ever truly lost

Key insight: `CLAUDE.md` is automatically loaded by Claude Code at session start.  
This is the hook that makes everything work — Claude knows to load the rest.

---

## Manual Memory Operations

### Add a fact right now

Edit `memory/core/user_profile.md` and add a bullet under the relevant section.

### Start a new project

```bash
cp memory/projects/_template.md memory/projects/your-project-name.md
# fill it in, then add a link in memory/00_INDEX.md
```

### Force Claude to re-read memory

Say: *"Re-read your memory files and summarize what you know about me."*

### Inspect what Claude knows

Open `memory/00_INDEX.md` in Obsidian — it links to everything.

---

## Git Workflow

Claude commits memory updates automatically.  
Commit messages follow the pattern: `memory: update YYYY-MM-DD — summary`

To review Claude's memory changes:

```bash
git log --oneline              # see all updates
git diff HEAD~1 HEAD           # see what changed last session
git log --all --follow memory/ # history of any memory file
```
