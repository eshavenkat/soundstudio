import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

class AudioAnalyzer:
    def __init__(self, processor):
        self.processor = processor
    
    def analyze(self):
        """Perform comprehensive audio analysis."""
        try:
            # Get basic audio information
            duration = self.processor.get_duration()
            tempo = self.processor.get_tempo()
            key = self.processor.get_key()
            
            # Get spectral features
            spectral_centroid = self.processor.get_spectral_centroid()
            spectral_rolloff = self.processor.get_spectral_rolloff()
            spectral_bandwidth = self.processor.get_spectral_bandwidth()
            spectral_contrast = self.processor.get_spectral_contrast()
            
            # Calculate statistical measures
            analysis_results = {
                'basic_info': {
                    'duration': duration,
                    'tempo': tempo,
                    'key': key
                },
                'spectral_features': {
                    'centroid_mean': float(np.mean(spectral_centroid)),
                    'centroid_std': float(np.std(spectral_centroid)),
                    'rolloff_mean': float(np.mean(spectral_rolloff)),
                    'rolloff_std': float(np.std(spectral_rolloff)),
                    'bandwidth_mean': float(np.mean(spectral_bandwidth)),
                    'bandwidth_std': float(np.std(spectral_bandwidth)),
                    'contrast_mean': float(np.mean(spectral_contrast)),
                    'contrast_std': float(np.std(spectral_contrast))
                },
                'rhythm_features': {
                    'onset_strength_mean': float(np.mean(self.processor.get_onset_strength())),
                    'onset_strength_std': float(np.std(self.processor.get_onset_strength()))
                },
                'timbre_features': {
                    'mfcc_mean': self.processor.get_mfcc().mean(axis=1).tolist(),
                    'mfcc_std': self.processor.get_mfcc().std(axis=1).tolist()
                }
            }
            
            # Add musical characteristics
            analysis_results['musical_characteristics'] = self._analyze_musical_characteristics()
            
            # Add production insights
            analysis_results['production_insights'] = self._analyze_production_insights()
            
            return analysis_results
            
        except Exception as e:
            raise Exception(f"Error during analysis: {str(e)}")
    
    def _analyze_musical_characteristics(self):
        """Analyze musical characteristics of the track."""
        onset_strength = self.processor.get_onset_strength()
        spectral_centroid = self.processor.get_spectral_centroid()
        
        # Calculate rhythm complexity
        rhythm_complexity = np.std(onset_strength) / np.mean(onset_strength)
        
        # Calculate timbre description
        brightness = np.mean(spectral_centroid)
        
        return {
            'rhythm_complexity': float(rhythm_complexity),
            'onset_strength': float(np.mean(onset_strength)),
            'timbre_description': self._get_timbre_description(brightness)
        }
    
    def _analyze_production_insights(self):
        """Analyze production characteristics of the track."""
        spectral_rolloff = self.processor.get_spectral_rolloff()
        spectral_bandwidth = self.processor.get_spectral_bandwidth()
        spectral_contrast = self.processor.get_spectral_contrast()
        
        # Calculate production metrics
        brightness = np.mean(spectral_rolloff)
        spectral_width = np.mean(spectral_bandwidth)
        harmonic_ratio = np.mean(spectral_contrast[0]) / np.mean(spectral_contrast[1:])
        
        return {
            'brightness': float(brightness),
            'spectral_width': float(spectral_width),
            'harmonic_ratio': float(harmonic_ratio)
        }
    
    def _get_timbre_description(self, brightness):
        """Get a human-readable description of the timbre based on brightness."""
        if brightness < 2000:
            return "Warm and mellow"
        elif brightness < 4000:
            return "Balanced"
        else:
            return "Bright and crisp"
    
    @staticmethod
    def cluster_songs(features_list, n_clusters=3):
        """Cluster multiple songs based on their features."""
        # Extract relevant features for clustering
        X = []
        for features in features_list:
            # Combine relevant features into a single vector
            feature_vector = [
                features['basic_info']['tempo'],
                features['spectral_features']['centroid_mean'],
                features['spectral_features']['bandwidth_mean'],
                features['rhythm_features']['onset_strength_mean']
            ]
            X.append(feature_vector)
        
        # Standardize features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Perform clustering
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        clusters = kmeans.fit_predict(X_scaled)
        
        return {
            'cluster_labels': clusters.tolist(),
            'cluster_centers': kmeans.cluster_centers_.tolist()
        } 