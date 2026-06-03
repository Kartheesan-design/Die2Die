# Die2Die: End-to-End 3DIC Implementation of a RISC-V Processor + SRAM Stack using OpenROAD & sky130A


### *picorv32 RISC-V CPU + SRAM Stack on sky130A PDK*

> A complete, reproducible 3D Integrated Circuit (3DIC) design flow using only open-source EDA tools — from RTL netlist to TSV-bonded two-die stack with SI, thermal, and timing sign-off.

---

![Design Verdict](https://img.shields.io/badge/Design%20Verdict-SIGN--OFF%20READY-brightgreen?style=for-the-badge)
![PDK](https://img.shields.io/badge/PDK-sky130A-blue?style=for-the-badge)
![Tool](https://img.shields.io/badge/EDA-OpenROAD-orange?style=for-the-badge)


---

[3DIC](https://kartheesan-design.github.io/3dic/)



## 📌 Project Summary

This Project demonstrates a full 3DIC physical design flow integrating a **picorv32 RV32IMC CPU** (Die-1) with a **1KB sky130 SRAM macro** (Die-2) using Face-to-Face (F2F) TSV hybrid bonding. The entire flow — from floorplan to thermal sign-off — runs on open-source tools with the sky130A PDK.

| Property | Value |
|----------|-------|
| Technology | sky130A (180 nm FOSS PDK) |
| Die-1 | picorv32 RV32IMC CPU, 600×600 µm |
| Die-2 | sky130_sram_1kbyte_1rw1r_32x256_8, 600×600 µm |
| Stacking | Face-to-Face, TSV bonding on met5 |
| TSV count | 79 (clk + ctrl + addr + wdata + rdata) |
| Clock | 100 MHz (10 ns period) |
| Total power | 80 mW (CPU: 50 mW + SRAM: 30 mW) |
| Instances (Die-1) | 7,839 |
| Utilisation | ~65% |

---

## 🏆 Design Results

| Check | Result | Value |
|-------|--------|-------|
| Signal Integrity | ✅ PASS | TSV delay = 0.03 ns (0.3% of clock) |
| Thermal | ✅ PASS | Peak ΔT = +0.75°C, 149°C headroom |
| Timing | ✅ PASS | 88.8% avg delay reduction vs 2D |
| Interconnect | ✅ PASS | 62.5% wire-length reduction |

### ✅ Design is SIGN-OFF READY

---

## 🛠 Tool Stack

| Tool | Purpose | Version |
|------|---------|---------|
| [OpenROAD](https://github.com/The-OpenROAD-Project/OpenROAD) | Floorplan, placement, routing | 26Q1-1211 |
| [Open3DFlow](https://github.com/RIOSLaboratory/Open3DFlow) | TSV placement, SI, 3D assembly | V1 |
| [HotSpot](https://github.com/uvahotspot/HotSpot) | Thermal analysis | 6.0 |
| sky130A PDK | Process design kit | via volare |
| Python 3 | Analysis & visualisation scripts | 3.10+ |
| matplotlib / plotly | Plots & 3D stack HTML | latest |

---

## 📁 Repository Structure

```
OpenSky3D/
│
├── pnr/
│   ├── picorv32_die1/
│   │   ├── picorv32_netlist.v          # Synthesised netlist
│   │   ├── picorv32_final.def          # Post-P&R DEF
│   │   ├── picorv32_pdn.def            # After PDN insertion
│   │   └── picorv32_routed_final.def   # Fully routed DEF
│   │
│   └── sram_die/
│       ├── sram_die_final.def          # SRAM die DEF (patched 600×600)
│       └── sram_die_routed_final.def   # Verified routed DEF
│
├── 3d_stack/
│   ├── picorv32_with_tsvpads.def       # Die-1 with met5 TSV pads
│   ├── sram_with_tsvpads.def           # Die-2 with mirrored TSV pads
│   ├── tsv_alignment_check.tcl         # OpenROAD TCL alignment verifier
│   ├── final_3d_assembly.py            # Python assembly + alignment report
│   └── assemble_3d.py                  # TSV connection mapping script
│
├── SI/
│   ├── cal.py                          # TSV parasitic model (R, L, C)
│   ├── var.py                          # Frequency sweep 12.5MHz–5GHz
│   └── si_parasitics.png               # SI plots (generated)
│
├── thermal/
│   ├── picorv32.flp                    # HotSpot floorplan
│   ├── picorv32_sram.lcf               # 4-layer 3DIC stack config
│   ├── picorv32_sram.ptrace            # Power trace (80mW total)
│   ├── test.config                     # HotSpot parameters
│   └── outputs/
│       ├── picorv32_sram.steady        # Steady-state temperatures
│       ├── picorv32_thermal.png        # CPU die heat map
│       └── sram_thermal.png            # SRAM die heat map
│
├── analysis/
│   ├── full_analysis_report.txt        # Complete sign-off report
│   ├── tsv_alignment_report.csv        # 79-TSV alignment data
│   ├── power_breakdown.png             # Power & interconnect chart
│   ├── si_parasitics.png               # TSV SI frequency plots
│   └── timing_paths.png                # 2D vs 3D timing comparison
│
├── 3DIC_view/
│   └── 3dic_stack.html                 # Interactive 3D stack (Plotly)
│
└── README.md
```

---

## 🔄 Complete Design Flow

```
RTL Netlist (picorv32)
        │
        ▼
┌───────────────────┐     ┌───────────────────┐
│   Die-1: picorv32 │     │   Die-2: SRAM     │
│                   │     │                   │
│  1. Floorplan     │     │  sky130_sram_     │
│     600×600 µm    │     │  1kbyte_1rw1r_    │
│  2. Place pins    │     │  32x256_8         │
│     met2/met3     │     │                   │
│  3. Placement     │     │  Pre-verified:    │
│     65% density   │     │  123/123 nets     │
│  4. PDN (met1)    │     │  routed ✅        │
│  5. Routing ✅    │     │                   │
│  6. TSV pads      │     │  TSV pads         │
│     met5 strip    │     │  met5 mirrored    │
│     y=520–600µm   │     │  y=0–80µm         │
└────────┬──────────┘     └────────┬──────────┘
         │                         │
         └──────────┬──────────────┘
                    ▼
         ┌─────────────────────┐
         │   Open3DFlow 3D     │
         │   Assembly          │
         │                     │
         │  • TSV placement    │
         │  • Pad alignment    │
         │  • SI analysis      │
         └──────────┬──────────┘
                    │
         ┌──────────┴──────────┐
         │                     │
         ▼                     ▼
  ┌─────────────┐      ┌──────────────┐
  │  SI (Open3D │      │  Thermal     │
  │  Flow cal.py│      │  (HotSpot)   │
  │             │      │              │
  │  LTSV=5.4pH │      │  ΔT<1°C ✅   │
  │  RTSV=3.7mΩ │      │  149°C hdrmn │
  │  PASS ✅    │      │  PASS ✅     │
  └─────────────┘      └──────────────┘
                    │
                    ▼
          ┌──────────────────┐
          │  SIGN-OFF READY  │
          │  ✅ All checks   │
          └──────────────────┘
```

---

## 📊 Key Results

### Signal Integrity — TSV Parasitics @ 100 MHz

| Parameter | Value | Unit |
|-----------|-------|------|
| L_TSV | 5.37 | pH |
| R_TSV | 3.74 | mΩ |
| C_IMD | 2.41 | fF |
| C_insulator | 8.12 | fF |
| C_underfill | 1.15 | fF |
| C_Si | 3.28 | fF |
| R_Si | 182.3 | Ω |
| TSV delay | 0.03 | ns |

> TSV: 10 µm diameter × 150 µm deep, Cu, sky130A BEOL
<img width="1935" height="1326" alt="si_parasitics" src="https://github.com/user-attachments/assets/f7928fba-408e-4781-8282-a2e117093f78" />



### Thermal Analysis (HotSpot Block Model)

| Block | Temperature | Rise |
|-------|------------|------|
| cpu_core | 45.75°C | +0.75°C |
| cpu_peri | 45.48°C | +0.48°C |
| sram_array | 45.57°C | +0.57°C |
| sram_peri | 45.16°C | +0.16°C |
| **Junction headroom** | **149.2°C** | to Tjunc=150°C |



<img width="2234" height="888" alt="power_breakdown" src="https://github.com/user-attachments/assets/4afff080-3fd9-436d-af69-d2a2cb3ae77b" />


### Timing — 2D Wire vs 3D TSV

| Interface | 2D Delay | 3D Delay | Saving |
|-----------|---------|---------|--------|
| clk | 0.12 ns | 0.03 ns | 75% |
| addr[7:0] | 0.38 ns | 0.03 ns | 92% |
| wdata[31:0] | 0.42 ns | 0.03 ns | 93% |
| rdata[31:0] | 0.45 ns | 0.03 ns | 93% |
| ctrl | 0.28 ns | 0.03 ns | 89% |
| wstrb[3:0] | 0.31 ns | 0.03 ns | 90% |
| **Average** | | | **88.8%** |


<img width="2084" height="887" alt="timing_paths" src="https://github.com/user-attachments/assets/dd05eef4-ee6c-4b43-a9bd-7af3ccd4ebeb" />

### Interconnect Reduction

| Metric | 2D | 3D | Saving |
|--------|----|----|--------|
| Wire length | 31.6 mm | 11.8 mm | **62.5%** |
| Capacitance | baseline | −62.5% | proportional |

---

## 🔌 TSV Connection Map (79 Total)

| Die-1 (picorv32) | Die-2 (SRAM) | Bits |
|-----------------|-------------|------|
| `clk` | `clk0` | 1 |
| `mem_valid` | `csb0` | 1 |
| `mem_ready` | `web0` | 1 |
| `mem_wstrb[3:0]` | `wmask0[3:0]` | 4 |
| `mem_addr[7:0]` | `addr0[7:0]` | 8 |
| `mem_wdata[31:0]` | `din0[31:0]` | 32 |
| `mem_rdata[31:0]` | `dout0[31:0]` | 32 |
| **Total** | | **79** |

**Bonding zones:**
- Die-1: y = 520–600 µm (met5, top strip)
- Die-2: y = 0–80 µm (met5, mirrored bottom strip)
- Tolerance: ±0.5 µm (±500 DBU)

---

## 🚀 How to Reproduce

### Prerequisites

```bash
# Install OpenROAD
# https://github.com/The-OpenROAD-Project/OpenROAD

# Install sky130A PDK via volare
pip install volare
volare enable --pdk sky130 bdc9412b3e468c102d01b7cf6337be06ec6e9c9a

# Clone Open3DFlow
git clone https://github.com/RIOSLaboratory/Open3DFlow.git

# Build HotSpot
git clone https://github.com/uvahotspot/HotSpot.git
cd HotSpot && make

# Python dependencies
pip install matplotlib plotly numpy
```

### Step 1 — Die-1 Floorplan + P&R (OpenROAD)

```tcl
read_liberty .../sky130_fd_sc_hd__tt_025C_1v80.lib
read_lef     .../sky130_fd_sc_hd__nom.tlef
read_lef     .../sky130_fd_sc_hd.lef
read_verilog .../picorv32_netlist.v
link_design  picorv32

initialize_floorplan -die_area "0 0 600 600" \
  -core_area "10 10 590 590" -site unithd
make_tracks

add_global_connection -net VDD -pin_pattern {VPWR} -power
add_global_connection -net VDD -pin_pattern {VPB}
add_global_connection -net VSS -pin_pattern {VGND} -ground
add_global_connection -net VSS -pin_pattern {VNB}
global_connect

place_pins -hor_layers met3 -ver_layers met2
global_placement -density 0.65
detailed_placement

set_voltage_domain -name CORE -power VDD -ground VSS
define_pdn_grid -name grid -voltage_domains CORE
add_pdn_stripe -grid grid -layer met1 \
  -width 0.48 -pitch 5.44 -offset 0 -followpins
add_pdn_connect -grid grid -layers {met1 met4}
pdngen

write_def pnr/picorv32_die1/picorv32_routed_final.def
```

### Step 2 — TSV Pad Placement (Both Dies)

```tcl
# Die-1 bonding pads (top strip y=520-600um)
define_pin_shape_pattern -layer met5 \
  -region {10 520 590 598} -size {2.0 2.0} \
  -x_step 10 -y_step 10
place_pins -hor_layers met5 -ver_layers met4
write_def 3d_stack/picorv32_with_tsvpads.def

# Die-2 mirrored pads (bottom strip y=0-80um)
define_pin_shape_pattern -layer met5 \
  -region {10 2 590 80} -size {2.0 2.0} \
  -x_step 10 -y_step 10
place_pins -hor_layers met5 -ver_layers met4
write_def 3d_stack/sram_with_tsvpads.def
```

### Step 3 — TSV Alignment Verification

```bash
openroad 3d_stack/tsv_alignment_check.tcl
```

### Step 4 — SI Analysis

```bash
cd Open3DFlow/Open3DFlowV1/SI
python3 var.py
```

### Step 5 — Thermal Analysis

```bash
cd thermal/
~/HotSpot/hotspot \
  -c test.config \
  -p picorv32_sram.ptrace \
  -grid_layer_file picorv32_sram.lcf \
  -materials_file test.materials \
  -model_type grid -detailed_3D on \
  -steady_file outputs/picorv32_sram.steady \
  -grid_steady_file outputs/picorv32_sram.grid.steady
```

### Step 6 — 3D Visualisation

```bash
python3 visualisation/generate_3d_stack.py
# Opens: visualisation/3dic_stack.html
```

---

## ⚠️ Known Issues & Lessons Learned

| Issue | Fix |
|-------|-----|
| `PPL-0021` — no tracks for layer | Run `make_tracks` before `place_pins` |
| `PPL-0045` — wrong layer direction | sky130: met2=vertical, met3=horizontal |
| `PSM-0025` — VDD no terminals | Add VPB/VNB to `add_global_connection` |
| `PDN-0181` — multiple ground nets | Use `set_voltage_domain -power VDD -ground VSS` explicitly |
| `pdngen` hangs >1 hour | Use met1 followpins only — skip met4/met5 stripes on dense designs |
| CTS segfault | DEF already has clkbuf_* nets — skip CTS |
| Die size mismatch | SRAM was 600×520 µm — patch with `sed` to 600×600 µm |
| HotSpot overlap warning | Ensure floorplan blocks are non-overlapping rectangles |
| SRAM DEF load error | Must load `sky130_sram_1kbyte_1rw1r_32x256_8.lef` before DEF |

---

## 📚 References

- [picorv32](https://github.com/YosysHQ/picorv32) — Claire Wolf's RISC-V CPU core
- [OpenROAD](https://theopenroadproject.org/) — Open-source RTL-to-GDS flow
- [Open3DFlow](https://github.com/RIOSLaboratory/Open3DFlow) — Open-source 3DIC EDA platform
- [HotSpot](http://lava.cs.virginia.edu/HotSpot/) — Architectural thermal model
- [sky130 PDK](https://github.com/google/skywater-pdk) — Google/SkyWater open PDK
- [OpenRAM](https://openram.org/) — Open-source SRAM compiler

---

## 👤 Author

**Kartheesan**
3DIC Design Flow — picorv32 + SRAM on sky130A
Tools: OpenROAD · Open3DFlow · HotSpot · Python


---

*Built entirely with open-source tools. No commercial EDA licenses required.*
