#!/usr/bin/env python3
"""
Skript pro generování všech footprintů a 3D modelů ze schématu
"""
import re
import subprocess
import os
from pathlib import Path

# Přečteme schématický soubor
sch_file = "fotaoparát.kicad_sch"
output_dir = "stlib.pretty"
os.makedirs(output_dir, exist_ok=True)

# Najdeme všechna LCSC ID v souboru
lcsc_pattern = r'\(property "LCSC"\s+"([^"]+)"'
lcsc_part_pattern = r'\(property "LCSC Part"\s+"([^"]+)"'

with open(sch_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Najdeme všechna LCSC ID
lcsc_ids = set()
matches = re.findall(lcsc_pattern, content)
lcsc_ids.update(matches)
matches = re.findall(lcsc_part_pattern, content)
lcsc_ids.update(matches)

# Filtrujeme jen validní LCSC ID (C + čísla)
lcsc_ids = {id for id in lcsc_ids if re.match(r'C\d+', id)}

print(f"Nalezeno {len(lcsc_ids)} LCSC komponent:")
for lcsc_id in sorted(lcsc_ids):
    print(f"  - {lcsc_id}")

print("\n" + "="*60)
print("Stahuji footprinty a 3D modely...")
print("="*60 + "\n")

success_count = 0
error_count = 0

for lcsc_id in sorted(lcsc_ids):
    print(f"\n[{lcsc_id}] Generuji footprint a 3D model...")
    
    cmd = [
        "C:/Users/Vita/AppData/Local/Microsoft/WindowsApps/python3.12.exe",
        "-m", "easyeda2kicad",
        "--lcsc_id", lcsc_id,
        "--full",  # Stáhne symbol, footprint a 3D model
        "--output", f"{output_dir}/{lcsc_id}_full.kicad_mod"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            print(f"  ✓ Úspěšně vygenerováno")
            success_count += 1
        else:
            print(f"  ✗ Chyba: {result.stderr[:100] if result.stderr else 'unknown'}")
            error_count += 1
    except subprocess.TimeoutExpired:
        print(f"  ✗ Timeout")
        error_count += 1
    except Exception as e:
        print(f"  ✗ Chyba: {e}")
        error_count += 1

print("\n" + "="*60)
print(f"Hotovo! Úspěšně: {success_count}, Chyby: {error_count}")
print("="*60)
