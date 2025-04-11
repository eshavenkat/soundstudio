import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from typing import Dict, Any, List
import pandas as pd

def create_visualizations(features: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create interactive visualizations for musical features.
    
    Args:
        features: Dictionary of musical features
        
    Returns:
        Dictionary containing Plotly figure objects
    """
    visualizations = {
        'spectral_analysis': create_spectral_plot(features),
        'mfcc_analysis': create_mfcc_plot(features),
        'onset_analysis': create_onset_plot(features)
    }
    
    return visualizations

def create_spectral_plot(features: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a spectral analysis visualization.
    
    Args:
        features: Dictionary of musical features
        
    Returns:
        Plotly figure object as dictionary
    """
    fig = go.Figure()
    
    # Add spectral features
    fig.add_trace(go.Scatter(
        x=['Spectral Centroid', 'Spectral Rolloff', 'Spectral Bandwidth'],
        y=[
            features['spectral_centroid'],
            features['spectral_rolloff'],
            features['spectral_bandwidth']
        ],
        mode='markers+lines',
        name='Spectral Features'
    ))
    
    fig.update_layout(
        title='Spectral Analysis',
        xaxis_title='Feature',
        yaxis_title='Value',
        showlegend=True
    )
    
    return fig.to_dict()

def create_mfcc_plot(features: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create an MFCC visualization.
    
    Args:
        features: Dictionary of musical features
        
    Returns:
        Plotly figure object as dictionary
    """
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=list(range(len(features['mfccs']))),
        y=features['mfccs'],
        mode='lines+markers',
        name='MFCC Coefficients'
    ))
    
    fig.update_layout(
        title='Mel-frequency Cepstral Coefficients',
        xaxis_title='Coefficient Index',
        yaxis_title='Value',
        showlegend=True
    )
    
    return fig.to_dict()

def create_onset_plot(features: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create an onset strength visualization.
    
    Args:
        features: Dictionary of musical features
        
    Returns:
        Plotly figure object as dictionary
    """
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=['Onset Strength'],
        y=[features['onset_strength']],
        mode='markers',
        name='Onset Strength'
    ))
    
    fig.update_layout(
        title='Onset Analysis',
        xaxis_title='Feature',
        yaxis_title='Strength',
        showlegend=True
    )
    
    return fig.to_dict()

def create_cluster_visualization(cluster_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a visualization for song clusters.
    
    Args:
        cluster_data: Dictionary containing clustering results
        
    Returns:
        Plotly figure object as dictionary
    """
    # Convert cluster analysis to DataFrame for easier plotting
    cluster_df = pd.DataFrame.from_dict(cluster_data['cluster_analysis'], orient='index')
    
    fig = px.scatter(
        cluster_df,
        x='avg_tempo',
        y='avg_brightness',
        size='size',
        title='Song Clusters Analysis',
        labels={
            'avg_tempo': 'Average Tempo',
            'avg_brightness': 'Average Brightness',
            'size': 'Number of Songs'
        }
    )
    
    return fig.to_dict()

def create_timeline_visualization(features_list: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Create a timeline visualization of multiple songs.
    
    Args:
        features_list: List of feature dictionaries
        
    Returns:
        Plotly figure object as dictionary
    """
    # Create DataFrame for timeline
    timeline_data = []
    for i, features in enumerate(features_list):
        timeline_data.append({
            'Song': f'Song {i+1}',
            'Tempo': features['tempo'],
            'Brightness': features['spectral_centroid'],
            'Duration': features['duration']
        })
    
    df = pd.DataFrame(timeline_data)
    
    fig = px.scatter(
        df,
        x='Duration',
        y='Tempo',
        size='Brightness',
        color='Brightness',
        title='Song Timeline Analysis',
        labels={
            'Duration': 'Duration (seconds)',
            'Tempo': 'Tempo (BPM)',
            'Brightness': 'Spectral Centroid'
        }
    )
    
    return fig.to_dict() 