---
name: pi-router-pintar
description: >
  Use when working on the pi-router-pintar project — an auto-model router
  extension for the pi coding agent (fork of beettlle/pi-smart-router,
  published on npm as pi-router-pintar). Triggers for: troubleshooting
  routing behavior or model selection, improving the router, reviewing
  features, or updating the router knowledge base (GitHub issues + Notion).
  Loads accumulated findings from GitHub issues first so sessions never
  start from zero.
---

# pi-router-pintar — Project Skill & Knowledge Base

Skill internal untuk proyek auto-model router pi-router-pintar milik Cokky.

## Identitas Proyek

- **Repo lokal:** `/Users/cokkyturnip/Documents/Github Repo/pi-smart-router` (branch `main`, origin = `cokkyturnip/pi-router-pintar`)
- **npm:** `pi-router-pintar` — selalu pakai nama ini. `pi-smart-router` = upstream (beettlle).
- **Gallery:** https://pi.dev/packages/pi-router-pintar (otomatis terindeks dari npm keyword `pi-package`)
- **Versi saat penulisan:** 0.17.2 · `minPiVersion` 0.80.8

## Knowledge Base — baca DULU sebelum bekerja

1. **GitHub issues = single source of truth:** https://github.com/cokkyturnip/pi-router-pintar/issues — baca SEMUA issue (judul + body + komentar) sebelum troubleshoot. GitHub yang manage penomoran & riwayat; jangan buat file duplikat temuan di repo.
2. **Notion:** halaman "pi-router-pintar — Engineering Notes" (https://app.notion.com/p/3bfc2fd56084813994e1eb292b1a614b) — ringkasan lintas mesin; bukan sumber utama.

## Protokol Wajib (Pre-Flight)

1. **SEBELUM troubleshoot/improve:** baca seluruh issue di GitHub (open & closed). Jangan mulai dari nol.
2. **Diagnosa empiris dulu, baru baca source:** minta user menjalankan `/smart-router status`, `/smart-router history [N]`, `/smart-router stats [N]`. `stage` + `reason_code` + `tier` + `selected_model_id` adalah bukti keputusan.
3. **Baca file sesuai Peta Observasi di bawah** — jangan baca ulang seluruh repo.
4. **Temuan baru / bantahan → WAJIB dicatat sebagai issue baru atau komentar di issue yang ada** (title deskriptif, tanpa prefix penomoran manual). Lalu sinkronkan ringkasan ke Notion.

## Peta Observasi — fitur/area → file yang dibaca

| Jika perlu review / troubleshoot | Baca file ini |
|---|---|
| Model mapping, tier, cost per model | `src/config/pi-model-mapper.ts` · `src/config/defaults.ts` |
| Turn classification (main_loop / planning / tool_result) | `.pi/extensions/smart-router/routing-context.ts` |
| Routing pipeline & urutan stage | `src/domain/pipeline/router-pipeline.ts` |
| Identity routing, multi-account, duplicate model id | `src/domain/types/entities.ts` · `src/domain/matching/hydra-matcher.ts` · `src/domain/scoring/multi-objective.ts` |
| Pricing: warning catalog, price cascade, Pi vs LiteLLM | `src/infrastructure/pricing/pricing-monitor.ts` · `src/infrastructure/pricing/price-broker.ts` · `src/infrastructure/pricing/litellm-fetch.ts` · `.pi/extensions/smart-router/pricing-lifecycle.ts` · `src/domain/routing/expected-cost.ts` · `src/domain/routing/complexity-scorer.ts` · `src/domain/pinning/sub-route-policy.ts` |
| Delegation & streaming (ke model terpilih) | `.pi/extensions/smart-router/delegation-runtime.ts` · `stream-delegation.ts` · `route-and-delegate.ts` · `delegate-stream.ts` |
| Fleet bootstrap & scoped models | `.pi/extensions/smart-router/fleet-bootstrap.ts` · `pi-model-scope.ts` |
| Commands & telemetry (/smart-router *) | `.pi/extensions/smart-router/commands.ts` · `routing-outcomes.ts` · `session-lifecycle.ts` |
| Extension startup / setup / lifecycle | `.pi/extensions/smart-router/extension-setup.ts` · `index.ts` |

## Fakta Terverifikasi (ringkas — detail di GitHub issues)

- **Turn classification** default = `main_loop`; `planning` hanya jika prompt user mengandung "plan"/"architect"/"design" (match substring → false positive: "airplane", "implant"); `tool_result` jika pesan terakhir toolResult.
- **Model families dengan rule eksplisit**: claude, gpt, gemini, composer, cursor, deepseek, qwen, grok, kimi, mistral, glm (commit `37c35a4`). Model tanpa rule → `UNKNOWN_DEFAULTS` = economical-cloud, capability 0.6/0.65/0.6, cost dari pi registry bila ada.
- **Identity routing = model_id only** — tanpa dimensi provider/account; duplicate id antar provider tidak di-dedup; `weightedSelect` hanya saat failover (task-observer #23).
- **Pricing dua sumber** (Pi registry vs LiteLLM) bisa beda ~10% untuk model sama; unit USD/1M sudah diverifikasi benar (issue #1).
- **Gallery pi.dev:** indeks otomatis dari npm keyword `pi-package`; downloads rendah → tidak muncul di listing utama, tapi halaman detail ada. Tidak ada registrasi manual.

## Konvensi Kecil

- **Bahasa:** semua konten GitHub (issue, komentar, PR, README) ditulis dalam **bahasa Inggris** — repo ini publik. Notion & catatan internal boleh Bahasa Indonesia.
- Jangan pernah menulis `pi install npm:pi-smart-router` — package install adalah `pi-router-pintar` (README sempat menunjuk upstream; perbaiki saat menyentuh README).
- Repo path mengandung spasi ("Github Repo") — selalu quote/escape path.
- Fork menambahkan: loop-escalation via `is_error`/`status`, `gpt-5.5+` → frontier-cloud, self-delegation guard, Plan B complexity re-scoring (v0.17.0), real context-window sync (v0.17.1).
- Issue title: deskriptif tanpa prefix penomoran (mis. "DeepSeek economical bias: ..."), karena GitHub manage nomor issue otomatis.
