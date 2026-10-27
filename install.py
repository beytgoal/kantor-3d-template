#!/usr/bin/env python3
"""
Kantor 3D — One-shot installer.

Jalankan:  python3 install.py
Script bertanya dulu BERAPA divisi (boleh 0 — bila belum punya divisi),
lalu untuk tiap divisi: nama, industri, fitur ruangan, workflow
(opsional), dan BERAPA agen di divisi itu; lalu tema visual
(malam/siang/senja, default malam); lalu generate file HTML kantor 3D
yang sudah dikustom. Semua jawaban ada default-nya (contoh generik) —
tinggal Enter bila belum tahu. Tema visual ditulis ke blok CONFIG
(CONFIG.visual) — tampilan bisa diubah kapan saja lewat CONFIG tanpa
menyentuh kode. Jumlah divisi, agen per divisi, dan lantai bebas
ditentukan (tanpa edit kode).

Setelah selesai, script mencetak prompt siap copy-paste ke Muse agar
Muse langsung menginisiasi setup lanjutan: struktur jumlah agen,
framework perusahaan, industri tiap divisi, workflow per divisi dan
agen utama, sampai artefak kantor 3D-nya.

Non-interaktif via env:
  COMPANY="Nusantara" DIV_COUNT=4 FLOORS=3 THEME="siang" python3 install.py
  DIV1="Data" DIV1_INDUSTRY="Teknologi" DIV1_AGENTS=3 DIV1_FEATURE="server"
  DIV1_WORKFLOW="Kumpulkan data,Olah data,Laporan" AGENT1="Budi" AGENT1_ROLE="CEO" ...
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
TPL = os.path.join(HERE, "index.html")

# Palet warna divisi (dipakai berurutan; berulang bila divisi > palet)
PALETTE = [
    ("0xf7b955", "#f7b955"), ("0x6ea8ff", "#6ea8ff"),
    ("0x7bd88f", "#7bd88f"), ("0xd88fd8", "#d88fd8"),
    ("0xff9d6b", "#ff9d6b"), ("0x6fd3d3", "#6fd3d3"),
    ("0xe0a83c", "#e0a83c"), ("0x9b8cf0", "#9b8cf0"),
]

FEATURES = ("server", "books", "studio", "none")
# Fitur bawaan menurut index divisi (dipakai bila tidak dijawab)
FEATURE_DEFAULTS = ["server", "studio", "books"]

# Default 3 divisi contoh generik (dipakai bila jumlah divisi <= 3).
# BUKAN data perusahaan nyata — ganti dengan divisimu sendiri.
DIV_DEFAULTS = [
    {"short": "Operasional", "full": "Divisi Operasional",
     "room": "Ruang Operasional", "floor": 1,
     "color": "0xf7b955", "css": "#f7b955", "cssDark": "#b57a2e",
     "url": "operasional.contoh.id", "screen": "Operasional",
     "board": "Papan Operasional",
     "boardDesc": "Papan pantau operasional: tugas harian dan progres tim operasional.",
     "roomDesc": "Ruang kerja tim operasional.",
     "industry": "Jasa & Operasional", "feature": "server",
     "workflow": ["Siapkan data harian", "Cek progres tim", "Laporan ke direktur"]},
    {"short": "Pemasaran", "full": "Divisi Pemasaran",
     "room": "Ruang Pemasaran", "floor": 2,
     "color": "0x6ea8ff", "css": "#6ea8ff", "cssDark": "#2e3a5c",
     "url": "pemasaran.contoh.id", "screen": "Pemasaran",
     "board": "Papan Pemasaran",
     "boardDesc": "Papan konsep pemasaran: jadwal konten dan ide promosi yang sedang digarap.",
     "roomDesc": "Ruang kerja tim pemasaran.",
     "industry": "Pemasaran Digital", "feature": "studio",
     "workflow": ["Susun konsep kampanye", "Garap materi promosi", "Jadwalkan tayang"]},
    {"short": "Keuangan", "full": "Divisi Keuangan",
     "room": "Ruang Keuangan", "floor": 2,
     "color": "0x7bd88f", "css": "#7bd88f", "cssDark": "#6b7a52",
     "url": "keuangan.contoh.id", "screen": "Keuangan",
     "board": "Papan Keuangan",
     "boardDesc": "Papan pantau keuangan: arus kas, anggaran, dan laporan tim keuangan.",
     "roomDesc": "Ruang kerja tim keuangan.",
     "industry": "Keuangan", "feature": "books",
     "workflow": ["Cek arus kas", "Rekonsiliasi laporan", "Siapkan anggaran"]},
]


def ask(prompt, default="", env=None):
    if env and os.environ.get(env):
        val = os.environ[env]
        print(f"  {prompt} [{default}]: {val} (env)")
        return val
    try:
        val = input(f"  {prompt} [{default}]: ").strip()
    except EOFError:
        val = ""
    return val or default


def ask_int(prompt, default, env=None, minimum=1):
    raw = ask(prompt, str(default), env)
    try:
        n = int(raw)
    except ValueError:
        n = default
    return max(minimum, n)


def slug(s):
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return s or "divisi"


def darken(css, f=0.55):
    """#rrggbb -> versi lebih gelap (untuk cssDark)."""
    try:
        r = int(css[1:3], 16); g = int(css[3:5], 16); b = int(css[5:7], 16)
        return "#%02x%02x%02x" % (int(r * f), int(g * f), int(b * f))
    except Exception:
        return css


def js_str(s):
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def parse_workflow(raw):
    """'a, b, c' -> ['a', 'b', 'c']; kosong -> []."""
    return [w.strip() for w in (raw or "").split(",") if w.strip()]


def main():
    print("== Kantor 3D — Installer ==\n")
    html = open(TPL, encoding="utf-8").read()

    # ---- jumlah (tanya dulu; divisi boleh 0 bila belum punya) ----
    print("Jumlah (bebas — tanpa edit kode):")
    div_count = ask_int("berapa divisi (0 bila belum punya)", 3, "DIV_COUNT", minimum=0)
    floors = ask_int("berapa lantai", 2, "FLOORS")

    # ---- perusahaan ----
    print("\nPerusahaan:")
    company = ask("Nama perusahaan", "Contoh", "COMPANY")
    domain = ask("Domain", "contoh.id", "DOMAIN")

    # ---- tema visual ----
    print("\nTema visual (malam = langit gelap seperti demo; siang = langit biru; senja = ungu/oranye):")
    theme = ask("tema visual (malam/siang/senja)", "malam", "THEME").strip().lower()
    if theme not in ("malam", "siang", "senja"):
        print(f"  tema {theme!r} tidak dikenal — memakai 'malam'.")
        theme = "malam"

    # ---- divisi ----
    print(f"\nDivisi ({div_count}):" if div_count else "\nDivisi: belum ada — file dibuat dengan lounge saja; divisi bisa ditambah nanti (lihat PANDUAN.md).")
    divisions = []
    agents_per_div = []
    for i in range(div_count):
        n = i + 1
        d0 = DIV_DEFAULTS[i] if i < len(DIV_DEFAULTS) else None
        print(f" Divisi {n}:")
        if d0:
            short = ask("nama pendek", d0["short"], f"DIV{n}")
            full = ask("nama lengkap", f"Divisi {short}", f"DIV{n}_FULL")
            room = ask("nama ruangan", d0["room"].replace(d0["short"], short), f"DIV{n}_ROOM")
            floor = ask_int("lantai (1-index)", d0["floor"], f"DIV{n}_FLOOR")
            color = ask("warna hex (cth 0xf7b955)", d0["color"], f"DIV{n}_COLOR")
            url = ask("url layar", d0["url"].replace("contoh.id", domain), f"DIV{n}_URL")
            board = ask("nama papan", d0["board"], f"DIV{n}_BOARD")
            industry = ask("industri divisi (cth Teknologi)", d0["industry"], f"DIV{n}_INDUSTRY")
            feature = ask("fitur ruangan (server/books/studio/none)", d0["feature"], f"DIV{n}_FEATURE").strip().lower()
            if feature not in FEATURES:
                print(f"  fitur {feature!r} tidak dikenal — memakai {d0['feature']!r}.")
                feature = d0["feature"]
            wf_raw = ask("workflow divisi (pisah koma, boleh kosong)", ", ".join(d0["workflow"]), f"DIV{n}_WORKFLOW")
            css = color.replace("0x", "#") if color.startswith("0x") else d0["css"]
            divisions.append({
                "short": short, "full": full, "room": room,
                "floor": max(1, min(floors, floor)),
                "color": color, "css": css, "cssDark": darken(css),
                "url": url, "screen": d0["screen"], "board": board,
                "boardDesc": d0["boardDesc"], "roomDesc": d0["roomDesc"],
                "industry": industry, "feature": feature,
                "workflow": parse_workflow(wf_raw),
            })
        else:
            col_hex, col_css = PALETTE[i % len(PALETTE)]
            short = ask("nama pendek", f"Divisi {n}", f"DIV{n}")
            full = ask("nama lengkap", f"Divisi {short}", f"DIV{n}_FULL")
            room = ask("nama ruangan", f"Ruang {short}", f"DIV{n}_ROOM")
            floor = ask_int("lantai (1-index)", 2 if floors >= 2 else 1, f"DIV{n}_FLOOR")
            color = ask("warna hex (cth 0xf7b955)", col_hex, f"DIV{n}_COLOR")
            url = ask("url layar", f"{slug(short)}.{domain}", f"DIV{n}_URL")
            board = ask("nama papan", f"Papan {short}", f"DIV{n}_BOARD")
            industry = ask("industri divisi (cth Teknologi)", "Umum", f"DIV{n}_INDUSTRY")
            feat_def = FEATURE_DEFAULTS[i % len(FEATURE_DEFAULTS)]
            feature = ask("fitur ruangan (server/books/studio/none)", feat_def, f"DIV{n}_FEATURE").strip().lower()
            if feature not in FEATURES:
                print(f"  fitur {feature!r} tidak dikenal — memakai {feat_def!r}.")
                feature = feat_def
            wf_raw = ask("workflow divisi (pisah koma, boleh kosong)", "", f"DIV{n}_WORKFLOW")
            css = color.replace("0x", "#") if color.startswith("0x") else col_css
            divisions.append({
                "short": short, "full": full, "room": room,
                "floor": max(1, min(floors, floor)),
                "color": color, "css": css, "cssDark": darken(css),
                "url": url, "screen": short, "board": board,
                "boardDesc": f"Papan pantau {short}: progres dan tugas tim {short}.",
                "roomDesc": f"Ruang kerja tim {short}.",
                "industry": industry, "feature": feature,
                "workflow": parse_workflow(wf_raw),
            })
        # jumlah agen di divisi ini (boleh 0)
        agents_per_div.append(ask_int(
            f"berapa agen di divisi {divisions[-1]['short']}", 2,
            f"DIV{n}_AGENTS", minimum=0))

    # ---- pipeline: divisi sumber data ----
    if div_count > 1:
        print("\nPipeline divisi (agen kurir membawa data dari divisi sumber ke divisi lain):")
        src = ask_int("divisi sumber data (0 = divisi pertama)", 0, "PIPELINE_SOURCE", minimum=0)
        pipeline_source = max(0, min(div_count - 1, src))
    else:
        pipeline_source = 0

    # ---- agen per divisi ----
    print("\nAgen:")
    agents = []
    gnum = 0  # nomor agen global (untuk env AGENTn)
    for di, d in enumerate(divisions):
        for j in range(agents_per_div[di]):
            gnum += 1
            if gnum == 1:
                name_def, role_def = "Ayu", "COO"  # agen utama
            elif j == 0:
                name_def, role_def = f"Kepala {d['short']}", f"Kepala Divisi {d['short']}"
            else:
                name_def, role_def = f"Staff {d['short']} {j}", f"Staff {d['short']}"
            print(f" Agen {gnum} (Divisi {d['short']}):")
            name = ask("nama", name_def, f"AGENT{gnum}")
            role = ask("peran", role_def, f"AGENT{gnum}_ROLE")
            agents.append({"id": slug(name) or f"agent-{gnum}", "name": name,
                           "role": role, "division": di, "desk": j})

    # ---- generate blok CONFIG baru ----
    lines = []
    lines.append("const CONFIG = {")
    lines.append("  // ── Identitas perusahaan (contoh generik — ganti dengan punyamu) ──")
    lines.append(f'  company: {js_str(company)},')
    lines.append(f'  companyUpper: {js_str(company.upper())},')
    lines.append(f'  domain: {js_str(domain)},')
    lines.append(f'  appUrl: {js_str("app." + domain)},')
    lines.append("  // Jumlah lantai gedung. Pelat lantai, tangga, dan tombol lompat lantai")
    lines.append("  // dibangun otomatis mengikuti angka ini (minimal 1).")
    lines.append(f"  floors: {floors},")
    lines.append("  // ── Pipeline divisi ──")
    lines.append("  //    Urutan divisi di bawah = urutan ruangan kiri → kanan di tiap lantai.")
    lines.append("  //    `feature`: \"server\" / \"books\" / \"studio\" / \"none\".")
    lines.append("  //    `pipeline.source`: index divisi sumber data (default 0).")
    lines.append(f"  pipeline: {{ source: {pipeline_source} }},")
    lines.append("  divisions: [")
    for d in divisions:
        lines.append("    {")
        lines.append(f'      short: {js_str(d["short"])},')
        lines.append(f'      full: {js_str(d["full"])},')
        lines.append(f'      room: {js_str(d["room"])},')
        lines.append(f'      floor: {d["floor"]},')
        lines.append(f'      color: {d["color"]}, css: {js_str(d["css"])}, cssDark: {js_str(d["cssDark"])},')
        lines.append(f'      url: {js_str(d["url"])},')
        lines.append(f'      screen: {js_str(d["screen"])},')
        lines.append(f'      board: {js_str(d["board"])},')
        lines.append(f'      boardDesc: {js_str(d["boardDesc"])},')
        lines.append(f'      roomDesc: {js_str(d["roomDesc"])},')
        lines.append(f'      industry: {js_str(d["industry"])},')
        lines.append(f'      feature: {js_str(d["feature"])},')
        wf = ", ".join(js_str(w) for w in d["workflow"])
        lines.append(f'      workflow: [{wf}]')
        lines.append("    },")
    lines.append("  ],")
    lines.append("  // Tambah agen tinggal tambah entri di sini — ruangan, kursi, dan warna")
    lines.append("  // dihitung otomatis. Field opsional per agen:")
    lines.append("  //   id: pengenal unik (default: nama dijadikan slug)")
    lines.append("  //   division: index divisi tempat ia duduk (0 = divisi pertama) atau")
    lines.append('  //             nama pendek divisi (mis. "Operasional"); kalau dikosongkan,')
    lines.append("  //             agen dibagi rata ke semua divisi (round-robin).")
    lines.append("  //   desk: nomor kursi di ruangan divisinya (0 = kursi pertama); kalau")
    lines.append("  //         dikosongkan, diambil kursi kosong berikutnya.")
    lines.append("  //   color: warna bubble & aksen agen (default: warna divisinya)")
    lines.append("  //   colorCss: warna baju agen (default: sama dengan `color`)")
    lines.append("  //   face: foto wajah (data URI atau URL) — opsional; tanpa foto, agen")
    lines.append("  //         memakai face mesh 3D bawaan.")
    lines.append("  //   role \"COO\", \"CEO\", atau \"Direktur\" = agen utama yang mengoordinasi")
    lines.append("  //         siklus kerja antar divisi.")
    lines.append("  agents: [")
    for a in agents:
        parts = [f'id: {js_str(a["id"])}', f'name: {js_str(a["name"])}',
                 f'role: {js_str(a["role"])}', f'division: {a["division"]}',
                 f'desk: {a["desk"]}']
        lines.append("    { " + ", ".join(parts) + " },")
    lines.append("  ],")
    lines.append("  // Tampilan visual: tema bawaan (\"malam\", \"siang\", \"senja\").")
    lines.append("  // Field lain di `visual` bisa ditambahkan untuk menimpa tema")
    lines.append("  // (sky, camera, palette, lights, ui) — lihat README.")
    lines.append(f'  visual: {{ theme: {js_str(theme)} }}')
    lines.append("};")
    new_cfg = "\n".join(lines)

    start = html.index("const CONFIG = {")
    end = html.index("// --- derived & normalisasi")
    html = html[:start] + new_cfg + "\n" + html[end:]

    slug_name = re.sub(r"[^a-z0-9]+", "-", company.lower()).strip("-") or "kantor"
    out = os.path.join(HERE, f"kantor-3d-{slug_name}.html")
    open(out, "w", encoding="utf-8").write(html)
    print(f"\nSelesai! File: {out}")
    print(f"({div_count} divisi, {len(agents)} agen, {floors} lantai, tema {theme})")
    print("Buka di browser — kantor 3D siap dipakai.")
    print("\n" + "=" * 64)
    print("Langkah berikut — inisiasi oleh Muse:")
    print("Copy-paste prompt ini ke Muse kamu:\n")
    print(f'  "Aku baru install Kantor 3D dari')
    print(f'  https://github.com/beytgoal/kantor-3d-template')
    print(f'  (file: {os.path.basename(out)} — {div_count} divisi, {len(agents)} agen,')
    print(f'  {floors} lantai, tema {theme}). Tolong inisiasi setup kantor 3D-ku:')
    print(f'  tanyakan nama perusahaanku, industri tiap divisi, jumlah agen')
    print(f'  per divisi, workflow tiap divisi, siapa agen utamanya, dan tema')
    print(f'  visual yang kumau — lalu ubah blok CONFIG di file itu (tanpa')
    print(f'  mengubah kode 3D-nya) dan bagikan hasilnya sebagai artefak web')
    print(f'  statis."')
    print("\nMuse akan mengarahkanmu membangun struktur agen, framework")
    print("perusahaan, dan workflow per divisi — lihat PANDUAN.md untuk")
    print("panduan lengkapnya.")
    print("=" * 64)


if __name__ == "__main__":
    main()
