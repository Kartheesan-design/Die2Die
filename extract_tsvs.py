import re

DEF_FILE = "/home/kartheesan/Desktop/3DIC/3d_stack/picorv32_with_tsvpads.def"

pins = []

with open(DEF_FILE) as f:
    lines = f.readlines()

inside = False
current_pin = None

for line in lines:
    if line.startswith("PINS"):
        inside = True
        continue

    if line.startswith("END PINS"):
        break

    if not inside:
        continue

    m = re.match(r"\s*-\s+(\S+)\s+\+ NET", line)
    if m:
        current_pin = m.group(1)
        continue

    if current_pin:
        m = re.search(r"PLACED\s+\(\s*(\d+)\s+(\d+)\s*\)", line)
        if m:
            x = int(m.group(1))/1000
            y = int(m.group(2))/1000

            if (
                current_pin == "clk"
                or current_pin.startswith("mem_addr")
                or current_pin.startswith("mem_wdata")
                or current_pin.startswith("mem_rdata")
                or current_pin.startswith("mem_wstrb")
                or current_pin in ["mem_valid","mem_ready"]
            ):
                pins.append((current_pin,x,y))

            current_pin = None

print("TSVs:", len(pins))

with open("tsv_coords.csv","w") as f:
    f.write("name,x,y\n")
    for p in pins:
        f.write(f"{p[0]},{p[1]},{p[2]}\n")
