import librosa
from librosa.feature import spectral_centroid

def extract_features(path):
    try:
        y, sr = librosa.load(path)
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        rms = librosa.feature.rms(y=y).mean()
        sc = librosa.feature.spectral_centroid(y=y, sr=sr).mean()
        zcr = librosa.feature.zero_crossing_rate(y=y).mean()

        return {
            'tempo' : tempo,
            'rms' : rms,
            'spectral_centroid' : sc,
            'zero_crossing_rate' : zcr
        }
    except FileNotFoundError:
        print(f"Audio file not found: {path}")
    except Exception as e:
        print(f"Error processing file {path}: {e}")

    return {}