---
name: markitdown
description: Use when needing to read, extract, or analyze the contents of a non-plain-text file — PDF, DOCX, PPTX, XLSX/XLS, EPUB, Outlook MSG, HTML, CSV, JSON, XML, Jupyter notebook, images, audio, YouTube URLs, or ZIP archives — or when a document is too large to `read` directly.
---

# MarkItDown — Documents → Markdown

## 1. Definisi

[markitdown](https://github.com/microsoft/markitdown) (Microsoft, MIT) mengubah
dokumen menjadi Markdown yang ramah LLM: heading, list, tabel, dan link
dipertahankan. Tujuannya dikonsumsi pipeline teks, bukan konversi
high-fidelity untuk manusia — tabel pada PDF kompleks bisa keluar kasar.

Pakai markitdown ketika:
- `read` tidak bisa dipakai karena filenya biner (PDF/DOCX/XLSX), atau
- dokumen terlalu besar untuk dibaca utuh, atau
- butuh struktur (heading/tabel) yang hilang bila diekstrak mentah.

Tidak perlu untuk file `.md`/`.txt` (baca langsung) atau audio/video yang
menuntut transkripsi berkualitas.

Properties yang selalu berlaku, terlepas dari platform:
- Konverter mengembalikan `DocumentConverterResult` dengan `.markdown`
  (string) dan `.title` (opsional).
- Setiap invocation mencetak warning `pydub` soal ffmpeg ke stderr — buang
  stderr agar output tidak terkontaminasi.
- Beberapa kegagalan tidak muncul sebagai error (lihat §4 dan §5).

## 2. Tool terkait

| Tool | Fungsi | Kapan dibutuhkan |
|---|---|---|
| `markitdown` (CLI) | konversi file/URL → markdown | pemakaian sehari-hari |
| `markitdown` (Python lib) | batch, stream, plugin, kontrol I/O | pipeline & aplikasi |
| `markitdown-mcp` | MCP server, mengekspos konversi ke agen lain | integrasi via MCP |
| `markitdown-ocr` | OCR gambar di dalam PDF/DOCX/PPTX/XLSX via LLM vision | PDF hasil scan, dokumen bergambar |
| plugin pihak ketiga | converter format tambahan | cari tag `#markitdown-plugin` |
| Azure Document Intelligence | layout/OCR cloud (`--use-docintel`) | tabel kompleks, scan massal |
| Azure Content Understanding | dokumen, gambar, audio, **video** (`--use-cu`) | video, ekstraksi field terstruktur |
| `ffmpeg` + `ffprobe` | dependency eksternal (bukan paket Python) | audio mp3/m4a/mp4 |

Deteksi tipe file ditangani `magika`; ekstensi atau MIME hint tetap dibutuhkan
saat input berupa stream.

## 3. Install / reinstall

Butuh Python ≥3.10 dan <3.15. Pilih satu manajer, jangan campur:

```bash
pip install "markitdown[all]"              # dalam venv
uv tool install "markitdown[all]"          # binary terisolasi
pipx install "markitdown[all]"             # alternatif binary terisolasi
```

Reinstall bersih atau upgrade:

```bash
uv tool install --force "markitdown[all]"
uv tool upgrade markitdown
pip install --upgrade --force-reinstall "markitdown[all]"
```

Verifikasi:

```bash
markitdown --version 2>/dev/null
markitdown --list-plugins 2>/dev/null
```

`[all]` bisa diganti subset sesuai kebutuhan: `[pdf]`, `[docx]`, `[pptx]`,
`[xlsx]`, `[xls]`, `[outlook]`, `[audio-transcription]`,
`[youtube-transcription]`, `[az-doc-intel]`, `[az-content-understanding]`.
Memasang subset memangkas dependensi berat (`pandas`, `pdfplumber`,
`python-pptx`).

Menambah OCR (butuh client vision OpenAI-compatible):

```bash
uv tool install --force --with markitdown-ocr --with openai markitdown
pip install markitdown-ocr openai
```

Jika memakai instalasi terisolasi (`uv tool`/`pipx`), API Python harus
dijalankan dengan interpreter milik env tersebut, bukan `python3` sistem:

```bash
uv tool run --with markitdown[all] python -c "import markitdown"
```

Audio butuh `ffmpeg`/`ffprobe` dari OS, di luar markitdown:

```bash
brew install ffmpeg        # macOS
apt install ffmpeg         # Debian/Ubuntu
```

## 4. Cara pemakaian

**CLI, selalu buang stderr:**

```bash
markitdown file.pdf -o file.md 2>/dev/null
markitdown "https://www.youtube.com/watch?v=..." -o transcript.md 2>/dev/null
```

**Peringatan penggunaan — periksa sendiri, CLI tidak akan mengingatkan:**

1. **Output kosong tetap exit 0.** Untuk gambar tanpa backend vision dan untuk
   stdin tanpa hint, markitdown selesai tanpa error tapi menghasilkan 0 byte.
   Selalu cek ukuran sebelum membaca hasilnya:

   ```bash
   markitdown gambar.jpg -o out.md 2>/dev/null; wc -c out.md   # 0 → gagal
   ```

2. **PDF hasil scan** menghasilkan output hampir kosong: 0 byte dengan `-o`,
   atau 1 byte bila ke stdout (newline). Angka sekecil itu artinya dokumen
   tidak punya text layer dan perlu jalur OCR, bukan dianggap sukses.

3. **stdin tidak ditebak tipenya.** Tanpa hint hasilnya kosong tanpa error.
   Selalu sertakan format:

   ```bash
   cat file.pdf | markitdown -x pdf > out.md 2>/dev/null   # atau -m application/pdf
   ```

4. **ZIP dikonversi seluruh entrinya.** Satu arsip bisa membengkak jadi ratusan
   KB markdown. Daftar isinya dulu, atau konversi per file:

   ```bash
   unzip -l arsip.zip | head -30
   ```

5. **Audio/video gagal di tengah jalan** bila `ffprobe` tidak ada
   (`FileNotFoundError`), setelah proses sempat berjalan. Cek dulu:
   `which ffprobe`.

6. **Output besar jangan dibaca utuh.** Konversi ke file, petakan heading-nya,
   baru baca bagian yang perlu:

   ```bash
   markitdown big.pdf -o big.md 2>/dev/null
   wc -c big.md; grep -n "^#" big.md | head -40
   ```

**Python API:**

```python
from markitdown import MarkItDown

md = MarkItDown(enable_plugins=False)
print(md.convert_local("report.pdf").markdown)
```

Method, dari paling sempit ke paling permisif: `convert_local` (path lokal),
`convert_stream` (file-like), `convert_response` (response `requests`),
`convert_url`/`convert_uri` (network), `convert` (semua).

**Keamanan:** markitdown melakukan I/O dengan privilege proses — `convert()`
membaca path apa pun dan mengambil URI apa pun. Untuk input tak terpercaya
pakai `convert_stream()` atau `convert_local()` setelah memvalidasi path, dan
blokir skema URI serta alamat private/loopback/link-local/metadata.

**Cek sebelum memakai hasilnya:**
- [ ] ukuran output wajar? (0 byte = gagal senyap; 0–1 byte pada PDF = hasil scan tanpa text layer)
- [ ] stderr dibuang sehingga tidak bocor ke log/JSON?
- [ ] isi ZIP didaftar dulu, tidak dikonversi borongan?
- [ ] audio: `ffprobe` tersedia?

## 5. Tipe file yang didukung & dependency-nya

Base dependency (selalu ikut, tanpa extras): `beautifulsoup4`, `requests`,
`certifi`, `markdownify`, `magika`, `charset-normalizer`, `defusedxml`.

| Tipe | Dependency | Catatan perilaku |
|---|---|---|
| PDF dengan text layer | `[pdf]`: `pdfminer.six`, `pdfplumber` | heading dan tabel ikut |
| PDF hasil scan | OCR: `markitdown-ocr` + LLM vision, atau Azure | tanpa OCR output 0–1 byte |
| Word `.docx` | `[docx]`: `mammoth`, `lxml` | komentar dibuang |
| PowerPoint `.pptx` | `[pptx]`: `python-pptx` | per slide jadi satu bagian |
| Excel `.xlsx` | `[xlsx]`: `pandas`, `openpyxl` | per sheet `## SheetN`, semua sheet |
| Excel `.xls` | `[xls]`: `pandas`, `xlrd` | sama seperti xlsx |
| Outlook `.msg` | `[outlook]`: `olefile` | header + body |
| HTML | `beautifulsoup4` + `markdownify` | konten utama, link dipertahankan |
| EPUB | stdlib (`zipfile` + HTML) | per bab |
| CSV / JSON / XML / RSS | stdlib + `pandas` | CSV jadi tabel, JSON/XML jadi code block |
| Jupyter `.ipynb` | stdlib `json` | sel digabung |
| ZIP | stdlib `zipfile` | **mengonversi setiap entri** — arsip kecil bisa jadi ratusan KB markdown |
| Gambar JPG/PNG | EXIF saja; isi gambar butuh OCR/LLM vision | tanpa backend vision: **0 byte, exit 0** |
| Audio `.wav` | `[audio-transcription]`: `pydub`, `SpeechRecognition` | transkrip dasar via Google Web Speech gratis |
| Audio `.mp3`/`.m4a`/video | + `ffmpeg`/`ffprobe` dari OS | tanpa ffmpeg: `FileNotFoundError: 'ffprobe'`, exit 1 |
| Video | hanya lewat Azure Content Understanding | converter lokal tidak mendukung |
| YouTube URL | `[youtube-transcription]`: `youtube-transcript-api` | butuh transkrip tersedia di YouTube |
| Biner / tak dikenal | — | `UnsupportedFormatException`, exit 1 |

Untuk satu gambar, membaca gambarnya langsung dengan model vision biasanya
lebih murah daripada menyiapkan pipeline OCR.
