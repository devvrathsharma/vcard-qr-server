# generate_qr.py
import qrcode

vcard = """BEGIN:VCARD
VERSION:3.0
N:Doe;John;;;
FN:John Doe
ORG:Example Company
TITLE:Software Engineer
TEL;TYPE=CELL:+1234567890
EMAIL:john.doe@example.com
URL:https://example.com
ADR:;;123 Main St;City;State;12345;Country
NOTE:This is a sample vCard.
END:VCARD"""

img = qrcode.make(vcard)
img.save("static/vcard_qr.png")
