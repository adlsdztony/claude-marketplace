#!/bin/bash
set -euo pipefail

# Read hook input
input=$(cat)

# Extract the current working directory and transcript path
cwd=$(echo "$input" | jq -r '.cwd // ""')
transcript_path=$(echo "$input" | jq -r '.transcript_path // ""')

if [ -z "$cwd" ]; then
  # If no cwd, cannot check, so approve
  echo '{"decision": "approve"}'
  exit 0
fi

cd "$cwd" || {
  echo '{"decision": "approve"}'
  exit 0
}

# Check if we're in a web-clone command session by looking at the transcript
# Only check if transcript exists and contains web-clone command markers
is_web_clone_command=false
active_command=""

if [ -n "$transcript_path" ] && [ -f "$transcript_path" ]; then
  # Check last 500 lines of transcript for command invocations
  if tail -n 500 "$transcript_path" 2>/dev/null | grep -q "You are the EXPLORATION COMMAND"; then
    is_web_clone_command=true
    active_command="explore"
  elif tail -n 500 "$transcript_path" 2>/dev/null | grep -q "You are the IMPLEMENTATION COMMAND"; then
    is_web_clone_command=true
    active_command="implement"
  elif tail -n 500 "$transcript_path" 2>/dev/null | grep -q "You are the AUDIT COMMAND"; then
    is_web_clone_command=true
    active_command="audit"
  fi
fi

# If not a web-clone command, always approve
if [ "$is_web_clone_command" = false ]; then
  echo '{"decision": "approve"}'
  exit 0
fi

# Function to check explore list completion
check_explore_list() {
  local file=".spec/explore_list.json"
  if [ ! -f "$file" ]; then
    return 1  # File doesn't exist, not relevant
  fi

  local max_depth=$(jq -r '.max_depth // 2' "$file")
  local pending=$(jq "[.items[] | select(.depth <= $max_depth and (.status == \"pending\" or .status == \"in_progress\"))] | length" "$file")

  if [ "$pending" -gt 0 ]; then
    local total=$(jq "[.items[] | select(.depth <= $max_depth)] | length" "$file")
    local done=$((total - pending))
    echo "{
      \"decision\": \"block\",
      \"reason\": \"Exploration is incomplete: $done/$total pages explored. $pending pages remaining within depth $max_depth.\",
      \"systemMessage\": \"The exploration command has not finished. There are still $pending pages pending exploration. Please continue the exploration loop by spawning the next exploration-subagent for the pending items.\"
    }" >&2
    exit 2
  fi

  return 0
}

# Function to check feature list completion
check_feature_list() {
  local file=".spec/feature_list.json"
  if [ ! -f "$file" ]; then
    return 1  # File doesn't exist, not relevant
  fi

  local total=$(jq '. | length' "$file")
  local passing=$(jq '[.[] | select(.passes == true)] | length' "$file")
  local remaining=$((total - passing))

  if [ "$remaining" -gt 0 ]; then
    echo "{
      \"decision\": \"block\",
      \"reason\": \"Implementation is incomplete: $passing/$total features complete. $remaining features remaining.\",
      \"systemMessage\": \"The implementation command has not finished. There are still $remaining features with 'passes': false in .spec/feature_list.json. Please continue the implementation loop by spawning the next coding-agent to implement the remaining features.\"
    }" >&2
    exit 2
  fi

  return 0
}

# Function to check audit list completion
check_audit_list() {
  local file=".spec/audit_list.json"
  if [ ! -f "$file" ]; then
    return 1  # File doesn't exist, not relevant
  fi

  local max_depth=$(jq -r '.max_depth // 2' "$file")
  local pending=$(jq "[.items[] | select(.depth <= $max_depth and (.status == \"pending\" or .status == \"in_progress\"))] | length" "$file")

  if [ "$pending" -gt 0 ]; then
    local total=$(jq "[.items[] | select(.depth <= $max_depth)] | length" "$file")
    local done=$((total - pending))
    echo "{
      \"decision\": \"block\",
      \"reason\": \"Audit is incomplete: $done/$total pages audited. $pending pages remaining.\",
      \"systemMessage\": \"The audit command has not finished. There are still $pending pages pending audit. Please continue the audit loop by spawning the next audit-subagent for the pending items.\"
    }" >&2
    exit 2
  fi

  return 0
}

# Check tracking file based on active command
case "$active_command" in
  explore)
    # Only check explore list for /explore command
    if check_explore_list; then
      :
    fi
    ;;
  implement)
    # Only check feature list for /implement command
    if check_feature_list; then
      :
    fi
    ;;
  audit)
    # Only check audit list for /audit command
    if check_audit_list; then
      :
    fi
    ;;
esac

# If we got here, either no tracking file exists or all tasks are complete
echo '{"decision": "approve"}'
exit 0
