"""Convert MP3 assets in sprites/ to OGG (and WAV if requested) using ffmpeg.

Usage:
  python3 scripts/convert_audio.py --to ogg
  python3 scripts/convert_audio.py --to wav

Requirements: `ffmpeg` must be installed and available on PATH.

The script finds .mp3 files under sprites/ and converts them alongside the original files.
"""
import subprocess
import shutil
import os
import argparse

SPRITES_DIR = os.path.join(os.path.dirname(__file__), '..', 'assets', 'audio')

CONVERT_EXTS = {
    'ogg': '.ogg',
    'wav': '.wav'
}


def ffmpeg_exists():
    return shutil.which('ffmpeg') is not None


def convert_file(src, dst):
    cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-i', src, dst]
    try:
        subprocess.check_call(cmd)
        print('Converted:', src, '->', dst)
        return True
    except subprocess.CalledProcessError as e:
        print('ffmpeg failed for', src, e)
        return False


def find_mp3_files(root):
    for dirpath, _, filenames in os.walk(root):
        for fn in filenames:
            if fn.lower().endswith('.mp3'):
                yield os.path.join(dirpath, fn)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--to', choices=['ogg', 'wav'], default='ogg', help='Target format')
    args = parser.parse_args()

    if not ffmpeg_exists():
        print('ffmpeg not found on PATH. Install ffmpeg and retry.')
        return 1

    ext = CONVERT_EXTS[args.to]
    files = list(find_mp3_files(SPRITES_DIR))
    if not files:
        print('No MP3 files found under', SPRITES_DIR)
        return 0

    for src in files:
        base, _ = os.path.splitext(src)
        dst = base + ext
        if os.path.isfile(dst):
            print('Skipping existing:', dst)
            continue
        convert_file(src, dst)
    print('Done.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
