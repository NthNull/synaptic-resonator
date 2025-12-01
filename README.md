# Synaptic Resonator API

A unique local API that transforms input data (text or numbers) into **frequency signatures** (complex audio waveforms) and cryptic **memory fragments**. Instead of returning typical JSON or XML responses, the API generates unique audio waveforms that represent the "resonance" of your input data.

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [API Reference](#api-reference)
- [Usage Examples](#usage-examples)
- [Working with Audio Files](#working-with-audio-files)
- [How It Works](#how-it-works)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)

## Overview

The Synaptic Resonator API accepts any text or numeric input and returns:
- **Frequency Signature**: A unique audio waveform (32-bit float PCM, 44.1kHz, mono, ~2 seconds)
- **Memory Fragment**: A cryptic sentence generated from your input

Each unique input produces a deterministic, reproducible output - the same input will always generate the same frequency signature and memory fragment.

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

Or if you prefer using `python3 -m pip`:

```bash
python3 -m pip install --user -r requirements.txt
```

### Step 2: Verify Installation

```bash
python3 -c "import fastapi, uvicorn, numpy; print('All dependencies installed successfully!')"
```

## Quick Start

### 1. Start the Server

```bash
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Application startup complete.
```

The `--reload` flag enables auto-reload on code changes (useful for development).

### 2. Test the API

**Using curl:**
```bash
curl -X POST http://127.0.0.1:8000/resonate \
  -H "Content-Type: application/json" \
  -d '{"input": "Hello world"}' \
  -D headers.txt \
  -o output.raw

# View the memory fragment
grep "X-Memory-Fragment" headers.txt
```

**Using Python:**
```python
import requests

response = requests.post(
    "http://127.0.0.1:8000/resonate",
    json={"input": "Hello world"}
)

print("Memory Fragment:", response.headers.get("X-Memory-Fragment"))
print("Sample Rate:", response.headers.get("X-Sample-Rate"))

# Save audio
with open("output.raw", "wb") as f:
    f.write(response.content)
```

### 3. Convert and Play Audio

```bash
# Convert .raw to .wav
python3 play_audio.py output.raw --convert

# Now open output.wav in any media player!
```

## API Reference

### Endpoint: `POST /resonate`

Transforms input data into a frequency signature and memory fragment.

#### Request

**URL:** `http://127.0.0.1:8000/resonate`

**Method:** `POST`

**Headers:**
```
Content-Type: application/json
```

**Body (JSON):**
```json
{
  "input": "Your text or number here"
}
```

**Parameters:**
- `input` (string, required): The text or number to transform

#### Response

**Status Code:** `200 OK`

**Headers:**
- `X-Memory-Fragment`: A cryptic sentence generated from the input
- `X-Sample-Rate`: Audio sample rate (always `44100`)
- `Content-Type`: `application/octet-stream`

**Body:**
- Raw audio data (32-bit float PCM, little-endian)
- Format: 44,100 Hz, Mono, ~2 seconds duration
- Size: ~352,800 bytes (88,200 samples × 4 bytes)

#### Example Response Headers

```
HTTP/1.1 200 OK
X-Memory-Fragment: Hello pulse shard flux
X-Sample-Rate: 44100
Content-Type: application/octet-stream
Content-Length: 352800
```

### Interactive API Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc

You can test the API directly from your browser using these interfaces.

## Usage Examples

### Example 1: Basic Text Input

```bash
curl -X POST http://127.0.0.1:8000/resonate \
  -H "Content-Type: application/json" \
  -d '{"input": "The quick brown fox"}' \
  -o fox.raw
```

### Example 2: Numeric Input

```bash
curl -X POST http://127.0.0.1:8000/resonate \
  -H "Content-Type: application/json" \
  -d '{"input": "42"}' \
  -o number.raw
```

### Example 3: Python Script

```python
import requests

def resonate(input_text):
    """Send input to Synaptic Resonator API"""
    response = requests.post(
        "http://127.0.0.1:8000/resonate",
        json={"input": input_text}
    )
    
    if response.status_code == 200:
        fragment = response.headers.get("X-Memory-Fragment")
        sample_rate = response.headers.get("X-Sample-Rate")
        
        print(f"Input: {input_text}")
        print(f"Memory Fragment: {fragment}")
        print(f"Sample Rate: {sample_rate} Hz")
        
        # Save audio
        filename = f"{input_text[:10].replace(' ', '_')}.raw"
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"Audio saved to: {filename}")
        
        return response.content, fragment
    else:
        print(f"Error: {response.status_code}")
        return None, None

# Test with different inputs
resonate("Hello world")
resonate("Synaptic resonance")
resonate("12345")
```

### Example 4: Batch Processing

```python
import requests
import time

inputs = [
    "First input",
    "Second input",
    "Third input"
]

for i, text in enumerate(inputs, 1):
    response = requests.post(
        "http://127.0.0.1:8000/resonate",
        json={"input": text}
    )
    
    fragment = response.headers.get("X-Memory-Fragment")
    print(f"{i}. {text} → {fragment}")
    
    with open(f"output_{i}.raw", "wb") as f:
        f.write(response.content)
    
    time.sleep(0.5)  # Be nice to the server
```

## Working with Audio Files

### Understanding .raw Files

The API returns audio in `.raw` format:
- **Format**: 32-bit float PCM (little-endian)
- **Sample Rate**: 44,100 Hz (CD quality)
- **Channels**: Mono (1 channel)
- **Duration**: ~2 seconds
- **Size**: ~352,800 bytes

This is raw binary audio data that most media players cannot open directly.

### Converting to WAV

Use the included `play_audio.py` utility:

```bash
# Convert .raw to .wav
python3 play_audio.py output.raw --convert

# This creates output.wav which can be played anywhere
```

**Options:**
- `--convert` or `-c`: Convert to WAV format
- `--info` or `-i`: Show file information
- `--play` or `-p`: Play directly (requires ffplay)
- `--output` or `-o`: Specify output filename

**Examples:**
```bash
# Show file info
python3 play_audio.py output.raw --info

# Convert with custom name
python3 play_audio.py output.raw --convert --output my_audio.wav

# Convert and play
python3 play_audio.py output.raw --convert --play
```

### Playing Audio Files

**Option 1: Convert to WAV (Recommended)**
```bash
python3 play_audio.py output.raw --convert
# Then open output.wav with any media player
```

**Option 2: Play Directly with ffplay**
```bash
ffplay -f f32le -ar 44100 -ac 1 output.raw
```

**Option 3: Use Audacity**
1. Open Audacity
2. File → Import → Raw Data
3. Select your `.raw` file
4. Set encoding to: 32-bit float
5. Set byte order to: Little-endian
6. Set channels to: 1 (Mono)
7. Set sample rate to: 44100 Hz

### Audio File Information

```bash
python3 play_audio.py output.raw --info
```

Output example:
```
File: output.raw
Size: 352,800 bytes
Samples: 88,200
Duration: 2.00 seconds
Format: 32-bit float PCM
Sample Rate: 44100 Hz
Channels: Mono
```

## How It Works

### Frequency Signature Generation

1. **Input Hashing**: The input text is converted to a deterministic seed using UUID5 hashing
2. **Random Frequency Generation**: Using the seed, 5 random frequencies are generated between 100-1200 Hz
3. **Waveform Synthesis**: Multiple sine waves at these frequencies are combined
4. **Noise Addition**: A small amount of noise (10% amplitude) is added for complexity
5. **Normalization**: The waveform is normalized to prevent clipping

### Memory Fragment Generation

1. **Word Extraction**: Words are extracted from the input text
2. **Seed Generation**: A seed is created from the sum of character codes
3. **Cryptic Combination**: A word from the input is combined with 3 abstract terms:
   - Abstract terms: "veil", "echo", "rift", "pulse", "haze", "shard", "lumen", "flux"
4. **Fragment Assembly**: The result is a cryptic sentence like "Hello pulse shard flux"

### Deterministic Behavior

The same input will **always** produce the same output:
- Same frequency signature (same audio waveform)
- Same memory fragment

This makes the API useful for:
- Data fingerprinting
- Creating unique identifiers
- Audio-based hashing
- Artistic/creative applications

## Project Structure

```
core/
├── main.py                      # FastAPI application and endpoint
├── play_audio.py                # Utility to convert/play .raw files
├── requirements.txt             # Python dependencies
├── README.md                    # This file
└── synaptic_resonator/
    ├── __init__.py
    └── generator.py             # Core waveform and fragment generation
```

### File Descriptions

- **`main.py`**: FastAPI server with the `/resonate` endpoint
- **`play_audio.py`**: Command-line utility for working with .raw audio files
- **`synaptic_resonator/generator.py`**: Core algorithms for generating waveforms and memory fragments
- **`requirements.txt`**: Python package dependencies

## Troubleshooting

### Server Won't Start

**Problem:** `Address already in use`

**Solution:** Port 8000 is already in use. Either:
- Stop the other process using port 8000
- Use a different port: `uvicorn main:app --host 127.0.0.1 --port 8001`

**Problem:** `ModuleNotFoundError`

**Solution:** Install dependencies:
```bash
pip install -r requirements.txt
```

### Can't Connect to API

**Problem:** `Connection refused` or `ConnectionError`

**Solution:** 
- Make sure the server is running
- Check the URL is correct: `http://127.0.0.1:8000/resonate`
- Verify the server is listening on the correct host/port

### Can't Play .raw Files

**Problem:** Media player can't open .raw file

**Solution:** Convert to WAV first:
```bash
python3 play_audio.py output.raw --convert
```

### Audio Sounds Distorted

**Problem:** Audio playback is distorted or too quiet/loud

**Solution:** This is normal - the waveforms are generated algorithmically and may sound unusual. The audio is normalized, but the frequency combinations can create interesting (sometimes harsh) sounds.

### Memory Fragment is Empty

**Problem:** Memory fragment header is missing or empty

**Solution:** Check that the response status is 200. If using curl, make sure to save headers:
```bash
curl -X POST ... -D headers.txt ...
```

## Advanced Usage

### Custom Server Configuration

Run on different host/port:
```bash
uvicorn main:app --host 0.0.0.0 --port 8080
```

Run without auto-reload (production):
```bash
uvicorn main:app --host 127.0.0.1 --port 8000
```

### Integration with Other Services

The API can be integrated into larger systems:

```python
# Example: Web application integration
from fastapi import FastAPI
import httpx

app = FastAPI()

@app.get("/process/{text}")
async def process_text(text: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://127.0.0.1:8000/resonate",
            json={"input": text}
        )
        return {
            "fragment": response.headers.get("X-Memory-Fragment"),
            "audio_size": len(response.content)
        }
```

## License

This project is provided as-is for educational and creative purposes.

## Contributing

Feel free to modify and extend the Synaptic Resonator API for your own projects. Some ideas:
- Add different waveform generation algorithms
- Support different audio formats (WAV, MP3)
- Add visualization of frequency signatures
- Implement batch processing endpoints
- Add audio analysis features

---

**Enjoy exploring the resonance of your data!** 🎵
