# Zoom Transcriber

Rekam audio sistem (Zoom, Meet, YouTube, dll) + transkrip real-time, lokal & offline.

## Install sekali

```powershell
python -m pip install numpy soundcard faster-whisper
```

## Pakai

1. Mulai / join meeting Zoom dulu, pastikan suara keluar dari speaker/headset.
2. Buka PowerShell di folder ini, lalu:

```powershell
python zoom_transcriber.py
```

3. Bicara seperti biasa. Teks muncul tiap ~5 detik.
4. `Ctrl+C` untuk berhenti.

Hasil tersimpan di folder `transcripts/`:

- `YYYY-MM-DD_HH-MM-SS.md` — transkrip dengan timestamp
- `YYYY-MM-DD_HH-MM-SS.wav` — rekaman audionya

## Opsi

| Opsi | Default | Keterangan |
|------|---------|------------|
| `--model` | `small` | `tiny`/`base` lebih cepat, `medium` lebih akurat tapi berat |
| `--chunk` | `5` | detik per potongan transkrip |
| `--lang` | `id` | `auto` untuk deteksi otomatis |
| `--device "Nama"` | speaker default | pilih output audio (lihat `--list`) |
| `--out` | `transcripts` | folder hasil |

```powershell
python zoom_transcriber.py --list          # daftar speaker
python zoom_transcriber.py --selftest      # cek logika tanpa mic/model
python zoom_transcriber.py --chunk 8 --lang auto
```

## Catatan

- Pertama kali jalan, model `small` (~460 MB) diunduh otomatis lalu disimpan di cache. Setelah itu 100% offline.
- Kalau hasil kacau, cek `--list`: pilih speaker yang benar-benar dipakai Zoom (misal headset, bukan speaker internal).
- Butuh Python 3.9+.
