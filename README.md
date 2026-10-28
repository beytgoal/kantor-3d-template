# Kantor 3D — Template

Kantor virtual 3D bergaya sinematik: ruangan per divisi, agen
3D yang beraktivitas, chat bubble, orbit/pan/zoom, tombol lompat ruangan,
mode POV, dan musik latar. Dibangun dengan Three.js.

> **Baru pertama kali? Baca [PANDUAN.md](PANDUAN.md)** — panduan
> pasca-instalasi: inisiasi setup oleh Muse, tambah divisi/agen,
> atur pipeline dan workflow per divisi, jumlah agen per divisi,
> agen utama, industri, dan wajah agen.

Isi bawaan template ini **contoh generik** (perusahaan "Contoh",
3 divisi contoh, 6 agen contoh) — bukan data perusahaan nyata.
Ganti dengan punyamu lewat CONFIG, `install.py`, atau minta Muse
yang mengisinya (lihat PANDUAN.md).

**Visual fleksibel, bisa dikustom ulang** — tampilan tidak dikunci.
Warna langit, cahaya, palet material, kamera, dan tema panel UI
semuanya diatur lewat `CONFIG.visual`: pilih tema bawaan (`"malam"`,
`"siang"`, `"senja"`) atau timpa per field (mis. `sky`, `palette.wall`,
`lights.ambient`). Tema bisa diganti kapan saja tanpa menyentuh kode.

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
     `boardDesc`, `roomDesc`, plus `industry`, `feature`
     (`"server"`/`"books"`/`"studio"`/`"none"`), `workflow` (langkah
     kerja divisi)
   - `pipeline.source`: index divisi sumber data (default 0)
   - `music`: `src` (URL MP3 no-copyright), `title`, `credit` — kosongkan
     `src` untuk memakai synth lo-fi generatif bawaan
   - `agents[]`: `name`, `role`, plus opsional `id`, `division`
     (index atau nama pendek divisi tempat ia duduk), `desk`
     (nomor kursi), `color`/`colorCss`, `face` (foto, opsional — tanpa
     foto agen memakai face mesh 3D bawaan). Role `"COO"`, `"CEO"`, atau
     `"Direktur"` = agen utama pengoordinasi siklus kerja.
   - `visual`: tema & tampilan — lihat bagian "Mengubah tampilan
     visual" di bawah
4. Simpan, lalu buka `index.html` di browser. Selesai.

Tidak perlu install apa pun — cukup browser modern. Three.js dimuat
dari CDN (butuh internet saat dibuka pertama kali).

## Mengubah tampilan visual — tanpa edit kode

Di blok CONFIG, `visual.theme` memilih tema bawaan:

- `"malam"` (bawaan) — langit gelap, ruangan hangat menyala, seperti demo
- `"siang"` — langit biru, cahaya matahari, tanpa bintang
- `"senja"` — langit ungu gelap, cahaya oranye hangat

Field lain di `visual` menimpa tema yang dipilih, jadi tema bisa
dipakai apa adanya atau dijadikan titik awal:

```js
visual: {
  theme: "siang",
  sky: 0x0a1428,                    // langit biru gelap (timpa tema)
  camera: { fov: 52, position: [20, 16, 24] },
  palette: { wall: 0xf0e6d2, wood: 0x8a6a45 },
  ui: { amber: "#ff8c42" }          // warna aksen panel UI
}
```

Yang bisa diubah per field (warna boleh hex number `0xffffff`
atau string CSS `"#ffffff"`):

| Field | Isi |
|---|---|
| `sky`, `fogNear`, `fogFar` | Warna latar langit + jarak kabut |
| `camera.fov`, `camera.position`, `camera.target` | Sudut & posisi kamera awal |
| `exposure` | Eksposur cahaya keseluruhan |
| `ground` | Warna tanah di bawah gedung |
| `stars.color/size/opacity/count` | Bintang di langit |
| `lights.ambient`, `lights.hemisphere`, `lights.moon` | Cahaya sekeliling (warna + intensitas) |
| `lights.room`, `lights.stair` | Lampu ruangan & tangga (warna hangat, intensitas, jangkauan) |
| `palette.*` | Material: `slab`, `wood`, `wall`, `wallSide`, `dark`, `metal`, `white`, `glass`, `leaf`, `pot`, `deskTop`, `deskLeg`, `screen`, `panelLight` |
| `ui.ink`, `ui.inkDim`, `ui.panel`, `ui.panelLine`, `ui.amber` | Tema panel UI (teks, tombol, kartu) |

Ganti `theme` atau field lain, simpan, refresh — tampilan langsung
berubah. Tidak ada nilai visual yang terkunci di kode.

## Menambah divisi, agen, dan lantai — tanpa edit kode

- **Divisi baru:** tambah satu objek ke `divisions[]` (isi `short`,
  `full`, `room`, `floor`, `color`/`css`, `url`, `screen`, `board`).
  Ruangan baru muncul otomatis di lantai yang dipilih, dibagi rata
  dengan ruangan lain di lantai yang sama, lengkap dengan karpet,
  meja, papan tulis, tanaman, dan lampu. Urutan entri = urutan ruangan
  kiri → kanan; `pipeline.source` memilih divisi sumber data;
  `feature` memilih fitur ruangan; `workflow` mengisi teks status lead.
  Detail: [PANDUAN.md](PANDUAN.md) bagian 4.
- **Agen baru:** tambah satu objek ke `agents[]` (cukup `name` +
  `role`). Kursi dan warna dihitung otomatis: `division` menentukan
  ruangan tempat ia duduk (kosongkan = dibagi rata), `desk` memilih
  kursi tertentu, `color`/`colorCss` mengganti warna (default: warna
  divisinya). Wajah agen memakai face mesh 3D bawaan (mata, alis,
  hidung, mulut); tambah field `face` (URL/data URI foto) untuk memakai
  foto sendiri. Role `"COO"`, `"CEO"`, atau `"Direktur"` = agen utama.
  Detail: [PANDUAN.md](PANDUAN.md) bagian 5–6.
- **Lantai baru:** naikkan angka `floors` (dan/atau beri `floor: 3`
  ke sebuah divisi). Pelat lantai, tangga, dan tombol lompat lantai
  dibangun otomatis mengikuti jumlah lantai.

## Struktur

| File         | Keterangan                                              |
|--------------|---------------------------------------------------------|
| `index.html` | Satu file mandiri: desain 3D + blok CONFIG di bagian atas |
| `install.py` | Installer interaktif (jumlah divisi, agen per divisi, industri, workflow, tema visual, musik latar) |
| `PANDUAN.md` | Panduan pengguna pasca-instalasi (inisiasi oleh Muse, atur pipeline, workflow, wajah agen) |
| `LICENSE`    | Lisensi MIT — bebas dipakai, diubah, dan dibagikan      |
| `README.md`  | File ini                                                |

## Catatan

- Musik latar: trek no-copyright **"Chill Lofi" oleh ZephiraMusic**
  (lisensi Pixabay — gratis, boleh dipakai komersial, tanpa atribusi
  wajib), diputar dari `CONFIG.music.src` saat tombol Musik kantor /
  boombox diklik. Ganti `src` dengan URL MP3 no-copyright lain, atau
  kosongkan untuk memakai synth lo-fi generatif bawaan (tanpa file
  eksternal, tetap jalan offline; dipakai otomatis bila trek gagal
  dimuat).
- Jumlah bawaan: 3 divisi, 6 agen, 2 lantai — semuanya bisa diubah
  lewat CONFIG tanpa menyentuh kode lain.
- Warna divisi: `color` (hex number, mis. `0xf7b955`) untuk objek 3D,
  `css`/`cssDark` (string, mis. `"#f7b955"`) untuk UI teks.
- Gedung ini open-plan total (tanpa dinding penuh, sesuai desain
  aslinya); ruangan ditandai karpet, furnitur, dan pembatas rendah.
- Tangga selalu di belakang-kiri gedung; lantai atas punya bukaan
  tangga di posisi yang sama di tiap lantai.

## Lisensi

Proyek ini berlisensi **MIT** — lihat [LICENSE](LICENSE).
Bebas dipakai, diubah, dan dibagikan, termasuk untuk keperluan
komersial, selama pemberitahuan hak cipta dan lisensi tetap disertakan.
