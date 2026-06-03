import re

mapping = {}

# clock/control
mapping["clk"] = "clk0"
mapping["mem_valid"] = "csb0"
mapping["mem_ready"] = "web0"

# wmask
for i in range(4):
    mapping[f"mem_wstrb[{i}]"] = f"wmask0[{i}]"

# address
for i in range(8):
    mapping[f"mem_addr[{i}]"] = f"addr0[{i}]"

# write data
for i in range(32):
    mapping[f"mem_wdata[{i}]"] = f"din0[{i}]"

# read data
for i in range(32):
    mapping[f"mem_rdata[{i}]"] = f"dout0[{i}]"

DIE_HEIGHT = 600000

with open("cpu_tsv_coords.txt") as f:
    lines = f.readlines()

out = []

for line in lines:
    m = re.match(r'(\S+)\s+\((\d+),\s*(\d+)\)', line)
    if not m:
        continue

    cpu_pin = m.group(1)
    x = int(m.group(2))
    y = int(m.group(3))

    if cpu_pin not in mapping:
        continue

    sram_pin = mapping[cpu_pin]

    x2 = x
    y2 = DIE_HEIGHT - y

    out.append(f"{sram_pin} ({x2},{y2})")

with open("sram_tsv_coords.txt","w") as f:
    for l in out:
        f.write(l + "\n")

print("Generated", len(out), "SRAM TSV coordinates")
