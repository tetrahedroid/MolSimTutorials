# write a simple code to convert a md.j2
# file to a md file

import sys

if len(sys.argv) != 2:
    print("Usage: python convert.py <md.j2>")
    sys.exit(1)

with open(sys.argv[1], "r") as f:
    content = f.read()

print(content)
