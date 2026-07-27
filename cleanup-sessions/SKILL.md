---
name: cleanup-sessions
description: Membersihkan session pi yang sudah lama/tidak terpakai. Retain 20 sesi terbaru per project, maksimal 14 hari.
---

# Cleanup Sessions

## Ketika digunakan

- Manual: user minta bersihin session
- Otomatis: tiap startup pi, cek via `.last_session_cleanup`

## Steps

1. Jalankan `bash ~/.pi/agent/cleanup-sessions.sh`
2. Kalo ada output "Deleting: ...", kasih tau user berapa yang kehapus
3. Kalo skip (udah jalan hari ini), bilang aja "Session sudah bersih, terakhir dicek tadi"
