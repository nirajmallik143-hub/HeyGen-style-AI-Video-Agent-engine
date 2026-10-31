import os
import gradio as gr
from engine.tts_engine import TTSEngine, DEFAULT_VOICES
from engine.script_agent import ScriptAgent

# Initialize engines
script_agent = ScriptAgent()
tts = TTSEngine()

def generate_video(avatar_img, script_text, voice_choice, topic_prompt):
    os.makedirs("output", exist_ok=True)
    
    # 1. Generate or use user script
    if topic_prompt.strip() and not script_text.strip():
        final_script = script_agent.create_script(topic_prompt)
    else:
        final_script = script_text

    if not final_script:
        return None, "Please provide a script or prompt topic."

    # 2. Audio Generation
    tts.voice = DEFAULT_VOICES.get(voice_choice, "en-US-ChristopherNeural")
    audio_path = "output/generated_audio.mp3"
    tts.generate_speech(final_script, audio_path)

    # 3. Animate (Pass to LipSync or preview audio)
    output_video = "output/final_video.mp4"
    
    # Placeholder: when SadTalker/Wav2Lip weights are installed locally:
    # from engine.lipsync_engine import LipSyncEngine
    # engine = LipSyncEngine()
    # engine.animate(avatar_img, audio_path, output_video)

    return audio_path, f"Generated Script:\n\n{final_script}\n\nAudio saved to: {audio_path}"

with gr.Blocks(title="HeyGen-Style AI Video Agent") as demo:
    gr.Markdown("# 🎬 Free HeyGen-Style AI Video Agent Engine")
    gr.Markdown("Create professional talking-head videos with zero subscription cost.")

    with gr.Row():
        with gr.Column():
            avatar_input = gr.Image(label="Presenter Avatar Image", type="filepath")
            topic_input = gr.Textbox(label="AI Script Prompt (Optional)", placeholder="e.g. 3 Tips for Productivity")
            script_input = gr.Textbox(label="Or write your own Script", lines=4, placeholder="Hello and welcome...")
            voice_dropdown = gr.Dropdown(
                choices=list(DEFAULT_VOICES.keys()),
                value="Male (US) - Christopher",
                label="Voice Selection"
            )
            generate_btn = gr.Button("Generate Video", variant="primary")

        with gr.Column():
            audio_preview = gr.Audio(label="Generated Audio")
            status_box = gr.Textbox(label="Agent Status / Script", lines=6)
            video_preview = gr.Video(label="Generated Video Output")

    generate_btn.click(
        fn=generate_video,
        inputs=[avatar_input, script_input, voice_dropdown, topic_input],
        outputs=[audio_preview, status_box]
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
