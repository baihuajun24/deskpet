from pydub import AudioSegment
import os

def convert_mp3_to_wav():
    # Use absolute path
    assets_dir = r"C:\Users\tianh\Documents\DeskPet\resources\assets"
    
    # Input and output paths
    mp3_path = os.path.join(assets_dir, '1026.mp3')
    wav_path = os.path.join(assets_dir, '1026.wav')
    
    # Debug prints
    print(f"Assets directory: {assets_dir}")
    print(f"MP3 path: {mp3_path}")
    print(f"WAV path: {wav_path}")
    
    # Check if files exist
    if not os.path.exists(mp3_path):
        print(f"MP3 file not found at: {mp3_path}")
        return
    
    # Convert MP3 to WAV
    try:
        print("Starting conversion...")
        audio = AudioSegment.from_mp3(mp3_path)
        audio.export(wav_path, format='wav')
        print(f"Successfully converted {mp3_path} to {wav_path}")
    except Exception as e:
        print(f"Error converting audio: {e}")
        print("Note: You need to install ffmpeg to convert audio files.")
        print("Try: conda install ffmpeg")

if __name__ == "__main__":
    convert_mp3_to_wav()
