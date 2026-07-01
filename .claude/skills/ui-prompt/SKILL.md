---
name: ui-prompt
description: Transforms UI design specifications into structured prompts for AI UI generation tools. Use when creating UI mockups, generating design prompts, or preparing visual assets from specifications.
---
# UI Design Prompt Generator

Transform UI Design Specification documents into structured, high-density prompts for UI generation tools, ensuring consistent visual implementation across all screens.

## When to Use

- Creating UI mockups from specifications
- Generating prompts for AI design tools
- Preparing visual assets for a phase
- Ensuring design consistency across screens

## Output Structure

```
docs/references/design-assets/
├── 00-design-token.md              # Shared across ALL phases
├── phase-01/
│   ├── 00-screen-inventory.md
│   └── 01-ui-prompts.md
├── phase-02/
│   ├── 00-screen-inventory.md
│   └── 01-ui-prompts.md
└── ...
```

## Instructions

### Step 1: Screen Inventory Analysis

Analyze the design specification to identify:

1. **Total Screen Count** - Distinct pages/views
2. **Screen Names & Routes** - Names and navigation paths
3. **Screen Purposes** - Primary functions
4. **Screen Relationships** - Navigation between screens

Output to `{phase}/00-screen-inventory.md`:

```markdown
# Screen Inventory

**Project**: [Name]
**Phase**: [Phase]
**Source**: [UI Design Spec Path]

## Summary
Total Screens: [N]

## Screen List
| # | Screen Name | Route/Path | Purpose |
|---|-------------|------------|---------|
| 1 | [Name] | [/route] | [Description] |

## Navigation Flow
[ASCII diagram or description]

## Screen Details
### Screen 1: [Name]
- **Entry Point**: How user arrives
- **Key Components**: Main UI elements
- **States**: Different states
- **Exit Points**: Navigation options
```

### Step 2: Extract Shared Design Token

> Create ONCE per project (typically Phase 01). All phases reference the same token.

Extract from `01-ui-design.md`:

| Category | What to Extract |
|----------|-----------------|
| Colors | Primary, secondary, accent, status (hex codes) |
| Typography | Font families, size scale, weights, line heights |
| Spacing | Base unit, spacing scale |
| Components | UI library, button/input/card styles |
| Breakpoints | Responsive breakpoints with pixels |
| Interactions | Animation durations, easing |
| Accessibility | Focus indicators, touch targets |

Output to `00-design-token.md` (root level):

```markdown
# Design Token

**Project**: [Name]
**Scope**: All Phases (Shared)
**Source**: [UI Design Spec Path]

## Token Summary (Single Paragraph)
Color palette using [Primary #XXXXXX] for [usage], [Secondary #XXXXXX] for [usage]...

## Token Details
### Colors
| Name | Hex | Usage |
|------|-----|-------|

### Typography
| Element | Font | Size | Weight | Line Height |
|---------|------|------|--------|-------------|

### Spacing
- Base unit: [X]px
- Scale: [values]

### Breakpoints
| Name | Min Width | Max Width | Layout Behavior |
|------|-----------|-----------|-----------------|
```

### Step 3: Analyze the Aesthetic (Vibe & Theme)

1. **Interpret the User's Requested Style**
   - Identify the requested aesthetic (e.g., "Corporate," "Retro," "Clean," "Playful")
   - If not specified, infer from project context or ask for clarification

2. **Generate a Specific Color Palette**
   - Primary color (main actions, branding)
   - Secondary color (supporting elements)
   - Background colors (page, cards, surfaces)
   - All colors MUST use Hex codes

3. **Select Vibe Adjectives**
   - Choose adjectives that influence fonts, borders, and overall feel
   - Examples: "Glassmorphism," "Brutalist," "Neumorphic," "Minimalist," "Skeuomorphic"
   - These adjectives guide typography, border radius, shadows, and spacing decisions

### Step 4: Define the Layout

Unless specified otherwise, enforce a layout optimized for component visibility:

**Default Layout**: "Fixed sidebar navigation for categories, main grid display for elements"

Layout considerations:
- Sidebar: Category navigation, collapsible sections
- Main area: Grid or list display of components
- Header: Search, filters, theme toggle
- Footer: Pagination or infinite scroll

### Step 5: Generate the Component Data

Generate a JSON array named `components` following this strict schema:

| Field | Type | Description |
|-------|------|-------------|
| `classGroup` | string | Category name (e.g., "Buttons", "Forms", "Cards") |
| `description` | string | Technical description of the component |
| `props` | array | Realistic React/Vue props including state variants |
| `emits` | array | Events the component emits |
| `usage` | string | Code snippet showing component usage |

**Required Props for Interactivity**:
- State variants: `isError`, `isDisabled`, `isLoading`
- Visual variants: `variant`, `size`, `color`
- Data binding: `modelValue`, `value`, `checked`

### Step 6: Output Format

Your final output must be a single code block containing:
1. Natural language description (layout + vibe)
2. Theme colors section
3. JSON data structure

**Do not include markdown chatter outside the code block.**

## Response Template

```
[Layout Description & Vibe Adjectives]
Theme Colours:
primary: [Hex]
secondary: [Hex]
background related: [Hex]

You can get the list of elements to display from the JSON below:

{
  "components": [
    {
      "classGroup": "[Category Name]",
      "description": "[Technical description]",
      "props": ["modelValue", "variant", "size", "isDisabled", "isLoading", "isError"],
      "emits": ["click", "change", "update:modelValue"],
      "usage": "<Component variant=\"solid\" size=\"md\" />"
    }
  ]
}
```

## Example Output

```
Clean, minimalist design with generous whitespace and subtle shadows. Fixed sidebar navigation for categories with icon + label, main content area displays components in a responsive grid. Glassmorphism influences with frosted backgrounds and soft borders.

Theme Colours:
primary: #4A90D9
secondary: #6C757D
background related: #F8F9FA, #FFFFFF, #E9ECEF

You can get the list of elements to display from the JSON below:

{
  "components": [
    {
      "classGroup": "Buttons",
      "description": "Interactive button components with multiple variants and states",
      "props": ["variant", "size", "isDisabled", "isLoading", "leftIcon", "rightIcon"],
      "emits": ["click"],
      "usage": "<Button variant=\"solid\" size=\"md\">Click Me</Button>"
    },
    {
      "classGroup": "Inputs",
      "description": "Text input fields with validation states and addons",
      "props": ["modelValue", "type", "placeholder", "isDisabled", "isError", "errorMessage"],
      "emits": ["update:modelValue", "focus", "blur"],
      "usage": "<Input v-model=\"value\" placeholder=\"Enter text\" />"
    },
    {
      "classGroup": "Cards",
      "description": "Container components for grouped content with optional header and footer",
      "props": ["title", "subtitle", "variant", "isHoverable", "isClickable"],
      "emits": ["click"],
      "usage": "<Card title=\"Card Title\" isHoverable>Content here</Card>"
    }
  ]
}
```

## Vibe Reference Guide

| Vibe | Typography | Borders | Shadows | Spacing |
|------|------------|---------|---------|---------|
| Glassmorphism | Light sans-serif | Soft, translucent | Blur backdrop | Generous |
| Brutalist | Bold, monospace | Sharp, thick | Hard, offset | Tight |
| Neumorphic | Rounded sans | Soft, inset | Inner + outer | Balanced |
| Minimalist | Thin, clean | None or hairline | Subtle | Generous |
| Corporate | Professional serif/sans | Standard | Medium | Standard |
| Retro | Pixel, vintage | Pixelated, thick | Hard | Compact |

## Component Category Reference

Common categories to include based on project type:

| Category | Components |
|----------|------------|
| Buttons | Primary, Secondary, Ghost, Icon, Loading |
| Forms | Input, Textarea, Select, Checkbox, Radio, Switch |
| Cards | Basic, Interactive, Media, Stats |
| Navigation | Navbar, Sidebar, Tabs, Breadcrumb, Pagination |
| Feedback | Alert, Toast, Modal, Tooltip, Progress |
| Data Display | Table, List, Badge, Avatar, Tag |
| Layout | Container, Grid, Stack, Divider |

## Phase Consistency Rules

All phases MUST:
1. Reference the same design token (`../00-design-token.md`)
2. Use identical hex codes, sizes, spacing across all prompts
3. Follow the same component library and vibe adjectives
4. Maintain consistent prop naming conventions

When adding new phases:
1. Check if design token exists
2. If YES → Reference it, do NOT create new
3. Generate phase-specific component data
4. Ensure prompts maintain the established vibe
