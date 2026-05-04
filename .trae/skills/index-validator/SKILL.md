---
name: "index-validator"
description: "Checks if all Markdown files are properly referenced in index.md and vice versa. Invoke when maintaining the deceased celebrities project to ensure data integrity."
---

# Index Validator

This skill validates the consistency between `index.md` and individual celebrity Markdown files in the project.

## Functionality

1. **Check Missing References**: Identifies Markdown files in the directory that are NOT listed in `index.md`
2. **Check Broken Links**: Identifies links in `index.md` that point to non-existent Markdown files
3. **Generate Report**: Provides a clear summary of inconsistencies found

## Usage

To use this validator, run the following command in the project directory:

```bash
python -c "
import re
import os

# Get all .md files (excluding index.md and spec.md)
md_files = [f for f in os.listdir('.') if f.endswith('.md') and f not in ['index.md', 'spec.md']]

# Read index.md content
with open('index.md', 'r', encoding='utf-8') as f:
    index_content = f.read()

# Extract linked files from index.md
linked_files = re.findall(r'\[.*?\]\((.*?\.md)\)', index_content)

# Find files not in index.md
not_in_index = [f for f in md_files if f not in linked_files]

# Find broken links
broken_links = [link for link in linked_files if not os.path.exists(link)]

print('=== Index Validation Report ===')
print()

if not_in_index:
    print('❌ Files NOT listed in index.md:')
    for f in sorted(not_in_index):
        print(f'  - {f}')
else:
    print('✅ All Markdown files are listed in index.md')

print()

if broken_links:
    print('❌ Broken links in index.md (files do not exist):')
    for link in sorted(broken_links):
        print(f'  - {link}')
else:
    print('✅ All links in index.md point to existing files')

print()
print(f'Total Markdown files: {len(md_files)}')
print(f'Total links in index.md: {len(linked_files)}')
"
```

## When to Invoke

- After adding new celebrity Markdown files
- Before committing changes to ensure data integrity
- Periodically to maintain project consistency
- When troubleshooting missing or broken references

## Example Output

```
=== Index Validation Report ===

✅ All Markdown files are listed in index.md

✅ All links in index.md point to existing files

Total Markdown files: 25
Total links in index.md: 25
```

## Requirements

- Python 3.x
- Run from the project root directory where `index.md` is located
