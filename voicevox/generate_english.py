#!/usr/bin/env python3
"""Generate English audio using VOICEVOX Core with multiple voices."""

from pathlib import Path

# Set up paths
SCRIPT_DIR = Path(__file__).parent
ONNXRUNTIME_DIR = SCRIPT_DIR / "voicevox_onnxruntime-linux-x64-1.17.3" / "lib"
DICT_DIR = SCRIPT_DIR / "open_jtalk_dic_utf_8-1.11"
MODEL_PATH = SCRIPT_DIR / "models" / "0.vvm"

# English text to synthesize
TEXT = "Hello, this is your robot vacuum speaking"

# Voice styles to use (from the 0.vvm model)
VOICES = [
    {"id": 2, "name": "shikoku_metan_normal"},
    {"id": 3, "name": "zundamon_normal"},
    {"id": 8, "name": "kasukabe_tsumugi"},
    {"id": 10, "name": "amehare_hau"},
]

def main():
    from voicevox_core.blocking import Onnxruntime, OpenJtalk, Synthesizer, VoiceModelFile

    # Load ONNX Runtime
    onnxruntime_lib = ONNXRUNTIME_DIR / Onnxruntime.LIB_VERSIONED_FILENAME
    print(f"Loading ONNX Runtime from: {onnxruntime_lib}")
    ort = Onnxruntime.load_once(filename=str(onnxruntime_lib))

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
        print("\nAvailable voices:")
        for meta in model.metas:
            print(f"  Speaker: {meta.name}")
            for style in meta.styles:
                print(f"    Style: {style.name} (ID: {style.id})")
        print()

        synthesizer.load_voice_model(model)

    # Generate audio for each voice
    print(f"Text: '{TEXT}'\n")

    output_files = []
    for voice in VOICES:
        style_id = voice["id"]
        name = voice["name"]
        output_path = SCRIPT_DIR / f"robot_vacuum_{name}.wav"

        print(f"Generating with style ID {style_id} ({name})...")
        try:
            audio_query = synthesizer.create_audio_query(TEXT, style_id)
            wav_bytes = synthesizer.synthesis(audio_query, style_id)
            output_path.write_bytes(wav_bytes)
            print(f"  Saved: {output_path} ({output_path.stat().st_size} bytes)")
            output_files.append(str(output_path))
        except Exception as e:
            print(f"  Error: {e}")

    print(f"\nGenerated {len(output_files)} audio files!")
    return output_files

if __name__ == "__main__":
    main()
