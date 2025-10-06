🚀 Kuyy Cafe & Food – Panduan Deploy ke Render atau Vercel

1️⃣ Upload semua file project ke GitHub:
   - Folder: kuyy_cafe_food/
   - Termasuk: app.py, config.py, templates/, static/, requirements.txt, Procfile

2️⃣ Buka https://render.com (atau https://vercel.com)
   - Login dengan akun GitHub
   - Pilih "New Web Service" → pilih repo kamu

3️⃣ Render akan otomatis membaca:
   - requirements.txt untuk dependensi
   - Procfile untuk cara menjalankan server

4️⃣ Setelah deploy berhasil, web kamu bisa diakses:
   🌐 https://kuyycafe.vercel.app

5️⃣ Untuk menjalankan di lokal:
   pip install -r requirements.txt
   python app.py