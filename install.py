#!/usr/bin/env python3
"""
Kantor 3D — One-shot installer.

Jalankan:  python3 install.py
Script bertanya (semua ada default), lalu generate file HTML kantor 3D
yang sudah dikustom. Desain visual tidak diubah sama sekali.

Non-interaktif via env:
  COMPANY="Nusantara" DIV1="Data" DIV2="Marketing" DIV3="Operasional" python3 install.py
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
TPL = os.path.join(HERE, "index.html")

DIVS = [
    {"short": "Riset", "full": "Divisi Riset",
     "room": "Ruang Riset · Big Data",
     "color": "0xf7b955", "css": "#f7b955",
     "url": "riset.moderate.id/big-data",
     "board": "Papan Pipeline Data"},
    {"short": "Branding & Promosi", "full": "Divisi Branding & Promosi",
     "room": "Ruang Branding & Promosi",
     "color": "0x6ea8ff", "css": "#6ea8ff",
     "url": "branding.moderate.id/kampanye",
     "board": "Papan Kampanye"},
    {"short": "Freelancer & Clipper", "full": "Divisi Freelancer & Clipper",
     "room": "Ruang Freelancer & Clipper",
     "color": "0x7bd88f", "css": "#7bd88f",
     "url": "clipper.moderate.id/antrean-klip",
     "board": "Papan Jadwal Clip"},
]
AGENTS = [
    {"name": "Ashila", "role": "COO"},
    {"name": "Lead Riset", "role": "Kepala Divisi Riset"},
    {"name": "Researcher Branding", "role": "Researcher — kurir data Branding"},
    {"name": "Researcher Clipper", "role": "Researcher — kurir data Clipper"},
    {"name": "Lead Branding", "role": "Kepala Divisi Branding & Promosi"},
    {"name": "Lead Clipper", "role": "Kepala Divisi Freelancer & Clipper"},
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


def main():
    print("== Kantor 3D — Installer ==\n")
    html = open(TPL, encoding="utf-8").read()
    start = html.index("★ KANTOR 3D — CONFIG ★")
    end = html.index("/* ============ END CONFIG")
    cfg = html[start:end]

    def rep(old, new):
        nonlocal cfg
        if old in cfg:
            cfg = cfg.replace(old, new)

    # ---- perusahaan ----
    print("Perusahaan:")
    company = ask("Nama perusahaan", "Moderate", "COMPANY")
    domain = ask("Domain", "moderate.id", "DOMAIN")
    rep('company: "Moderate"', f'company: "{company}"')
    rep('companyUpper: "MODERATE"', f'companyUpper: "{company.upper()}"')
    rep('domain: "moderate.id"', f'domain: "{domain}"')
    rep('appUrl: "app.moderate.id"', f'appUrl: "app.{domain}"')

    # ---- divisi ----
    print("\nDivisi (3):")
    short_map = {}  # old short -> new short (untuk update role/deskripsi)
    for i, d in enumerate(DIVS):
        n = i + 1
        print(f" Divisi {n}:")
        short = ask("nama pendek", d["short"], f"DIV{n}")
        full = ask("nama lengkap", f"Divisi {short}", f"DIV{n}_FULL")
        room = ask("nama ruangan", d["room"].replace(d["short"], short), f"DIV{n}_ROOM")
        color = ask("warna hex (cth 0xf7b955)", d["color"], f"DIV{n}_COLOR")
        url = ask("url layar", d["url"].replace("moderate.id", domain), f"DIV{n}_URL")
        board = ask("nama papan", d["board"], f"DIV{n}_BOARD")
        short_map[d["short"]] = short

        rep(f'short: "{d["short"]}"', f'short: "{short}"')
        rep(f'full: "{d["full"]}"', f'full: "{full}"')
        rep(f'room: "{d["room"]}"', f'room: "{room}"')
        rep(f'color: {d["color"]}', f'color: {color}')
        rep(f'css: "{d["css"]}"', f'css: "{color.replace("0x", "#")}"')
        rep(f'url: "{d["url"]}"', f'url: "{url}"')
        rep(f'board: "{d["board"]}"', f'board: "{board}"')

    # ---- agen (default role sudah mengikuti nama divisi baru) ----
    print("\nAgen (6):")
    for i, a in enumerate(AGENTS):
        role_def = a["role"]
        for old_s, new_s in short_map.items():
            role_def = role_def.replace(old_s, new_s)
        name_def = a["name"]
        for old_s, new_s in short_map.items():
            # "Lead Riset" -> "Lead Data"
            if old_s in name_def:
                name_def = name_def.replace(old_s, new_s)
        name = ask("nama", name_def, f"AGENT{i+1}")
        role = ask("peran", role_def, f"AGENT{i+1}_ROLE")
        rep(f'name: "{a["name"]}"', f'name: "{name}"')
        rep(f'role: "{a["role"]}"', f'role: "{role}"')

    # ---- sisa nama divisi lama di deskripsi -> nama baru ----
    for old_s, new_s in short_map.items():
        if old_s != new_s and old_s in cfg:
            cfg = cfg.replace(old_s, new_s)

    html = html[:start] + cfg + html[end:]
    slug = re.sub(r"[^a-z0-9]+", "-", company.lower()).strip("-") or "kantor"
    out = os.path.join(HERE, f"kantor-3d-{slug}.html")
    open(out, "w", encoding="utf-8").write(html)
    print(f"\nSelesai! File: {out}")
    print("Buka di browser — kantor 3D siap dipakai.")


if __name__ == "__main__":
    main()
