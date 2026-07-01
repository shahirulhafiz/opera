# Project Documentation Structure

## Overview

Phased development system where each phase produces three document sets: scoped spec (what), implementation plan (how), and completion report (learnings).

**Core Principles:**
1. One full spec per project (overall vision)
2. Three document sets per phase (spec folder → plan → report)
3. Sequential numbering (01, 02, 03...)
4. Each phase builds on previous completion report

## Document Flow

```
{project-name}-full-spec.md (created once)
            ↓
Phase 01: specs/phase-01/ (folder) → implementation-plan.md → [BUILD] → completion-report.md
            ↓
Phase 02: specs/phase-02/ (folder) → implementation-plan.md → [BUILD] → completion-report.md
            ↓ (repeats)
```

---

## Directory Structure

```
docs/
├── README.md                           # This guide
├── {project-name}-full-spec.md         # Project vision (ONE per project)
├── specs/                              # What to build (folder per phase)
│   └── phase-{NN}/                     # Phase scoped spec (folder with 8 files)
│       ├── 00-overview.md              # Phase overview & context
│       ├── 01-ui-design.md             # UI/UX specifications
│       ├── 02-api-design.md            # API endpoints & contracts
│       ├── 03-database-design.md       # Database schema & migrations
│       ├── 04-integrations.md          # Integration points
│       ├── 05-testing.md               # Testing requirements
│       ├── 06-non-functional.md        # NFRs, security, performance
│       └── 07-checklist.md             # Implementation checklist
├── plans/                              # How to build (one per phase)
│   └── phase-{NN}-implementation-plan.md
├── reports/                            # What was built + learnings (one per phase)
│   └── phase-{NN}-completion-report.md
└── references/                         # Supporting documents & external context
    ├── {topic}-reference.md            # Topic-specific reference docs
    ├── external-links.md               # Curated external links & resources
    ├── design-assets/                  # Design files, mockups, diagrams
    ├── research/                       # Research notes, competitor analysis
    └── api-docs/                       # External API documentation snapshots
```

---

## File Naming Rules

| Document | Location | Pattern | Example |
|----------|----------|---------|---------|
| Full Spec | `docs/` | `{project}-full-spec.md` | `blog-app-full-spec.md` |
| Scoped Spec | `docs/specs/` | `phase-{NN}/` (folder) | `phase-03/` (with 8 files inside) |
| Implementation Plan | `docs/plans/` | `phase-{NN}-implementation-plan.md` | `phase-03-implementation-plan.md` |
| Completion Report | `docs/reports/` | `phase-{NN}-completion-report.md` | `phase-03-completion-report.md` |
| Reference Document | `docs/references/` | `{topic}-reference.md` | `auth-flow-reference.md` |

### Scoped Spec Files (inside `phase-{NN}/` folder)

| File | Purpose |
|------|---------|
| `00-overview.md` | Phase overview, goals, context, success criteria |
| `01-ui-design.md` | UI/UX specifications, screens, components |
| `02-api-design.md` | API endpoints, contracts, authentication |
| `03-database-design.md` | Database schema, migrations, indexes |
| `04-integrations.md` | External integrations, third-party services |
| `05-testing.md` | Testing requirements, test cases |
| `06-non-functional.md` | NFRs, security, performance requirements |
| `07-checklist.md` | Implementation checklist, deliverables |

### References Folder Structure

| Path | Purpose |
|------|---------|
| `references/{topic}-reference.md` | Topic-specific reference documentation |
| `references/external-links.md` | Curated collection of external resources and links |
| `references/design-assets/` | Design files, mockups, wireframes, diagrams |
| `references/research/` | Research notes, competitor analysis, market research |
| `references/api-docs/` | External API documentation snapshots for offline reference |

**Naming conventions:**
- Project names: lowercase-with-hyphens (e.g., `task-manager`)
- Phase numbers: two digits with leading zero (e.g., `01`, `02`, `15`)
- Use hyphens, never underscores or spaces

---

## Document Relationships

**Full Spec** (vision) → references nothing  
**Scoped Spec** (folder) → references Full Spec + Previous Completion Report + References  
**Implementation Plan** → references Full Spec + Current Scoped Spec folder + References  
**Completion Report** → references all three above + actual code  
**References** (supporting) → standalone context documents, can be referenced by any document

**Context Chain Example (Phase 3):**
```
Phase 3 Scoped Spec (folder) references:
  ├─ Full Spec (overall vision)
  ├─ Phase 2 Completion Report (what exists)
  ├─ Phase 2 Scoped Spec folder (previous decisions)
  └─ References (supporting context as needed)
```

---

## References Folder

The `references/` folder provides supporting context that AI assistants and developers can use to gain deeper understanding of project-specific requirements, external constraints, and domain knowledge.

### Purpose

- **Context enrichment**: Provide additional background information beyond specs
- **External resources**: Curate links to relevant documentation, tutorials, APIs
- **Design assets**: Store mockups, wireframes, and visual references
- **Research data**: Keep competitor analysis, user research, market data
- **API snapshots**: Maintain offline copies of external API documentation

### When to Use References

| Scenario | Action |
|----------|--------|
| Need domain-specific context | Create `{domain}-reference.md` |
| Collecting external links | Add to `external-links.md` |
| Storing design mockups | Place in `design-assets/` |
| Documenting research findings | Place in `research/` |
| Saving external API docs | Place in `api-docs/` |

### AI Context Usage

AI assistants should check `references/` when:
- Starting a new phase (for domain context)
- Encountering unfamiliar terminology
- Needing external API integration details
- Requiring design/UX guidance
- Looking for prior research or decisions

---

## Quick Reference for AI

### Common Tasks

| Task | Action |
|------|--------|
| New project | Create `{project}-full-spec.md` in `docs/` |
| Start phase N | Create `phase-{NN}/` folder in `specs/` with all 8 files |
| Plan phase N | Create `phase-{NN}-implementation-plan.md` in `plans/` |
| Complete phase N | Create `phase-{NN}-completion-report.md` in `reports/` |
| Add reference | Create `{topic}-reference.md` in `references/` |
| Add external links | Update `references/external-links.md` |
| Store design assets | Place files in `references/design-assets/` |
| Document research | Create notes in `references/research/` |

### Common Mistakes

| ❌ Wrong | ✅ Correct |
|---------|-----------|
| `phase-01-scoped-spec.md` (single file) | `phase-01/` folder with 8 files |
| `docs/phase-01-implementation-plan.md` | `docs/plans/phase-01-implementation-plan.md` |
| `phase-1/` (single digit) | `phase-01/` (two digits) |
| `task_manager_full_spec.md` | `task-manager-full-spec.md` |
| Missing spec files in folder | All 8 files present (00-overview.md through 07-checklist.md) |
| `docs/auth-reference.md` (root) | `docs/references/auth-reference.md` |
| Ignoring references for context | Check `references/` for supporting context |

### Cross-Reference Templates

**In Spec Validation:**
```markdown
**Reference Documents:**
- Full Spec: [../{project}-full-spec.md]
- Supporting References: [../references/] (as applicable)
```

**In Scoped Spec (00-overview.md):**
```markdown
**Reference Documents:**
- Full Spec: [../../{project}-full-spec.md]
- Previous Report: [../../reports/phase-{NN-1}-completion-report.md] (if Phase 2+)
- Supporting References: [../../references/] (as applicable)
```

**In Implementation Plan:**
```markdown
**Reference Documents:**
- Full Spec: [../{project}-full-spec.md]
- Scoped Spec: [../specs/phase-{NN}/] (folder with all spec files)
- Supporting References: [../references/] (as applicable)
```

**In Completion Report:**
```markdown
**Reference Documents:**
- Full Spec: [../{project}-full-spec.md]
- Scoped Spec: [../specs/phase-{NN}/] (folder with all spec files)
- Implementation Plan: [../plans/phase-{NN}-implementation-plan.md]
- Supporting References: [../references/] (as applicable)
```

---

## Phase Workflow Checklist

**Starting Phase N:**
- [ ] Read previous completion report (if Phase 2+)
- [ ] Read full specification
- [ ] Create `phase-{NN}/` folder in `specs/` with all 8 spec files:
  - [ ] `00-overview.md` - Phase overview & context
  - [ ] `01-ui-design.md` - UI/UX specifications
  - [ ] `02-api-design.md` - API endpoints & contracts
  - [ ] `03-database-design.md` - Database schema & migrations
  - [ ] `04-integrations.md` - Integration points
  - [ ] `05-testing.md` - Testing requirements
  - [ ] `06-non-functional.md` - NFRs, security, performance
  - [ ] `07-checklist.md` - Implementation checklist
- [ ] Create `phase-{NN}-implementation-plan.md` in `plans/`
- [ ] Implement code following plan
- [ ] Create `phase-{NN}-completion-report.md` in `reports/`

---

## Critical Rules

1. **Read this file first** before creating/modifying docs
2. **Follow naming patterns exactly** - no variations
3. **Use two-digit phase numbers** - always `01`, not `1`
4. **Files in correct subdirectories** - specs/, plans/, reports/, references/
5. **Scoped specs are folders** - `phase-{NN}/` with all 8 files
6. **Include cross-references** - link related documents
7. **One full spec per project** - in docs/ root only
8. **All 8 spec files required** - 00-overview.md through 07-checklist.md
9. **Check references for context** - use `references/` for supporting information
10. **Keep references organized** - use subfolders for assets, research, api-docs

---

**Detailed templates and commands for each document type are in `.cursor/commands/` directory.**

## Commands

The `.cursor/commands/` directory contains ready-to-run command templates that guide each documentation action.
Each command is named for the document it creates or updates and includes the required structure and cross-references.

| Step | Command | Description |
|------|---------|-------------|
| 1. | `/full-specs` | Create the one-time project full specification document in `docs/`. |
| 2. | `/scoped-spec` | Create the phase scoped spec folder `specs/phase-{NN}/` with all 8 files. |
| 3. | `/implementation-plan` | Create a phase implementation plan based on the scoped spec. |
| 4. | `/execute` | Execute an implementation plan step by step with validation and documentation checkpoints. |
| 5. | `/completion-report` | Create a phase completion report after implementation is finished. |
| 6. | `/check-phase` | Verify a phase completion report against the scoped spec and full spec, and generate a readiness verdict for the next phase. |


