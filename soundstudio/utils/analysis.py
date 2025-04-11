import numpy as np
from sklearn.cluster import KMeans
from typing import Dict, List, Any
import pandas as pd

def analyze_track(features: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze musical features and generate insights.
    
    Args:
        features: Dictionary of extracted musical features
        
    Returns:
        Dictionary containing analysis results and insights
    """
    analysis = {
        'basic_info': {
            'tempo': round(features['tempo'], 2),
            'key': features['key'],
            'duration': round(features['duration'], 2),
            'duration_formatted': format_duration(features['duration'])
        },
        'spectral_analysis': {
            'brightness': round(features['spectral_centroid'], 2),
            'spectral_rolloff': round(features['spectral_rolloff'], 2),
            'spectral_bandwidth': round(features['spectral_bandwidth'], 2)
        },
        'rhythm_analysis': {
            'onset_strength': round(features['onset_strength'], 2),
            'rhythm_complexity': calculate_rhythm_complexity(features['onset_strength'])
        },
        'timbre_analysis': {
            'harmonic_ratio': round(features['harmonic_ratio'], 2),
            'timbre_description': describe_timbre(features)
        }
    }
    
    return analysis

def calculate_rhythm_complexity(onset_strength: float) -> str:
    """
    Calculate and describe rhythm complexity based on onset strength.
    
    Args:
        onset_strength: Onset strength value
        
    Returns:
        String description of rhythm complexity
    """
    if onset_strength < 0.3:
        return "Simple and steady"
    elif onset_strength < 0.6:
        return "Moderate complexity"
    else:
        return "Complex and dynamic"

def describe_timbre(features: Dict[str, Any]) -> str:
    """
    Generate a description of the track's timbre based on its features.
    
    Args:
        features: Dictionary of musical features
        
    Returns:
        String description of timbre
    """
    descriptions = []
    
    # Analyze harmonic content
    if features['harmonic_ratio'] > 0.7:
        descriptions.append("rich in harmonic content")
    elif features['harmonic_ratio'] < 0.3:
        descriptions.append("percussive and rhythmic")
    
    # Analyze spectral characteristics
    if features['spectral_centroid'] > 5000:
        descriptions.append("bright and clear")
    elif features['spectral_centroid'] < 2000:
        descriptions.append("warm and mellow")
    
    return " and ".join(descriptions) if descriptions else "balanced in tone"

def format_duration(seconds: float) -> str:
    """
    Format duration in seconds to a human-readable string.
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Formatted duration string
    """
    minutes = int(seconds // 60)
    remaining_seconds = int(seconds % 60)
    return f"{minutes}:{remaining_seconds:02d}"

def cluster_songs(features_list: List[Dict[str, Any]], n_clusters: int = 3) -> Dict[str, Any]:
    """
    Cluster songs based on their musical features.
    
    Args:
        features_list: List of feature dictionaries
        n_clusters: Number of clusters to create
        
    Returns:
        Dictionary containing clustering results
    """
    # Extract relevant features for clustering
    feature_matrix = []
    for features in features_list:
        feature_vector = [
            features['tempo'],
            features['spectral_centroid'],
            features['spectral_rolloff'],
            features['spectral_bandwidth'],
            features['onset_strength'],
            features['harmonic_ratio']
        ]
        feature_matrix.append(feature_vector)
    
    # Perform clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    clusters = kmeans.fit_predict(feature_matrix)
    
    # Analyze clusters
    cluster_analysis = {}
    for i in range(n_clusters):
        cluster_songs = [features_list[j] for j in range(len(features_list)) if clusters[j] == i]
        cluster_analysis[f'cluster_{i}'] = {
            'size': len(cluster_songs),
            'avg_tempo': np.mean([song['tempo'] for song in cluster_songs]),
            'avg_brightness': np.mean([song['spectral_centroid'] for song in cluster_songs])
        }
    
    return {
        'clusters': clusters.tolist(),
        'cluster_analysis': cluster_analysis
    } 