---
name: audit
description: Audit the implemented website to identify non-functional elements and generate a report. This command should NOT be triggered directly by agents.
arguments:
  depth:
    description: "Maximum audit depth (number of hops from root)"
    default: 3
---

# Audit Website
You are the AUDIT COMMAND (/audit).

This command audits your implemented website to identify non-functional buttons, broken links, and incomplete features. It generates a comprehensive report and adds missing test cases to `feature_list.json`.

## What This Command Does

When invoked, this command will:

1. **Start the local server** - Run `.spec/init.sh` to start the app
2. **Crawl the implemented site** - Visit all pages within depth
3. **Test interactive elements** - Click buttons, submit forms, follow links
4. **Identify broken functionality** - Elements that don't respond or error
5. **Generate audit report** - Comprehensive list of issues found
6. **Update feature_list.json** - Add missing test cases for broken features

## Arguments


### `depth` (optional, default: 3)
- **Description**: Maximum audit depth (hops from root URL)
- **Values**:
  - `1` = Homepage only
  - `2` = Homepage + direct links
  - `3` = Homepage + links + their links

## Audit Workflow

You are the AUDIT COMMAND. Your job is to audit the implemented website, identify non-functional elements, and update the feature list with missing test cases.

### INPUTS
- Max depth: {AUDIT_DEPTH} (provided by user, default: 3)

### OUTPUT LOCATIONS (ALL UNDER .spec/)
- Audit report: `.spec/audit_report.md`
- Audit list: `.spec/audit_list.json`
- Updated feature list: `.spec/feature_list.json`

### BROWSER SETTINGS
- Default to headless Playwright or Chrome DevTools MCP
- Use viewport 1600x900
- Launch with `--no-sandbox` argument

### SUBAGENT POLICY
- Do NOT try to audit everything in a single context window. Use the Task tool to spawn subagents (audit-subagent) that audit specific pages.
- DO NOT use background agents, use SINGLE **foreground** agent.
- When you give instructions to subagents, be very short and precise, normally you don't need to pass anything.

---

## STEP 1: Start Local Server

Start the local server if not already running:

```bash
chmod +x .spec/init.sh
./.spec/init.sh
```

Wait for server to be ready, then verify it's accessible.

## STEP 2: Prepare Directories

Create these directories if missing:
```
.spec/audit/
.spec/audit/screenshots/
.spec/audit/reports/
```

## STEP 3: Initialize Audit List

Create `.spec/audit_list.json`:

```json
{
  "root_url": "http://localhost:3000",
  "max_depth": 2,
  "audit_started": "ISO timestamp",
  "items": [
    {
      "id": 1,
      "url": "http://localhost:3000/",
      "page": "home",
      "depth": 0,
      "status": "pending",
      "issues": []
    }
  ]
}
```

**Rules:**
- Only include URLs on the same host
- `depth` is hops from root (root is depth 0)
- Do not add URLs with depth greater than max_depth
- Normalize URLs before deduping
- Deduplicate by URL
- Use statuses: `pending`, `in_progress`, `done`, `blocked`

## STEP 4: Audit Pending Items (LOOP)

For each `pending` item within the depth limit:

1. **Use the Task tool** to spawn audit-subagent
2. **Pass**: The item ID to audit
3. **Verify**: ID exists and is `done`

**Repeat** until no `pending` items remain within depth.

## STEP 5: Generate Audit Report

**When audit is complete (no pending items within depth)**:

1. Read all audit results from `.spec/audit_list.json`
2. Compile issues from all pages
3. Generate `.spec/audit_report.md`:

```markdown
# Audit Report

**Generated**: [timestamp]
**URL**: [audited URL]
**Pages Audited**: [count]

## Summary

- **Total Issues Found**: [count]
- **Non-functional Buttons**: [count]
- **Placeholder Functions**: [count]
- **Broken Links**: [count]
- **Form Issues**: [count]
- **Console Errors**: [count]
- **Missing Functionality**: [count]

## Critical Issues

[Issues that break core functionality]

## Non-functional Elements

### Buttons Without Actions
| Page | Element | Expected Behavior | Actual Behavior |
|------|---------|-------------------|-----------------|
| /home | "Submit" button | Submit form | No response |

### Placeholder/Stub Functions
| Page | Element | Expected Behavior | Placeholder Message |
|------|---------|-------------------|---------------------|
| /home | "Like" button | Update like count | "Not implemented yet" |
| /profile | "Edit" button | Open edit modal | "Coming soon" |

### Broken Links
| Page | Link Text | Target | Issue |
|------|-----------|--------|-------|
| /home | "About Us" | /about | 404 error |

### Form Issues
| Page | Form | Issue |
|------|------|-------|
| /contact | Contact form | No submission handler |

### Console Errors
| Page | Error | Count |
|------|-------|-------|
| /home | TypeError: undefined | 3 |

## Recommendations

1. [Priority fix 1]
2. [Priority fix 2]
...
```

## STEP 6: Update Feature List

For each issue found, add a new test case to `.spec/feature_list.json`:

1. Read current feature list
2. For each unique issue:
   - Check if similar test case exists
   - If not, create new test case:

```json
{
  "id": <next_id>,
  "category": "functional",
  "description": "[Element] on [page] should [expected behavior]",
  "steps": [
    "Navigate to [page]",
    "Locate [element]",
    "Click/interact with [element]",
    "Verify [expected behavior]"
  ],
  "passes": false,
  "source": "audit",
  "audit_issue": "[issue type]"
}
```

3. Save updated feature list

## STEP 7: Summary

Output final summary:

```
Audit Complete

Pages audited: N
Total issues found: M

Issues by type:
  Non-functional buttons: X
  Placeholder functions: P
  Broken links: Y
  Form issues: Z
  Console errors: W

New test cases added: K

Report: .spec/audit_report.md
Updated: .spec/feature_list.json

Next: Run /implement to fix identified issues
```

## Output

After completion, you'll have:
- `.spec/audit_report.md` - Comprehensive audit report
- `.spec/audit_list.json` - Audit history with all issues
- `.spec/feature_list.json` - Updated with new test cases for broken features
- `.spec/audit/screenshots/` - Screenshots of issues found
