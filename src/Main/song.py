class Song:

    def __init__(self, track_id, title, filepath):
        self.track_id = track_id
        self.title = title
        self.filepath = filepath

        self.tempo = None
        self.rms = None
        self.sc = None
        self.zcr = None
        self.energy_score = None

    def set_features(self, tempo, rms, sc, zcr):
        self.tempo = tempo
        self.rms = rms
        self.sc = sc
        self.zcr = zcr

    def set_energy_score(self, energy_score):
        self.energy_score = int(energy_score)
