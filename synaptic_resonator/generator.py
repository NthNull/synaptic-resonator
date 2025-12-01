import numpy as np
import uuid

def generate_waveform(text: str, duration: float = 2.0, sample_rate: int = 44100):
    """Generate pseudo-random waveform based on input text using hash as seed."""
    seed = uuid.uuid5(uuid.NAMESPACE_DNS, text).int & 0xFFFFFFFF
    rng = np.random.default_rng(seed)
    t = np.linspace(0, duration, int(sample_rate*duration), endpoint=False)
    # create complex waveform: mix of sin with random freqs
    freqs = rng.uniform(100, 1200, size=5)
    waveform = np.zeros_like(t)
    for i in range(len(freqs)):
        waveform += np.sin(2*np.pi*freqs[i]*t + rng.uniform(0,2*np.pi))
    # add noise
    waveform += 0.1*rng.standard_normal(len(t))
    # normalize
    waveform /= np.max(np.abs(waveform))
    return waveform.astype(np.float32), sample_rate

def generate_fragment(text: str):
    words = text.split()
    seed = sum(ord(c) for c in text)
    rng = np.random.default_rng(seed)
    cryptic_word = rng.choice(words) if words else "echo"
    abstract = ["veil", "echo", "rift", "pulse", "haze", "shard", "lumen", "flux"]
    fragment_words = rng.choice(abstract, size=3)
    fragment = " ".join(fragment_words)
    return f"{cryptic_word} {fragment}"
