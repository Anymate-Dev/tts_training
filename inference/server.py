import gradio as gr
import os
import soundfile as sf
from tools.i18n.i18n import I18nAuto
from GPT_SoVITS.inference_webui import change_gpt_weights, change_sovits_weights, get_tts_wav

i18n = I18nAuto()

def synthesize(GPT_model_path, SoVITS_model_path, ref_audio_path, ref_text_content, ref_language, target_text_content, target_language, output_path):
    # Change model weights
    change_gpt_weights(gpt_path=GPT_model_path)
    change_sovits_weights(sovits_path=SoVITS_model_path)

    # Synthesize audio
    synthesis_result = get_tts_wav(ref_wav_path=ref_audio_path, 
                                   prompt_text=ref_text_content, 
                                   prompt_language=i18n(ref_language), 
                                   text=target_text_content, 
                                   text_language=i18n(target_language), top_p=1, temperature=1)
    
    result_list = list(synthesis_result)

    if result_list:
        last_sampling_rate, last_audio_data = result_list[-1]
        output_wav_path = os.path.join(output_path, "output.wav")
        sf.write(output_wav_path, last_audio_data, last_sampling_rate)
        return output_wav_path

def main():
    def gradio_synthesize(GPT_model_path, SoVITS_model_path, ref_audio, ref_text, ref_language, target_text, target_language):
        output_path = "output"
        os.makedirs(output_path, exist_ok=True)
        ref_audio_path = ref_audio  # ref_audio is now a file path string
        output_wav_path = synthesize(GPT_model_path, SoVITS_model_path, ref_audio_path, ref_text, ref_language, target_text, target_language, output_path)
        return output_wav_path

    with gr.Blocks() as server:
        gr.Markdown("# GPT-SoVITS Web Interface")
        GPT_model_path = gr.Textbox(label="Path to the GPT model file")
        SoVITS_model_path = gr.Textbox(label="Path to the SoVITS model file")
        ref_audio = gr.Textbox(label="Path to the Reference Audio File")
        ref_text = gr.TextArea(label="Reference Text")
        ref_language = gr.Dropdown(choices=["中文", "英文", "日文"], label="Reference Language")
        target_text = gr.TextArea(label="Target Text")
        target_language = gr.Dropdown(choices=["中文", "英文", "日文", "中英混合", "日英混合", "多语种混合"], label="Target Language")
        output_audio = gr.Audio(label="Output Audio", type="filepath")

        synthesize_button = gr.Button("Synthesize")
        synthesize_button.click(gradio_synthesize, inputs=[GPT_model_path, SoVITS_model_path, ref_audio, ref_text, ref_language, target_text, target_language], outputs=output_audio, concurrency_limit=16)

    server.launch(server_name="0.0.0.0", max_threads=16)

if __name__ == '__main__':
    main()