# VOICEVOX Audio Generation

Generate Japanese text-to-speech audio using VOICEVOX Core.

## Setup

Download the required components:

```bash
# Download the VOICEVOX downloader
curl -L -o download-linux-x64 "https://github.com/VOICEVOX/voicevox_core/releases/download/0.16.2/download-linux-x64"
chmod +x download-linux-x64

# Download ONNX Runtime
curl -L -o onnxruntime.tgz "https://github.com/VOICEVOX/onnxruntime-builder/releases/download/voicevox_onnxruntime-1.17.3/voicevox_onnxruntime-linux-x64-1.17.3.tgz"
tar -xzf onnxruntime.tgz

# Download Open JTalk dictionary
curl -L -o open_jtalk_dic.tar.gz "https://github.com/r9y9/open_jtalk/releases/download/v1.11.1/open_jtalk_dic_utf_8-1.11.tar.gz"
tar -xzf open_jtalk_dic.tar.gz

# Download voice model
mkdir -p models
curl -L -o models/0.vvm "https://github.com/VOICEVOX/voicevox_vvm/releases/download/0.16.0/0.vvm"

# Install Python package
curl -L -o voicevox_core.whl "https://github.com/VOICEVOX/voicevox_core/releases/download/0.16.2/voicevox_core-0.16.2-cp310-abi3-manylinux_2_34_x86_64.whl"
pip install ./voicevox_core.whl
```

## Usage

```bash
python generate_audio.py
```

This generates `output.wav` with Japanese speech.

## Available Voices

The 0.vvm model includes:
- 四国めたん (Shikoku Metan)
- ずんだもん (Zundamon)
- 春日部つむぎ (Kasukabe Tsumugi)
- 雨晴はう (Amehare Hau)

Each speaker has multiple styles (normal, sweet, tsundere, sexy, etc.)
