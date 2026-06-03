import re

def_text = open(
    "/home/kartheesan/Desktop/3DIC/3d_stack/picorv32_with_tsvpads.def"
).read()

signals = {}

targets = (
    ["clk", "mem_valid", "mem_ready"] +
    [f"mem_addr[{i}]" for i in range(8)] +
    [f"mem_wdata[{i}]" for i in range(32)] +
    [f"mem_rdata[{i}]" for i in range(32)] +
    [f"mem_wstrb[{i}]" for i in range(4)]
)

for sig in targets:

    pattern = (
        r"-\s+" + re.escape(sig) +
        r".*?\+ PLACED\s+\(\s*(\d+)\s+(\d+)\s*\)"
    )

    m = re.search(pattern, def_text, re.S)

    if m:
        signals[sig] = (
            int(m.group(1)),
            int(m.group(2))
        )

print("Found:", len(signals))

for k,v in sorted(signals.items()):
    print(k,v)
