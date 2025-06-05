from flask import Flask, render_template, request
import qrcode
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    qr_generated = False
    if request.method == "POST":
        data = request.form
        vcard = f"""BEGIN:VCARD
VERSION:3.0
N:{data['lastName']};{data['firstName']};;;
FN:{data['firstName']} {data['lastName']}
ORG:{data.get('organization', '')}
TITLE:{data.get('title', '')}
TEL;TYPE=CELL:{data.get('phone', '')}
EMAIL:{data.get('email', '')}
URL:{data.get('url', '')}
ADR:;;{data.get('address', '')}
NOTE:{data.get('note', '')}
END:VCARD"""

        # Generate QR and save
        os.makedirs("static", exist_ok=True)
        img = qrcode.make(vcard)
        img.save("static/vcard_qr.png")
        qr_generated = True

    return render_template("index.html", qr_generated=qr_generated)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
