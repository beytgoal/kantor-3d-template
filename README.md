# Kantor 3D — Template

Kantor virtual 3D dua lantai bergaya sinematik: ruangan per divisi, agen
3D yang beraktivitas, chat bubble, orbit/pan/zoom, tombol lompat ruangan,
mode POV, dan musik latar. Dibangun dengan Three.js.

**Desain visual dikunci** — yang bisa kamu sesuaikan hanya identitas
perusahaan: nama, divisi, warna divisi, dan agen. Tampilannya tetap
sama persis seperti demo.

## Install sekali perintah

Lihat **[INSTALL.md](INSTALL.md)** — satu prompt copy-paste untuk Muse,
atau `python3 install.py` untuk install interaktif.

## Cara pakai (manual, 2 menit)

1. Buka `index.html` dengan text editor.
2. Cari blok `★ KANTOR 3D — CONFIG ★` di bagian atas `<script>`.
3. Ganti nilainya dengan identitas perusahaanmu:
   - `company`, `companyUpper`, `domain`, `appUrl`
   - `divisions[]`: `short`, `full`, `room`, `floor`, `color`/`css`/`cssDark`,
     `url`, `board`, `boardDesc`, `roomDesc`
   - `agents[]`: `name`, `role`
4. Simpan, lalu buka `index.html` di browser. Selesai.

Tidak perlu install apa pun — cukup browser modern. Three.js dimuat
dari CDN (butuh internet saat dibuka pertama kali).

## Struktur

| File         | Keterangan                                              |
|--------------|---------------------------------------------------------|
| `index.html` | Satu file mandiri: desain 3D + blok CONFIG di bagian atas |
| `README.md`  | File ini                                                |

## Catatan

- Jumlah divisi bawaan: 3 (2 di lantai 2, 1 di lantai 1). Menambah divisi
  baru butuh penyesuaian layout di kode — desainnya tidak otomatis.
- Jumlah agen bawaan: 6. Nama dan peran bebas diganti di CONFIG.
- Warna divisi: `color` (hex number, mis. `0xf7b955`) untuk objek 3D,
  `css`/`cssDark` (string, mis. `"#f7b955"`) untuk UI teks.

## Lisensi

Bebas dipakai dan dimodifikasi untuk keperluan pribadi maupun komersial.
Atribusi dihargai tapi tidak diwajibkan.
