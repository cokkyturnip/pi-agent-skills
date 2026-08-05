#!/usr/bin/env python3
"""
Create a Notion page with the proposal content from the markdown file.
Uses Notion REST API directly with an integration token.
"""

import os
import sys
import json
import re
import requests
from pathlib import Path

NOTION_API_BASE = "https://api.notion.com/v1"
NOTION_VERSION = "2022-06-28"

def get_token():
    """Get Notion integration token from environment variable."""
    token = os.environ.get("NOTION_TOKEN")
    if not token:
        print("ERROR: NOTION_TOKEN environment variable is not set.")
        print("Please set it with your Notion Internal Integration Token:")
        print("  export NOTION_TOKEN='secret_xxxxxxxxxxxx'")
        print("Or on Windows:")
        print("  set NOTION_TOKEN=secret_xxxxxxxxxxxx")
        sys.exit(1)
    return token

def get_headers(token):
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Notion-Version": NOTION_VERSION,
    }

def search_pages(token, query="", page_size=25):
    """Search for pages in the workspace."""
    url = f"{NOTION_API_BASE}/search"
    headers = get_headers(token)
    payload = {
        "query": query,
        "filter": {"property": "object", "value": "page"},
        "page_size": page_size,
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        print(f"ERROR searching pages: {response.status_code} - {response.text}")
        return []
    results = response.json().get("results", [])
    return results

def list_databases(token, page_size=25):
    """List databases in the workspace."""
    url = f"{NOTION_API_BASE}/databases"
    headers = get_headers(token)
    params = {"page_size": page_size}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        print(f"ERROR listing databases: {response.status_code} - {response.text}")
        return []
    return response.json().get("results", [])

def get_page_children(token, page_id, page_size=100):
    """Get children blocks of a page."""
    url = f"{NOTION_API_BASE}/blocks/{page_id}/children"
    headers = get_headers(token)
    params = {"page_size": page_size, "start_cursor": None}
    all_children = []
    while True:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            print(f"ERROR getting children: {response.status_code} - {response.text}")
            return []
        data = response.json()
        all_children.extend(data.get("results", []))
        if not data.get("has_more"):
            break
        params["start_cursor"] = data.get("next_cursor")
    return all_children

def create_page(token, parent_page_id, title, children_blocks):
    """Create a new Notion page under a parent page."""
    url = f"{NOTION_API_BASE}/pages"
    headers = get_headers(token)
    payload = {
        "parent": {"page_id": parent_page_id},
        "properties": {
            "title": [{"text": {"content": title}}]
        },
        "children": children_blocks,
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        print(f"ERROR creating page: {response.status_code} - {response.text}")
        return None
    return response.json()

def create_page_in_workspace(token, title, children_blocks):
    """Create a new Notion page at workspace root (requires integration to have workspace access)."""
    url = f"{NOTION_API_BASE}/pages"
    headers = get_headers(token)
    payload = {
        "parent": {"workspace": True},
        "properties": {
            "title": [{"text": {"content": title}}]
        },
        "children": children_blocks,
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        print(f"ERROR creating page at workspace root: {response.status_code} - {response.text}")
        return None
    return response.json()

def create_page_in_database(token, database_id, title, properties, children_blocks=None):
    """Create a new page (database row) in a database."""
    url = f"{NOTION_API_BASE}/pages"
    headers = get_headers(token)
    payload = {
        "parent": {"database_id": database_id},
        "properties": properties,
    }
    if children_blocks:
        payload["children"] = children_blocks
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        print(f"ERROR creating database page: {response.status_code} - {response.text}")
        return None
    return response.json()

def parse_markdown_to_blocks(markdown_text):
    """Convert markdown text to Notion API blocks."""
    blocks = []
    lines = markdown_text.split("\n")
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Skip empty lines
        if not stripped:
            i += 1
            continue

        # Headings
        if stripped.startswith("# "):
            blocks.append(make_heading(stripped[2:], 1))
            i += 1
        elif stripped.startswith("## "):
            blocks.append(make_heading(stripped[3:], 2))
            i += 1
        elif stripped.startswith("### "):
            blocks.append(make_heading(stripped[4:], 3))
            i += 1
        elif stripped.startswith("#### "):
            blocks.append(make_heading(stripped[5:], 4))
            i += 1

        # Code blocks
        elif stripped.startswith("```"):
            lang = stripped[3:].strip()
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            i += 1  # Skip closing ```
            blocks.append(make_code_block("\n".join(code_lines), lang))

        # Bullet list
        elif stripped.startswith("- ") or stripped.startswith("• "):
            items = []
            while i < len(lines) and (lines[i].strip().startswith("- ") or lines[i].strip().startswith("• ")):
                content = lines[i].strip()[2:].strip()
                items.append(content)
                i += 1
            blocks.append(make_bulleted_list(items))

        # Numbered list
        elif re.match(r'^\d+\.\s', stripped):
            items = []
            while i < len(lines) and re.match(r'^\d+\.\s', lines[i].strip()):
                content = re.sub(r'^\d+\.\s', '', lines[i].strip())
                items.append(content)
                i += 1
            blocks.append(make_numbered_list(items))

        # Table (simple | col1 | col2 | format)
        elif stripped.startswith("|") and i + 1 < len(lines) and set(lines[i+1].strip().replace("|", "").replace("-", "").replace(" ", "")) == set():
            table_lines = [stripped]
            i += 1
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_lines.append(lines[i].strip())
                i += 1
            blocks.extend(make_table(table_lines))

        # Horizontal rule
        elif stripped in ("---", "***", "___"):
            blocks.append(make_divider())
            i += 1

        # Blockquote
        elif stripped.startswith("> "):
            content = stripped[2:].strip()
            blocks.append(make_quote(content))
            i += 1

        # Toggle list (for collapsible sections)
        elif stripped.startswith("<details>"):
            # Find the closing </details>
            detail_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("</details>"):
                detail_lines.append(lines[i])
                i += 1
            i += 1  # Skip </details>
            blocks.append(make_toggle(stripped, "\n".join(detail_lines)))

        # Regular paragraph
        else:
            # Collect consecutive non-empty lines as a paragraph
            para_lines = []
            while i < len(lines) and lines[i].strip() and not is_block_start(lines[i].strip()):
                para_lines.append(lines[i].strip())
                i += 1
            if para_lines:
                blocks.append(make_paragraph(" ".join(para_lines)))

        # Limit blocks to avoid API issues (Notion has limits)
        if len(blocks) >= 95:  # Leave room for more
            blocks.append(make_callout("⚠️ Proposal content continues — truncated due to block limits. Full content available in the markdown file."))
            break

    return blocks

def is_block_start(line):
    """Check if a line starts a new block element."""
    return (
        line.startswith("#") or
        line.startswith("```") or
        line.startswith("- ") or
        line.startswith("• ") or
        bool(re.match(r'^\d+\.\s', line)) or
        line.startswith("|") or
        line in ("---", "***", "___") or
        line.startswith("> ") or
        line.startswith("<details>")
    )

def make_heading(text, level):
    return {
        "object": "block",
        "type": f"heading_{level}",
        f"heading_{level}": {
            "rich_text": [{"type": "text", "text": {"content": clean_text(text)}}]
        }
    }

def make_paragraph(text):
    # Handle bold, italic, strikethrough in text
    rich_text = parse_inline_formatting(text)
    return {
        "object": "block",
        "type": "paragraph",
        "paragraph": {"rich_text": rich_text}
    }

def make_code_block(code, language=""):
    # Map common languages
    lang_map = {
        "json": "json", "python": "python", "bash": "bash", "sh": "bash",
        "javascript": "javascript", "js": "javascript", "typescript": "typescript",
        "ts": "typescript", "yaml": "yaml", "yml": "yaml", "sql": "sql",
        "html": "html", "css": "css", "xml": "xml", "text": "", "": "",
    }
    lang = lang_map.get(language.lower(), language.lower() if language else "")
    return {
        "object": "block",
        "type": "code",
        "code": {
            "text": [{"type": "text", "text": {"content": code}}],
            "language": lang
        }
    }

def make_bulleted_list(items):
    blocks = []
    for item in items:
        blocks.append({
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": clean_text(item)}}]}
        })
    return blocks

def make_numbered_list(items):
    blocks = []
    for item in items:
        blocks.append({
            "object": "block",
            "type": "numbered_list_item",
            "numbered_list_item": {"rich_text": [{"type": "text", "text": {"content": clean_text(item)}}]}
        })
    return blocks

def make_table(table_lines):
    """Convert markdown table to a single Notion table block with all rows."""
    # Parse table
    rows = []
    for line in table_lines:
        cells = [cell.strip() for cell in line.split("|")[1:-1]]
        rows.append(cells)

    if len(rows) < 2:
        return [make_paragraph(" ".join(table_lines))]

    headers = rows[0]
    # Skip separator row (|---|) if present, otherwise use headers as data
    data_rows = rows[2:] if len(rows) > 2 and rows[1] and all(cell.replace("-", "").strip() == "" for cell in rows[1]) else rows[1:]
    num_cols = len(headers)

    # Helper: build a table_row block
    def make_row(values, is_header=False):
        cells = []
        for val in values:
            cells.append([{"type": "text", "text": {"content": clean_text(val)}}])
        # Pad to match column count
        while len(cells) < num_cols:
            cells.append([{"type": "text", "text": {"content": ""}}])
        return {
            "type": "table_row",
            "table_row": {"cells": cells}
        }

    # Build single table block with ALL rows as children
    children = []
    children.append(make_row(headers, is_header=True))
    for row in data_rows:
        children.append(make_row(row))

    return [{
        "object": "block",
        "type": "table",
        "table": {
            "table_width": num_cols,
            "has_column_header": True,
            "has_row_header": False,
            "children": children
        }
    }]

def make_divider():
    return {"object": "block", "type": "divider", "divider": {}}

def make_quote(text):
    return {
        "object": "block",
        "type": "quote",
        "quote": {"rich_text": [{"type": "text", "text": {"content": clean_text(text)}}]}
    }

def make_callout(text):
    return {
        "object": "block",
        "type": "callout",
        "callout": {
            "icon": {"emoji": "⚠️"},
            "rich_text": [{"type": "text", "text": {"content": clean_text(text)}}]
        }
    }

def make_toggle(summary, content):
    return {
        "object": "block",
        "type": "toggle",
        "toggle": {
            "rich_text": [{"type": "text", "text": {"content": clean_text(summary)}}],
            "children": [make_paragraph(content)]
        }
    }

def clean_text(text):
    """Clean text for Notion - remove markdown formatting characters."""
    # Remove markdown link syntax but keep the text
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    # Remove remaining markdown
    text = text.replace("**", "").replace("__", "").replace("`", "").replace("~", "")
    return text[:2000]  # Notion text limit

def parse_inline_formatting(text):
    """Parse inline markdown formatting into Notion rich text annotations."""
    # Simple implementation - just return plain text
    # Full implementation would handle bold, italic, strikethrough, links, code
    cleaned = clean_text(text)
    return [{"type": "text", "text": {"content": cleaned}}]

def main():
    token = get_token()
    print("✓ Token ditemukan")

    # Read the proposal markdown
    md_path = Path(__file__).parent / "proposal-new-mobile-banking-bsb.md"
    if not md_path.exists():
        print(f"ERROR: File not found: {md_path}")
        sys.exit(1)

    with open(md_path, "r", encoding="utf-8") as f:
        markdown_content = f.read()

    print(f"✓ Proposal markdown loaded ({len(markdown_content)} chars)")

    # Parse markdown to Notion blocks
    print("Parsing markdown to Notion blocks...")
    blocks = parse_markdown_to_blocks(markdown_content)
    print(f"✓ Generated {len(blocks)} blocks")

    # Search for pages to find a parent
    print("\nSearching workspace for existing pages...")
    pages = search_pages(token, "", 10)
    print(f"\nFound {len(pages)} pages in workspace:")
    for idx, page in enumerate(pages):
        title = ""
        props = page.get("properties", {})
        for key, val in props.items():
            if val.get("type") == "title":
                title = val.get("title", [{}])[0].get("text", {}).get("content", "") or page.get("url", "").split("/")[-1]
                break
        if not title:
            title = page.get("url", "").split("/")[-1]
        print(f"  [{idx}] {title[:60]}... (ID: {page['id'][:8]}...)")

    # Also list databases
    databases = list_databases(token, 10)
    if databases:
        print(f"\nFound {len(databases)} databases:")
        for idx, db in enumerate(databases):
            title = ""
            props = db.get("title", [])
            if props:
                title = props[0].get("text", {}).get("content", "")
            print(f"  [D{idx}] {title[:60]}... (ID: {db['id'][:8]}...)")

    print("\n--- Options ---")
    print("1. Create page at workspace root (may fail if integration lacks permission)")
    print("2. Create page under an existing page (specify page number)")
    print("3. Create page as a database entry (specify database number)")

    choice = input("\nChoose option (1/2/3): ").strip()

    page_result = None

    if choice == "1":
        print("Creating page at workspace root...")
        page_result = create_page_in_workspace(token, "Proposal: New Mobile Banking Bank Sumsel Babel", blocks)
    elif choice == "2":
        if not pages:
            print("No pages found!")
            sys.exit(1)
        idx = int(input("Enter page number: ").strip())
        parent_id = pages[idx]["id"]
        print(f"Creating page under '{pages[idx].get('url', '')}'...")
        page_result = create_page(token, parent_id, "Proposal: New Mobile Banking Bank Sumsel Babel", blocks)
    elif choice == "3":
        if not databases:
            print("No databases found!")
            sys.exit(1)
        idx = int(input("Enter database number: ").strip())
        db_id = databases[idx]["id"]
        print(f"Creating page in database '{databases[idx].get('title', [{}])[0].get('text', {}).get('content', '')}'...")
        # Create a simple title property
        props = {"Name": {"title": [{"text": {"content": "Proposal: New Mobile Banking Bank Sumsel Babel"}}]}}
        page_result = create_page_in_database(token, db_id, "Proposal: New Mobile Banking Bank Sumsel Babel", props, blocks)
    else:
        print("Invalid choice!")
        sys.exit(1)

    if page_result:
        print(f"\n✓ Page created successfully!")
        print(f"  URL: {page_result.get('url', 'N/A')}")
        print(f"  Page ID: {page_result.get('id', 'N/A')}")
    else:
        print("\n✗ Failed to create page")
        sys.exit(1)

if __name__ == "__main__":
    main()
