# Panduan Pengguna — Kantor 3D

Kantor virtual 3D untuk perusahaanmu: ruangan per divisi, agen 3D yang
beraktivitas dan saling mengantar data, chat bubble, orbit/pan/zoom,
tombol lompat ruangan, mode POV, dan musik latar. Satu file HTML,
tanpa install apa pun — cukup browser modern + internet (Three.js
dimuat dari CDN saat pertama dibuka).

> **Isi template ini contoh generik** (perusahaan "Contoh", 3 divisi
> contoh, 6 agen contoh). Bukan data perusahaan nyata — ganti dengan
> punyamu lewat panduan di bawah.

## 1. Baru install? Inisiasi oleh Muse

Setelah install (`python3 install.py` selesai, atau file HTML sudah
di tangan), langkah tercepat adalah minta Muse menginisiasi setup.
Copy-paste prompt ini ke Muse kamu:

> "Aku baru install Kantor 3D dari https://github.com/beytgoal/kantor-3d-template
> (file: kantor-3d-contoh.html — 3 divisi, 6 agen, 2 agen cadangan, 3 lantai, tema malam).
> Tolong inisiasi setup kantor 3D-ku: tanyakan nama perusahaanku, industri
> tiap divisi, jumlah agen per divisi, workflow tiap divisi, siapa agen
> utamanya, dan tema visual yang kumau — lalu ubah blok CONFIG di file itu
> (tanpa mengubah kode 3D-nya) dan bagikan hasilnya sebagai artefak web statis."

Muse akan mengarahkanmu membangun, satu per satu:

1. **Nama perusahaan** — nama, domain, dan nama tampilannya.
2. **Framework perusahaan** — struktur organisasinya: divisi apa saja,
   di lantai berapa, dan divisi mana yang jadi sumber data (pipeline).
3. **Industri tiap divisi** — bidang yang digerakkan tiap divisi
   (mis. Teknologi, Pemasaran Digital, Keuangan). Industri dipakai teks
   status dan kartu ruangan.
4. **Jumlah agen per divisi** — berapa orang di tiap divisi, siapa
   kepalanya, dan siapa agen utamanya (COO/CEO/Direktur) yang
   mengoordinasi siklus kerja antar divisi.
5. **Workflow per divisi** — langkah kerja tiap divisi (mis. "Siapkan
   data harian, Cek progres tim, Laporan ke direktur"). Workflow dipakai
   teks status agen saat siklus kerja berjalan — jadi chat selingan
   (bubble) agen mencerminkan industri dan datanya.
6. **Tema visual** — malam, siang, atau senja; plus warna/kamera/cahaya
   bila mau disesuaikan (lihat README bagian "Mengubah tampilan visual").

Hasilnya: file HTML yang sudah dikustom + artefak web yang bisa dibuka
dan dibagikan — visualisasi agen-agenmu berjalan realtime mengikuti
struktur dan framework perusahaanmu.

## 2. Belum punya divisi / agen?

Tidak masalah. Template tetap jalan dengan **0 divisi dan 0 agen**:
gedung hanya berisi lounge (ruang bersama) di lantai 1. Tambah nanti
dengan salah satu cara ini:

- **Tanya Muse** — pakai prompt di bagian 1; Muse yang mengisi
  divisinya untukmu.
- **Jalankan ulang installer** — `python3 install.py`, jawab berapa
  divisi dan berapa agen per divisi (boleh 0 bila belum tahu).
- **Edit CONFIG manual** — buka file HTML, cari blok
  `★ KANTOR 3D — CONFIG ★`, tambah entri ke `divisions: []` dan
  `agents: []` (contoh format ada di file; lihat bagian 3–5 di bawah).

## 3. Mengatur nama perusahaan

Di blok CONFIG:

```js
company: "Contoh",          // nama perusahaan (judul halaman + kartu)
companyUpper: "CONTOH",     // nama tampil di HUD kiri atas
domain: "contoh.id",        // domain (dipakai URL layar tiap divisi)
appUrl: "app.contoh.id",    // URL aplikasi (tampil di kartu)
```

## 4. Mengatur pipeline divisi

Divisi diatur di `divisions: [...]`. **Urutan entri = urutan ruangan
kiri → kanan** di tiap lantai — susun bebas sesuai pipeline-mu.
Tambah/hapus/susun ulang entri, ruangan dan tombol lompat ikut berubah
otomatis.

```js
{
  short: "Operasional",            // nama pendek (tombol lompat, bubble)
  full: "Divisi Operasional",      // nama lengkap (kartu ruangan)
  room: "Ruang Operasional",       // nama ruangan (klik karpet)
  floor: 1,                        // lantai ruangan (1-index)
  color: 0xf7b955, css: "#f7b955", cssDark: "#b57a2e",
  url: "operasional.contoh.id",    // URL layar di ruangan
  screen: "Operasional",           // teks layar
  board: "Papan Operasional",      // nama papan tulis
  boardDesc: "Papan pantau operasional: tugas harian dan progres tim.",
  roomDesc: "Ruang kerja tim operasional.",
  industry: "Jasa & Operasional",  // industri divisi
  feature: "server",               // fitur ruangan (lihat bawah)
  workflow: ["Siapkan data harian", "Cek progres tim", "Laporan ke direktur"]
}
```

- **`pipeline.source`** (di CONFIG, default `0`) — index divisi sumber
  data. Agen kurir membawa data dari divisi sumber ke divisi lain
  dalam siklus kerja. Ganti angkanya untuk memindah sumber pipeline.
- **`feature`** — fitur khusus ruangan: `"server"` (rak server),
  `"books"` (rak buku + poster), `"studio"` (sudut studio ring-light),
  atau `"none"` (tanpa fitur). Bila dikosongkan, bawaan menurut urutan:
  divisi ke-1 server, ke-2 studio, ke-3 buku.
- **`workflow`** — langkah kerja divisi. Lead divisi menampilkan
  langkah ini sebagai status saat siklus kerja berjalan. Boleh
  dikosongkan — status jadi teks generik memakai nama divisi.
- **`industry`** — bidang industri divisi; tampil di kartu dan dipakai
  konteks teks status.

## 5. Jumlah agen per divisi & agen utama

Agen diatur di `agents: [...]`. Tiap agen duduk di ruangan divisinya
(`division`: index divisi, `0` = divisi pertama) di kursi yang dipilih
(`desk`: nomor kursi, `0` = kursi pertama) — atau kosongkan `desk`
untuk kursi kosong berikutnya.

```js
{ id: "direktur", name: "Ayu", role: "COO", division: 0, desk: 1 },
{ id: "kepala-operasional", name: "Budi", role: "Kepala Divisi Operasional", division: 0, desk: 0 },
{ id: "staff-pemasaran", name: "Citra", role: "Staff Pemasaran", division: 1, desk: 1 },
```

- **Agen utama** — agen ber-role `"COO"`, `"CEO"`, atau `"Direktur"`
  adalah agen utama yang mengoordinasi siklus kerja antar divisi.
  Pastikan tepat satu agen memakai role ini.
- **Kepala divisi** — role mengandung kata "Kepala" atau "Lead"
  (mis. "Kepala Divisi Pemasaran") dikenali sebagai lead divisi.
- **Kurir** — agen lain di divisi sumber (selain agen utama dan lead)
  otomatis jadi kurir yang mengantar data ke divisi lain.
- Bila `division` dikosongkan, agen dibagi rata ke semua divisi.

## 5b. Agen cadangan, pose duduk, dan kerja paralel

- **Agen cadangan** (`CONFIG.reserves`, bawaan 2; `0` = tanpa) —
  agen standby fleksibel yang duduk di **Area Standby** (lounge
  lantai 1). Mereka otomatis berjalan membantu divisi secara
  bergiliran: datang ke ruangan divisi, **duduk di meja cadangan**
  (satu meja ekstra yang selalu disediakan di tiap ruangan divisi di
  luar jumlah agen tetap), bekerja di sana beberapa saat, lalu
  kembali standby atau berpindah ke divisi lain.
- **Pose duduk** — semua agen duduk di kursi meja kerja dengan kaki
  dua segmen berengsel lutut (paha horizontal, betis vertikal,
  pinggul di atas dudukan kursi) dan lengan ke keyboard dengan gerak
  mengetik halus; mereka berdiri dan berjalan hanya saat berpindah
  tempat.
- **Kerja paralel** — agen tetap semua divisi aktif bersamaan di
  penempatannya: staf di luar siklus kurir berputar status mengikuti
  langkah `workflow` divisi masing-masing, jadi bubble status tiap
  divisi bergerak sendiri-sendiri secara simultan.

## 6. Wajah agen (face mesh)

Setiap agen punya **face mesh 3D bawaan** — mata, alis, hidung, dan
mulut dari geometri — jadi wajah selalu ada walau tanpa foto.
Gaya rambut dan warna kulit diatur per agen lewat `AGENT_STYLE`
(di bawah CONFIG, per `id`) atau langsung di entri agen
(`hair`, `hairStyle: "short" | "long"`, `skin`, `skirt: true`).

Mau pakai foto sendiri? Tambah field `face` di entri agen:

```js
{ id: "direktur", name: "Ayu", role: "COO", division: 0,
  face: "https://contoh.id/foto-ayu.jpg" }   // URL atau data URI
```

Foto tampil sebagai patch di wajah 3D dan di kartu detail agen.
Tanpa `face`, yang tampil face mesh bawaan.

## 7. Mengubah tampilan visual

`visual.theme`: `"malam"` (bawaan), `"siang"`, atau `"senja"`.
Field lain di `visual` menimpa tema — langit (`sky`), kamera
(`camera`), palet material (`palette`), cahaya (`lights`), dan tema
panel UI (`ui`). Detail lengkap: README bagian
"Mengubah tampilan visual".

## 8. Mengubah musik latar

Musik bawaan: **"Chill Lofi" oleh ZephiraMusic** (lisensi Pixabay —
gratis, boleh dipakai komersial, tanpa atribusi wajib). Diatur di
`CONFIG.music`:

```js
music: {
  src: "https://cdn.pixabay.com/.../audio_a5f2abd4d3.mp3?...",
  title: "Chill Lofi — ZephiraMusic (Pixabay)",
  credit: "Musik: 'Chill Lofi' oleh ZephiraMusic, lisensi Pixabay"
}
```

Ganti `src` dengan URL MP3 no-copyright lain (Pixabay, Kevin MacLeod,
dan sejenisnya — perhatikan syarat atribusi masing-masing, dan isi
`credit` sesuai lisensinya), atau kosongkan `src` (`""`) untuk memakai
synth lo-fi generatif bawaan. Bila trek tidak bisa dimuat (mis.
offline), synth dipakai otomatis sebagai fallback.

Di HP, musik selalu mulai dari ketukanmu: tombol **Musik kantor**
sengaja besar dan jelas, dan konteks audio dibuka/di-unlock tepat di
dalam handler kliknya (sesuai kebijakan autoplay browser) — jadi
sekali ketuk, musik langsung berbunyi dari speaker HP.

## 9. Membuka & membagikan kantor

- Buka file HTML di browser modern (Chrome/Firefox/Safari/Edge).
  Tidak perlu server — tapi butuh internet saat pertama dibuka
  (Three.js dari CDN).
- Untuk dibagikan: kirim file-nya, atau minta Muse menjadikannya
  artefak web (lihat prompt di bagian 1).

## 10. Gedung & kontrol tampilan

- **Bentuk gedung** — gabungan persegi + silinder: badan kotak
  menyatu dengan menara silinder di sisi timur, tanpa tiang/kolom/
  pilar. Tiap lantai, satu ruangan divisi menempati menara (divisi
  bertanda `tower: true`, atau divisi terakhir di lantai itu);
  lounge selalu di badan kotak lantai 1. Dua tangga tidak sejajar:
  Tangga A di badan kotak (naik ke timur) dan Tangga B di menara
  (naik ke utara, lantai 2 ke atas).
- **Tombol "Sembunyikan Bubble & Ruangan"** — satu tombol master di
  kiri atas: sekali klik menyembunyikan SEMUA bubble agen DAN semua
  tombol ruangan sekaligus (visualisasi bersih); klik lagi
  ("Tampilkan Bubble & Ruangan") mengembalikan keduanya. Tidak ada
  tombol per-agen.
