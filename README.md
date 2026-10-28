# Zia AI — paket proyek lengkap

Paket baru dengan cakupan inti setara paket Zaralyn AI terakhir: Chat, Writer, Presentation, Voice, login workspace, history lokal, pengujian dan konfigurasi deployment. Source Zaralyn sebelumnya tidak tersedia di workspace saat pembuatan; paket ini dibuat ulang sebagai Zia AI, bukan klaim salinan byte-identik. Tidak ada AI hardcoded pada aplikasi produksi.

## 1. Kebutuhan
- Python 3.10 atau lebih baru.
- Akun API OpenAI dengan model Responses yang dapat diakses dan kredit/billing bila diperlukan.
- Untuk online: repository GitHub dan hosting Python seperti Render. Belum ada layanan dibuat/diaktifkan pada akun Anda, belum ada URL publik.
- API key harus tetap di server. Jangan kirim secret ke percakapan atau upload .env ke repository.

## 2. Setup lokal
Ekstrak ZIP. Buka terminal pada folder yang berisi app.py.

Opsional, buat virtual environment:
```
python -m venv .venv
```
Aktifkan sesuai OS: Windows `.venv\Scripts\activate`, macOS/Linux `source .venv/bin/activate`.

Instal dependency runtime:
```
pip install -r requirements.txt
```
Salin `.env.example` menjadi `.env` dan atur secara privat:
```
OPENAI_API_KEY=kunci_api_proyek_anda
OPENAI_MODEL=model_responses_yang_tersedia_untuk_proyek_anda
APP_PASSWORD=kata_sandi_workspace_kuat_minimal_12_karakter
SESSION_SECRET=rahasia_acak_panjang
APP_ORIGIN=http://localhost:3000
PORT=3000
```
Buat SESSION_SECRET secara lokal menggunakan:
```
python -c "import secrets; print(secrets.token_hex(32))"
```
Jangan bagikan outputnya. Nilai asli tidak disertakan di ZIP.

Jalankan:
```
python -m unittest -v test_app
python app.py
```
Buka http://localhost:3000 dan masuk dengan APP_PASSWORD. Jangan membuka index.html langsung atau preview lampiran. `/health` harus mengembalikan status ok. Jika model/key belum diatur, permintaan AI akan menampilkan error konfigurasi, bukan jawaban palsu.

## 3. Fitur
### Zia Chat
Pertanyaan/instruksi bahasa alami melalui OpenAI Responses API, follow-up memakai history, bahasa otomatis melalui inferensi model, chat baru, riwayat browser, cari judul, rename, delete, copy, retry, Markdown dasar dan code blocks. Metadata model/usage disimpan bersama jawaban bila dilaporkan provider. Jawaban diterima sekaligus, BUKAN streaming. Batalkan menghentikan penantian browser; pemrosesan/biaya provider mungkin masih berlanjut.
### Zia Writer
Email, surat bisnis, artikel, akademik, laporan, proposal, esai, posting, marketing, deskripsi produk, caption, creative writing, ringkasan/terjemahan. Kontrol bahasa, nada, panjang, audiens, topik. Generate/regenerate, rewrite, grammar, summarize, translate, shorten/expand, output editable, copy dan ekspor TXT. Semua generasi menggunakan backend AI sungguhan bila terkonfigurasi.
### Zia Presentation
AI menghasilkan outline JSON yang divalidasi; python-pptx membuat file PowerPoint nyata. 2–12 slide, tema Midnight/Light, poin utama, judul, catatan pembicara. Unduhan .pptx, bukan preview palsu. File dapat diuji struktur dan dibuka ulang dengan library. Belum ada charts/tabel/images. Teks padat/multibahasa tetap perlu inspeksi visual pada software presentasi. Output AI yang tidak memenuhi struktur ditolak dengan pesan error.
### Zia Voice
SpeechRecognition browser, transcript, submit ke chat yang sama, text-to-speech, pilihan suara perangkat, stop/replay, fallback teks. Input bahasa dipilih manual. Audio pengenalan dapat diproses layanan vendor browser. Bukan API suara eksternal; tidak menjamin semua browser/bahasa. Kualitas/gender suara bergantung suara yang tersedia. Bahasa jawaban mengikuti instruksi/model, bahasa audio mengikuti pilihan.

## 4. Hosting: Render
Belum di-deploy. Langkah ini memerlukan otorisasi Anda dan dapat melibatkan biaya hosting/API; periksa harga/limit terbaru sebelum menyetujui pembuatan resource. Tidak ada pembelian atau kredit disertakan.
1. Buat repository GitHub dan upload ISI folder proyek ke root repository. app.py, requirements.txt, render.yaml dan folder public harus di root. Jangan hanya upload ZIP. Jangan upload .env, .venv atau secret.
2. Di Render pilih New > Web Service, hubungkan repository dan beri otorisasi hanya yang diperlukan.
3. Runtime Python. Build command: `pip install -r requirements.txt`.
4. Start command:
```
gunicorn app:application --bind 0.0.0.0:$PORT --workers 1 --threads 4 --timeout 120
```
5. Health check: `/health`.
6. Pilih plan setelah memeriksa biaya; tidak ada janji gratis selamanya. Masukkan OPENAI_API_KEY, OPENAI_MODEL, APP_PASSWORD dan SESSION_SECRET melalui menu Environment, bukan source publik.
7. APP_ORIGIN harus persis alamat HTTPS service yang ditetapkan Render, tanpa slash akhir. Jika alamat baru diketahui setelah service dibuat, update environment dan redeploy sebelum menguji login. PORT diberikan platform. Konfigurasi Blueprint setara tersedia di render.yaml.
8. Setelah startup sukses, buka URL sebenarnya. Uji /health, login, chat, follow-up, Writer dan unduh PPTX. Periksa log yang sudah disensor. Jangan sebut live AI berhasil sebelum pertanyaan nyata terjawab.
9. Bila ingin menghubungkan domain, lakukan setelah URL platform lolos pengujian.

## 5. Biaya/provider
Chat subscription terpisah dari API. Model tidak dipilih secara hardcoded: atur OPENAI_MODEL berdasarkan akses, kualitas dan biaya proyek Anda. Tidak ada model yang dijamin tersedia. Pemrosesan token API bisa berbayar. Set batas anggaran di penyedia sebelum dipakai. Belum ada billing SaaS, cost ledger, hard spending cap atau dynamic model routing. Model dapat diganti via environment, penyedia lain membutuhkan adapter generate().

## 6. Keamanan dan privasi
Versi SINGLE-OWNER, bukan SaaS multi-user yang diaudit. APP_PASSWORD membatasi akses API. Password tidak ditulis di browser/arsip; disimpan sebagai environment secret server. Cookie signed HttpOnly, SameSite=Strict, Secure untuk HTTPS, expiry 8 jam. Logout merevoke token dalam memori proses; restart menghapus daftar revokasi. Rotasi SESSION_SECRET untuk membatalkan semua sesi lintas restart. Gunakan satu worker sesuai start command; rate/revocation belum shared-store.
Riwayat localStorage tidak terenkripsi, tidak terisolasi antar akun, dapat hilang/penuh. Jangan gunakan perangkat bersama untuk data sensitif. Logout tidak menghapus history. Ekspor data penting. Tidak ada database/cloud history, registrasi, recovery email atau pengelolaan user. Data chat tidak ditulis ke storage server oleh aplikasi. Provider tetap punya kebijakan data sendiri; store:false tidak membuktikan nol retensi log. Hapus lokal tidak menghapus data provider.
Ada validasi role/input, origin check, body limit, rate limit, timeout, pesan error aman, CSP, dan DOM rendering tanpa HTML mentah. Ini bukan sertifikasi keamanan. Rate limit per proses/socket IP tidak cocok tanpa peninjauan untuk proxy/multi-user. Tambahkan auth per-user, quota terdistribusi, privacy policy, audit dan spending protection sebelum akses publik luas. Server python app.py untuk lokal; Gunicorn untuk produksi.

## 7. Batas konteks/rendering
Maksimum 80 pesan/request, 16.000 karakter/pesan, body 250KB, konteks recent-history 40.000 karakter, output 5000 token, timeout provider 60 detik. Pesan lama bisa tidak dikirim; jumlah yang dihilangkan dilaporkan. Ini character budgeting, bukan token-exact atau ringkasan semantik. Model bisa punya batas berbeda. Tidak ada permanent AI memory. Markdown renderer sederhana mendukung heading, emphasis, list, tables, fenced code; bukan CommonMark penuh atau LaTeX.

## 8. Tes dan status
TEST-RESULTS.txt berisi hasil aktual. 11 tes lokal lulus: static/health/secrets, auth/origin/logout revocation, input/context, missing key, mock chat context, kategori error/rate, validasi slide, download PPTX, validitas ZIP dan roundtrip slides/notes. JavaScript syntax check lulus.
AI dalam tes memakai mock HANYA untuk pengujian, bukan fallback produksi. Belum ada inferensi AI langsung, verifikasi kualitas bahasa, billing error live, browser audio/mikrofon atau public deployment. Belum ada inspeksi Microsoft PowerPoint/LibreOffice. Tes struktur PPTX tidak sama dengan review visual.
BROWSER-RESULTS.txt mencatat pemeriksaan browser bila tersedia. Hanya hasil eksplisit lulus yang boleh dianggap dilakukan. Pemeriksaan dependency installation dan production Gunicorn startup belum diklaim lulus di lingkungan pembuatan.

## 9. Tes manual setelah konfigurasi
- Chat: tanya machine learning, minta dipersingkat, lalu English/Japanese. Pastikan konteks benar. Chat baru tidak membawa topik lama. Rename/search/delete/reload history.
- Writer: email formal, rewrite, translate, copy dan TXT. Draf akademik tidak boleh mengarang sumber/hasil.
- PPT: buat 6 slide, unduh, buka di PowerPoint/LibreOffice dan periksa layout, bahasa, notes; coba tema Light.
- Voice: izinkan/deny mic, cek transcript, send, dengarkan, stop/replay, fallback teks. Catat browser dan bahasa per hasil. Jangan klaim universal.
- Error: wrong password, invalid/missing model/key, long input, origin salah. Jangan sengaja menghabiskan kredit untuk tes quota.

## 10. Struktur
app.py: backend/provider/auth/PPTX
public/index.html, style.css, app.js: UI
requirements.txt: runtime
requirements-dev.txt: optional Playwright test dependency
render.yaml: deployment
.env.example: placeholder
.gitignore: cegah secret ikut Git
README.md: panduan ini
DEPLOYMENT.md: panduan ringkas deployment
TEST-RESULTS.txt: bukti tes
browser_check.py/BROWSER-RESULTS.txt: pemeriksaan browser jika disertakan

Tidak ada URL publik yang dibuat atau direkayasa. Paket ini source aplikasi yang dapat dikonfigurasi dan diuji, bukan bukti deployment sukses.
