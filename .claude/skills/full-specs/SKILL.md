---
name: full-specs
description: Creates comprehensive full specification documents for AI-driven projects. Use when starting a new project, defining project requirements, or creating the foundation document for phased implementation.
---
# Full Specification Generator

Generate a comprehensive full specification document that serves as the foundation for AI-driven projects, breaking down into scoped specifications, implementation plans, and completion reports for each phase. **Designed for parallel execution** - phases and tasks are marked with dependency indicators to enable concurrent agent execution.

## When to Use

- Starting a new project
- Defining complete project requirements
- Creating foundation document for phased implementation
- When detailed technical specifications are needed

## Output Location

**File**: `docs/{project-name}-full-spec.md`

Use lowercase with hyphens for project name (e.g., `blog-system-full-spec.md`)

## Required Documentation Structure

```
docs/
├── {project-name}-full-spec.md        # This document
├── specs/                              # Phase scoped specifications
├── plans/                              # Phase implementation plans
└── reports/                            # Phase completion reports
```

## Parallel Execution Model

### Dependency Markers

Use these markers throughout specifications to indicate parallelization:

| Marker | Meaning | Agent Behavior |
|--------|---------|----------------|
| `🔀 PARALLEL` | Can run simultaneously with siblings | Spawn multiple agents |
| `⏳ SEQUENTIAL` | Must complete before next starts | Wait for completion |
| `🔗 DEPENDS:[X,Y]` | Requires X and Y to complete first | Check dependencies |
| `🚀 INDEPENDENT` | No dependencies, can start immediately | Spawn without waiting |

### Phase Parallelization Strategy

```
Phase 1 (Foundation)          ← Usually sequential (establishes base)
    ↓
Phase 2 ──┬── Phase 3        ← Can often run in parallel if independent
          │
          ↓
Phase 4 (Integration)         ← Depends on parallel phases completing
```

**Rule**: Design phases to maximize parallelization. Group related work into phases that can execute concurrently when they don't share dependencies.

## Specification Sections

### 1. Project Overview
- **Project Name**: Clear, descriptive name
- **Project Vision**: High-level objectives
- **Target Audience**: Who will use this system
- **Success Metrics**: How success will be measured

### 2. Technical Stack
- **Frontend**: Technologies, frameworks, libraries
- **Backend**: Technologies, frameworks, libraries
- **Database**: Database systems
- **Infrastructure**: Hosting, deployment, CI/CD
- **Third-party Services**: External APIs

> Always use latest stable versions. Verify packages are actively maintained.

### 3. Architecture Overview
- System architecture (text-based diagrams)
- Component breakdown with responsibilities
- Data flow descriptions
- Integration points
- Complete file structure
- Naming conventions

### 4. Phase Dependency Graph

**REQUIRED**: Include a dependency graph showing which phases can run in parallel:

```
Example Dependency Graph:
========================
Phase 01: Foundation Setup        🚀 INDEPENDENT
    ↓
Phase 02: Auth System      ───┐
                              ├──→ 🔀 PARALLEL GROUP A
Phase 03: User Management  ───┘
    ↓                    ↓
Phase 04: Dashboard (🔗 DEPENDS:[02,03])
    ↓
Phase 05: API Integration  ───┐
                              ├──→ 🔀 PARALLEL GROUP B  
Phase 06: Notifications    ───┘
    ↓                    ↓
Phase 07: Final Integration (🔗 DEPENDS:[05,06])
```

### 5. Phases Breakdown

For each phase, document:

#### Phase [N]: [Phase Name]
**Parallelization**: `🚀 INDEPENDENT` | `🔀 PARALLEL` | `🔗 DEPENDS:[phases]`

**Goals**: What this phase achieves

**UI Design Requirements:** `🔀 PARALLEL` with API Design
- User interfaces to build
- User flows and interactions
- Responsive/accessibility requirements

**API Design Requirements:** `🔀 PARALLEL` with UI Design
- Endpoints (method, path, purpose)
- Request/response schemas
- Authentication/authorization
- Error handling specifications
- Validation rules

**Database Design Requirements:** `⏳ SEQUENTIAL` - must complete before API
- Tables/collections to create
- Schema definitions
- Relationships
- Indexes and migrations

### 6. Cross-Cutting Concerns
- Security (auth, data protection)
- Performance targets
- Scalability approach
- Monitoring and logging
- Testing strategy
- Documentation standards
- Code quality standards
- Error handling patterns

### 7. Dependencies and Constraints
- External dependencies
- Timeline constraints
- Resource constraints
- Technical/business constraints

### 8. Risk Assessment
- Potential risks and mitigations
- Technical challenges
- Dependency risks

### 9. Deliverables
- List all expected deliverables

### 10. AI Implementation Guidance
- Logic examples for complex business rules
- Configuration file structures
- Environment variables (complete list)
- Setup instructions
- Validation criteria
- Edge cases and handling
- Default values and fallbacks
- Data formats and schemas

### 11. Package Verification
Before finalizing:
- All packages actively maintained
- No deprecation warnings
- Use modern patterns from official docs

## Post-Full Spec: Parallel Phase Execution

### CRITICAL: Phases Can Run Fully in Parallel

When phases are marked `🔀 PARALLEL` in the dependency graph, **the entire phase lifecycle runs simultaneously**:

```
┌─────────────────────────────────────────────────────────────────────────┐
│  FULL PARALLEL PHASE EXECUTION                                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  AGENT 1 (Phase 02 - Complete Lifecycle)                                │
│  ════════════════════════════════════════                               │
│  Scoped Spec → Impl Plan → IMPLEMENTATION → Tests → Completion Report   │
│                                                                          │
│                    🔀 RUNS SIMULTANEOUSLY                                │
│                                                                          │
│  AGENT 2 (Phase 03 - Complete Lifecycle)                                │
│  ════════════════════════════════════════                               │
│  Scoped Spec → Impl Plan → IMPLEMENTATION → Tests → Completion Report   │
│                                                                          │
│  ═══════════════════ SYNC POINT ═══════════════════                     │
│  (Both phases must complete before dependent phase starts)              │
│                                                                          │
│  SINGLE AGENT (Phase 04 - Depends on 02 & 03)                           │
│  ════════════════════════════════════════════                           │
│  Scoped Spec → Impl Plan → Integration → Tests → Completion Report      │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### How to Spawn Parallel Phase Agents

**To run phases in parallel, spawn one agent per phase with full lifecycle responsibility:**

```python
# RECOMMENDED: Each agent handles complete phase lifecycle
Task(
    subagent_type="implementer",
    prompt="""Execute Phase 02 completely:
    1. Create scoped spec (docs/specs/phase-02/)
    2. Create implementation plan (docs/plans/phase-02-implementation-plan.md)
    3. Implement all code for Phase 02
    4. Run tests and validate
    5. Create completion report (docs/reports/phase-02-completion-report.md)
    """
)
# Spawn simultaneously with:
Task(
    subagent_type="implementer", 
    prompt="""Execute Phase 03 completely:
    1. Create scoped spec (docs/specs/phase-03/)
    2. Create implementation plan (docs/plans/phase-03-implementation-plan.md)
    3. Implement all code for Phase 03
    4. Run tests and validate
    5. Create completion report (docs/reports/phase-03-completion-report.md)
    """
)
```

### Parallel Phase Execution Patterns

| Pattern | When to Use | Agent Spawn |
|---------|-------------|-------------|
| **Full Phase Parallel** | Independent phases (no shared DB/API) | 1 agent per phase, complete lifecycle |
| **Spec-First Parallel** | Shared resources, need coordination | Agents for specs first, then sync, then implement |
| **Staggered Parallel** | Limited resources | Start Phase N+1 spec while Phase N implements |

### Document Lifecycle per Phase

| Step | Document | Location | Parallelizable |
|------|----------|----------|----------------|
| 1 | Scoped Specification | `docs/specs/phase-{NN}/` | ✅ Between independent phases |
| 2 | Implementation Plan | `docs/plans/phase-{NN}-implementation-plan.md` | ✅ Between independent phases |
| 3 | Implementation | Source code | ✅ Between independent phases |
| 4 | Completion Report | `docs/reports/phase-{NN}-completion-report.md` | ✅ Between independent phases |

### Agent Spawning Rules

**Rules for Parallel Phase Execution:**
1. **Max 4 concurrent phase agents** - Avoid overwhelming resources
2. **One agent owns one phase** - Complete lifecycle responsibility
3. **Sync before dependent phases** - Wait for all parallel phases to complete
4. **Shared resources require coordination**:
   - Database migrations: Execute sequentially within sync points
   - Shared config files: One agent owns, others read
   - Common utilities: First phase to need it creates it
5. **Independent validation** - Each agent validates its own phase
6. **Completion reports required** - Must generate before phase is "done"

### Handling Shared Resources in Parallel Phases

```
Phase 02 (Auth)          Phase 03 (User Profiles)
      │                         │
      ├─ Creates: users table   ├─ Needs: users table
      │                         │
      └─────────┬───────────────┘
                │
        COORDINATION STRATEGY:
        ════════════════════════
        Option A: Phase 02 creates users table first (sequential DB step)
        Option B: Shared "foundation" mini-phase creates common tables
        Option C: Each phase creates own tables, merge in integration phase
```

## AI Implementation Notes

- Keep specifications extremely detailed and unambiguous
- Provide concrete examples for complex logic
- Use text-based diagrams
- Verify all dependencies are maintained
- Include complete file paths and structures
- Document all assumptions explicitly
- Provide validation steps for deliverables
- Include error handling patterns
- Specify all configuration upfront
- Define data structures precisely
- Document all business rules clearly
- Update spec if significant changes occur during implementation
- **Always include parallelization markers** (`🔀`, `⏳`, `🔗`, `🚀`)
- **Design phases for maximum parallel execution**
- **Identify and document sync points clearly**
