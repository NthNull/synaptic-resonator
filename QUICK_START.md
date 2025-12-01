# Quick Start Guide

## 1. Install Dependencies

```bash
pip install -r requirements.txt
```

## 2. Start the Server

```bash
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

## 3. Test the API

**Using curl:**
```bash
curl -X POST http://127.0.0.1:8000/resonate \
  -H "Content-Type: application/json" \
  -d '{"input": "Hello world"}' \
  -o output.raw
```

**Using Python:**
```python
import requests

response = requests.post(
    "http://127.0.0.1:8000/resonate",
    json={"input": "Hello world"}
)

print(response.headers.get("X-Memory-Fragment"))

with open("output.raw", "wb") as f:
    f.write(response.content)
```

## 4. Convert and Play

```bash
python3 play_audio.py output.raw --convert
# Now open output.wav in any media player!
```

## Interactive API Docs

Visit http://127.0.0.1:8000/docs in your browser to test the API interactively.

---

For complete documentation, see [README.md](README.md).

