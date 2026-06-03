import re

fname = "/home/kartheesan/Desktop/3DIC/3d_stack/picorv32_with_tsvpads.def"

with open(fname) as f:
    lines = f.readlines()

signals = {}

for i,line in enumerate(lines):

    if not line.strip().startswith("-"):
        continue

    tokens = line.split()

    if len(tokens) < 2:
        continue

    sig = tokens[1]

    for j in range(i, min(i+10, len(lines))):

        if "+ PLACED (" in lines[j]:

            m = re.search(
                r"\(\s*(\d+)\s+(\d+)\s*\)",
                lines[j]
            )

            if m:

                x = int(m.group(1))
                y = int(m.group(2))

                if y >= 520000:
                    signals[sig] = (x,y)

            break

print("TSV pads:", len(signals))

for k,v in sorted(signals.items()):
    print(k, v)
