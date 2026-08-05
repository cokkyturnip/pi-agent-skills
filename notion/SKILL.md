---
name: notion
description: Use when the user wants to create, append, or update Notion pages. Handles both MCP OAuth (primary) and REST API fallback with Python for cases where browser-based OAuth fails.
---

# Notion Skill

## Pendekatan

Skill ini punya **dua jalur** akses ke Notion:

| Jalur | Tools | Kapan Dipakai |
|-------|-------|---------------|
| **MCP OAuth** | `notion_mcp_connect`, `notion_mcp_status`, `notion_mcp_disconnect` + MCP tools (notion-search, notion-fetch, dll) | **Primary** — ketika OAuth via browser berfungsi |
| **Python REST API** | `create_notion_page.py` + `NOTION_TOKEN` env | **Fallback** — ketika OAuth gagal, browser tidak terbuka, atau butuh create page baru dari markdown |

---

## Jalur 1: MCP OAuth (Primary)

### Workflow Appending Content

1. **Call notion_search** to find the target page
2. **Fetch existing content** with notion_fetch
3. **Show preview** to the user:
   - Block count
   - First few lines of content
   - Whether page contains images/attachments
4. **Ask for user confirmation** before appending
5. **Merge** existing content with new content
6. **Update** the page with notion_update

### Workflow Membuat Page Baru

Gunakan MCP tools yang tersedia setelah koneksi:
```
notion_mcp_connect  →  notion-search  →  notion-create-pages
```

### Guidelines

- ALWAYS show a preview before updating
- `notion_update` REPLACES all content (full overwrite)
- Warn user if page contains images/attachments
- If unsure, ask for confirmation before proceeding

### Troubleshooting OAuth

Jika `notion_mcp_connect` gagal karena browser tidak membuka tab:
- Coba set Arc/Chrome sebagai default browser
- Atau gunakan **Jalur 2: Python REST API** sebagai fallback

---

## Jalur 2: Python REST API (Fallback)

Gunakan ketika OAuth MCP gagal (browser tidak terbuka, timeout, error koneksi). Jalur ini menggunakan **Notion Internal Integration Token** langsung ke REST API.

### Prerequisites

1. **Buat Integration Token** di https://www.notion.so/my-integrations
   - Klik **+ New Integration**
   - Beri nama (misal: "Pi Agent")
   - Pilih workspace → Submit → copy `secret_xxx`
2. **Invite integration** ke halaman/database target di Notion:
   - Buka halaman/database → **Share** → cari nama integration → **Invite**
3. **Set environment variable**:
   ```bash
   # CMD
   set NOTION_TOKEN=secret_xxx
   # PowerShell
   $env:NOTION_TOKEN="secret_xxx"
   ```

### Script: `create_notion_page.py`

Script ada di direktori yang sama dengan SKILL.md ini.

```
notion/
  SKILL.md                 ← file ini
  create_notion_page.py    ← Python script
```

### Cara Pakai

```bash
python3 /path/to/notion/create_notion_page.py
```

Script akan:
1. Membaca `NOTION_TOKEN` dari environment
2. Membaca file `.md` di direktori yang sama (ubah `md_path` dalam script jika berbeda)
3. Parse markdown ke Notion blocks (heading, paragraph, list, table, code, quote)
4. Menampilkan daftar halaman/database di workspace
5. Membuat page baru di halaman induk/database yang dipilih

### Konversi Markdown → Notion Blocks

| Markdown | Notion Block |
|----------|-------------|
| `# Heading 1` | `heading_1` |
| `## Heading 2` | `heading_2` |
| `### Heading 3` | `heading_3` |
| Paragraph | `paragraph` |
| `- item` | `bulleted_list_item` |
| `1. item` | `numbered_list_item` |
| `` `code` `` | `code` |
| `> quote` | `quote` |
| `\| col1 \| col2 \|` | `table` (dengan `table_width` + semua row sbg children) |
| `---` | `divider` |

**Table handling:** Markdown table akan dikonversi menjadi satu block `table` dengan:
- `table_width` = jumlah kolom
- `has_column_header` = True
- Semua rows (header + data) sebagai `children` di dalam table block
- Row separator `|---|---|` otomatis dideteksi dan dilewati

### Notion API Block Limits

| Aspek | Batas |
|-------|-------|
| Blocks per create request | ~100 blocks |
| Text per rich_text element | 2000 karakter |
| Table columns | 100 kolom max |

### Common Pitfalls

| Error | Kemungkinan | Solusi |
|-------|-------------|--------|
| `401 Unauthorized` | Token invalid/expired | Buat ulang di Notion Integrations |
| `403 Forbidden` | Integration belum di-invite | Share page → Invite integration |
| `409 Conflict` | Page dengan judul sama | Ganti judul |
| `validation_error` | Block terlalu besar | Kurangi konten per block |

---

## Penting

- Jalur **MCP OAuth** adalah primary — coba dulu selalu
- **Python REST API** adalah fallback untuk situasi OAuth bermasalah
- Untuk **membaca/meng-update halaman eksisting**, prioritaskan MCP tools
- Untuk **membuat page baru dari markdown besar**, Python script lebih stabil
- Integration token harus di-invite ke setiap halaman/database yang akan diakses
