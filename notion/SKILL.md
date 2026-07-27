---
name: notion
description: Skill ini digunakan untuk menambahkan (append) konten ke halaman Notion dengan aman, dengan menampilkan preview terlebih dahulu sebelum melakukan perubahan.
---
# Notion Skill

## Kapan Menggunakan Skill Ini

- Ketika user ingin menambahkan ringkasan atau konten baru ke halaman Notion yang sudah ada
- Ketika halaman sudah memiliki konten kompleks (gambar, format khusus, dll)
- Ketika user takut konten lama akan terhapus

## Workflow

1. **Panggil notion_search** untuk cari page yang dimaksud (atau langsung jika sudah tahu page ID)
2. **Fetch konten existing** dengan notion_fetch untuk melihat apa yang ada di halaman tersebut
3. **Tampilkan preview** ke user:
   - Jumlah block yang ada
   - Beberapa baris pertama konten
   - Apakah ada gambar/attachment
4. **Minta konfirmasi** dari user sebelum append
5. **Ambil konten yang mau di-appen** ( bisa dari file .md atau input user langsung )
6. **Gabungkan** konten existing + konten baru
7. **Update** halaman dengan notion_update

## Guidelines

- SELALU tampilkan preview sebelum update
- Peringatkan jika halaman punya gambar/attachment yang mungkin perlu perhatian extra
- Jika ragu, tanya user lagi sebelum proceeding
- Jika halaman punya banyak gambar, sarankan untuk append manual via UI Notion saja

## Contoh Prompt

User: "Append ringkasan YouTube ini ke halaman Notion Jumbo"

Aksi:
1. Search/fetch halaman Jumbo
2. Tampilkan: "Halaman ini punya X block, termasuk Y gambar. Akan ditambahkan ringkasan baru di bawah. Lanjutkan?"
3. Tunggu konfirmasi
4. Baru append

## Catatan Penting

- notion_update akan MENGGANTIKAN semua konten (replace all)
- Gambar yang di-host di S3 dengan signed URL akan expired dan tidak bisa di-restore jika dihapus
- Jika halaman penting, selalu sarankan backup atau cek page history sebelum update