---
name: qrcode
description: "Generate a QR code for a URL or text"
version: "1.0.0"
permissions:
  filesystem: write
  network: false
triggers:
  - command: /qrcode
metadata:
  openclaw:
    emoji: "📱"
    requires:
      bins: ["python3"]
---

## Overview

Generates a QR code for any URL or text string. Outputs a self-contained inline SVG suitable for embedding in HTML presentations, emails, or documents.

## Steps

1. Receive the URL or text to encode from the user
2. Check if the `qrcode` Python library is available:
   ```bash
   python3 -c "import qrcode" 2>/dev/null || pip3 install qrcode -q
   ```
3. Generate the QR code as inline SVG:
   ```bash
   python3 << 'EOF'
   import qrcode
   import qrcode.image.svg
   from io import BytesIO

   factory = qrcode.image.svg.SvgPathImage
   qr = qrcode.QRCode(
       version=None,
       error_correction=qrcode.constants.ERROR_CORRECT_M,
       box_size=10,
       border=1
   )
   qr.add_data('[URL_OR_TEXT]')
   qr.make(fit=True)
   img = qr.make_image(image_factory=factory)
   buf = BytesIO()
   img.save(buf)
   svg_str = buf.getvalue().decode('utf-8')
   # Extract just the <path> element for embedding
   import re
   path_match = re.search(r'<path d="([^"]+)"', svg_str)
   if path_match:
       path_d = path_match.group(1)
       print(f'<svg width="[WIDTH]" height="[WIDTH]" viewBox="0 0 35 35" xmlns="http://www.w3.org/2000/svg"><path d="{path_d}" fill="#000000" fill-rule="nonzero"/></svg>')
   EOF
   ```
4. Return the inline SVG to the user

## Output

- Inline SVG element, ready to embed in any HTML document
- No external dependencies once rendered — works in email, offline HTML, Notion
- Default size: 200x200px (adjust `width`/`height` attributes as needed)
- For dark backgrounds: add `fill="white"` to the `<path>` and a dark wrapper

## Usage Examples

- `/qrcode https://www.[the organization's domain]/start/breakthrough-call` — generates QR for breakthrough call
- `/qrcode https://[the organization's domain]` — home page QR
- Output can be saved to file: `python3 generate_qr.py > qr-output.svg`

## Error Handling

- If `qrcode` module missing: run `pip3 install qrcode` and retry
- If `pillow` is also required: `pip3 install qrcode[pil]`
- If the URL is very long (>300 chars), increase `version=5` for better readability
- Test by rendering the SVG in a browser — if modules appear square and scannable, it's correct
