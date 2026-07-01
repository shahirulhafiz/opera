---
name: docs-context-awareness
description: Enforces documentation standards and context synchronization for docs/ folder operations. Use when creating, restructuring, or materially updating documentation.
---

## When to Apply This Rule

Apply this rule when one of the following is true:

- ✅ Creating new documentation files in `docs/` or subdirectories
- ✅ Renaming/reorganizing documentation structure
- ✅ Updating cross-references across multiple docs
- ✅ Working in unfamiliar docs areas where naming/location is uncertain

Usually skip this rule for:
- ❌ Small, local edits to one known docs file
- ❌ Read-only lookups that do not change docs structure
- ❌ Non-doc tasks

---

## Context Synchronization Checklist

When working with documentation, ensure:

- [ ] Read `docs/README.md` when naming, placement, or structure is relevant
- [ ] Identified current project name
- [ ] Identified current phase number
- [ ] Verified naming pattern matches conventions
- [ ] Confirmed correct subdirectory (specs/, plans/, reports/, references/, or root)
- [ ] Checked cross-references are valid
- [ ] Used two-digit phase numbers (01, 02, not 1, 2)
- [ ] Used hyphens (not underscores or spaces)
- [ ] Lowercase project names
- [ ] Checked `references/` only if domain context is required

---

## Quick Decision Tree

```
Need to work with docs/ directory?
        ↓
Creating/restructuring files or unsure of conventions?
    → Read docs/README.md
    → Validate naming and placement
    → Check references/ only when domain context is needed
        ↓
Small edit in a known file?
    → Apply local change directly
        ↓
Creating new file?
    → Check naming pattern in README
    → Check subdirectory rules in README
    → Check phase number format in README
    → If reference doc: place in references/
        ↓
Modifying existing file?
    → Check document relationships in README
    → Check cross-reference templates in README
    → Check references/ for supporting context
        ↓
Deleting file?
    → Check if it breaks document chain in README
        ↓
Proceed with operation
```

---

## Examples of Correct Behavior

### ✅ Correct: Creating Phase 3 Scoped Spec
```
1. Read docs/README.md
2. Verify pattern: phase-{NN}-scoped-spec.md
3. Verify location: docs/specs/
4. Create: docs/specs/phase-03-scoped-spec.md
5. Add cross-references per README templates
```

### ✅ Correct: Small Known Edit
```
1. User asks to fix one typo in an existing report
2. Edit that file directly
3. Skip full docs context pass (no structural change)
```

---

## AI Assistant Instructions

**As an AI assistant, you MUST:**

1. Read `docs/README.md` before docs creation, structural edits, or uncertain conventions
2. Check `references/` only when domain context is needed
3. Validate file names and locations against README patterns for new/reorganized docs
4. Include cross-references when creating docs that participate in a chain
5. Use two-digit phase numbers and lowercase-with-hyphens naming

**Never:**
- Skip README checks when creating/restructuring docs
- Guess at naming patterns
- Place files in wrong directories
- Use underscores or spaces in filenames
- Use single-digit phase numbers (1, 2) instead of (01, 02)
- Create documentation files without cross-references
- Force reference loading when it is not relevant

---

## References Folder Usage

The `references/` folder contains supporting documents for AI context enrichment.

### When to Check References

- **Starting a new phase**: Check for domain-specific context if required by scope
- **Working on integrations**: Check `references/api-docs/` for external API info
- **UI/UX work**: Check `references/design-assets/` for mockups and wireframes
- **Unfamiliar terminology**: Check topic-specific reference docs
- **External dependencies**: Check `references/external-links.md`

### References Structure

```
references/
├── {topic}-reference.md      # Domain/topic documentation
├── external-links.md         # Curated external resources
├── design-assets/            # Mockups, wireframes, diagrams
├── research/                 # Research notes, analysis
└── api-docs/                 # External API documentation
```

### Creating Reference Documents

When creating new reference documents:
- Use `{topic}-reference.md` naming pattern
- Place in appropriate subfolder (design-assets/, research/, api-docs/)
- Use lowercase-with-hyphens for file names
- Include source/date information for external content

---

## Error Recovery

If you realize you've created/restructured documentation without checking `docs/README.md`:

1. **STOP immediately**
2. Read `docs/README.md`
3. Compare your work against the standards
4. Fix any naming, location, or reference issues
5. Inform the user of corrections made

---

## Summary: The Golden Rule

```
╔════════════════════════════════════════════════╗
║  BEFORE structural docs changes in docs/      ║
║                                                ║
║      CHECK docs/README.md FIRST                ║
║                                                ║
║  Use context loading on demand, not always-on. ║
╔════════════════════════════════════════════════╗
```

This rule ensures:
- ✅ Consistent naming across all documentation
- ✅ Proper file organization
- ✅ Valid cross-references
- ✅ Maintained context chains
- ✅ Professional documentation standards
- ✅ AI has access to supporting reference context
- ✅ Domain knowledge is preserved and accessible