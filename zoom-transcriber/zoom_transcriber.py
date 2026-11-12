"""Rekam audio sistem (Zoom) + transkrip real-time pakai faster-whisper.

Jalankan:
    python zoom_transcriber.py

Opsi:
    --model small      model whisper (tiny/base/small/medium)
    --chunk 5          panjang potongan audio per transkrip (detik)
    --lang id          bahasa ("auto" untuk deteksi otomatis)
    --device "Nama"    pilih output speaker (lihat --list)
    --list             tampilkan daftar device audio
    --selftest         cek logika pemotongan audio saja

Hasil: transcripts/<tanggal>.md  +  transcripts/<tanggal>.wav
"""
import argparse
import queue
import sys
import threading
import wave
from datetime import datetime
from pathlib import Path

import numpy as np

SAMPLE_RATE = 16000
BLOCK_SECONDS = 0.25
PROMPT = "Percakapan meeting dalam bahasa Indonesia, kadang campur istilah teknis bahasa Inggris."


def iter_chunks(blocks, sr=SAMPLE_RATE, seconds=5.0):
    """Gabungkan blok audio kecil jadi potongan ~seconds detik (float32 mono)."""
    need = int(sr * seconds)
    buf, have = [], 0
    for b in blocks:
        buf.append(b)
        have += len(b)
        if have >= need:
            cat = np.concatenate(buf)
            n = len(cat) // need * need
            for i in range(0, n, need):
                yield cat[i:i + need]
            rest = cat[n:]
            buf = [rest] if len(rest) else []
            have = len(rest)
    if have:
        yield np.concatenate(buf)


def iter_queue(q):
    while True:
        item = q.get()
        if item is None:
            return
        yield item


def record(loop, q, stop, wavfile):
    """Thread perekam: baca blok kecil, simpan ke wav, kirim ke antrean."""
    try:
        with loop.recorder(samplerate=SAMPLE_RATE, channels=1) as rec:
            while not stop.is_set():
                block = np.asarray(
                    rec.record(numframes=int(SAMPLE_RATE * BLOCK_SECONDS)),
                    dtype=np.float32,
                )
                if block.ndim > 1:
                    block = block.mean(axis=1)
                pcm = (np.clip(block, -1, 1) * 32767).astype(np.int16)
                wavfile.writeframes(pcm.tobytes())
                q.put(block)
    except Exception as exc:  # noqa: BLE001
        print(f"[error rekam] {exc}", file=sys.stderr)
    finally:
        q.put(None)


def fmt(seconds):
    seconds = int(seconds)
    return f"{seconds // 3600:02d}:{seconds % 3600 // 60:02d}:{seconds % 60:02d}"


def pick_speaker(sc, wanted):
    if not wanted:
        return sc.default_speaker()
    for spk in sc.all_speakers():
        if wanted.lower() in spk.name.lower():
            return spk
    raise SystemExit(f"Speaker '{wanted}' tidak ditemukan. Coba --list.")


def list_devices():
    import soundcard as sc

    print("Output speaker:")
    for spk in sc.all_speakers():
        print("  -", spk.name)
    default = sc.default_speaker()
    loop = sc.get_microphone(default.name, include_loopback=True)
    print(f"\nDefault loopback: {loop.name}")


def selftest():
    blocks = [np.zeros(4000, np.float32) for _ in range(25)]
    assert [len(c) for c in iter_chunks(blocks, 16000, 5.0)] == [80000, 20000]
    assert [len(c) for c in iter_chunks(blocks[:20], 16000, 5.0)] == [80000]
    assert list(iter_chunks([], 16000, 5.0)) == []
    print("selftest OK")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="small")
    ap.add_argument("--chunk", type=float, default=5.0)
    ap.add_argument("--lang", default="id")
    ap.add_argument("--device", default="")
    ap.add_argument("--out", default="transcripts")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return selftest()
    if args.list:
        return list_devices()

    import soundcard as sc
    from faster_whisper import WhisperModel

    loop = sc.get_microphone(pick_speaker(sc, args.device).name, include_loopback=True)

    out_dir = Path(args.out)
    out_dir.mkdir(exist_ok=True)
    base = out_dir / datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    wav_path, md_path = base.with_suffix(".wav"), base.with_suffix(".md")

    print(f"Model        : {args.model}")
    print(f"Loopback     : {loop.name}")
    print(f"Rekaman      : {wav_path}")
    print(f"Transkrip    : {md_path}")
    print("Mulai merekam. Tekan Ctrl+C untuk berhenti.\n")

    model = WhisperModel(args.model, device="cpu", compute_type="int8")
    language = None if args.lang == "auto" else args.lang

    stop, q = threading.Event(), queue.Queue()
    wavfile = wave.open(str(wav_path), "wb")
    wavfile.setnchannels(1)
    wavfile.setsampwidth(2)
    wavfile.setframerate(SAMPLE_RATE)

    worker = threading.Thread(target=record, args=(loop, q, stop, wavfile), daemon=True)
    worker.start()

    offset = 0.0
    try:
        with open(md_path, "a", encoding="utf-8") as f:
            f.write(f"# Transkrip {base.name}\n\n")
            for chunk in iter_chunks(iter_queue(q), SAMPLE_RATE, args.chunk):
                segments, _ = model.transcribe(
                    chunk,
                    language=language,
                    task="transcribe",
                    beam_size=1,
                    vad_filter=True,
                    initial_prompt=PROMPT,
                )
                for seg in segments:
                    text = seg.text.strip()
                    if not text:
                        continue
                    line = f"[{fmt(offset + seg.start)}] {text}"
                    print(line, flush=True)
                    f.write(line + "\n")
                    f.flush()
                offset += len(chunk) / SAMPLE_RATE
    except KeyboardInterrupt:
        print("\nBerhenti.")
    finally:
        stop.set()
        worker.join(timeout=3)
        wavfile.close()
        print(f"\nTersimpan: {md_path} dan {wav_path}")


if __name__ == "__main__":
    main()
