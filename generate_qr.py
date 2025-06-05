# generate_qr.py
import qrcode

vcard = """BEGIN:VCARD
VERSION:3.0
N:Smith;Steve;;;
FN:David Warner
ORG:Australian Cricket Team
TITLE:Batter
TEL;TYPE=CELL:+98765456789
EMAIL:david.warner@example.com
URL:https://example.com
ADR:;;678 Main St;Sydney;NSW;12345;Australia
NOTE:This is a sample vCard.
END:VCARD"""

img = qrcode.make(vcard)
img.save("static/vcard_qr.png")
