# Importando as bibliotecas necessárias
from pytubefix import YouTube
import whisper
import os

# Link do vídeo
video_url = "https://www.youtube.com/watch?v=vAz7MBrgQzw"

print("Iniciando o processo...")

# Definimos new_file aqui fora para que o bloco 'finally' possa acessá-lo
new_file = ""

try:
    # --- Parte 1: Download do Áudio para um Arquivo Físico ---
    yt = YouTube(video_url)
    print(f"Título do vídeo: {yt.title}")

    print("Buscando o melhor stream de áudio...")
    # Seleciona o stream de áudio de MELHOR qualidade (mais robusto)
    audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()

    print("Baixando o áudio para o disco...")
    output_file = audio_stream.download()

    base, ext = os.path.splitext(output_file)
    new_file = base + '.mp3'

    # Verifica se um arquivo com o mesmo nome já existe e o remove
    if os.path.exists(new_file):
        os.remove(new_file)
    os.rename(output_file, new_file)

    print(f"Download concluído! Áudio salvo temporariamente como: {new_file}")
    print("-" * 30)

    # --- Parte 2: Transcrição com Whisper a partir do arquivo ---
    print("Iniciando a transcrição com o Whisper...")

    model = whisper.load_model("small")

    result = model.transcribe(new_file, fp16=False, language="pt")

    transcribed_text = result["text"]

    print("Transcrição concluída!")
    print("-" * 30)
    print("Texto Transcrito:")
    print(transcribed_text)
    print("-" * 30)

except Exception as e:
    print(f"\nOcorreu um erro durante o processo: {e}")

finally:
    if new_file and os.path.exists(new_file):
        print(f"Limpando arquivo temporário: {new_file}")
        os.remove(new_file)