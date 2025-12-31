#!/usr/bin/env python3
"""
Progress tracking script for autonomous coding projects.

Checks .spec/feature_list.json and displays progress summary.
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
        print("Run /start-project first to initialize the project")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {spec_path}: {e}")
        sys.exit(1)


def calculate_progress(features):
    """Calculate progress statistics."""
    total = len(features)
    passing = sum(1 for f in features if f.get('passes', False))
    remaining = total - passing
    percentage = (passing / total * 100) if total > 0 else 0

    # Count by category
    functional_total = sum(1 for f in features if f.get('category') == 'functional')
    functional_passing = sum(1 for f in features if f.get('category') == 'functional' and f.get('passes', False))

    style_total = sum(1 for f in features if f.get('category') == 'style')
    style_passing = sum(1 for f in features if f.get('category') == 'style' and f.get('passes', False))

    return {
        'total': total,
        'passing': passing,
        'remaining': remaining,
        'percentage': percentage,
        'functional': {'total': functional_total, 'passing': functional_passing},
        'style': {'total': style_total, 'passing': style_passing}
    }


def display_progress(progress):
    """Display progress summary."""
    print("\n=== Development Progress ===\n")
    print(f"Total Features: {progress['total']}")
    print(f"✓ Completed: {progress['passing']} ({progress['percentage']:.0f}%)")
    print(f"○ Remaining: {progress['remaining']} ({100 - progress['percentage']:.0f}%)\n")

    print("Category Breakdown:")
    func_pct = (progress['functional']['passing'] / progress['functional']['total'] * 100) if progress['functional']['total'] > 0 else 0
    print(f"  Functional: {progress['functional']['passing']}/{progress['functional']['total']} ({func_pct:.0f}%)")

    style_pct = (progress['style']['passing'] / progress['style']['total'] * 100) if progress['style']['total'] > 0 else 0
    print(f"  Style: {progress['style']['passing']}/{progress['style']['total']} ({style_pct:.0f}%)")


def find_next_feature(features):
    """Find the next feature to implement (first non-passing)."""
    for feature in features:
        if not feature.get('passes', False):
            return feature
    return None


def display_next_feature(feature):
    """Display the next feature to implement."""
    if feature:
        print(f"\nNext Feature:")
        print(f"  ID: {feature['id']}")
        print(f"  Category: {feature['category']}")
        print(f"  Description: {feature['description']}")


def main():
    """Main entry point."""
    # Load feature list
    features = load_feature_list()

    # Calculate progress
    progress = calculate_progress(features)

    # Display progress
    display_progress(progress)

    # Show next feature
    next_feature = find_next_feature(features)
    display_next_feature(next_feature)

    # Check if complete
    if progress['remaining'] == 0:
        print("\n🎉 Project complete! All features verified.")
    elif progress['passing'] == 0:
        print("\nUse /continue to start implementing features")
    else:
        print("\nUse /continue to continue development")


if __name__ == "__main__":
    main()
