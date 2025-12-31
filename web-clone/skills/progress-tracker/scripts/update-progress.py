#!/usr/bin/env python3
"""
Progress update script for autonomous coding projects.

Safely updates the "passes" field in .spec/feature_list.json.
"""

import json
import sys
from pathlib import Path


def load_feature_list(spec_path=".spec/feature_list.json"):
    """Load feature list from JSON file."""
    try:
        with open(spec_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {spec_path} not found")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {spec_path}: {e}")
        sys.exit(1)


def save_feature_list(features, spec_path=".spec/feature_list.json"):
    """Save feature list to JSON file."""
    with open(spec_path, 'w') as f:
        json.dump(features, f, indent=2)


def update_feature_status(features, feature_id, passes):
    """Update the passes field for a specific feature."""
    for feature in features:
        if feature['id'] == feature_id:
            feature['passes'] = passes
            return feature
    print(f"Error: Feature with id {feature_id} not found")
    sys.exit(1)


def main():
    """Main entry point."""
    if len(sys.argv) != 3:
        print("Usage: update-progress.py <feature_id> <true|false>")
        print("Example: update-progress.py 1 true")
        sys.exit(1)

    feature_id = int(sys.argv[1])
    passes = sys.argv[2].lower() == 'true'

    # Load feature list
    features = load_feature_list()

    # Update feature
    feature = update_feature_status(features, feature_id, passes)

    # Save feature list
    save_feature_list(features)

    status = "passing" if passes else "not passing"
    print(f"✓ Updated feature #{feature_id} ({feature['description']}) to {status}")


if __name__ == "__main__":
    main()
