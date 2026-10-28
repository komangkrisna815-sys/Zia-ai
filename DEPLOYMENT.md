# Deployment Zia AI

Panduan lengkap ada di README.md bagian 4.

Runtime Python 3.10+. Build: `pip install -r requirements.txt`.
Start: `gunicorn app:application --bind 0.0.0.0:$PORT --workers 1 --threads 4 --timeout 120`.
Health: `/health`.
Secret server: OPENAI_API_KEY, APP_PASSWORD (12+), SESSION_SECRET.
Config: OPENAI_MODEL, APP_ORIGIN (HTTPS origin sebenarnya tanpa slash akhir).
Render Blueprint: render.yaml.

Verifikasi: service startup, health, login, real AI chat, follow-up, Writer, PPTX download, voice/manual browser compatibility. Tanpa hasil real AI, jangan tandai live integration berhasil.
Belum ada hosting dibuat, pembayaran disetujui, atau URL publik. Lakukan deployment hanya melalui akun sendiri dengan memahami biaya. Jangan mengunggah .env berisi secret.
