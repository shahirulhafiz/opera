---
name: scoped-spec
description: Creates detailed scoped specifications for specific phases with multi-file organization. Use when creating phase specifications, breaking down full specs into implementation-ready details, or preparing for AI-driven implementation.
---
# Scoped Specification Generator

Generate detailed scoped specifications for a specific phase based on the full specification. Scoped specs are divided into multiple files by area for better organization. **Designed for parallel execution** - files and tasks are marked with dependency indicators to enable concurrent agent execution.

## When to Use

- After full specification is complete
- Before creating implementation plan
- When preparing detailed phase requirements
- For AI-driven implementation preparation

## Prerequisites

- Full specification exists (`docs/{project-name}-full-spec.md`)
- Target phase identified from full spec
- **If NOT Phase 1**: Previous phase completion report must be reviewed
- **Check phase dependency graph** in full spec to identify parallel opportunities

## Output Structure

```
docs/specs/phase-{NN}/
├── 00-overview.md           # Phase goals, scope, context      🚀 FIRST
├── 01-ui-design.md          # UI/UX, components, design       🔀 PARALLEL
├── 02-api-design.md         # API endpoints, auth, errors     🔀 PARALLEL (🔒 LOCKED)
├── 03-database-design.md    # Schema, migrations, indexes     🔀 PARALLEL (🔒 LOCKED)
├── 04-integrations.md       # Internal/external integrations  🔗 DEPENDS:[01,02,03]
├── 05-testing.md            # Test requirements & strategy    🔗 DEPENDS:[01,02,03]
├── 06-non-functional.md     # Performance, security, NFRs     🔀 PARALLEL
└── 07-checklist.md          # Implementation readiness        ⏳ LAST
```

Use two-digit phase numbers: `01`, `02`, `03`, etc.

## Parallel File Generation

### File Dependency Graph

```
                    00-overview.md
                    (🚀 MUST BE FIRST)
                          │
          ┌───────────────┼───────────────┐
          ↓               ↓               ↓
    01-ui-design    02-api-design   03-database-design
          │               │               │
          │         🔀 PARALLEL          │
          └───────────────┼───────────────┘
                          │
          ┌───────────────┼───────────────┐
          ↓               ↓               ↓
    04-integrations  05-testing    06-non-functional
          │               │               │
          │      🔗 DEPENDS:[01,02,03]    │
          └───────────────┼───────────────┘
                          │
                          ↓
                    07-checklist.md
                    (⏳ MUST BE LAST)
```

### Agent Spawning for Scoped Spec

```python
# Parallel scoped spec generation
# Step 1: Create overview first (required context)
create_file("00-overview.md")

# Step 2: Spawn parallel agents for independent files
spawn_parallel([
    Task(prompt="Create 01-ui-design.md for phase {NN}"),
    Task(prompt="Create 02-api-design.md for phase {NN}"),
    Task(prompt="Create 03-database-design.md for phase {NN}"),
    Task(prompt="Create 06-non-functional.md for phase {NN}"),
])  # Max 4 concurrent agents

# Step 3: After parallel files complete, create dependent files
spawn_parallel([
    Task(prompt="Create 04-integrations.md for phase {NN}"),
    Task(prompt="Create 05-testing.md for phase {NN}"),
])

# Step 4: Create checklist last (needs all other files)
create_file("07-checklist.md")
```

## File Specifications

### 00-overview.md `🚀 FIRST - Creates context for all other files`
- Phase goals and objectives
- Scope boundaries (included/excluded)
- Dependencies on previous phases
- Context from previous phase (if Phase 2+)
- Technology stack summary
- Phase milestones
- **Parallelization notes**: Which tasks in this phase can run concurrently

### 01-ui-design.md `🔀 PARALLEL` - Can run with 02, 03, 06
- User interface components with states
- Design system (colors, typography, spacing)
- Responsive design breakpoints
- Accessibility requirements (WCAG)
- User interactions and forms
- Complete component examples
- **Component independence markers**: Tag components that can be built in parallel

### 02-api-design.md (🔒 LOCKED) `🔀 PARALLEL` - Can run with 01, 03, 06
> Once approved, changes require stakeholder review

- Base URL configuration
- Common headers
- All endpoints with:
  - Method, path, purpose
  - Request/response schemas
  - Error responses
  - Business logic
  - Validation rules
  - Side effects
- Data validation rules
- Authentication & authorization
- Error handling format
- Performance requirements
- Rate limiting
- Security considerations
- **Endpoint independence markers**: Tag endpoints that can be implemented in parallel

### 03-database-design.md (🔒 LOCKED) `🔀 PARALLEL` - Can run with 01, 02, 06
> Changes require migration planning

- Schema design (all tables)
- Entity relationships (ERD)
- Data integrity constraints
- Indexing strategy
- Migration scripts (up/down)
- Seed data
- Performance optimization
- Backup/recovery strategy
- **Table independence markers**: Tag tables that can be created in parallel

### 04-integrations.md `🔗 DEPENDS:[01,02,03]`
- UI ↔ API connection
- API ↔ Database connection
- External integrations with:
  - Configuration
  - Endpoints used
  - Error handling
  - Fallback strategy
- Webhooks (incoming/outgoing)
- Event streams (if applicable)

### 05-testing.md `🔗 DEPENDS:[01,02,03]`
- Testing strategy overview
- UI testing (unit, integration, E2E, visual)
- API testing (unit, integration, load, security)
- Database testing (schema, performance, integrity)
- Test data management
- CI/CD testing pipeline
- **Test parallelization strategy**: Which test suites can run concurrently

### 06-non-functional.md `🔀 PARALLEL` - Can run with 01, 02, 03
- Performance requirements (page load, API, DB)
- Security requirements (encryption, auth, audit)
- Scalability targets and strategy
- Reliability & availability (SLA, DR)
- Monitoring & observability
- Accessibility (WCAG compliance)
- Internationalization (if applicable)

### 07-checklist.md `⏳ LAST - Requires all other files complete`
- Pre-implementation verification
- Locked structures review
- Specification completeness check
- Dependency verification
- Pattern verification
- Implementation progress tracking
- Testing completion
- Documentation checklist
- Open questions log
- Deviations from spec
- Sign-off criteria
- **Parallel execution readiness**: Verify all independence markers are set

## Context from Previous Phase (Phase 2+)

Review the previous completion report for:

1. **Lessons Learned**: What worked/didn't work
2. **Technical Decisions**: Technologies, architecture
3. **Changes from Plan**: What was added/deferred
4. **Known Issues**: Technical debt, bugs
5. **Dependencies**: Components available
6. **Recommendations**: Specific suggestions

When writing this scoped spec:
- ✅ Build on successes
- ✅ Avoid past mistakes
- ✅ Maintain compatibility
- ✅ Address high-priority debt
- ✅ Apply lessons learned
- ✅ Acknowledge constraints

## Parallel Phase Execution

### CRITICAL: Run Entire Phases in Parallel

When phases are marked `🔀 PARALLEL` in the full spec dependency graph, **spawn separate agents to execute complete phases simultaneously**.

```
┌─────────────────────────────────────────────────────────────────┐
│  PARALLEL PHASE EXECUTION - EACH AGENT OWNS A FULL PHASE       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  AGENT A ──→ Phase 02 (Complete Lifecycle)                      │
│              ├─ Scoped Spec (all 8 files)                       │
│              ├─ Implementation Plan                              │
│              ├─ CODE IMPLEMENTATION                              │
│              ├─ Testing                                          │
│              └─ Completion Report                                │
│                                                                  │
│                    🔀 SIMULTANEOUSLY                             │
│                                                                  │
│  AGENT B ──→ Phase 03 (Complete Lifecycle)                      │
│              ├─ Scoped Spec (all 8 files)                       │
│              ├─ Implementation Plan                              │
│              ├─ CODE IMPLEMENTATION                              │
│              ├─ Testing                                          │
│              └─ Completion Report                                │
│                                                                  │
│  ════════════════ SYNC POINT ════════════════                   │
│  Both must complete before Phase 04 starts                      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### How to Spawn Parallel Phase Agents

```python
# SPAWN PARALLEL PHASE AGENTS - Each handles complete phase
Task(
    subagent_type="implementer",
    prompt="""Execute Phase 02 COMPLETELY:
    - Create all scoped spec files (docs/specs/phase-02/)
    - Create implementation plan
    - Implement ALL code for this phase
    - Run tests
    - Generate completion report
    Phase 02 scope: [describe from full spec]
    """
)
# SIMULTANEOUSLY spawn:
Task(
    subagent_type="implementer",
    prompt="""Execute Phase 03 COMPLETELY:
    - Create all scoped spec files (docs/specs/phase-03/)
    - Create implementation plan  
    - Implement ALL code for this phase
    - Run tests
    - Generate completion report
    Phase 03 scope: [describe from full spec]
    """
)
```

### Parallel Phase Patterns

| Pattern | Description | When to Use |
|---------|-------------|-------------|
| **Full Parallel** | Each agent executes complete phase | Independent phases, no shared resources |
| **Spec-Parallel** | Agents create specs in parallel, then sync before implementation | Phases share database or APIs |
| **Staggered** | Start Phase N+1 spec while Phase N implements | Resource constraints |

### Within-Phase Parallelization

Each scoped spec should document which implementation tasks can run in parallel:

```markdown
## Implementation Task Dependencies (include in 00-overview.md)

### Parallel Group A (🔀 Can run simultaneously)
- [ ] DB-1: Create users table
- [ ] DB-2: Create sessions table  
- [ ] DB-3: Create audit_logs table

### Parallel Group B (🔀 Can run simultaneously, after Group A)
- [ ] API-1: User registration endpoint
- [ ] API-2: User login endpoint
- [ ] API-3: Session management endpoints

### Parallel Group C (🔀 Can run simultaneously, after Group B)
- [ ] UI-1: Registration form component
- [ ] UI-2: Login form component
- [ ] UI-3: Session status component

### Sequential Tasks (⏳ Must run in order)
- [ ] INT-1: Connect auth flow (depends on all above)
- [ ] INT-2: E2E testing
```

### Shared Resource Coordination

When parallel phases share resources:

```
Phase 02 (Auth)              Phase 03 (Profiles)
     │                             │
     ├─ Creates: users table       ├─ Needs: users table
     │                             │
     └──────────┬──────────────────┘
                │
     COORDINATION OPTIONS:
     ═══════════════════════
     1. Foundation First: Create shared tables in Phase 01
     2. Owner Pattern: Phase 02 owns users table, Phase 03 waits
     3. Merge Later: Each creates own, integrate in Phase 04
```

## AI Implementation Notes

- Reference full specification for context
- Keep each file focused on its area
- Be extremely specific - AI needs unambiguous instructions
- Provide complete logic examples
- Verify dependencies are maintained
- Specify all file paths and structures
- Document assumptions explicitly
- Include validation steps
- Provide example inputs/outputs
- Cross-link between files where needed
- **Always include parallelization markers** (`🔀`, `⏳`, `🔗`, `🚀`)
- **Tag independent components/endpoints/tables** for parallel implementation
- **Document sync points** where parallel work must converge
- **Limit concurrent agents to 4** to avoid resource conflicts
- **Identify shared resources** that require sequential access (migrations, config files)
