#!/usr/bin/env python3
"""
05_3dic_visualize.py  —  3D-IC Stack Visualization v3
Fixes:
  - Camera now faces the bonding strip (y=520-600) directly
  - Bonding zones rendered as proper rectangles (correct vertex winding)
  - TSVs correctly span x=20..550 across the full width
"""

from pathlib import Path
import numpy as np
import plotly.graph_objects as go

OUT_HTML = Path.home() / "Desktop/3DIC/3DIC_view/view.html"

# ── geometry ──────────────────────────────────────────────────────────────────
DIE_W, DIE_H = 600, 600
DIE_T        = 10        # visual die thickness
GAP          = 35        # gap between dies
TSV_R        = 3.0       # TSV cylinder radius

SRAM_Z0 = 0
SRAM_Z1 = SRAM_Z0 + DIE_T
CPU_Z0  = SRAM_Z1 + GAP
CPU_Z1  = CPU_Z0  + DIE_T

BUS_COLOR = {
    "clk":   "#ff3333",
    "ctrl":  "#cc44ff",
    "wstrb": "#ff9900",
    "addr":  "#33aaff",
    "wdata": "#33dd55",
    "rdata": "#ff6699",
}

# ── 79 TSVs ───────────────────────────────────────────────────────────────────
def build_tsvs():
    t = []
    def a(x, y, bus, lbl): t.append((float(x), float(y), bus, lbl))
    a(20.0, 560.0, "clk",  "clk")
    a(34.0, 560.0, "ctrl", "mem_valid")
    a(48.0, 560.0, "ctrl", "mem_ready")
    for i in range(4):  a(70.0  + i*12, 560.0, "wstrb", f"wstrb[{i}]")
    for i in range(8):  a(128.0 + i*12, 560.0, "addr",  f"addr[{i}]")
    for i in range(32): a(240.0 + i*10, 560.0, "wdata", f"wdata[{i}]")
    for i in range(32): a(240.0 + i*10, 540.0, "rdata", f"rdata[{i}]")
    return t

TSVS = build_tsvs()

# ── box mesh (6 faces, correct winding) ───────────────────────────────────────
def add_box(fig, label, x0,x1, y0,y1, z0,z1, color, opacity, group,
            showlegend=True):
    # 8 vertices
    vx = [x0,x1,x1,x0, x0,x1,x1,x0]
    vy = [y0,y0,y1,y1, y0,y0,y1,y1]
    vz = [z0,z0,z0,z0, z1,z1,z1,z1]
    #       bottom       top          front        back         left         right
    i  = [0,2, 4,6, 0,1, 3,2, 0,4, 1,5]
    j  = [1,3, 5,7, 1,5, 2,6, 4,7, 2,6]
    k  = [2,0, 6,4, 5,4, 6,7, 7,3, 6,7]
    fig.add_trace(go.Mesh3d(
        x=vx, y=vy, z=vz, i=i, j=j, k=k,
        color=color, opacity=opacity,
        name=label, legendgroup=group, showlegend=showlegend,
        hovertemplate=f"<b>{label}</b><extra></extra>",
    ))
    # wireframe
    edges = [(0,1),(1,2),(2,3),(3,0),
             (4,5),(5,6),(6,7),(7,4),
             (0,4),(1,5),(2,6),(3,7)]
    for a,b in edges:
        fig.add_trace(go.Scatter3d(
            x=[vx[a],vx[b]], y=[vy[a],vy[b]], z=[vz[a],vz[b]],
            mode='lines', line=dict(color=color, width=1.5),
            showlegend=False, hoverinfo='skip', legendgroup=group,
        ))

# ── cylinder ──────────────────────────────────────────────────────────────────
def add_cylinder(fig, cx, cy, z0, z1, color, name, group,
                 showlegend=False, label="", r=TSV_R, n=14):
    th  = np.linspace(0, 2*np.pi, n, endpoint=False)
    rx, ry = r*np.cos(th), r*np.sin(th)
    vx = np.concatenate([cx+rx, cx+rx, [cx, cx]])
    vy = np.concatenate([cy+ry, cy+ry, [cy, cy]])
    vz = np.concatenate([np.full(n,z0), np.full(n,z1), [z0, z1]])
    ii,jj,kk = [],[],[]
    for idx in range(n):
        nxt = (idx+1)%n
        ii += [idx,   idx,   n+idx]
        jj += [nxt,   n+idx, n+nxt]
        kk += [n+idx, nxt,   n+nxt]
    bc = 2*n
    for idx in range(n):
        ii.append(bc); jj.append(idx); kk.append((idx+1)%n)
    tc = 2*n+1
    for idx in range(n):
        ii.append(tc); jj.append(n+idx); kk.append(n+(idx+1)%n)
    fig.add_trace(go.Mesh3d(
        x=vx, y=vy, z=vz, i=ii, j=jj, k=kk,
        color=color, opacity=1.0,
        name=name, legendgroup=group, showlegend=showlegend,
        hovertemplate=(
            f"<b>{label}</b><br>bus: {group}<br>"
            f"x={cx:.0f} µm, y_cpu={cy:.0f} µm<br>"
            f"y_sram={600-cy:.0f} µm<extra></extra>"
        ),
    ))

# ── build figure ──────────────────────────────────────────────────────────────
fig = go.Figure()

# main dies
add_box(fig, "SRAM die (sky130)",  0,600, 0,600, SRAM_Z0,SRAM_Z1,
        "#1faa44", 0.30, "sram")
add_box(fig, "CPU die (picorv32)", 0,600, 0,600, CPU_Z0, CPU_Z1,
        "#2255cc", 0.30, "cpu")

# bonding zones — correct y extents
add_box(fig, "CPU bonding zone  (y=520–600 µm)",
        0,600, 520,600, CPU_Z0,CPU_Z1,
        "#ffee00", 0.55, "cpuzone")
add_box(fig, "SRAM bonding zone (y=0–80 µm)",
        0,600, 0,80, SRAM_Z0,SRAM_Z1,
        "#ffee00", 0.55, "sramzone")

# TSVs — span from SRAM top to CPU bottom through the gap
legend_done = set()
for (x, y_cpu, bus, label) in TSVS:
    show = bus not in legend_done
    legend_done.add(bus)
    add_cylinder(fig, x, y_cpu, SRAM_Z1, CPU_Z0,
                 color=BUS_COLOR[bus],
                 name=f"{bus} bus",
                 group=bus,
                 showlegend=show,
                 label=label)

# ── camera: eye at high-Y, low-X so bonding strip (y≈540-560) faces viewer ───
fig.update_layout(
    title=dict(
        text=(
            "<b>3D-IC Stack: picorv32 CPU + sky130 SRAM</b><br>"
            "<sup>79 TSVs | sky130A PDK | 600×600 µm | "
            "Rotate · Zoom · Pan · Toggle buses in legend</sup>"
        ),
        font=dict(color="white", size=16),
        x=0.5, xanchor="center",
    ),
    paper_bgcolor="#0d0d1a",
    scene=dict(
        bgcolor="#0d0d1a",
        camera=dict(
            # Position: x=-0.3 (slight left), y=2.2 (in front of high-Y face),
            # z=0.9 (above) → bonding strip is front-and-centre
            eye=dict(x=-0.3, y=2.2, z=0.9),
            center=dict(x=0.1, y=0.0, z=-0.05),
            up=dict(x=0, y=0, z=1),
        ),
        xaxis=dict(
            title=dict(text="X (µm)", font=dict(color="#aaa", size=11)),
            range=[0,600], gridcolor="#252535",
            backgroundcolor="#0f0f20", showbackground=True,
            tickfont=dict(color="#aaa"), nticks=7,
        ),
        yaxis=dict(
            title=dict(text="Y (µm)", font=dict(color="#aaa", size=11)),
            range=[0,600], gridcolor="#252535",
            backgroundcolor="#0f0f20", showbackground=True,
            tickfont=dict(color="#aaa"), nticks=7,
        ),
        zaxis=dict(
            title=dict(text="Z (µm)", font=dict(color="#aaa", size=11)),
            range=[-3, CPU_Z1+8], gridcolor="#252535",
            backgroundcolor="#0a0a18", showbackground=True,
            tickfont=dict(color="#aaa"),
            tickvals=[SRAM_Z0, SRAM_Z1, (SRAM_Z1+CPU_Z0)//2, CPU_Z0, CPU_Z1],
            ticktext=[
                f"z={SRAM_Z0} SRAM⊥",
                f"z={SRAM_Z1} SRAM⊤",
                f"← TSVs →",
                f"z={CPU_Z0} CPU⊥",
                f"z={CPU_Z1} CPU⊤",
            ],
        ),
        aspectmode="manual",
        aspectratio=dict(x=1.5, y=1.5, z=0.6),
    ),
    legend=dict(
        font=dict(color="white", size=11),
        bgcolor="#1a1a2e", bordercolor="#445", borderwidth=1,
        itemclick="toggle", itemdoubleclick="toggleothers",
        title=dict(text="<b>Click to toggle</b>",
                   font=dict(color="#aaa", size=10)),
        tracegroupgap=3,
    ),
    margin=dict(l=0, r=0, t=90, b=0),
    height=800,
)

# TSV summary box
bus_counts = {}
for _,_,b,_ in TSVS: bus_counts[b] = bus_counts.get(b,0)+1
lines = ["<b>TSV Summary</b>"]
for bus in ["clk","ctrl","wstrb","addr","wdata","rdata"]:
    c = BUS_COLOR[bus]
    lines.append(f"<span style='color:{c}'>■</span> {bus:<8}{bus_counts[bus]:3d}")
lines.append(f"<b>Total:    {len(TSVS):3d}</b>")
fig.add_annotation(
    x=0.01, y=0.97, xref="paper", yref="paper",
    text="<br>".join(lines), showarrow=False, align="left",
    bgcolor="#1a1a2e", bordercolor="#445", borderwidth=1,
    font=dict(family="monospace", size=11, color="white"),
)

fig.write_html(str(OUT_HTML), include_plotlyjs="cdn", full_html=True,
               config={"displayModeBar":True,"displaylogo":False,
                       "modeBarButtonsToRemove":["toImage"]})
print(f"Generated: {OUT_HTML}  ({len(TSVS)} TSVs)")
for b in ["clk","ctrl","wstrb","addr","wdata","rdata"]:
    print(f"  {b:<8}: {bus_counts[b]:3d}")
