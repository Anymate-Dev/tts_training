import gradio as gr
import os
import soundfile as sf
import uuid  # Add this line
from tools.i18n.i18n import I18nAuto
from GPT_SoVITS.inference_webui import change_gpt_weights, change_sovits_weights, get_tts_wav

i18n = I18nAuto()

def synthesize( ref_audio_path, ref_text_content, ref_language, target_text_content, target_language, output_path, how_to_cut):

    

    GPT_model_path='/home/anymate/project/GPT-SoVITS/GPT_weights_v2/09070900-e50.ckpt'
    SoVITS_model_path='/home/anymate/project/GPT-SoVITS/SoVITS_weights_v2/09070900_e24_s4248.pth'

    try:
        # Change model weights
        change_gpt_weights(gpt_path=GPT_model_path)
        change_sovits_weights(sovits_path=SoVITS_model_path)

        # Synthesize audio
        synthesis_result = get_tts_wav(ref_wav_path=ref_audio_path, 
                                       prompt_text=ref_text_content, 
                                       prompt_language=i18n(ref_language), 
                                       text=target_text_content, 
                                       text_language=i18n(target_language), 
                                       top_k=30,top_p=0.5, temperature=0.5, how_to_cut=how_to_cut,
                                       ref_free=False, speed=1, if_freeze=False, inp_refs=None
                                       )
        
        result_list = list(synthesis_result)
        os.makedirs(output_path, exist_ok=True)

        if result_list:
            last_sampling_rate, last_audio_data = result_list[-1]
            unique_filename = f"output_{uuid.uuid4().hex[:8]}.wav"

            output_wav_path = os.path.join(output_path, unique_filename)
            print(f"Synthesis complete. Output path: {output_wav_path}")
            sf.write(output_wav_path, last_audio_data, last_sampling_rate)
            return output_wav_path
        else:
            print("Synthesis produced no results.")
            return None
    except Exception as e:
        print(f"An error occurred during synthesis: {str(e)}")
        return None

def gradio_synthesize(ref_audio, ref_text, ref_language, target_text, target_language, how_to_cut):
    output_path = "output"
    os.makedirs(output_path, exist_ok=True)

    output_wav_path = synthesize(ref_audio, ref_text, ref_language, target_text, target_language, output_path, how_to_cut)
    return output_wav_path

def main():
    with gr.Blocks() as server:
        gr.Markdown("# GPT-SoVITS Web Interface")
        
        ref_audio = gr.Textbox(label="Path to the Reference Audio File")
        ref_text = gr.TextArea(label="Reference Text")
        ref_language = gr.Dropdown(choices=["中文", "英文", "日文"], label="Reference Language")
        target_text = gr.TextArea(label="Target Text")
        how_to_cut = gr.TextArea(label="How to cut")
        target_language = gr.Dropdown(choices=["中文", "英文", "日文", "中英混合", "日英混合", "多语种混合"], label="Target Language")
        output_audio = gr.Audio(label="Output Audio", type="filepath")


        synthesize_button = gr.Button("Synthesize")
        synthesize_button.click(gradio_synthesize, 
                                inputs=[ref_audio, ref_text, ref_language, target_text, target_language, how_to_cut],
                                outputs=output_audio, 
                                concurrency_limit=16)

    server.launch(server_name="0.0.0.0", max_threads=16)

if __name__ == '__main__':
    main()