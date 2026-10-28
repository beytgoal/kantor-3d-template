# Install Kantor 3D — Sekali Perintah

Copy-paste prompt ini ke Muse kamu:

> Install kantor 3D dari https://github.com/beytgoal/kantor-3d-template :
> clone repo-nya, jalankan `python3 install.py`, jawab pertanyaannya
> (nama perusahaan, jumlah divisi, jumlah agen per divisi, industri
> tiap divisi, workflow, dan lantai — bebas ditentukan, contoh:
> "buatkan dengan 4 divisi, 8 agen, 3 lantai"; semua ada default
> 3 divisi, 6 agen, 2 lantai — plus tema visual: malam, siang, atau
> senja), lalu buatkan hasilnya sebagai artefak web
> statis dan bagikan link publiknya.
>
> Setelah install, inisiasi setup lanjutannya oleh Muse (lihat
> PANDUAN.md di repo): Muse menanyakan nama perusahaan, industri tiap
> divisi, jumlah agen per divisi, workflow tiap divisi, siapa agen
> utamanya, dan tema visual — lalu mengubah blok CONFIG dan membagikan
> artefaknya.

Muse akan otomatis: download template → generate file HTML yang sudah
dikustom → jadiin artefak → kasih link yang bisa dibuka & dibagikan.

Jumlah divisi, agen per divisi, industri, workflow, dan lantai bebas
ditentukan lewat prompt — Muse yang menginstall cukup mengedit blok
CONFIG saja, tanpa mengubah kode 3D-nya. Contoh lain: "buatkan dengan
2 divisi, 4 agen, 1 lantai" atau "buatkan dengan 5 divisi, 10 agen,
3 lantai". Tema visual (malam, siang, senja) juga dipilih lewat prompt
— dan bisa diganti kapan saja di `CONFIG.visual` tanpa menyentuh kode.
Belum punya divisi/agen? Boleh 0 — lihat [PANDUAN.md](PANDUAN.md)
bagian 2, lalu inisiasi setup oleh Muse.

## Cara manual (tanpa Muse)

1. Download `index.html` dari repo.
2. Buka dengan text editor, cari blok `★ KANTOR 3D — CONFIG ★`.
3. Ganti nama perusahaan, divisi, warna, dan agen — tambah divisi,
   agen, atau lantai tinggal tambah entri di CONFIG (lihat README).
4. Simpan → buka di browser. Selesai.

Atau via script: `python3 install.py` (interaktif — tanya dulu berapa
divisi, lalu per divisi: industri, fitur ruangan, workflow, dan jumlah
agennya; lalu tema visual dan musik latar) atau dengan env var, contoh:
`COMPANY="Nusantara" DIV_COUNT=4 FLOORS=3 THEME="siang" python3 install.py`
(env per divisi: `DIV1_INDUSTRY`, `DIV1_AGENTS`, `DIV1_FEATURE`,
`DIV1_WORKFLOW`, `DIV1="Data"`; per agen: `AGENT1="Budi" AGENT1_ROLE="CEO"`).
Setelah selesai, script mencetak prompt siap copy-paste ke Muse untuk
inisiasi setup lanjutan — panduan lengkapnya di [PANDUAN.md](PANDUAN.md).
