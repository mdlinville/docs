#!/usr/bin/env python3
"""
Convert W&B SDK CHANGELOG.md to Hugo-compatible release notes with combined minor versions.

This script parses the SDK's CHANGELOG.md file and generates combined
Hugo markdown files for each minor version (e.g., 0.21.md contains 0.21.0, 0.21.1, etc.),
with various transformations to make the content more suitable for documentation.

Usage:
    python sdk-changelog-to-hugo-combined.py [--changelog PATH] [--output DIR] [--version VERSION]

Args:
    --changelog: Path to CHANGELOG.md (default: ../wandb/CHANGELOG.md)
    --output: Output directory (default: ./content/en/ref/release-notes/sdk)
    --version: Specific version to process (e.g., 0.21.1)

Examples:
    # Process a specific version
    python sdk-changelog-to-hugo-combined.py --version 0.21.1
"""

import os
import re
import argparse
from datetime import datetime
from pathlib import Path


# Common conventional commit prefixes to remove
COMMIT_PREFIXES = [
    r'^feat\([^)]+\):\s*',
    r'^fix\([^)]+\):\s*',
    r'^docs\([^)]+\):\s*',
    r'^style\([^)]+\):\s*',
    r'^refactor\([^)]+\):\s*',
    r'^perf\([^)]+\):\s*',
    r'^test\([^)]+\):\s*',
    r'^build\([^)]+\):\s*',
    r'^ci\([^)]+\):\s*',
    r'^chore\([^)]+\):\s*',
    r'^revert\([^)]+\):\s*',
    # Without scope
    r'^feat:\s*',
    r'^fix:\s*',
    r'^docs:\s*',
    r'^style:\s*',
    r'^refactor:\s*',
    r'^perf:\s*',
    r'^test:\s*',
    r'^build:\s*',
    r'^ci:\s*',
    r'^chore:\s*',
    r'^revert:\s*',
]


def remove_emojis(text):
    """
    Remove emojis from text.

    Args:
        text (str): The text to clean.

    Returns:
        str: Text without emojis.
    """
    try:
        import emoji
        return emoji.replace_emoji(text, replace='')
    except ImportError:
        # If emoji library isn't installed, return text as-is
        print("Warning: emoji library not installed. Emojis will not be removed.")
        return text


def parse_changelog(filepath):
    """
    Parse the CHANGELOG.md file and extract releases.

    Args:
        filepath (str): Path to the CHANGELOG.md file.

    Returns:
        list: List of release dictionaries.
    """
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Split by release headers (## [version] - date)
    release_pattern = r'^## \[([^\]]+)\] - (.+?)$'
    
    releases = []
    current_release = None
    current_content = []
    
    for line in content.split('\n'):
        match = re.match(release_pattern, line)
        if match:
            # Save previous release if exists
            if current_release:
                current_release['content'] = '\n'.join(current_content).strip()
                releases.append(current_release)
            
            # Start new release
            version = match.group(1)
            date_str = match.group(2)
            
            # Parse date
            try:
                date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                formatted_date = date_obj.strftime('%Y-%m-%d')
                description = date_obj.strftime('%B %d, %Y')
            except ValueError:
                formatted_date = date_str
                description = date_str
            
            current_release = {
                'version': version,
                'title': f'[{version}] - {date_str}',
                'date': formatted_date,
                'description': description,
                'content': ''
            }
            current_content = []
        elif current_release:
            current_content.append(line)
    
    # Save last release
    if current_release:
        current_release['content'] = '\n'.join(current_content).strip()
        releases.append(current_release)
    
    return releases


def transform_content(content, is_patch=False):
    """
    Transform the changelog content to be more suitable for documentation.

    Args:
        content (str): The raw changelog content.
        is_patch (bool): Whether this is a patch release (affects heading levels).

    Returns:
        str: The transformed content.
    """
    lines = content.split('\n')
    transformed_lines = []
    in_contributors_section = False
    
    for line in lines:
        # Remove emojis from the line
        line = remove_emojis(line)
        
        # Skip empty lines at the start
        if not transformed_lines and not line.strip():
            continue
        
        # Check if we're entering the Contributors section
        if line.strip().startswith('### Contributors') or line.strip().startswith('## Contributors'):
            in_contributors_section = True
            continue
        
        # Skip everything in the Contributors section
        if in_contributors_section:
            # Check if we're starting a new section (which would end Contributors)
            if line.strip().startswith('###') or line.strip().startswith('##'):
                in_contributors_section = False
                # Process this line normally (it's a new section header)
            else:
                continue  # Skip contributor lines
        
        # Transform list items
        if line.startswith('- '):
            # Check if this is a docs(sdk) item - skip it entirely
            if re.search(r'docs\(sdk\)', line, re.IGNORECASE):
                continue
            
            # Extract the main content before the PR link
            # Handle both formats: "(@user in URL)" and "by @user in URL"
            # Also handle when period comes after the PR info
            match = re.match(r'^- (.+?)(\s+(?:\(@[^)]+\s+in\s+https://[^)]+\)|by\s+@[^)]+\s+in\s+https://[^)]+\)))?\.?\s*$', line)
            if match:
                main_content = match.group(1)
                pr_info = match.group(2) or ''
                
                # Remove conventional commit prefixes
                for prefix in COMMIT_PREFIXES:
                    main_content = re.sub(prefix, '', main_content, flags=re.IGNORECASE)
                
                # Clean up the main content
                # Ensure it ends with a period
                if main_content and not main_content.endswith(('.', '!', '?')):
                    main_content += '.'
                
                # Fix whitespace issues
                main_content = re.sub(r'\s+', ' ', main_content).strip()
                
                # Create the transformed line
                if pr_info:
                    # Move PR info to HTML comment
                    pr_comment = f"<!-- {pr_info.strip()} -->"
                    transformed_line = f"- {main_content} {pr_comment}"
                else:
                    transformed_line = f"- {main_content}"
                
                transformed_lines.append(transformed_line)
            else:
                # Keep the line as-is if it doesn't match our pattern
                transformed_lines.append(line)
        elif line.startswith('#'):
            # Adjust heading levels
            if is_patch:
                # For patches, use H4 for sections (### becomes ####)
                if line.startswith('### '):
                    transformed_lines.append(line.replace('### ', '#### ', 1))
                elif line.startswith('#### '):
                    transformed_lines.append(line.replace('#### ', '##### ', 1))
                elif line.startswith('##### '):
                    transformed_lines.append(line.replace('##### ', '###### ', 1))
                else:
                    transformed_lines.append(line)
            else:
                # For main releases, reduce by one level (### becomes ##)
                if line.startswith('### '):
                    transformed_lines.append(line.replace('### ', '## ', 1))
                elif line.startswith('#### '):
                    transformed_lines.append(line.replace('#### ', '### ', 1))
                elif line.startswith('##### '):
                    transformed_lines.append(line.replace('##### ', '#### ', 1))
                elif line.startswith('###### '):
                    transformed_lines.append(line.replace('###### ', '##### ', 1))
                else:
                    transformed_lines.append(line)
        else:
            # Keep other lines as-is (but with emojis removed)
            transformed_lines.append(line)
    
    # Join lines and clean up trailing whitespace
    result = '\n'.join(transformed_lines)
    result = '\n'.join(line.rstrip() for line in result.split('\n'))
    
    return result


def get_minor_version(version):
    """
    Extract the minor version from a full version string.
    
    Args:
        version (str): Full version string (e.g., "0.21.1").
    
    Returns:
        str: Minor version (e.g., "0.21").
    """
    parts = version.split('.')
    if len(parts) >= 2:
        return f"{parts[0]}.{parts[1]}"
    return version


def is_patch_release(version):
    """
    Check if a version is a patch release (not .0).
    
    Args:
        version (str): Version string (e.g., "0.21.1").
    
    Returns:
        bool: True if patch release, False if .0 release.
    """
    parts = version.split('.')
    if len(parts) >= 3:
        return parts[2] != '0'
    return False


def format_patch_content(release):
    """
    Format a patch release for inclusion in the Patches section.
    
    Args:
        release (dict): Release information.
    
    Returns:
        str: Formatted patch content.
    """
    version = release['version']
    description = release['description']
    
    # Transform content with patch-specific heading levels
    transformed_content = transform_content(release['content'], is_patch=True)
    
    # Build the patch section
    lines = [
        f"### v{version}",
        f"**{description}**",
        "",
        '{{% alert color="info" %}}View the [v' + version + ' changelog](https://github.com/wandb/wandb/releases/tag/v' + version + ') on GitHub.{{% /alert %}}',
        "",
        transformed_content
    ]
    
    return '\n'.join(lines)


def update_or_create_combined_file(release, output_dir):
    """
    Update or create a combined minor version file.
    
    Args:
        release (dict): Release information.
        output_dir (str): Output directory path.
    """
    version = release['version']
    minor_version = get_minor_version(version)
    is_patch = is_patch_release(version)
    
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Generate filename for minor version
    filename = f"{minor_version}.md"
    filepath = os.path.join(output_dir, filename)
    
    if is_patch:
        # For patches, we need to update an existing file
        if not os.path.exists(filepath):
            print(f"⚠️  Warning: Base release file {filepath} doesn't exist for patch {version}")
            print(f"   Creating it anyway with patch content only...")
            
            # Create a minimal file with just the patch
            alert_text = '{{% alert color="info" %}}View the [v' + minor_version + '.0 changelog](https://github.com/wandb/wandb/releases/tag/v' + minor_version + '.0) on GitHub.{{% /alert %}}'
            content = f"""---
title: "{minor_version}.x"
date: {release['date']}
description: "Unknown base release date"
---

{alert_text}

## Patches

{format_patch_content(release)}"""
            with open(filepath, 'w') as f:
                f.write(content)
            print(f"✓ Created: {filepath} (patch only)")
        else:
            # Read existing file
            with open(filepath, 'r') as f:
                existing_content = f.read()
            
            # Update the date in frontmatter (to the patch date for sorting)
            existing_content = re.sub(
                r'^date: \d{4}-\d{2}-\d{2}',
                f'date: {release["date"]}',
                existing_content,
                flags=re.MULTILINE
            )
            
            # Check if Patches section exists
            if '## Patches' not in existing_content:
                # Add Patches section
                existing_content = existing_content.rstrip() + '\n\n## Patches\n\n' + format_patch_content(release)
            else:
                # Append to existing Patches section
                existing_content = existing_content.rstrip() + '\n\n' + format_patch_content(release)
            
            # Ensure content ends with a newline
            if not existing_content.endswith('\n'):
                existing_content += '\n'
            
            # Write updated content
            with open(filepath, 'w') as f:
                f.write(existing_content)
            print(f"✓ Updated: {filepath} (added v{version})")
    else:
        # For .0 releases, create a new file
        transformed_content = transform_content(release['content'], is_patch=False)
        
        # Build the Hugo frontmatter and content
        alert_text = '{{% alert color="info" %}}View the [v' + version + ' changelog](https://github.com/wandb/wandb/releases/tag/v' + version + ') on GitHub.{{% /alert %}}'
        content = f"""---
title: "{minor_version}.x"
date: {release['date']}
description: "{release['description']}"
---

{alert_text}

{transformed_content}
"""
        
        # Write file
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"✓ Created: {filepath}")


def main():
    """Main function to process changelog and generate release notes."""
    parser = argparse.ArgumentParser(description='Convert SDK CHANGELOG to Hugo release notes (combined minor versions)')
    parser.add_argument('--changelog', 
                       default='/Users/matt.linville/wandb/CHANGELOG.md',
                       help='Path to CHANGELOG.md')
    parser.add_argument('--output', 
                       default='/Users/matt.linville/docs/content/en/ref/release-notes/sdk',
                       help='Output directory for release notes')
    parser.add_argument('--version',
                       help='Specific version to process (e.g., 0.21.1)')
    
    args = parser.parse_args()
    
    # Check if changelog exists
    if not os.path.exists(args.changelog):
        print(f"Error: Changelog not found at {args.changelog}")
        return 1
    
    print(f"📖 Reading changelog from: {args.changelog}")
    print(f"📁 Output directory: {args.output}")
    
    # Parse changelog
    releases = parse_changelog(args.changelog)
    print(f"📊 Found {len(releases)} releases")
    
    # Filter for specific version if requested
    if args.version:
        # Normalize version (remove 'v' prefix if present)
        target_version = args.version.lstrip('v')
        print(f"🔍 Looking for version: {target_version}")
        releases = [r for r in releases if r['version'] == target_version]
        if not releases:
            print(f"❌ Error: Version {target_version} not found in changelog")
            return 1
        print(f"🎯 Processing specific version: v{target_version}")
    
    # Process each release
    for i, release in enumerate(releases, 1):
        print(f"\n[{i}/{len(releases)}] Processing {release['title']} ({release['date']})")
        update_or_create_combined_file(release, args.output)
    
    print(f"\n✅ Successfully processed {len(releases)} release(s)!")
    print(f"📍 Location: {args.output}")
    
    return 0


if __name__ == '__main__':
    exit(main())
