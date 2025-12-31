---
name: implement
description: Implement features from the project specification. Automatically detects project state and routes to initializer (new project) or coding agent (existing project), then continues implementation until all features are complete.
arguments:
  sessions:
    description: "Maximum number of coding sessions to run (0 = unlimited until all features complete)"
    default: 0
---

# Implement Project

This command implements features from the project specification. It automatically detects the project state and routes to the appropriate agent.

## What This Command Does

When invoked, this command will:

1. **Detect project state** - Check if `.spec/init.sh` exists
2. **Route to appropriate agent**:
   - **New project**: Invoke initializer-agent to set up project structure
   - **Existing project**: Invoke coding-agent to continue implementation
3. **Continue implementation** - Loop through coding sessions until all features complete
4. **Track progress** - Update feature_list.json after each feature
5. **Auto-continue** - Automatically start next session after completion (if sessions > 1 or unlimited)

## Arguments

### `sessions` (optional, default: 0)
- **Description**: Maximum number of coding sessions to run
- **0** = Unlimited (continue until all features are complete)
- **N** = Run exactly N sessions

## Usage Examples

### Implement all features (unlimited sessions):
```
/implement
```

### Implement for 5 sessions only:
```
/implement sessions=5
```

### Resume implementation:
```
/implement
```

## Workflow

### Step 1: Detect Project State

Check if `.spec/init.sh` exists:

**If NOT exists (New Project):**
1. Read `.spec/app_spec.txt` or use provided spec
2. Invoke **initializer-agent** to:
   - Create `.spec/init.sh` environment setup script
   - Initialize git repository
   - Create basic project structure
3. After initializer completes, proceed to Step 3

**If exists (Existing Project):**
- Proceed to Step 2

**Note:** `.spec/feature_list.json` may already exist from `/explore` command, but the project still needs initialization (init.sh, project structure, etc.).

### Step 2: Invoke Coding Agent

Invoke **coding-agent** to:

1. **Get bearings** - Read progress, feature list, and project spec
2. **Start servers** - Run `.spec/init.sh` if exists
3. **Verify existing features** - Run tests to ensure nothing is broken
4. **Implement ONE feature** - Complete the highest-priority remaining feature
5. **Browser verification** - Test through actual UI interaction with screenshots
6. **Update progress** - Mark feature as passing in feature_list.json
7. **Commit changes** - Save progress with descriptive commit message
8. **End session cleanly** - Leave code in working state

### Step 3: Continue Loop

After each coding-agent session:

1. **Check remaining features** - Count features with "passes": false
2. **If features remain** AND (sessions == 0 OR session_count < sessions):
   - Wait 3 seconds
   - Start next session (return to Step 2)
3. **If all features complete** OR session_count == sessions:
   - Display final progress summary
   - Exit

## Initializer Agent

**Triggered when:** `.spec/feature_list.json` does not exist

**Role:** Set up project foundation

**Process:**
1. Read project specification (`.spec/app_spec.txt` or spec text)
2. Create `.spec/feature_list.json` with detailed test cases (minimum 30 features)
3. Create `.spec/init.sh` for environment setup
4. Initialize git repository
5. Create basic project structure
6. Create `CLAUDE.md` with project overview

**Output:**
- `.spec/feature_list.json` - Test cases (source of truth)
- `.spec/init.sh` - Environment setup script
- Git repository initialized
- Basic project structure

## Coding Agent

**Triggered when:** `.spec/feature_list.json` exists

**Role:** Implement features one at a time

**Process per session:**
1. Get bearings (read progress, feature list, spec)
2. Start servers with `.spec/init.sh`
3. Run verification tests on existing features
4. Implement ONE new feature (highest priority)
5. Verify with browser automation (screenshots + console check)
6. Update feature_list.json (mark "passes": true)
7. Update `.spec/claude-progress.txt`
8. Commit changes

**Quality Standards:**
- Zero console errors
- Polished UI matching spec
- End-to-end testing through UI
- Professional, production-ready

## Browser Verification

All features must be verified through actual browser interaction:

1. **Navigate** to relevant page
2. **Interact** like a human user (click, type, scroll)
3. **Capture** screenshots at each step
4. **Verify** functionality AND visual appearance
5. **Check** console for errors (zero expected)

**DO:**
- Test through the UI with clicks and keyboard input
- Take screenshots to verify visual appearance
- Check for console errors in browser
- Verify complete user workflows end-to-end

**DON'T:**
- Only test with curl commands (insufficient)
- Use JavaScript evaluation to bypass UI (no shortcuts)
- Skip visual verification
- Mark tests passing without thorough verification

## Progress Tracking

Progress is tracked in `.spec/feature_list.json`:

```json
[
  {
    "id": 1,
    "category": "functional",
    "description": "User can login with email and password",
    "steps": [
      "Navigate to /login",
      "Enter email and password",
      "Click submit button",
      "Verify redirect to dashboard"
    ],
    "passes": false  // ← Only modify this field
  }
]
```

**Critical Rule:** Only modify the `"passes"` field. Never remove, edit, or reorder features.

## Artifacts Generated

After `/implement` completes:

**New Project:**
- `.spec/feature_list.json` - Test cases
- `.spec/init.sh` - Environment setup
- Project structure
- Git repository

**Existing Project:**
- Implemented features
- Updated progress notes
- Git commits for each feature

## Session Management

**Auto-continue mode** (default):
- After each feature, wait 3 seconds
- Automatically start next session
- Continue until all features complete or session limit reached

**Single session mode** (`sessions=1`):
- Implement one feature
- Exit after commit
- User must re-run `/implement` to continue

## Quality Assurance

Before marking a feature as passing, verify:

- [ ] All test steps completed successfully
- [ ] Screenshots captured for each step
- [ ] Final state matches expected outcome
- [ ] Zero console errors
- [ ] Visual appearance matches requirements
- [ ] Edge cases tested (if applicable)
- [ ] No regressions in existing features

## Example Output

**New project:**
```
✓ Project initialized

Created:
- .spec/feature_list.json with 30 test cases
- .spec/init.sh environment setup script
- Project structure for React + Node.js
- Git repository initialized

Starting implementation...
[Invokes coding-agent]
```

**Existing project:**
```
=== Current Progress ===

Total Features: 30
✓ Completed: 15 (50%)
○ Remaining: 15 (50%)

Invoking coding-agent to implement next feature...
```

## Next Steps

After `/implement` completes:

- **If features remain**: Run `/implement` again to continue
- **If all features complete**: Project is ready for deployment!

## Troubleshooting

### Project Not Initialized

```
Error: .spec/app_spec.txt not found
```

**Solution:** Run `/explore` first to generate specification, or provide spec when implementing

### No Features Passing

Normal for new projects. The coding-agent will implement features systematically.

### All Features Passing

```
Progress: 30/30 (100%) ✓
🎉 Project complete! All features verified.
```

### Browser Automation Fails

- Check server is running (`./.spec/init.sh`)
- Verify correct URL/port
- Check for console errors
- Ensure Playwright is installed
