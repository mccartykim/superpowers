#!/usr/bin/env python3
"""Generate audio using VOICEVOX Core."""

import os
from pathlib import Path

# Set up paths
SCRIPT_DIR = Path(__file__).parent
ONNXRUNTIME_DIR = SCRIPT_DIR / "voicevox_onnxruntime-linux-x64-1.17.3" / "lib"
DICT_DIR = SCRIPT_DIR / "open_jtalk_dic_utf_8-1.11"
MODEL_PATH = SCRIPT_DIR / "models" / "0.vvm"
OUTPUT_PATH = SCRIPT_DIR / "output.wav"

# Text to synthesize (Japanese)
TEXT = "こんにちは、世界！私はボイスボックスです。"

def main():
    from voicevox_core.blocking import Onnxruntime, OpenJtalk, Synthesizer, VoiceModelFile

    # Find the ONNX runtime library
    onnxruntime_lib = ONNXRUNTIME_DIR / Onnxruntime.LIB_VERSIONED_FILENAME
    print(f"Loading ONNX Runtime from: {onnxruntime_lib}")

    # Load ONNX Runtime
    ort = Onnxruntime.load_once(filename=str(onnxruntime_lib))
    print(f"ONNX Runtime loaded. Supported devices: {ort.supported_devices()}")

    # Initialize Open JTalk
    print(f"Loading Open JTalk dictionary from: {DICT_DIR}")
    open_jtalk = OpenJtalk(str(DICT_DIR))

    # Create synthesizer
    print("Creating synthesizer...")
    synthesizer = Synthesizer(ort, open_jtalk)

    # Load voice model
    print(f"Loading voice model from: {MODEL_PATH}")
    with VoiceModelFile.open(str(MODEL_PATH)) as model:
        # Show available speakers/styles
        for meta in model.metas:
            print(f"  Speaker: {meta.name}")
            for style in meta.styles:
                print(f"    Style: {style.name} (ID: {style.id})")

        synthesizer.load_voice_model(model)

    # Use style_id 0 (first available style)
    style_id = 0

    # Create audio query and synthesize
    print(f"Generating audio for: '{TEXT}'")
    audio_query = synthesizer.create_audio_query(TEXT, style_id)
    wav_bytes = synthesizer.synthesis(audio_query, style_id)

    # Save to file
    OUTPUT_PATH.write_bytes(wav_bytes)
    print(f"Audio saved to: {OUTPUT_PATH}")
    print(f"File size: {OUTPUT_PATH.stat().st_size} bytes")

    return str(OUTPUT_PATH)

if __name__ == "__main__":
    main()
