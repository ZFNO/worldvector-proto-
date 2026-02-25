import pyperclip
from pathlib import Path
from bs4 import BeautifulSoup
import sys

def replace_template_with_clip_or_file(html_path="index.html", fallback_file="dtv.py"):
    # Read HTML
    html = Path(html_path).read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")
    
    # Get clipboard content
    clipboard = pyperclip.paste().strip()
    
    # If clipboard empty, read fallback file
    if not clipboard:
        clipboard = Path(fallback_file).read_text(encoding="utf-8")
    
    # Find <template> tag
    template_tag = soup.find("template")
    if template_tag:
        template_tag.clear()
        template_tag.append(clipboard)
    else:
        # If no <template>, create one in <body> or <head>
        new_template = soup.new_tag("template")
        new_template.append(clipboard)
        if soup.body:
            soup.body.insert(0, new_template)
        else:
            soup.html.insert(0, new_template)
    
    # Write back
    Path(html_path).write_text(str(soup), encoding="utf-8")
    print(f"Updated {html_path}")

if __name__ == "__main__":
    # Use first command-line argument as html_path, else default
    html_path = sys.argv[1] if len(sys.argv) > 1 else "index.html"
    replace_template_with_clip_or_file(html_path)
