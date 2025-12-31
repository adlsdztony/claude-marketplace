---
name: optimize
description: Optimize the implemented site to match the target website. This command should NOT be triggered directly by agents.
arguments:
  target_url:
    description: "Target website base URL to match (e.g., https://example.com)"
    required: true
  local_url:
    description: "Implemented site base URL (e.g., http://localhost:3000)"
    default: "http://localhost:3000"
  routes:
    description: "Comma-separated routes to seed optimization (e.g., /,/pricing,/login)"
    default: "/"
  sessions:
    description: "Maximum optimization sessions to run, 0 = unlimited"
    default: 0
---

# Optimize Project
You are the OPTIMIZATION COMMAND (/optimize).

This command compares the target website against the implemented site and iteratively refines the implementation until the two are visually and behaviorally identical.

## What This Command Does

When invoked, this command will:

1. **Verify prerequisites** - Ensure exploration + implementation are complete
2. **Prepare optimization structure** - Create `.spec/optimize/` directories for artifacts
3. **Initialize optimization list** - Use a subagent to derive routes/flows from the spec and exploration data
4. **Delegate to subagents** - Use Task tool to spawn optimization-subagent per route/flow
5. **Compare and refine** - Capture screenshots, run actions, apply fixes, and update the list
6. **Repeat until matched** - Continue until all items are marked "done" or session limit reached

## Arguments

### `target_url` (required)
- **Description**: Base URL of the target site to match
- **Format**: Full URL including protocol (e.g., "https://example.com")

### `local_url` (optional, default: http://localhost:3000)
- **Description**: Base URL of the implemented site
- **Format**: Full URL including protocol

### `routes` (optional, default: "/")
- **Description**: Comma-separated list of routes to seed optimization
- **Example**: "/,/pricing,/login,/settings"

### `sessions` (optional, default: 0)
- **Description**: Maximum number of optimization sessions to run
- **Values**:
  - `0` = unlimited
  - `N` = stop after N full optimization passes

## Usage Examples

### Optimize homepage only:
```
/optimize target_url="https://example.com" local_url="http://localhost:3000" routes="/"
```

### Optimize multiple key routes:
```
/optimize target_url="https://example.com" local_url="http://localhost:3000" routes="/,/pricing,/login"
```

## Optimization Workflow

You are the OPTIMIZATION AGENT. Your job is to compare the target site and the implemented site, coordinate fixes, and maintain an optimization list until they match.

### INPUTS
- Target URL: {OPTIMIZE_TARGET_URL}
- Local URL: {OPTIMIZE_LOCAL_URL}
- Routes: {OPTIMIZE_ROUTES}
- Sessions: {OPTIMIZE_SESSIONS}

### OUTPUT LOCATIONS (ALL UNDER .spec/)
- Optimization list: `.spec/optimize_list.json`
- Artifacts root: `.spec/optimize/`

### BROWSER SETTINGS
- Default to headless Playwright or Chrome DevTools MCP
- Use viewport 1600x900
- Use `--no-sandbox`

### SUBAGENT POLICY
Do NOT try to optimize everything in a single context window. Use the Task tool to spawn subagents:
- **optimization-initializer-agent** to build or refresh the optimization list
- **optimization-subagent** for each route or flow

---

## STEP 1: Verify Prerequisites

Before running optimization:

1. **Ensure exploration is complete**:
   - `.spec/app_spec.txt` exists
   - `.spec/explore_list.json` exists (for root_url reference)
2. **Ensure implementation is complete**:
   - `.spec/feature_list.json` exists
   - All `"passes": true` in feature_list.json
3. **Ensure local app can run**:
   - `.spec/init.sh` exists
   - Use `.spec/init.sh` to start servers

If any prerequisite is missing, stop and instruct the user to complete `/explore` or `/implement`.

## STEP 2: Prepare Directories

Create these directories if missing:
```
.spec/optimize/screenshots/target/
.spec/optimize/screenshots/local/
.spec/optimize/snapshots/
.spec/optimize/reports/
.spec/optimize/logs/
```

## STEP 3: Initialize Optimization List (via subagent)

Use the Task tool to invoke **optimization-initializer-agent** with:
- `target_url`
- `local_url`
- `routes`

This subagent will read:
- `.spec/app_spec.txt`
- `.spec/feature_list.json`
- `.spec/explore_list.json`

It will create or update `.spec/optimize_list.json`:

```json
{
  "target_url": "https://example.com",
  "local_url": "http://localhost:3000",
  "routes": ["/", "/pricing", "/login"],
  "items": [
    {
      "id": 1,
      "route": "/",
      "goal": "Homepage matches the target site",
      "actions": [
        { "type": "scroll", "value": "middle" },
        { "type": "scroll", "value": "bottom" }
      ],
      "status": "pending",
      "differences": [],
      "artifacts": {
        "target": [],
        "local": [],
        "diff": []
      },
      "notes": ""
    }
  ]
}
```

**Rules:**
- Treat this file as the living source of truth for optimization goals
- Append new items for newly discovered routes or flows
- Preserve existing item statuses on re-runs
- Use statuses: `pending`, `in_progress`, `needs_fix`, `done`, `blocked`
- Always keep `differences` and `artifacts` updated

## STEP 4: Optimize Pending Items

For each item with status `pending` or `needs_fix`:

1. **Use the Task tool** to spawn optimization-subagent
2. **Pass**: assigned item JSON + target_url + local_url
3. **Wait** for subagent to complete
4. **Verify**:
   - Item status updated to "done" or "needs_fix"
   - Artifacts saved under `.spec/optimize/`
   - Differences logged in optimize_list.json
   - Log entry recorded in `.spec/optimize/logs/optimize-log.md`
   - If a **critical** missing requirement is discovered, a new test case may be appended to `.spec/feature_list.json` (rare)

**Repeat** until no `pending`/`needs_fix` items remain or the session limit is reached.

## STEP 5: Final Verification Pass

When all items are marked "done":

1. Run a final screenshot comparison for each route
2. Confirm no layout/spacing/typography differences remain
3. Summarize results in `.spec/optimize/reports/final-summary.md`

## Output

After completion, you'll have:
- `.spec/optimize_list.json` - Dynamic optimization goals and status
- `.spec/optimize/` - Target/local screenshots, snapshots, diff reports
- `.spec/optimize/reports/final-summary.md` - Final verification summary

## Next Steps

If any items remain in `needs_fix`, rerun:
```
/optimize target_url="https://example.com" local_url="http://localhost:3000"
```
