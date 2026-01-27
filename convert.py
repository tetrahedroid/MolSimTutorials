# write a simple code to convert a md.j2
# file to a md file with jinja2

import sys
import jinja2
import os

if len(sys.argv) != 2:
    print("Usage: python convert.py <md.j2>")
    sys.exit(1)

template_path = sys.argv[1]
template_dir = os.path.dirname(os.path.abspath(template_path)) or "."
template_file = os.path.basename(template_path)

loader = jinja2.FileSystemLoader(template_dir)
env = jinja2.Environment(loader=loader)

try:
    template = env.get_template(template_file)
    print(template.render())
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)
