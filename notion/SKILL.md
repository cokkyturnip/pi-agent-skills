---
name: notion
description: This skill appends content to Notion pages safely, always previewing proposed changes before updating.
---
# Notion Skill

## When to Use This Skill

- When the user wants to add summaries or new content to an existing Notion page
- When the page contains complex content (images, special formatting, etc.)
- When there is a risk of accidentally deleting/overwriting old content

## Workflow

1. **Call notion_search** to find the target page (or use a known page ID directly)
2. **Fetch existing content** with notion_fetch to review the current page contents
3. **Show a preview** to the user:
   - Block count
   - The first few lines of content
   - Whether the page contains images/attachments
4. **Ask for user confirmation** before appending
5. **Get content to append** (from a .md file or user input)
6. **Merge** existing content with new content
7. **Update** the page with notion_update

## Guidelines

- ALWAYS show a preview before updating
- Warn the user if the page contains images or attachments (may require special handling)
- If unsure about the update, ask the user for confirmation before proceeding
- If the page contains many images, suggest manual appending via the Notion UI instead

## Example Prompt

User: "Append this YouTube summary to the Notion page ‘Jumbo’"

Action:
1. Search/fetch the ‘Jumbo’ page
2. Show: "This page has X blocks and Y images. A new summary will be appended at the end. Continue?"
3. Wait for confirmation
4. Append the content only after user confirmation

## Important Notes

- `notion_update` REPLACES all content on the page (full overwrite)
- Images hosted on S3 with signed URLs will expire and cannot be restored if deleted
- For important pages, always recommend backing up or reviewing page history before making updates
