#!/usr/bin/env python3
"""
Skript pro generování footprintů z EasyEDA komponent
"""
import subprocess
import os

# LCSC IDs pro komponenty
components = {
    "C118278": "ESDA6V1U1RL",  # ESD protection diode
    "C915148": "Inductor_4.7uH"  # 4.7uH Inductor
}

# Adresář pro výstup
output_dir = "stlib.pretty"
os.makedirs(output_dir, exist_ok=True)

for lcsc_id, name in components.items():
    print(f"\nGeneruji footprint pro {name} (LCSC: {lcsc_id})...")
    
    # easyeda2kicad - stáhne a konvertuje
    cmd = [
        "easyeda2kicad",
        "--lcsc", lcsc_id,
        "--output", output_dir,
        "--footprint"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ Úspěšně vygenerován footprint pro {name}")
        else:
            print(f"✗ Chyba při generování {name}:")
            print(result.stderr)
    except Exception as e:
        print(f"✗ Chyba: {e}")

print("\n✓ Hotovo!")
