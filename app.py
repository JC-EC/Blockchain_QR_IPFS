from flask import Flask, render_template, request, url_for
from blockchain import Blockchain
import os
import qrcode
from xhtml2pdf import pisa
import re
from unidecode import unidecode
import ipfshttpclient
from datetime import datetime , timezone
import pytz

app = Flask(__name__)

@app.template_filter("ecuador_time")
def ecuador_time(value):
    if value is None:
        return ""
    dt_utc = datetime.fromtimestamp(value, tz=timezone.utc)
    ecuador_tz = pytz.timezone("America/Guayaquil")
    dt_ecuador = dt_utc.astimezone(ecuador_tz)
    return dt_ecuador.strftime("%d/%m/%Y %H:%M:%S")

QR_FOLDER = 'static/qrs'
PDF_FOLDER = 'certificados/certs_generados'
JSON_FILE = 'registros.json'

os.makedirs(QR_FOLDER, exist_ok=True)
os.makedirs(PDF_FOLDER, exist_ok=True)

blockchain = Blockchain(file_path=JSON_FILE)
ipfs_client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001/http')

def generar_pdf(html_string, pdf_path):
    with open(pdf_path, "w+b") as f:
        pisa.CreatePDF(html_string, dest=f)

def normalizar_texto(texto):
    texto = unidecode(texto).upper()
    texto = re.sub(r'[^A-Z0-9]', '', texto)
    return texto

def subir_pdf_a_ipfs(file_path):
    if not os.path.exists(file_path):
        return None
    try:
        res = ipfs_client.add(file_path)
        cid = res['Hash']
        file_name = res['Name']
        ipfs_client.files.cp(f"/ipfs/{cid}", f"/{file_name}")
        ipfs_client.pin.add(cid)
        return f"https://ipfs.io/ipfs/{cid}"
    except Exception as e:
        print(f"Error IPFS: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registrar', methods=['POST'])
def registrar():
    tipo = request.form['tipo']
    nombre = request.form['nombre']
    apellido = request.form['apellido']

    datos = dict(request.form)
    datos['ipfs_pdf'] = None

    bloque = blockchain.add_block(datos)
    hash_code = bloque.hash
    timestamp = getattr(bloque, "timestamp", None)

    archivo_base = f"{normalizar_texto(nombre)}_{normalizar_texto(apellido)}"

    rendered_html_temp = render_template(
        'certificado.html',
        data=datos,
        hash=hash_code,
        qr_path=None,
        ipfs_pdf_url=None,
        verificar_url=url_for("verificar", hash_code=hash_code, _external=True),
        timestamp=timestamp,
        archivo_base=archivo_base
    )
    pdf_path = f"{PDF_FOLDER}/{archivo_base}.pdf"
    generar_pdf(rendered_html_temp, pdf_path)

    ipfs_pdf_url = subir_pdf_a_ipfs(pdf_path)
    datos['ipfs_pdf'] = ipfs_pdf_url

    qr_path = f"{QR_FOLDER}/{archivo_base}.png"
    qr_content = ipfs_pdf_url or url_for("verificar", hash_code=hash_code, _external=True)
    qrcode.make(qr_content).save(qr_path)

    rendered_html_final = render_template(
        'certificado.html',
        data=datos,
        hash=hash_code,
        qr_path=qr_path,
        ipfs_pdf_url=ipfs_pdf_url,
        verificar_url=url_for("verificar", hash_code=hash_code, _external=True),
        timestamp=timestamp,
        archivo_base=archivo_base
    )
    generar_pdf(rendered_html_final, pdf_path)

    return render_template(
        'certificado.html',
        data=datos,
        hash=hash_code,
        qr_path=qr_path,
        ipfs_pdf_url=ipfs_pdf_url,
        verificar_url=url_for("verificar", hash_code=hash_code, _external=True),
        timestamp=timestamp,
        archivo_base=archivo_base
    )

@app.route('/verificar/<hash_code>')
def verificar(hash_code):
    certificado = next((b for b in blockchain.chain if b.hash == hash_code), None)
    return render_template("verificar.html", certificado=certificado, hash_code=hash_code)

if __name__ == '__main__':
    app.run(debug=True)
