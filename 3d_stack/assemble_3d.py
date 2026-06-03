
#!/usr/bin/env python3
"""
Phase 3: 3D IC Assembly
Merges Die-1 (PicoRV32) and Die-2 (SRAM) DEF files
Creates TSV connections and stacked DEF for cross-die analysis
"""

import re
import os

# ── Paths ──────────────────────────────────────────────────────────────
DIE1_DEF = os.path.expanduser(
    "~/Desktop/3DIC/pnr/picorv32_die1/picorv32_final.def")
DIE2_DEF = os.path.expanduser(
    "~/Desktop/3DIC/pnr/sram_die/sram_die_final.def")
OUT_DIR  = os.path.expanduser("~/Desktop/3DIC/3d_stack")
os.makedirs(OUT_DIR, exist_ok=True)

# ── TSV interface definition ────────────────────────────────────────────
# Signals that cross the die boundary via TSVs
# Die-1 pin name → Die-2 pin name
TSV_CONNECTIONS = {
    # Clock
    "clk"       : "clk0",
    # Memory interface
    "mem_addr_0": "addr0[0]",
    "mem_addr_1": "addr0[1]",
    "mem_addr_2": "addr0[2]",
    "mem_addr_3": "addr0[3]",
    "mem_addr_4": "addr0[4]",
    "mem_addr_5": "addr0[5]",
    "mem_addr_6": "addr0[6]",
    "mem_addr_7": "addr0[7]",
    "mem_wdata_0" : "din0[0]",
    "mem_wdata_1" : "din0[1]",
    "mem_wdata_2" : "din0[2]",
    "mem_wdata_3" : "din0[3]",
    "mem_wdata_4" : "din0[4]",
    "mem_wdata_5" : "din0[5]",
    "mem_wdata_6" : "din0[6]",
    "mem_wdata_7" : "din0[7]",
    "mem_wdata_8" : "din0[8]",
    "mem_wdata_9" : "din0[9]",
    "mem_wdata_10": "din0[10]",
    "mem_wdata_11": "din0[11]",
    "mem_wdata_12": "din0[12]",
    "mem_wdata_13": "din0[13]",
    "mem_wdata_14": "din0[14]",
    "mem_wdata_15": "din0[15]",
    "mem_wdata_16": "din0[16]",
    "mem_wdata_17": "din0[17]",
    "mem_wdata_18": "din0[18]",
    "mem_wdata_19": "din0[19]",
    "mem_wdata_20": "din0[20]",
    "mem_wdata_21": "din0[21]",
    "mem_wdata_22": "din0[22]",
    "mem_wdata_23": "din0[23]",
    "mem_wdata_24": "din0[24]",
    "mem_wdata_25": "din0[25]",
    "mem_wdata_26": "din0[26]",
    "mem_wdata_27": "din0[27]",
    "mem_wdata_28": "din0[28]",
    "mem_wdata_29": "din0[29]",
    "mem_wdata_30": "din0[30]",
    "mem_wdata_31": "din0[31]",
    "mem_wstrb_0" : "wmask0[0]",
    "mem_wstrb_1" : "wmask0[1]",
    "mem_wstrb_2" : "wmask0[2]",
    "mem_wstrb_3" : "wmask0[3]",
    "mem_valid"   : "csb0",
    "mem_ready"   : "web0",
}

# ── Read DEF files ──────────────────────────────────────────────────────
def read_def(path):
    with open(os.path.expanduser(path)) as f:
        return f.read()

print("Reading Die-1 DEF...")
die1 = read_def(DIE1_DEF)
print(f"  Die-1 size: {len(die1)//1024} KB")

print("Reading Die-2 DEF...")
die2 = read_def(DIE2_DEF)
print(f"  Die-2 size: {len(die2)//1024} KB")

# ── Extract pin locations from DEF ──────────────────────────────────────
def extract_pins(def_content):
    pins = {}
    # Match PIN blocks in DEF format
    pattern = re.compile(
        r'-\s+(\S+)\s+\+[^+]*\+\s+PLACED\s+\(\s*(\d+)\s+(\d+)\s*\)',
        re.MULTILINE)
    for m in pattern.finditer(def_content):
        name, x, y = m.group(1), int(m.group(2)), int(m.group(3))
        pins[name] = (x, y)
    return pins

die1_pins = extract_pins(die1)
die2_pins = extract_pins(die2)

print(f"\nDie-1 pins found: {len(die1_pins)}")
print(f"Die-2 pins found: {len(die2_pins)}")

# ── Show some pin locations ─────────────────────────────────────────────
print("\nSample Die-1 pins:")
for name, (x,y) in list(die1_pins.items())[:5]:
    print(f"  {name:20s} @ ({x/1000:.1f}, {y/1000:.1f}) um")

print("\nSample Die-2 pins:")
for name, (x,y) in list(die2_pins.items())[:5]:
    print(f"  {name:20s} @ ({x/1000:.1f}, {y/1000:.1f}) um")

# ── Generate TSV placement report ──────────────────────────────────────
print("\n=== TSV CONNECTION PLAN ===")
print(f"{'Die-1 Pin':<20} {'Die-1 Location':<20} "
      f"{'Die-2 Pin':<20} {'Die-2 Location':<20} Status")
print("-" * 90)

tsv_report = []
connected  = 0
missing    = 0

for d1_pin, d2_pin in TSV_CONNECTIONS.items():
    d1_loc = die1_pins.get(d1_pin, None)
    d2_loc = die2_pins.get(d2_pin, None)
    if d1_loc and d2_loc:
        d1_str = f"({d1_loc[0]/1000:.1f},{d1_loc[1]/1000:.1f})um"
        d2_str = f"({d2_loc[0]/1000:.1f},{d2_loc[1]/1000:.1f})um"
        status = "CONNECTED"
        connected += 1
    else:
        d1_str = str(d1_loc) if d1_loc else "NOT FOUND"
        d2_str = str(d2_loc) if d2_loc else "NOT FOUND"
        status = "MISSING"
        missing += 1
    print(f"{d1_pin:<20} {d1_str:<20} {d2_pin:<20} {d2_str:<20} {status}")
    tsv_report.append((d1_pin, d1_loc, d2_pin, d2_loc, status))

print("-" * 90)
print(f"Connected: {connected}  |  Missing: {missing}  |  "
      f"Total TSVs: {len(TSV_CONNECTIONS)}")

# ── Generate stacked DEF header ─────────────────────────────────────────
# Die-2 is stacked on top of Die-1 with Z-offset
# In 2D DEF we represent this by offsetting Die-2 components
# with a prefix to avoid name collisions

print("\n=== GENERATING STACKED DEF ===")

stacked_def = f"""VERSION 5.8 ;
DIVIDERCHAR "/" ;
BUSBITCHARS "[]" ;
DESIGN picorv32_3d_stack ;
UNITS DISTANCE MICRONS 1000 ;

# 3D Stack: Die-1 (PicoRV32 CPU) + Die-2 (SRAM)
# Stacking mode: Face-to-Face (F2F)
# Die-1: bottom die  (0,0) to (600,600) um
# Die-2: top die     mirrored, offset for F2F alignment
# TSV pitch: 10 um
# Bond interface: met5 on both dies

DIEAREA ( 0 0 ) ( 600000 600000 ) ;

"""

# Write stacked DEF
out_path = os.path.join(OUT_DIR, "stack_3d.def")
with open(out_path, 'w') as f:
    f.write(stacked_def)

# ── Write TSV report ────────────────────────────────────────────────────
report_path = os.path.join(OUT_DIR, "tsv_report.txt")
with open(report_path, 'w') as f:
    f.write("3D IC TSV Connection Report\n")
    f.write("=" * 60 + "\n\n")
    f.write(f"Die-1: PicoRV32 CPU  (600x600 um)\n")
    f.write(f"Die-2: SRAM 256x32   (600x520 um)\n")
    f.write(f"Stacking: Face-to-Face (F2F)\n\n")
    f.write(f"Total TSV connections planned: {len(TSV_CONNECTIONS)}\n")
    f.write(f"Connected: {connected}\n")
    f.write(f"Missing:   {missing}\n\n")
    f.write(f"{'Die-1 Pin':<20} {'Die-2 Pin':<20} Status\n")
    f.write("-" * 60 + "\n")
    for d1_pin, d1_loc, d2_pin, d2_loc, status in tsv_report:
        f.write(f"{d1_pin:<20} {d2_pin:<20} {status}\n")

print(f"\nOutputs written to {OUT_DIR}/")
print(f"  stack_3d.def   — stacked DEF skeleton")
print(f"  tsv_report.txt — TSV connection report")
print("\n=== PHASE 3 STEP 1 COMPLETE ===")

