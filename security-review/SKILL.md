---
name: security-review
description: Security review for generated code. Three layers — pattern warnings, LLM diff review, and cross-file data flow. Use when implementing features involving authentication, authorization, user input handling, database operations, file uploads, API endpoints, or sensitive data processing.
---

# Security Review

Security review untuk semua kode yang dihasilkan. Tiga layer:

1. **Pattern warnings** — instant inline checks saat menulis kode untuk pola berbahaya (unsafe deserialization, hardcoded secrets, XSS, dll.)
2. **LLM diff review** — setelah selesai menulis kode, review seluruh diff dengan security lens sebelum dikirim ke user
3. **Cross-file data flow** — telusuri aliran data input user melintasi file untuk mendeteksi kerentanan multi-file (IDOR, auth bypass, SSRF)

<HARD-GATE>
JANGAN kirim kode yang menyentuh autentikasi, otorisasi, input user, file upload, API endpoints, atau database tanpa menjalankan ketiga layer security review di atas. Ini MUTLAK.
</HARD-GATE>

## Layer 1 — Pattern Warnings (Saat Menulis)

Periksa setiap blok kode yang ditulis untuk pola berbahaya berikut. Jika ketemu, hentikan dan perbaiki sebelum lanjut:

| Pola | Tindakan |
|------|----------|
| `pickle.load` tanpa kontrol sumber data | BLOCKED |
| `torch.load(weights_only=False)` | BLOCKED — pakai `weights_only=True` |
| `yaml.load` tanpa `SafeLoader` | BLOCKED — pakai `yaml.safe_load` |
| `eval()` / `exec()` dengan input user | BLOCKED |
| `innerHTML` / `dangerouslySetInnerHTML` dengan konten user | BLOCKED — pakai `textContent` atau DOMPurify |
| API key, token, password hardcoded | BLOCKED — pakai env vars |
| SQL concat dengan input user (`f"SELECT {x}"`) | BLOCKED — pakai parameterized query |
| `subprocess` / `os.system` dengan argumen user | BLOCKED — validasi ketat |

## Layer 2 — LLM Diff Review (Setelah Selesai)

Setelah selesai menulis kode untuk suatu fitur, lakukan review menyeluruh:

1. Baca `SECURITY_RULES.md` untuk rules lengkap
2. Review setiap file yang dimodifikasi — cari injection, XSS, hardcoded secrets, path traversal
3. Verifikasi autentikasi — setiap endpoint punya guard?
4. Verifikasi otorisasi — user hanya bisa akses resource miliknya? (cegah IDOR)
5. Cek input validation — tiap input user tervalidasi di boundary API?
6. Cek secrets — tidak ada credentials di kode/komentar/log?
7. Lapor temuan — jika ada BLOCKED, perbaiki dulu. Jika WARN, tulis penjelasan kenapa aman.
8. Baru deliver ke user setelah semua bersih.

## Layer 3 — Cross-File Data Flow

Untuk fitur yang kompleks (multi-file, melibatkan auth/user input):

1. Identifikasi entry point (endpoint API, handler, webhook)
2. Trace aliran data dari entry point ke database/file system/response
3. Di setiap titik, cek:
   - Apakah autentikasi sudah diverifikasi?
   - Apakah otorisasi sudah diverifikasi (user punya akses ke resource ini)?
   - Apakah input sudah divalidasi (tipe, panjang, format)?
   - Apakah output sudah di-escape untuk konteksnya (HTML, JSON, SQL)?
4. Catat kelemahan yang ditemukan dan perbaiki

## Checklist — Harus Diikuti Urut

```markdown
- [ ] Layer 1: pattern scan selesai, tidak ada BLOCKED
- [ ] Layer 2: diff review selesai, semua temuan diatasi
- [ ] Layer 3: data flow trace selesai (jika kompleks)
- [ ] SECURITY_RULES.md sudah dirujuk
- [ ] Semua BLOCKED diperbaiki, semua WARN didokumentasikan
- [ ] Kode siap dideliver
```

## Red Flags — Berhenti dan Perbaiki

Jika menemukan salah satu dari ini, STOP dan perbaiki sebelum lanjut:

- Hardcoded credentials di kode
- Raw SQL concat dengan input user
- Endpoint API tanpa autentikasi
- IDOR — user A bisa akses data user B
- `innerHTML` dengan konten user tanpa sanitasi
- `pickle` / `yaml.load` dari sumber tidak tepercaya
- File path dari user tanpa normalisasi
- Stack trace atau debug info bocor ke response