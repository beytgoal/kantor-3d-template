#!/usr/bin/env python3
"""
Kantor 3D — One-shot installer.

Jalankan:  python3 install.py
Script bertanya dulu BERAPA divisi, BERAPA agen, dan BERAPA lantai
(default 3/6/2), lalu menanyakan nama tiap divisi/agen sesuai jumlah
yang diminta, lalu generate file HTML kantor 3D yang sudah dikustom.
Desain visual tidak diubah sama sekali — hanya blok CONFIG yang diganti.
Jumlah divisi, agen, dan lantai bebas ditentukan (tanpa edit kode).

Non-interaktif via env:
  COMPANY="Nusantara" DIV_COUNT=4 AGENT_COUNT=8 FLOORS=3 python3 install.py
  DIV1="Data" DIV2="Marketing" AGENT1="Budi" AGENT1_ROLE="CEO" ...
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

# Default 3 divisi bawaan template (dipakai bila jumlah divisi <= 3)
DIV_DEFAULTS = [
    {"short": "Riset", "full": "Divisi Riset",
     "room": "Ruang Riset · Big Data", "floor": 1,
     "color": "0xf7b955", "css": "#f7b955", "cssDark": "#b57a2e",
     "url": "riset.moderate.id/big-data", "screen": "Big Data",
     "board": "Papan Pipeline Data",
     "boardDesc": "Papan pantau pipeline Big Data: grafik volume data dan alur filter yang sedang berjalan.",
     "roomDesc": "Ruang kerja tim riset: data mentah dikumpulkan dan difilter di sini."},
    {"short": "Branding & Promosi", "full": "Divisi Branding & Promosi",
     "room": "Ruang Branding & Promosi", "floor": 2,
     "color": "0x6ea8ff", "css": "#6ea8ff", "cssDark": "#2e3a5c",
     "url": "branding.moderate.id/kampanye", "screen": "Kampanye",
     "board": "Papan Kampanye",
     "boardDesc": "Papan konsep kampanye: jadwal konten dan ide promosi yang sedang digarap tim branding.",
     "roomDesc": "Ruang kerja tim branding: konsep kampanye dan materi promosi digarap di sini."},
    {"short": "Freelancer & Clipper", "full": "Divisi Freelancer & Clipper",
     "room": "Ruang Freelancer & Clipper", "floor": 2,
     "color": "0x7bd88f", "css": "#7bd88f", "cssDark": "#6b7a52",
     "url": "clipper.moderate.id/antrean-klip", "screen": "Antrean Klip",
     "board": "Papan Jadwal Clip",
     "boardDesc": "Papan jadwal produksi klip: antrean video, hook yang dipakai, dan target tayang tiap campaign.",
     "roomDesc": "Ruang kerja tim clipper, lengkap dengan sudut studio ring-light untuk produksi klip."},
]

# Default 6 agen bawaan template. `id` dipertahankan apa adanya supaya
# foto wajah di AGENT_STYLE tetap cocok walau nama diubah.
AGENT_DEFAULTS = [
    {"id": "coo", "name": "Ashila", "role": "COO",
     "division": 0, "desk": 1, "color": "#ffd700", "colorCss": "#e8b64c"},
    {"id": "lead-riset", "name": "Lead Riset", "role": "Kepala Divisi Riset",
     "division": 0, "desk": 0},
    {"id": "researcher-branding", "name": "Researcher Branding",
     "role": "Researcher — kurir data Branding",
     "division": 0, "desk": 3, "color": "#ffb347", "colorCss": "#4f8a94"},
    {"id": "researcher-clipper", "name": "Researcher Clipper",
     "role": "Researcher — kurir data Clipper",
     "division": 0, "desk": 2, "color": "#ff8c42", "colorCss": "#2e4a7a"},
    {"id": "lead-branding", "name": "Lead Branding",
     "role": "Kepala Divisi Branding & Promosi",
     "division": 1, "desk": 0, "colorCss": "#2e3a5c"},
    {"id": "lead-clipper", "name": "Lead Clipper",
     "role": "Kepala Divisi Freelancer & Clipper",
     "division": 2, "desk": 0, "colorCss": "#6b7a52"},
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


def ask_int(prompt, default, env=None):
    raw = ask(prompt, str(default), env)
    try:
        n = int(raw)
    except ValueError:
        n = default
    return max(1, n)


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


def main():
    print("== Kantor 3D — Installer ==\n")
    html = open(TPL, encoding="utf-8").read()

    # ---- jumlah (tanya dulu, default 3/6/2) ----
    print("Jumlah (bebas — tanpa edit kode):")
    div_count = ask_int("berapa divisi", 3, "DIV_COUNT")
    agent_count = ask_int("berapa agen", 6, "AGENT_COUNT")
    floors = ask_int("berapa lantai", 2, "FLOORS")

    # ---- perusahaan ----
    print("\nPerusahaan:")
    company = ask("Nama perusahaan", "Moderate", "COMPANY")
    domain = ask("Domain", "moderate.id", "DOMAIN")

    # ---- divisi ----
    print(f"\nDivisi ({div_count}):")
    divisions = []
    short_map = {}
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
            url = ask("url layar", d0["url"].replace("moderate.id", domain), f"DIV{n}_URL")
            board = ask("nama papan", d0["board"], f"DIV{n}_BOARD")
            css = color.replace("0x", "#") if color.startswith("0x") else d0["css"]
            divisions.append({
                "short": short, "full": full, "room": room,
                "floor": max(1, min(floors, floor)),
                "color": color, "css": css, "cssDark": darken(css),
                "url": url, "screen": d0["screen"], "board": board,
                "boardDesc": d0["boardDesc"], "roomDesc": d0["roomDesc"],
            })
            short_map[d0["short"]] = short
        else:
            col_hex, col_css = PALETTE[i % len(PALETTE)]
            short = ask("nama pendek", f"Divisi {n}", f"DIV{n}")
            full = ask("nama lengkap", f"Divisi {short}", f"DIV{n}_FULL")
            room = ask("nama ruangan", f"Ruang {short}", f"DIV{n}_ROOM")
            floor = ask_int("lantai (1-index)", 2 if floors >= 2 else 1, f"DIV{n}_FLOOR")
            color = ask("warna hex (cth 0xf7b955)", col_hex, f"DIV{n}_COLOR")
            url = ask("url layar", f"{slug(short)}.{domain}", f"DIV{n}_URL")
            board = ask("nama papan", f"Papan {short}", f"DIV{n}_BOARD")
            css = color.replace("0x", "#") if color.startswith("0x") else col_css
            divisions.append({
                "short": short, "full": full, "room": room,
                "floor": max(1, min(floors, floor)),
                "color": color, "css": css, "cssDark": darken(css),
                "url": url, "screen": short, "board": board,
                "boardDesc": f"Papan pantau {short}: progres dan tugas tim {short}.",
                "roomDesc": f"Ruang kerja tim {short}.",
            })

    # ---- agen ----
    print(f"\nAgen ({agent_count}):")
    agents = []
    for i in range(agent_count):
        n = i + 1
        a0 = AGENT_DEFAULTS[i] if i < len(AGENT_DEFAULTS) else None
        print(f" Agen {n}:")
        if a0:
            role_def = a0["role"]
            name_def = a0["name"]
            for old_s, new_s in short_map.items():
                role_def = role_def.replace(old_s, new_s)
                if old_s in name_def:
                    name_def = name_def.replace(old_s, new_s)
            name = ask("nama", name_def, f"AGENT{n}")
            role = ask("peran", role_def, f"AGENT{n}_ROLE")
            div_def = a0["division"] if a0["division"] < div_count else (i % div_count)
            div = ask_int("divisi (0 = divisi pertama)", div_def, f"AGENT{n}_DIV")
            agent = {"id": a0["id"], "name": name, "role": role,
                     "division": max(0, min(div_count - 1, div))}
            if "desk" in a0:
                agent["desk"] = a0["desk"]
            if "color" in a0:
                agent["color"] = a0["color"]
            if "colorCss" in a0:
                agent["colorCss"] = a0["colorCss"]
            agents.append(agent)
        else:
            name = ask("nama", f"Agent {n}", f"AGENT{n}")
            role = ask("peran", "Staff", f"AGENT{n}_ROLE")
            div = ask_int("divisi (0 = divisi pertama)", i % div_count, f"AGENT{n}_DIV")
            agents.append({"id": slug(name) or f"agent-{n}", "name": name,
                           "role": role,
                           "division": max(0, min(div_count - 1, div))})

    # ---- generate blok CONFIG baru ----
    lines = []
    lines.append("const CONFIG = {")
    lines.append(f'  company: {js_str(company)},')
    lines.append(f'  companyUpper: {js_str(company.upper())},')
    lines.append(f'  domain: {js_str(domain)},')
    lines.append(f'  appUrl: {js_str("app." + domain)},')
    lines.append("  // Jumlah lantai gedung. Pelat lantai, tangga, dan tombol lompat lantai")
    lines.append("  // dibangun otomatis mengikuti angka ini (minimal 1).")
    lines.append(f"  floors: {floors},")
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
        lines.append(f'      roomDesc: {js_str(d["roomDesc"])}')
        lines.append("    },")
    lines.append("  ],")
    lines.append("  // Tambah agen tinggal tambah entri di sini — ruangan, kursi, dan warna")
    lines.append("  // dihitung otomatis. Field opsional per agen:")
    lines.append("  //   id: pengenal unik (default: nama dijadikan slug)")
    lines.append("  //   division: index divisi tempat ia duduk (0 = divisi pertama) atau")
    lines.append('  //             nama pendek divisi (mis. "Riset"); kalau dikosongkan,')
    lines.append("  //             agen dibagi rata ke semua divisi (round-robin).")
    lines.append("  //   desk: nomor kursi di ruangan divisinya (0 = kursi pertama); kalau")
    lines.append("  //         dikosongkan, diambil kursi kosong berikutnya.")
    lines.append("  //   color: warna bubble & aksen agen (default: warna divisinya)")
    lines.append("  //   colorCss: warna baju agen (default: sama dengan `color`)")
    lines.append("  agents: [")
    for a in agents:
        parts = [f'id: {js_str(a["id"])}', f'name: {js_str(a["name"])}',
                 f'role: {js_str(a["role"])}', f'division: {a["division"]}']
        if "desk" in a:
            parts.append(f'desk: {a["desk"]}')
        if "color" in a:
            parts.append(f'color: {js_str(a["color"])}')
        if "colorCss" in a:
            parts.append(f'colorCss: {js_str(a["colorCss"])}')
        lines.append("    { " + ", ".join(parts) + " },")
    lines.append("  ]")
    lines.append("};")
    new_cfg = "\n".join(lines)

    start = html.index("const CONFIG = {")
    end = html.index("// --- derived & normalisasi")
    html = html[:start] + new_cfg + "\n" + html[end:]

    slug_name = re.sub(r"[^a-z0-9]+", "-", company.lower()).strip("-") or "kantor"
    out = os.path.join(HERE, f"kantor-3d-{slug_name}.html")
    open(out, "w", encoding="utf-8").write(html)
    print(f"\nSelesai! File: {out}")
    print(f"({div_count} divisi, {agent_count} agen, {floors} lantai)")
    print("Buka di browser — kantor 3D siap dipakai.")


if __name__ == "__main__":
    main()
