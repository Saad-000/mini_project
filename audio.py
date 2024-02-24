from pydub import AudioSegment
import os

def convert_wav_to_mp3(wav_file, mp3_file, bitrate='192k'):
    # Charger le fichier audio WAV
    audio = AudioSegment.from_wav(wav_file)
    
    # Déterminer le chemin complet du fichier de sortie MP3
    mp3_path = os.path.join(os.path.dirname(wav_file), mp3_file)
    
    # Compression du fichier audio en MP3 avec le bitrate spécifié
    audio.export(mp3_path, format="mp3", bitrate=bitrate)

# Demander à l'utilisateur de saisir le chemin du fichier WAV
wav_path = input("Entrez le chemin complet du fichier WAV : ")

# Demander à l'utilisateur de saisir le nom du fichier MP3 de sortie
mp3_filename = input("Entrez le nom du fichier MP3 de sortie : ")

# Utilisation de la fonction pour convertir le fichier WAV en fichier MP3
convert_wav_to_mp3(wav_path, mp3_filename)
