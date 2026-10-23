# Install Kantor 3D — Sekali Perintah

Copy-paste prompt ini ke Muse kamu:

> Install kantor 3D dari https://github.com/beytgoal/kantor-3d-template :
> clone repo-nya, jalankan `python3 install.py`, jawab pertanyaannya
> (nama perusahaan, 3 divisi, 6 agen — semua ada default),
> lalu buatkan hasilnya sebagai artefak web statis dan bagikan link publiknya.

Muse akan otomatis: download template → generate file HTML yang sudah
dikustom → jadiin artefak → kasih link yang bisa dibuka & dibagikan.

## Cara manual (tanpa Muse)

1. Download `index.html` dari repo.
2. Buka dengan text editor, cari blok `★ KANTOR 3D — CONFIG ★`.
3. Ganti nama perusahaan, divisi, warna, dan agen.
4. Simpan → buka di browser. Selesai.

Atau via script: `python3 install.py` (interaktif) atau dengan env var,
contoh: `COMPANY="Nusantara" DIV1="Data" DIV2="Marketing" DIV3="Operasional" python3 install.py`
