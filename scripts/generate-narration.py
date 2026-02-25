#!/usr/bin/env python3
"""
Generate narrated audio for Joe's book using voice cloning (Chatterbox)
and produce word-level timestamps (Whisper).

Usage:
  python3 generate-narration.py                  # generate all chapters
  python3 generate-narration.py --chapter who-am-i
  python3 generate-narration.py --dry-run         # print extracted text only

Output:
  src/audio/joe/<chapter-id>.mp3
  src/audio/joe/<chapter-id>.json  (timestamps)
  src/audio/joe/index.json          (chapter manifest)
"""

import argparse
import html
import json
import os
import re
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
NJK_FILE = REPO_ROOT / "src" / "joe.njk"
AUDIO_DIR = REPO_ROOT / "src" / "audio" / "joe"
REFERENCE_AUDIO = Path("/Users/parachute/Downloads/joe-neyer-aljazeera.wav")

AUDIO_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# Text extraction
# ---------------------------------------------------------------------------

def strip_tags(text: str) -> str:
    """Remove HTML tags and decode entities."""
    text = re.sub(r"<figure[^>]*>.*?</figure>", " ", text, flags=re.DOTALL)
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def extract_paragraphs(html_block: str) -> list[str]:
    """Return list of non-empty paragraph texts from an HTML block."""
    paras = re.findall(r"<p[^>]*>(.*?)</p>", html_block, re.DOTALL)
    result = []
    for p in paras:
        text = strip_tags(p).strip()
        if text:
            result.append(text)
    return result


def extract_chapters(njk_path: Path) -> list[dict]:
    """Parse joe.njk and return list of chapter dicts."""
    source = njk_path.read_text(encoding="utf-8")

    # Find all <section id="..." class="joe-chapter"> blocks
    section_pattern = re.compile(
        r'<section\s+id="([^"]+)"\s+class="joe-chapter">(.*?)</section>',
        re.DOTALL,
    )

    chapters = []
    for m in section_pattern.finditer(source):
        chapter_id = m.group(1)
        content = m.group(2)

        # Get title
        title_match = re.search(r'<h2[^>]*>(.*?)</h2>', content, re.DOTALL)
        title = strip_tags(title_match.group(1)) if title_match else chapter_id.replace("-", " ").title()

        # Get text block
        text_match = re.search(r'<div class="joe-chapter__text[^"]*">(.*?)</div>', content, re.DOTALL)
        if not text_match:
            continue

        paragraphs = extract_paragraphs(text_match.group(1))
        if not paragraphs:
            continue

        chapters.append({
            "id": chapter_id,
            "title": title,
            "paragraphs": paragraphs,
        })

    return chapters


# ---------------------------------------------------------------------------
# Audio generation with Chatterbox
# ---------------------------------------------------------------------------

def generate_audio_for_chapter(chapter: dict, reference_audio: Path, output_path: Path):
    """Generate WAV audio for a chapter using Chatterbox voice clone."""
    # resemble-perth native extension doesn't load on Apple Silicon —
    # patch in the DummyWatermarker before Chatterbox imports perth.
    import perth
    if perth.PerthImplicitWatermarker is None:
        perth.PerthImplicitWatermarker = perth.DummyWatermarker
    from chatterbox.tts import ChatterboxTTS
    import torchaudio

    print(f"  Loading Chatterbox model...")
    model = ChatterboxTTS.from_pretrained(device="mps")

    all_wavs = []
    sr = model.sr

    for i, para in enumerate(chapter["paragraphs"]):
        print(f"  Generating paragraph {i+1}/{len(chapter['paragraphs'])}...")
        # Chatterbox handles moderate-length text; split very long paragraphs at sentences
        sentences = split_into_chunks(para, max_chars=400)
        for chunk in sentences:
            wav = model.generate(
                chunk,
                audio_prompt_path=str(reference_audio),
                exaggeration=0.45,
                cfg_weight=0.5,
            )
            all_wavs.append(wav)

    import torch
    combined = torch.cat(all_wavs, dim=-1)
    torchaudio.save(str(output_path), combined, sr)
    print(f"  Saved WAV: {output_path}")


def split_into_chunks(text: str, max_chars: int = 400) -> list[str]:
    """Split text into sentence-boundary chunks under max_chars."""
    if len(text) <= max_chars:
        return [text]
    sentences = re.split(r'(?<=[.!?…])\s+', text)
    chunks = []
    current = ""
    for s in sentences:
        if len(current) + len(s) + 1 <= max_chars:
            current = (current + " " + s).strip()
        else:
            if current:
                chunks.append(current)
            current = s
    if current:
        chunks.append(current)
    return chunks if chunks else [text]


# ---------------------------------------------------------------------------
# Timestamps with Whisper
# ---------------------------------------------------------------------------

def get_timestamps(wav_path: Path, chapter: dict) -> dict:
    """
    Transcribe the WAV with Whisper (word timestamps) and align back to
    the original paragraphs by matching word sequences.
    """
    import whisper

    print(f"  Transcribing with Whisper...")
    model = whisper.load_model("base")
    result = model.transcribe(str(wav_path), word_timestamps=True, language="en")

    # Flatten all words from whisper output
    all_words = []
    for seg in result["segments"]:
        for w in seg.get("words", []):
            all_words.append({
                "word": w["word"].strip(),
                "start": round(w["start"], 3),
                "end": round(w["end"], 3),
            })

    # Assign words to paragraphs by walking through sequentially
    # (Whisper transcribes the concatenated audio in order)
    total_words = len(all_words)
    para_count = len(chapter["paragraphs"])
    words_per_para = max(1, total_words // para_count)

    paragraphs_with_timing = []
    word_index = 0
    for i, para_text in enumerate(chapter["paragraphs"]):
        # Estimate how many words this paragraph has
        para_word_count = len(para_text.split())
        end_index = min(word_index + para_word_count, total_words)

        para_words = all_words[word_index:end_index]
        word_index = end_index

        if para_words:
            start = para_words[0]["start"]
            end = para_words[-1]["end"]
        else:
            # Fallback: use previous end or 0
            start = paragraphs_with_timing[-1]["end"] if paragraphs_with_timing else 0
            end = start + 3.0

        paragraphs_with_timing.append({
            "text": para_text,
            "start": round(start, 3),
            "end": round(end, 3),
            "words": para_words,
        })

    duration = all_words[-1]["end"] if all_words else 0

    return {
        "id": chapter["id"],
        "title": chapter["title"],
        "audio": f"/audio/joe/{chapter['id']}.mp3",
        "duration": round(duration, 3),
        "paragraphs": paragraphs_with_timing,
    }


# ---------------------------------------------------------------------------
# WAV → MP3 conversion
# ---------------------------------------------------------------------------

def wav_to_mp3(wav_path: Path, mp3_path: Path):
    import subprocess
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(wav_path), "-codec:a", "libmp3lame", "-qscale:a", "3", str(mp3_path)],
        check=True,
        capture_output=True,
    )
    print(f"  Converted to MP3: {mp3_path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def process_chapter(chapter: dict, reference_audio: Path, dry_run: bool = False):
    chapter_id = chapter["id"]
    wav_path = AUDIO_DIR / f"{chapter_id}.wav"
    mp3_path = AUDIO_DIR / f"{chapter_id}.mp3"
    json_path = AUDIO_DIR / f"{chapter_id}.json"

    print(f"\n{'='*60}")
    print(f"Chapter: {chapter['title']} ({chapter_id})")
    print(f"Paragraphs: {len(chapter['paragraphs'])}")
    full_text = " ".join(chapter["paragraphs"])
    print(f"Characters: {len(full_text)}")

    if dry_run:
        print("\n--- TEXT PREVIEW ---")
        for i, p in enumerate(chapter["paragraphs"]):
            print(f"[{i}] {p[:120]}{'...' if len(p) > 120 else ''}")
        return

    if mp3_path.exists() and json_path.exists():
        print(f"  Already exists, skipping. (delete to regenerate)")
        return

    # Generate audio
    if not wav_path.exists():
        generate_audio_for_chapter(chapter, reference_audio, wav_path)
    else:
        print(f"  WAV already exists, skipping generation.")

    # Get timestamps
    timestamps = get_timestamps(wav_path, chapter)

    # Convert to MP3
    wav_to_mp3(wav_path, mp3_path)
    wav_path.unlink()  # remove WAV after conversion

    # Save JSON
    json_path.write_text(json.dumps(timestamps, indent=2, ensure_ascii=False))
    print(f"  Saved timestamps: {json_path}")


def build_index(chapters: list[dict]):
    """Write index.json with chapter metadata (no paragraph text)."""
    index = []
    for ch in chapters:
        mp3_path = AUDIO_DIR / f"{ch['id']}.mp3"
        json_path = AUDIO_DIR / f"{ch['id']}.json"
        status = "ready" if (mp3_path.exists() and json_path.exists()) else "pending"
        index.append({
            "id": ch["id"],
            "title": ch["title"],
            "audio": f"/audio/joe/{ch['id']}.mp3",
            "timestamps": f"/audio/joe/{ch['id']}.json",
            "status": status,
        })
    index_path = AUDIO_DIR / "index.json"
    index_path.write_text(json.dumps(index, indent=2))
    print(f"\nWrote index: {index_path}")


def main():
    parser = argparse.ArgumentParser(description="Generate Joe's book narration")
    parser.add_argument("--chapter", help="Generate only this chapter ID")
    parser.add_argument("--dry-run", action="store_true", help="Print extracted text, don't generate")
    parser.add_argument("--reference", default=str(REFERENCE_AUDIO), help="Reference audio file for voice clone")
    args = parser.parse_args()

    reference_audio = Path(args.reference)
    if not args.dry_run and not reference_audio.exists():
        print(f"ERROR: Reference audio not found: {reference_audio}")
        sys.exit(1)

    print(f"Extracting chapters from {NJK_FILE}...")
    all_chapters = extract_chapters(NJK_FILE)
    print(f"Found {len(all_chapters)} chapters.")

    chapters_to_process = all_chapters
    if args.chapter:
        chapters_to_process = [c for c in all_chapters if c["id"] == args.chapter]
        if not chapters_to_process:
            print(f"ERROR: Chapter '{args.chapter}' not found.")
            sys.exit(1)

    for chapter in chapters_to_process:
        process_chapter(chapter, reference_audio, dry_run=args.dry_run)

    if not args.dry_run:
        # Always build index from all chapters so order is correct and new files are included
        build_index(all_chapters)


if __name__ == "__main__":
    main()
