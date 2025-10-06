from flask import Flask, render_template, request, redirect, url_for, session, send_file
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import sqlite3, io, os
from config import ADMIN_USERNAME, ADMIN_PASSWORD

app = Flask(__name__)
app.secret_key = 'kuyy_secret_key'

DB_FILE = 'data.db'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS menu (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama TEXT NOT NULL,
        harga INTEGER NOT NULL
    )''')
    cur.execute('''CREATE TABLE IF NOT EXISTS transaksi (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item TEXT,
        total INTEGER,
        tanggal TEXT
    )''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    if 'user' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('kasir'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['user'] = username
            return redirect(url_for('kasir'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/kasir')
def kasir():
    if 'user' not in session:
        return redirect(url_for('login'))
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT * FROM menu")
    menu = cur.fetchall()
    conn.close()
    return render_template('kasir.html', menu=menu)

@app.route('/tambah_menu', methods=['POST'])
def tambah_menu():
    if 'user' not in session:
        return redirect(url_for('login'))
    nama = request.form['nama']
    harga = request.form['harga']
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("INSERT INTO menu (nama, harga) VALUES (?, ?)", (nama, harga))
    conn.commit()
    conn.close()
    return redirect(url_for('admin_page'))

@app.route('/hapus_menu/<int:id>')
def hapus_menu(id):
    if 'user' not in session:
        return redirect(url_for('login'))
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("DELETE FROM menu WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin_page'))

@app.route('/admin')
def admin_page():
    if 'user' not in session:
        return redirect(url_for('login'))
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT * FROM menu")
    menu = cur.fetchall()
    conn.close()
    return render_template('admin.html', menu=menu)

@app.route('/bayar', methods=['POST'])
def bayar():
    items = request.form.getlist('item')
    total = sum(int(harga) for harga in request.form.getlist('harga'))
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("INSERT INTO transaksi (item, total, tanggal) VALUES (?, ?, datetime('now'))", 
                (', '.join(items), total))
    conn.commit()
    conn.close()
    return render_template('pembayaran.html', items=items, total=total)

@app.route('/struk_pdf/<int:total>')
def struk_pdf(total):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    p.drawString(100, 800, "Kuyy Cafe & Food")
    p.drawString(100, 780, f"Total Pembayaran: Rp {total}")
    p.drawString(100, 760, "Terima kasih telah berbelanja!")
    p.showPage()
    p.save()
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name='struk.pdf', mimetype='application/pdf')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
    