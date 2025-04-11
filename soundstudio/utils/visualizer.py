import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class AudioVisualizer:
    def __init__(self, analyzer):
        self.analyzer = analyzer
        self.processor = analyzer.processor
    
    def create_visualizations(self):
        """Create all visualizations for the audio analysis."""
        try:
            visualizations = {
                'spectral_analysis': self._create_spectral_analysis(),
                'mfcc_analysis': self._create_mfcc_analysis(),
                'onset_analysis': self._create_onset_analysis(),
                'feature_distribution': self._create_feature_distribution()
            }
            return visualizations
        except Exception as e:
            raise Exception(f"Error creating visualizations: {str(e)}")
    
    def _create_spectral_analysis(self):
        """Create spectrogram visualization."""
        spectrogram = self.processor.get_spectrogram()
        
        fig = go.Figure(data=go.Heatmap(
            z=spectrogram,
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title='dB')
        ))
        
        fig.update_layout(
            title='Spectrogram',
            xaxis_title='Time (frames)',
            yaxis_title='Frequency (Hz)',
            height=400
        )
        
        return fig.to_json()
    
    def _create_mfcc_analysis(self):
        """Create MFCC visualization."""
        mfcc = self.processor.get_mfcc()
        
        fig = go.Figure(data=go.Heatmap(
            z=mfcc,
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title='Magnitude')
        ))
        
        fig.update_layout(
            title='MFCC Features',
            xaxis_title='Time (frames)',
            yaxis_title='MFCC Coefficients',
            height=400
        )
        
        return fig.to_json()
    
    def _create_onset_analysis(self):
        """Create onset strength visualization."""
        onset_env = self.processor.get_onset_strength()
        times = np.arange(len(onset_env)) * self.processor.sr / len(onset_env)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=times,
            y=onset_env,
            mode='lines',
            name='Onset Strength'
        ))
        
        fig.update_layout(
            title='Onset Strength Over Time',
            xaxis_title='Time (s)',
            yaxis_title='Onset Strength',
            height=400
        )
        
        return fig.to_json()
    
    def _create_feature_distribution(self):
        """Create feature distribution visualization."""
        spectral_centroid = self.processor.get_spectral_centroid()
        spectral_rolloff = self.processor.get_spectral_rolloff()
        spectral_bandwidth = self.processor.get_spectral_bandwidth()
        
        fig = make_subplots(rows=3, cols=1, subplot_titles=('Spectral Centroid', 'Spectral Rolloff', 'Spectral Bandwidth'))
        
        # Add spectral centroid
        fig.add_trace(
            go.Scatter(y=spectral_centroid[0], mode='lines', name='Centroid'),
            row=1, col=1
        )
        
        # Add spectral rolloff
        fig.add_trace(
            go.Scatter(y=spectral_rolloff[0], mode='lines', name='Rolloff'),
            row=2, col=1
        )
        
        # Add spectral bandwidth
        fig.add_trace(
            go.Scatter(y=spectral_bandwidth[0], mode='lines', name='Bandwidth'),
            row=3, col=1
        )
        
        fig.update_layout(
            height=800,
            showlegend=False,
            title_text="Spectral Feature Distributions"
        )
        
        return fig.to_json()
    
    @staticmethod
    def create_cluster_visualization(cluster_data):
        """Create visualization for song clustering results."""
        labels = cluster_data['cluster_labels']
        centers = cluster_data['cluster_centers']
        
        # Create scatter plot of cluster centers
        fig = go.Figure()
        
        # Add cluster centers
        fig.add_trace(go.Scatter(
            x=[center[0] for center in centers],
            y=[center[1] for center in centers],
            mode='markers+text',
            marker=dict(size=15),
            text=[f'Cluster {i}' for i in range(len(centers))],
            textposition="top center",
            name='Cluster Centers'
        ))
        
        fig.update_layout(
            title='Song Clusters',
            xaxis_title='Tempo (normalized)',
            yaxis_title='Spectral Centroid (normalized)',
            height=500
        )
        
        return fig.to_json()
    
    @staticmethod
    def create_timeline_visualization(features_list):
        """Create timeline visualization for multiple songs."""
        # Extract relevant features
        tempos = [features['basic_info']['tempo'] for features in features_list]
        durations = [features['basic_info']['duration'] for features in features_list]
        
        # Create timeline plot
        fig = go.Figure()
        
        # Add tempo bars
        fig.add_trace(go.Bar(
            x=durations,
            y=tempos,
            text=[f'{tempo:.1f} BPM' for tempo in tempos],
            textposition='auto',
            name='Tempo'
        ))
        
        fig.update_layout(
            title='Song Timeline Analysis',
            xaxis_title='Duration (s)',
            yaxis_title='Tempo (BPM)',
            height=400
        )
        
        return fig.to_json() 