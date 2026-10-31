import subprocess
import os
from pathlib import Path

class LipSyncEngine:
    def __init__(self, backend: str = "sadtalker", weights_dir: str = "checkpoints"):
        self.backend = backend.lower()
        self.weights_dir = weights_dir

    def animate(self, image_path: str, audio_path: str, output_path: str) -> str:
        """
        Drives the avatar image with the generated audio file.
        Dispatches to SadTalker or Wav2Lip CLI.
        """
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        if self.backend == "sadtalker":
            cmd = [
                "python", "inference.py",
                "--driven_audio", audio_path,
                "--source_image", image_path,
                "--result_dir", str(output_file.parent),
                "--still",
                "--preprocess", "full"
            ]
        elif self.backend == "wav2lip":
            cmd = [
                "python", "inference.py",
                "--checkpoint_path", f"{self.weights_dir}/wav2lip_gan.pth",
                "--face", image_path,
                "--audio", audio_path,
                "--outfile", str(output_file)
            ]
        else:
            raise ValueError(f"Unsupported backend: {self.backend}")

        print(f"[LipSyncEngine] Running command: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Error executing lipsync:\n{result.stderr}")
            raise RuntimeError(f"Animation failed: {result.stderr}")

        return str(output_file)
