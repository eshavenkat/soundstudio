import librosa
import numpy as np
import pandas as pd
from typing import Dict, Any

def extract_features(file_path: str) -> Dict[str, Any]:
    """
    Extract musical features from an audio file using librosa.
    
    Args:
        file_path: Path to the audio file
        
    Returns:
        Dictionary containing extracted features
    """
    # Load the audio file
    y, sr = librosa.load(file_path)
    
    # Extract basic features
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr).mean()
    spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr).mean()
    spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr).mean()
    
    # Extract MFCCs
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    mfccs_mean = np.mean(mfccs, axis=1)
    
    # Extract chromagram for key detection
    chromagram = librosa.feature.chroma_cqt(y=y, sr=sr)
    key = detect_key(chromagram)
    
    # Extract onset strength
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    
    # Extract harmonic and percussive components
    y_harmonic, y_percussive = librosa.effects.hpss(y)
    
    features = {
        'tempo': tempo,
        'spectral_centroid': spectral_centroid,
        'spectral_rolloff': spectral_rolloff,
        'spectral_bandwidth': spectral_bandwidth,
        'mfccs': mfccs_mean.tolist(),
        'key': key,
        'onset_strength': np.mean(onset_env),
        'harmonic_ratio': np.mean(np.abs(y_harmonic)) / (np.mean(np.abs(y_harmonic)) + np.mean(np.abs(y_percussive))),
        'duration': librosa.get_duration(y=y, sr=sr)
    }
    
    return features

def detect_key(chromagram: np.ndarray) -> str:
    """
    Detect the musical key from a chromagram.
    
    Args:
        chromagram: Chromagram matrix
        
    Returns:
        String representing the detected key
    """
    # Define key profiles (major and minor)
    major_profile = np.array([1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1])
    minor_profile = np.array([1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0])
    
    # Calculate correlation with each key profile
    major_correlation = np.correlate(np.mean(chromagram, axis=1), major_profile)
    minor_correlation = np.correlate(np.mean(chromagram, axis=1), minor_profile)
    
    # Determine if major or minor
    is_major = major_correlation > minor_correlation
    
    # Map to key names
    key_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    key_index = np.argmax(np.mean(chromagram, axis=1))
    
    return f"{key_names[key_index]} {'major' if is_major else 'minor'}"

def get_beat_frames(y: np.ndarray, sr: int) -> np.ndarray:
    """
    Get beat frames from audio signal.
    
    Args:
        y: Audio time series
        sr: Sampling rate
        
    Returns:
        Array of beat frame indices
    """
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    return beat_frames 