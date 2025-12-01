#!/usr/bin/env python3
"""
Utility to play or convert .raw audio files from the Synaptic Resonator API.

The .raw files contain:
- Format: 32-bit float PCM (little-endian)
- Sample Rate: 44100 Hz
- Channels: Mono (1 channel)
"""

import sys
import numpy as np
import argparse

def convert_to_wav(raw_file, wav_file=None):
    """Convert .raw file to .wav format for easier playback"""
    try:
        # Read raw audio data
        with open(raw_file, 'rb') as f:
            audio_data = np.frombuffer(f.read(), dtype=np.float32)
        
        # Normalize to 16-bit PCM range
        audio_data = np.clip(audio_data, -1.0, 1.0)
        audio_int16 = (audio_data * 32767).astype(np.int16)
        
        # Generate output filename if not provided
        if wav_file is None:
            wav_file = raw_file.replace('.raw', '.wav')
        
        # Write WAV file
        import wave
        with wave.open(wav_file, 'wb') as wav:
            wav.setnchannels(1)  # Mono
            wav.setsampwidth(2)  # 16-bit = 2 bytes
            wav.setframerate(44100)
            wav.writeframes(audio_int16.tobytes())
        
        print(f"✓ Converted {raw_file} to {wav_file}")
        print(f"  Duration: {len(audio_data) / 44100:.2f} seconds")
        print(f"  Samples: {len(audio_data):,}")
        return wav_file
    except Exception as e:
        print(f"Error converting file: {e}")
        return None

def play_with_ffplay(raw_file):
    """Play .raw file using ffplay"""
    import subprocess
    try:
        cmd = ['ffplay', '-f', 'f32le', '-ar', '44100', '-ac', '1', '-autoexit', raw_file]
        subprocess.run(cmd, check=True)
    except FileNotFoundError:
        print("Error: ffplay not found. Install ffmpeg to use this feature.")
        print("  Or convert to WAV first: python3 play_audio.py --convert", raw_file)
    except Exception as e:
        print(f"Error playing file: {e}")

def info(raw_file):
    """Display information about the .raw file"""
    try:
        with open(raw_file, 'rb') as f:
            data = f.read()
        
        samples = len(data) // 4  # 4 bytes per float32
        duration = samples / 44100
        
        print(f"File: {raw_file}")
        print(f"Size: {len(data):,} bytes")
        print(f"Samples: {samples:,}")
        print(f"Duration: {duration:.2f} seconds")
        print(f"Format: 32-bit float PCM")
        print(f"Sample Rate: 44100 Hz")
        print(f"Channels: Mono")
    except Exception as e:
        print(f"Error reading file: {e}")

def main():
    parser = argparse.ArgumentParser(
        description='Play or convert .raw audio files from Synaptic Resonator API'
    )
    parser.add_argument('file', help='.raw audio file to process')
    parser.add_argument('--convert', '-c', action='store_true', 
                       help='Convert to WAV format')
    parser.add_argument('--play', '-p', action='store_true',
                       help='Play the audio file (requires ffplay)')
    parser.add_argument('--info', '-i', action='store_true',
                       help='Show file information')
    parser.add_argument('--output', '-o', help='Output WAV filename')
    
    args = parser.parse_args()
    
    if args.info or (not args.convert and not args.play):
        info(args.file)
    
    if args.convert:
        convert_to_wav(args.file, args.output)
    
    if args.play:
        play_with_ffplay(args.file)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print(__doc__)
        print("\nUsage examples:")
        print("  python3 play_audio.py file.raw --info")
        print("  python3 play_audio.py file.raw --convert")
        print("  python3 play_audio.py file.raw --play")
        print("  python3 play_audio.py file.raw --convert --output output.wav")
    else:
        main()

