import librosa
import numpy as np
import soundfile as sf

class AudioProcessor:
    def __init__(self, filepath):
        self.filepath = filepath
        self.y = None  # Audio time series
        self.sr = None  # Sampling rate
        self.duration = None
        self.load_audio()
    
    def load_audio(self):
        """Load audio file and extract basic information."""
        try:
            # Load audio file
            self.y, self.sr = librosa.load(self.filepath)
            
            # Get duration in seconds
            self.duration = librosa.get_duration(y=self.y, sr=self.sr)
            
        except Exception as e:
            raise Exception(f"Error loading audio file: {str(e)}")
    
    def get_audio_data(self):
        """Return the audio time series and sampling rate."""
        return self.y, self.sr
    
    def get_duration(self):
        """Return the duration of the audio in seconds."""
        return self.duration
    
    def get_onset_strength(self):
        """Calculate onset strength."""
        onset_env = librosa.onset.onset_strength(y=self.y, sr=self.sr)
        return onset_env
    
    def get_spectrogram(self, n_fft=2048, hop_length=512):
        """Calculate spectrogram."""
        D = librosa.stft(y=self.y, n_fft=n_fft, hop_length=hop_length)
        S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)
        return S_db
    
    def get_mfcc(self, n_mfcc=13):
        """Calculate MFCC features."""
        mfcc = librosa.feature.mfcc(y=self.y, sr=self.sr, n_mfcc=n_mfcc)
        return mfcc
    
    def get_spectral_centroid(self):
        """Calculate spectral centroid."""
        spectral_centroid = librosa.feature.spectral_centroid(y=self.y, sr=self.sr)
        return spectral_centroid
    
    def get_spectral_rolloff(self):
        """Calculate spectral rolloff."""
        spectral_rolloff = librosa.feature.spectral_rolloff(y=self.y, sr=self.sr)
        return spectral_rolloff
    
    def get_spectral_bandwidth(self):
        """Calculate spectral bandwidth."""
        spectral_bandwidth = librosa.feature.spectral_bandwidth(y=self.y, sr=self.sr)
        return spectral_bandwidth
    
    def get_spectral_contrast(self):
        """Calculate spectral contrast."""
        spectral_contrast = librosa.feature.spectral_contrast(y=self.y, sr=self.sr)
        return spectral_contrast
    
    def get_chroma_features(self):
        """Calculate chroma features."""
        chroma = librosa.feature.chroma_stft(y=self.y, sr=self.sr)
        return chroma
    
    def get_tempo(self):
        """Estimate tempo."""
        tempo, _ = librosa.beat.beat_track(y=self.y, sr=self.sr)
        return tempo
    
    def get_key(self):
        """Estimate musical key."""
        chroma = self.get_chroma_features()
        key_raw = np.argmax(np.mean(chroma, axis=1))
        keys = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        return keys[key_raw] 