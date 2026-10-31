import subprocess
from pathlib import Path

class VideoCompositor:
    @staticmethod
    def add_subtitles(video_path: str, srt_path: str, output_path: str) -> str:
        """Burns styled subtitles into the bottom of the video."""
        cmd = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-vf", f"subtitles={srt_path}:force_style='FontSize=18,PrimaryColour=&H00FFFFFF,BorderStyle=3'",
            "-c:a", "copy",
            output_path
        ]
        subprocess.run(cmd, check=True)
        return output_path

    @staticmethod
    def overlay_on_background(avatar_video: str, bg_image: str, output_path: str) -> str:
        """Overlays avatar video onto a custom 16:9 or 9:16 background."""
        cmd = [
            "ffmpeg", "-y",
            "-i", bg_image,
            "-i", avatar_video,
            "-filter_complex", "[0:v][1:v]overlay=(W-w)/2:(H-h)/2[out]",
            "-map", "[out]",
            "-map", "1:a",
            "-c:v", "libx264",
            "-shortest",
            output_path
        ]
        subprocess.run(cmd, check=True)
        return output_path
