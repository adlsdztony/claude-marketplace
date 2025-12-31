# Web Clone Plugin

Autonomous web application cloning with browser automation - a simplified 3-command workflow for Claude Code.

## Overview

Web Clone is a streamlined plugin that transforms Claude Code into an autonomous development system. It combines web exploration, multi-agent coordination, and browser verification to build complete applications.

## Key Features

- **3-Command Workflow** - `/explore`, `/implement`, and `/optimize`
- **Web Exploration** - Crawl websites to automatically generate specifications
- **Smart Routing** - Automatically detects project state and routes to appropriate agent
- **Browser Verification** - All features tested through actual UI interaction
- **Auto-Continue** - Continuously implements features until project complete
- **Visual Optimization** - Compare target vs implemented pages and refine until matched
- **Multi-Agent Coordination** - Specialized agents for exploration, implementation, and optimization

## Quick Start

### Complete Workflow

```bash
# Step 1: Explore a website to generate specification
/explore url="https://claude.ai" depth=2

# Step 2: Implement all features automatically
/implement

# Step 3: Optimize to match the target website
/optimize target_url="https://claude.ai" local_url="http://localhost:3000" routes="/"
```

That's it! The plugin handles everything else.

**How it works:**
- `/explore` dynamically generates test cases as it explores each page
- Subagents add discovered features to `feature_list.json` in real-time
- The `/explore` command organizes and prioritizes the test cases at the end
- `/implement` detects if `init.sh` exists to determine if project needs initialization
- `/optimize` compares target and local UI, applies refinements, and records diffs

## Commands

### `/explore`

Explore a target website and generate application specification.

**What it does:**
- Crawls the website using browser automation
- Captures screenshots, snapshots, and summaries
- Delegates to subagents for each page
- **Subagents dynamically add test cases to `feature_list.json` as they explore**
- Generates `app_spec.txt`
- **Organizes and reorders `feature_list.json` by priority**

**Arguments:**
- `url` (required): Target URL to explore
- `depth` (optional): Maximum exploration depth, default 2
- `auth` (optional): Path to auth storage state

**Examples:**
```bash
/explore url="https://claude.ai" depth=2
/explore url="https://app.example.com" depth=3 auth=".spec/info/auth/storage_state.json"
```

**Output:**
- `.spec/app_spec.txt` - Comprehensive specification
- `.spec/feature_list.json` - Test cases (30-50 features)
- `.spec/info/` - All exploration artifacts

### `/implement`

Implement features from the specification with auto-continue.

**What it does:**
- Detects project state (new vs existing)
- Routes to initializer-agent (new) or coding-agent (existing)
- Continuously implements features one at a time
- Verifies each feature with browser automation
- Continues until all features complete

**Arguments:**
- `sessions` (optional): Max sessions to run, default 0 (unlimited)

**Examples:**
```bash
/implement              # Implement all features (unlimited)
/implement sessions=5   # Implement for 5 sessions only
```

**Output:**
- Implemented features
- Updated progress notes
- Git commits for each feature
- Production-ready application

### `/optimize`

Optimize the implemented site to match the target website.

**What it does:**
- Seeds and updates `.spec/optimize_list.json`
- Delegates to optimization-subagent per route/flow
- Captures target/local screenshots and snapshots
- Applies visual and behavioral refinements until matched

**Arguments:**
- `target_url` (required): Base URL of the target site
- `local_url` (optional): Base URL of the implemented site, default `http://localhost:3000`
- `routes` (optional): Comma-separated routes to seed optimization
- `sessions` (optional): Max optimization passes, default 0 (unlimited)

**Examples:**
```bash
/optimize target_url="https://example.com" local_url="http://localhost:3000" routes="/,/pricing"
```

**Output:**
- `.spec/optimize_list.json` - Optimization goals and status
- `.spec/optimize/` - Screenshots, snapshots, diff reports
- `.spec/optimize/reports/final-summary.md` - Final verification summary

## Agents

The plugin includes 6 autonomous agents:

### Exploration Subagent

**Triggered by:** `/explore` command via Task tool

**Role:** Explore individual pages

**Tasks:**
- Visit assigned URL with Playwright or Chrome DevTools MCP
- Capture artifacts (screenshots, snapshots, summaries)
- Extract links for further exploration
- **Dynamically add discovered features to `feature_list.json`**
- Update explore list

**Key feature:** Each subagent adds 3-10 test cases to `feature_list.json` based on discovered functionality.

### Exploration Summary Agent

**Triggered by:** `/explore` command after crawling complete

**Role:** Synthesize exploration results

**Tasks:**
- Review all captured artifacts
- Review test cases generated by subagents
- Generate `app_spec.txt`

**Note:** Does NOT generate `feature_list.json` (already done by subagents).

### Initializer Agent

**Triggered by:** `/implement` command when `init.sh` doesn't exist

**Role:** Set up project foundation

**Tasks:**
- Read project specification
- Create `.spec/init.sh` setup script
- Initialize git repository
- Create project structure

**Note:** `feature_list.json` may already exist from `/explore`, but project still needs initialization.

### Coding Agent

**Triggered by:** `/implement` command when project exists

**Role:** Implement features one at a time

**Workflow per session:**
1. Get bearings (read progress, spec, features)
2. Start servers
3. Verify existing features (regression testing)
4. Implement ONE new feature
5. Verify with browser automation (screenshots + console)
6. Update progress
7. Commit changes

**Quality Standards:**
- Zero console errors
- Polished UI matching spec
- End-to-end testing
- Production-ready

### Optimization Initializer Agent

**Triggered by:** `/optimize` command via Task tool

**Role:** Build or refresh the optimization list from app spec, feature list, and explore list

**Tasks:**
- Read `.spec/app_spec.txt`, `.spec/feature_list.json`, `.spec/explore_list.json`
- Derive key routes and flows
- Create or update `.spec/optimize_list.json`
- Preserve existing statuses and artifacts on re-runs

### Optimization Subagent

**Triggered by:** `/optimize` command via Task tool

**Role:** Compare target and local pages, eliminate visual and behavioral differences

**Tasks:**
- Open target and local pages with the same viewport
- Capture baseline + action screenshots
- Identify differences (layout, typography, color, interactions)
- Implement fixes and re-verify
- Update `.spec/optimize_list.json` and log artifacts

## Skills

### Progress Tracker

**Triggered by:** Progress checking operations

**Provides:**
- Progress calculation utilities
- Feature validation guidance
- Completion status tracking

**Resources:**
- `scripts/check-progress.py` - Progress checker
- `scripts/update-progress.py` - Progress updater
- `references/feature-validation.md` - Validation guide

### Browser Verification

**Triggered by:** Browser testing operations

**Provides:**
- Playwright or Chrome DevTools MCP automation patterns
- Testing strategies
- Screenshot guidelines

## Workflow

### Complete Example

```bash
# 1. Explore a website
/explore url="https://todoapp.example.com" depth=2

# Process:
# - Subagent explores homepage → adds 5 test cases
# - Subagent explores login → adds 8 test cases
# - Subagent explores dashboard → adds 12 test cases
# ... (continues for all pages)
# - Exploration-summary-agent generates app_spec.txt
# - Main command reorganizes feature_list.json by priority

# Output:
# ✓ Explored 15 pages
# ✓ Generated app_spec.txt
# ✓ Generated and organized feature_list.json with 50 test cases

# 2. Implement all features
/implement

# Output:
# ✓ Project initialized (init.sh created)
# ✓ Feature 1/50 implemented
# ✓ Feature 2/50 implemented
# ...
# ✓ Feature 50/50 implemented
# 🎉 Project complete!

# 3. Optimize to match the target site
/optimize target_url="https://todoapp.example.com" local_url="http://localhost:3000" routes="/,/login,/dashboard"

# Output:
# ✓ Target vs local compared with screenshots
# ✓ Differences logged in .spec/optimize_list.json
# ✓ UI refined to match target
# 🎉 Visual parity achieved!
```

## Project Structure

After exploration:
```
.spec/
├── app_spec.txt              # Application specification
├── feature_list.json         # Test cases (dynamically generated by subagents)
├── explore_list.json         # Exploration history
└── info/                     # Exploration artifacts
    ├── screenshots/
    ├── snapshots/
    └── summaries/
```

After initialization:
```
.spec/
├── feature_list.json         # From exploration
├── init.sh                   # Environment setup script
├── claude-progress.txt       # Progress notes
└── app_spec.txt              # From exploration
```

After implementation:
```
.spec/
├── feature_list.json         # Updated with passing status
├── init.sh                   # Environment setup
├── claude-progress.txt       # Session notes
└── app_spec.txt              # Original specification
```

After optimization:
```
.spec/
├── optimize_list.json         # Optimization goals and status
└── optimize/                  # Optimization artifacts
    ├── screenshots/
    │   ├── target/
    │   └── local/
    ├── snapshots/
    ├── reports/
    └── logs/
```

## Feature List Format

`.spec/feature_list.json` is the source of truth:

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

**Critical Rule:** Only modify `"passes"` field. Never edit, remove, or reorder.

## Browser Verification

All features verified through actual browser interaction:

1. Navigate to page
2. Interact like human (click, type, scroll)
3. Capture screenshots
4. Verify functionality AND appearance
5. Check console (zero errors expected)

## Progress Tracking

Check progress anytime:

```bash
# Run progress checker script
python3 .claude/plugins/web-clone/skills/progress-tracker/scripts/check-progress.py
```

## Quality Standards

The coding-agent maintains:

- **Zero console errors** - No browser or backend errors
- **Polished UI** - Matches spec design
- **End-to-end testing** - All features tested through UI
- **Professional quality** - Fast, responsive, production-ready

## Best Practices

1. **Explore first** - Always run `/explore` before `/implement`
2. **Let it run** - Auto-continue handles everything
3. **Trust the process** - One feature per session, quality over speed
4. **Check progress** - Use the progress script to see status
5. **Review commits** - Each feature gets a descriptive commit
6. **Optimize last** - Run `/optimize` only after all features pass

## Troubleshooting

### Exploration Fails

- Check URL is accessible
- Increase depth if site is large
- Use auth parameter for login-required sites

### Implementation Fails

- Ensure server is running
- Check browser automation tools are installed
- Review `.spec/claude-progress.txt` for errors

### Browser Errors

- Verify Playwright or Chrome DevTools MCP is installed
- Check server is running on correct port
- Ensure `--no-sandbox` flag is used

## Configuration

**Browser:**
- Tool: Playwright or Chrome DevTools MCP
- Viewport: 1600x900
- Mode: Headless (headful for auth)
- Args: `--no-sandbox`

**Exploration:**
- Default depth: 2
- Screenshot size: 1600x900
- Link discovery: Same domain only

## Under the Hood

### How `/explore` Works

1. Creates `.spec/` directory structure
2. Initializes `explore_list.json` with root URL
3. For each pending URL:
   - Spawns exploration-subagent via Task tool
   - **Subagent captures artifacts AND adds test cases to `feature_list.json`**
   - Subagent extracts links for further exploration
4. After all URLs explored:
   - Invokes exploration-summary-agent to generate `app_spec.txt`
   - **Main command organizes and reorders `feature_list.json`** by priority
5. Output: Organized test cases ready for implementation

### How `/implement` Works

1. **Checks if `.spec/init.sh` exists** (not feature_list.json)
2. If init.sh does NOT exist:
   - Invokes initializer-agent
   - Creates project structure, init.sh, git repo
   - feature_list.json may already exist from exploration
3. If init.sh exists:
   - Invokes coding-agent
   - Implements ONE feature
   - Verifies with browser automation
   - Updates progress
   - Commits changes
4. If features remain AND (sessions=0 OR more sessions available):
   - Waits 3 seconds
   - Loops back to step 3
5. When all features complete:
   - Displays final summary
   - Exits

### How `/optimize` Works

1. Verifies exploration + implementation are complete
2. Invokes optimization-initializer-agent to build `.spec/optimize_list.json`
3. For each pending route:
   - Spawns optimization-subagent via Task tool
   - Subagent captures target/local screenshots and actions
   - Subagent applies fixes and updates optimize_list.json
4. Loops until all items are marked "done"
5. Writes final verification summary under `.spec/optimize/reports/`

## Technical Details

### Multi-Agent System

- **Exploration:** Main command delegates to subagents via Task tool
- **Implementation:** Auto-continue loop with 3-second delay
- **Optimization:** Initializer builds optimize list, subagents compare and refine pages route-by-route
- **Context management:** Clean session starts

### Artifacts

- **All under `.spec/`** - Unified location
- **Git-tracked** - Version controlled
- **Human-readable** - Markdown and JSON

### Skills

- **Progressive disclosure** - Load resources as needed
- **Imperative format** - Clear instructions
- **Third-person triggers** - Specific activation

## Advanced Usage

### Resume Partial Implementation

If implementation was interrupted:

```bash
/implement
```

The command detects existing work and continues from where it left off.

### Implement Specific Number of Features

```bash
/implement sessions=10
```

Implements 10 features (or fewer if project completes sooner).

### Explore with Authentication

```bash
# First run: handle login manually
/explore url="https://app.example.com" depth=2

# Browser will prompt for login, then save state

# Subsequent runs: use saved state
/explore url="https://app.example.com" depth=2 auth=".spec/info/auth/storage_state.json"
```

## Examples

### Clone a Simple Website

```bash
/explore url="https://simple.example.com" depth=1
/implement
/optimize target_url="https://simple.example.com" local_url="http://localhost:3000" routes="/"
```

### Clone a Complex Application

```bash
/explore url="https://complex.example.com" depth=3
/implement
/optimize target_url="https://complex.example.com" local_url="http://localhost:3000" routes="/,/login,/dashboard"
```

### Clone Authenticated Application

```bash
/explore url="https://app.example.com" depth=2 auth=".spec/info/auth/storage_state.json"
/implement
/optimize target_url="https://app.example.com" local_url="http://localhost:3000" routes="/,/login"
```

## Contributing

This plugin simplifies autonomous web development. For issues or improvements, review:

- Command prompts in `commands/*.md`
- Agent definitions in `agents/*.md`
- Skill guidance in `skills/*/SKILL.md`

## License

Same license as the autonomous coding pipeline.

## Acknowledgments

Based on the autonomous coding multi-agent pipeline with browser verification.
