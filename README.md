# Kantor 3D — Template

Kantor virtual 3D bergaya sinematik: ruangan per divisi, agen
3D yang beraktivitas, chat bubble, orbit/pan/zoom, tombol lompat ruangan,
mode POV, dan musik latar. Dibangun dengan Three.js.

**Desain visual dikunci** — yang bisa kamu sesuaikan hanya identitas
perusahaan: nama, divisi, warna divisi, dan agen. Tampilannya tetap
sama persis seperti demo.

**Tanpa edit kode** — jumlah divisi, agen, dan lantai semuanya diatur
lewat blok CONFIG (atau lewat `install.py`). Tambah divisi, agen, atau
lantai tinggal tambah entri di CONFIG; ruangan, meja, kursi, tangga,
dan tombol lompat dibangun otomatis.

## Install sekali perintah

Lihat **[INSTALL.md](INSTALL.md)** — satu prompt copy-paste untuk Muse,
atau `python3 install.py` untuk install interaktif.

## Cara pakai (manual, 2 menit)

1. Buka `index.html` dengan text editor.
2. Cari blok `★ KANTOR 3D — CONFIG ★` di bagian atas `<script>`.
3. Ganti nilainya dengan identitas perusahaanmu:
   - `company`, `companyUpper`, `domain`, `appUrl`
   - `floors`: jumlah lantai gedung (default 2)
   - `divisions[]`: `short`, `full`, `room`, `floor` (1-index, lantai
     ruangan), `color`/`css`/`cssDark`, `url`, `screen`, `board`,
     `boardDesc`, `roomDesc`
   - `agents[]`: `name`, `role`, plus opsional `id`, `division`
     (index atau nama pendek divisi tempat ia duduk), `desk`
     (nomor kursi), `color`/`colorCss`
4. Simpan, lalu buka `index.html` di browser. Selesai.

Tidak perlu install apa pun — cukup browser modern. Three.js dimuat
dari CDN (butuh internet saat dibuka pertama kali).

## Menambah divisi, agen, dan lantai — tanpa edit kode

- **Divisi baru:** tambah satu objek ke `divisions[]` (isi `short`,
  `full`, `room`, `floor`, `color`/`css`, `url`, `screen`, `board`).
  Ruangan baru muncul otomatis di lantai yang dipilih, dibagi rata
  dengan ruangan lain di lantai yang sama, lengkap dengan karpet,
  meja, papan tulis, tanaman, dan lampu.
- **Agen baru:** tambah satu objek ke `agents[]` (cukup `name` +
  `role`). Kursi dan warna dihitung otomatis: `division` menentukan
  ruangan tempat ia duduk (kosongkan = dibagi rata), `desk` memilih
  kursi tertentu, `color`/`colorCss` mengganti warna (default: warna
  divisinya). Foto wajah agen bawaan tersimpan terpisah per `id` —
  agen baru tanpa `id` yang dikenal memakai tampilan default.
- **Lantai baru:** naikkan angka `floors` (dan/atau beri `floor: 3`
  ke sebuah divisi). Pelat lantai, tangga, dan tombol lompat lantai
  dibangun otomatis mengikuti jumlah lantai.

## Struktur

| File         | Keterangan                                              |
|--------------|---------------------------------------------------------|
| `index.html` | Satu file mandiri: desain 3D + blok CONFIG di bagian atas |
| `install.py` | Installer interaktif (jumlah divisi/agen/lantai bebas)  |
| `README.md`  | File ini                                                |

## Catatan

- Jumlah bawaan: 3 divisi, 6 agen, 2 lantai — semuanya bisa diubah
  lewat CONFIG tanpa menyentuh kode lain.
- Warna divisi: `color` (hex number, mis. `0xf7b955`) untuk objek 3D,
  `css`/`cssDark` (string, mis. `"#f7b955"`) untuk UI teks.
- Gedung ini open-plan total (tanpa dinding penuh, sesuai desain
  aslinya); ruangan ditandai karpet, furnitur, dan pembatas rendah.
- Tangga selalu di belakang-kiri gedung; lantai atas punya bukaan
  tangga di posisi yang sama di tiap lantai.

## Lisensi

Bebas dipakai dan dimodifikasi untuk keperluan pribadi maupun komersial.
Atribusi dihargai tapi tidak diwajibkan.
