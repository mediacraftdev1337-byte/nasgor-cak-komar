# -*- coding: utf-8 -*-
"""
Nama Proyek: Server API Serverless Nasi Goreng Cak Komar
Fungsi: Dioptimalkan khusus untuk berjalan di atas serverless function Vercel.
"""

from flask import Flask, request, jsonify
import qrcode
import io
import base64
import json
from datetime import datetime

# Inisialisasi aplikasi server Flask
app = Flask(__name__)

# Kunci Keamanan Utama untuk enkripsi data siber Cak Komar
SECRET_KEY = "CAK_KOMAR_SUPER_SECRET"

# =======================================================
# KEAMANAN SIBER: Penanganan CORS (Cross-Origin Resource Sharing)
# =======================================================
@app.after_request
def add_cors_headers(response):
    """
    Menambahkan Header CORS agar frontend (index.html) bisa mengakses API serverless
    dari domain mana pun di Vercel tanpa diblokir browser.
    """
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    return response

# =======================================================
# [FITUR 1] API GENERATOR QR CODE MEJA DINAMIS
# =======================================================
@app.route('/api/qr/generate', methods=['GET'])
def generate_qr():
    """
    Menerima parameter 'table' via URL GET, membuat QR Code dengan URL tujuan unik,
    dan mengembalikan string gambar Base64 yang siap dipakai di HTML.
    """
    table_num = request.args.get('table', '0')
    
    # Deteksi URL host otomatis agar QR Code selalu mengarah ke domain Vercel Anda yang aktif!
    host = request.host_url
    target_url = f"{host}index.html?table={table_num}"
    
    try:
        # Spesifikasi pembuatan QR Code beresolusi tinggi dengan proteksi koreksi error (Level H)
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(target_url)
        qr.make(fit=True)
        
        # Membuat gambar QR Code dengan warna gelap premium (#1e293b)
        img = qr.make_image(fill_color="#1e293b", back_color="white")
        
        # Mengonversi format gambar PNG menjadi data teks Base64
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
        
        return jsonify({
            "status": "success",
            "table": table_num,
            "target_url": target_url,
            "qr_code_base64": f"data:image/png;base64,{img_base64}"
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Gagal memproses QR Code: {str(e)}"
        }), 500

# =======================================================
# [FITUR 7] API ENKRIPSI DATA SENSITIF
# =======================================================
@app.route('/api/security/encrypt', methods=['POST'])
def encrypt_data():
    try:
        data = request.json.get('data', '')
        if not data:
            return jsonify({"status": "error", "message": "Tidak ada data yang dikirim"}), 400
            
        # Algoritma Enkripsi XOR Dua Arah
        encrypted_chars = []
        for i, char in enumerate(data):
            key_char = SECRET_KEY[i % len(SECRET_KEY)]
            encrypted_chars.append(chr(ord(char) ^ ord(key_char)))
            
        encrypted_string = "".join(encrypted_chars)
        encoded_base64 = base64.b64encode(encrypted_string.encode('utf-8')).decode('utf-8')
        
        return jsonify({
            "status": "success",
            "original_data": data,
            "encrypted_data": encoded_base64
        })
    except Exception as e:
        return jsonify({"status": "error", "message": f"Enkripsi gagal: {str(e)}"}), 500

# =======================================================
# [FITUR 8] API CADANGAN DATA (SIMULASI SERVERLESS)
# =======================================================
@app.route('/api/backup/create', methods=['POST'])
def create_backup():
    """
    Karena Vercel bersifat Serverless (Read-Only Disk), route ini akan mengembalikan
    respons sukses agar sistem frontend secara otomatis mengunduh berkas backup (.json)
    secara lokal ke komputer pengguna.
    """
    return jsonify({
        "status": "success",
        "message": "Arsitektur Vercel Serverless aktif. Cadangan Anda akan otomatis diunduh langsung oleh browser!",
        "serverless": True
    })

# Diperlukan oleh Vercel untuk memanggil handler WSGI
# Tidak menggunakan app.run() karena Vercel yang mengontrol daur hidup server