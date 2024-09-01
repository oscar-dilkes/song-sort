import os

import librosa
import numpy as np
from librosa.feature import spectral_centroid
from multiprocessing import Pool

def extract_features(song):
    try:
        y, sr = librosa.load(song.filepath, mono=True)
        stft = np.abs(librosa.stft(y))
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        rms = librosa.feature.rms(S=stft, y=y).mean()
        sc = librosa.feature.spectral_centroid(S=stft, y=y, sr=sr).mean()
        zcr = librosa.feature.zero_crossing_rate(y=y).mean()

        song.set_features(tempo, rms, sc, zcr)
        compute_energy_score(song, 0.3, 0.2, 0.2)
        print(song.title + " " + str(song.energy_score))
        return song
    except FileNotFoundError:
        print(f"Audio file not found: {song.filepath}")
    except Exception as e:
        print(f"Error processing file {song.filepath}: {e}")

    return None

def para_extract(songs, num_workers = os.cpu_count()):
    with Pool(processes=num_workers) as pool:
        results = pool.map(extract_features, songs)

    return [song for song in results if song is not None]

def compute_energy_score(song, r_factor, sc_factor, zcr_factor):
    energy_score = (r_factor * song.rms) + (sc_factor * song.sc) + (zcr_factor * song.zcr)
    song.set_energy_score(energy_score)