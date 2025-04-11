# SoundStudio - Music Analytics Platform

A powerful music analytics and visualization platform that helps musicians analyze their music collection and gain insights through interactive visualizations.

## Features

- Audio feature extraction (tempo, key, chord progressions)
- Interactive visualizations of musical characteristics
- Song clustering based on musical features
- Production technique recommendations
- Modern, responsive web interface

## Tech Stack

- Backend: Python/Flask
- Audio Processing: librosa
- Data Analysis: pandas, numpy, scikit-learn
- Visualization: Plotly
- Frontend: HTML, CSS, JavaScript

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python app.py
   ```

## Project Structure

```
soundstudio/
├── app.py              # Main Flask application
├── static/            # Static files (CSS, JS, images)
├── templates/         # HTML templates
├── utils/            # Utility functions
│   ├── audio.py      # Audio processing functions
│   ├── analysis.py   # Music analysis functions
│   └── visualization.py # Visualization helpers
└── uploads/          # Directory for uploaded music files
```

## Usage

1. Upload your music files through the web interface
2. View detailed analysis of each track
3. Explore interactive visualizations
4. Get recommendations based on your music collection

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
