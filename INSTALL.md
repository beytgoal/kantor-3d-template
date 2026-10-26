# Install Kantor 3D — Sekali Perintah

Copy-paste prompt ini ke Muse kamu:

> Install kantor 3D dari https://github.com/beytgoal/kantor-3d-template :
> clone repo-nya, jalankan `python3 install.py`, jawab pertanyaannya
> (nama perusahaan, jumlah divisi, agen, dan lantai — bebas ditentukan,
> contoh: "buatkan dengan 4 divisi, 8 agen, 3 lantai"; semua ada default
> 3 divisi, 6 agen, 2 lantai), lalu buatkan hasilnya sebagai artefak web
> statis dan bagikan link publiknya.

Muse akan otomatis: download template → generate file HTML yang sudah
dikustom → jadiin artefak → kasih link yang bisa dibuka & dibagikan.

Jumlah divisi, agen, dan lantai bebas ditentukan lewat prompt — Muse
yang menginstall cukup mengedit blok CONFIG saja, tanpa mengubah kode
3D-nya. Contoh lain: "buatkan dengan 2 divisi, 4 agen, 1 lantai" atau
"buatkan dengan 5 divisi, 10 agen, 3 lantai".

## Cara manual (tanpa Muse)

1. Download `index.html` dari repo.
2. Buka dengan text editor, cari blok `★ KANTOR 3D — CONFIG ★`.
3. Ganti nama perusahaan, divisi, warna, dan agen — tambah divisi,
   agen, atau lantai tinggal tambah entri di CONFIG (lihat README).
4. Simpan → buka di browser. Selesai.

Atau via script: `python3 install.py` (interaktif — tanya dulu berapa
divisi, agen, dan lantai, lalu loop menanyakan nama tiap divisi/agen)
atau dengan env var, contoh:
`COMPANY="Nusantara" DIV_COUNT=4 AGENT_COUNT=8 FLOORS=3 python3 install.py`
