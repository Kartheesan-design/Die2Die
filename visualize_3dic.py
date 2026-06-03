import plotly.graph_objects as go

# Die dimensions (microns)
DIE_X = 600
DIE_Y = 600

# Stack heights
SRAM_Z = 0
CPU_Z = 60

# Example TSV coordinates extracted from your DEF
tsvs = [
    (40, 520, "clk"),
    (140, 590, "mem_valid"),
    (140, 560, "mem_ready"),
    (290, 520, "mem_addr0"),
    (300, 560, "mem_wdata0"),
    (450, 560, "mem_rdata0"),
]

fig = go.Figure()

# SRAM die
fig.add_trace(
    go.Mesh3d(
        x=[0, DIE_X, DIE_X, 0, 0, DIE_X, DIE_X, 0],
        y=[0, 0, DIE_Y, DIE_Y, 0, 0, DIE_Y, DIE_Y],
        z=[0, 0, 0, 0, 5, 5, 5, 5],
        opacity=0.5,
        name="SRAM Die"
    )
)

# CPU die
fig.add_trace(
    go.Mesh3d(
        x=[0, DIE_X, DIE_X, 0, 0, DIE_X, DIE_X, 0],
        y=[0, 0, DIE_Y, DIE_Y, 0, 0, DIE_Y, DIE_Y],
        z=[CPU_Z, CPU_Z, CPU_Z, CPU_Z,
           CPU_Z+5, CPU_Z+5, CPU_Z+5, CPU_Z+5],
        opacity=0.5,
        name="CPU Die"
    )
)

# TSVs
for x, y, label in tsvs:
    fig.add_trace(
        go.Scatter3d(
            x=[x, x],
            y=[y, y],
            z=[5, CPU_Z],
            mode="lines+markers",
            name=label
        )
    )

fig.update_layout(
    title="3D IC Stack: Picorv32 + SRAM",
    scene=dict(
        xaxis_title="X (µm)",
        yaxis_title="Y (µm)",
        zaxis_title="Z (µm)"
    )
)

fig.write_html("3dic_stack.html")
print("Generated: 3dic_stack.html")
