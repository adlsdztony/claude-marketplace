---
name: implement
description: Implement features from the project specification. This command should NOT be triggered directly by agents.
---

# Implement Project
You are the IMPLEMENTATION COMMAND (/implement).

This command implements features from the project specification. It automatically automatically detects project state and routes to initializer (new project) or coding agent (existing project), then continues implementation until **all features are complete**.

## What This Command Does

When invoked, this command will:

1. **Detect project state** - Check if `.spec/init.sh` exists
2. **Route to appropriate agent**:
   - **New project**: Invoke initializer-agent to set up project structure
   - **Existing project**: Invoke coding-agent to continue implementation
3. **Continue implementation** - Repeatly invoke coding-agent until all features are complete

### SUBAGENT POLICY
- Do NOT try to implement everything in a single context window. Use the Task tool to spawn subagents (initializer-agent or coding-agent) as needed based on project state. 
- DO NOT use background agents, use SINGLE **foreground** agent. 
- When you give instructions to subagents, be very short and precise, normally you don't need to pass anything.

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
2. **If features remain**:
   - Invoke next coding agent (return to Step 2)
3. **If all features complete**:
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
- Implemented features
- Updated progress notes
- Git commits for each feature

**Existing Project:**
- Implemented features
- Updated progress notes
- Git commits for each feature

**IMPORTANT:** ONLY exit when ALL features have `"passes": true`. Otherwise, continue invoking coding-agent until complete.

## Next Steps

After all features pass, run:
```
/optimize
```
