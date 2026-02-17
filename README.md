# SpectraMining AI

Advanced Satellite-Based Multi-Mineral Exploration Platform

## 🛰️ Overview

SpectraMining AI is a cutting-edge web application that leverages Google Earth Engine and Sentinel-2 satellite imagery to detect and analyze mineral deposits across the globe. The platform provides real-time analysis of Iron, Aluminum, and Copper deposits with stunning visualizations and comprehensive data insights.

## ✨ Features

- **Multi-Mineral Detection**: Analyze Iron (Fe₂O₃), Aluminum (Al₂O₃), and Copper (Cu) deposits
- **Satellite Imagery Analysis**: Process Sentinel-2 satellite data with cloud filtering
- **Interactive Mapping**: Explore results with multiple visualization layers
  - True Color Satellite View
  - Mineral-Specific Heatmaps
  - False Color (NIR) Imagery
- **Legal Mining Database**: Compare findings with 149+ verified legal mining sites worldwide
- **Point Analysis**: Click anywhere on the map for detailed mineral index values
- **Modern UI**: Premium glassmorphism design with dark theme
- **Fast Performance**: Optimized queries for quick analysis results

## 🎨 Mineral Color Schemes

- **Iron**: Coral Red (`#ff6b6b`) - Red gradient heatmap
- **Aluminum**: Turquoise (`#4ecdc4`) - Cyan/Teal gradient heatmap
- **Copper**: Warm Orange (`#ffa94d`) - Orange/Amber gradient heatmap

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Google Earth Engine account (free)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/pujith-vijay-swamy/Data-Dynamos.git
cd Data-Dynamos
```

2. Run the application:
```bash
# Windows
run.bat

# Linux/Mac
chmod +x run.sh
./run.sh
```

3. Open your browser and navigate to:
```
http://localhost:5000
```

## 📁 Project Structure

```
SpectraMining AI/
├── backend/
│   ├── app.py                    # Flask API server
│   ├── legal_mining_sites.py     # Mining database (149 sites)
│   ├── requirements.txt          # Python dependencies
│   └── templates/
│       └── index.html            # Frontend application
├── run.bat                       # Windows launcher
├── run.sh                        # Linux/Mac launcher
└── README.md
```

## 🔧 Technology Stack

### Backend
- **Flask**: Web framework
- **Google Earth Engine**: Satellite imagery processing
- **Geopy**: Geocoding and distance calculations
- **Sentinel-2**: ESA satellite data source

### Frontend
- **React**: UI framework
- **Leaflet.js**: Interactive mapping
- **Axios**: HTTP client
- **Babel**: JSX transpilation

## 📊 How It Works

1. **Location Input**: Enter any location name or coordinates
2. **Geocoding**: Convert location to precise coordinates
3. **Satellite Query**: Fetch Sentinel-2 imagery (last 1 year, <20% cloud cover)
4. **Mineral Index Calculation**:
   - Iron: B4/B2 ratio
   - Aluminum: B11/B12 ratio
   - Copper: (B4/B3) × (B8/B4)
5. **Statistical Analysis**: Calculate mean, standard deviation, and threshold
6. **Visualization**: Generate color-coded heatmaps
7. **Classification**: Compare with legal mining database

## 🗺️ Supported Minerals

### Iron Ore (Fe₂O₃)
- 57 verified mining sites globally
- Red oxide detection using visible bands

### Aluminum/Bauxite (Al₂O₃)
- 37 verified mining sites globally
- SWIR band ratio analysis

### Copper (Cu)
- 55 verified mining sites globally
- Multi-band composite analysis

## 🌍 Global Coverage

The platform includes a comprehensive database of legal mining areas across:
- Australia, Brazil, Chile, China, India, USA
- Canada, Russia, South Africa, Sweden
- And 20+ other countries

## ⚡ Performance Optimizations

- **Reduced timeframe**: 1 year instead of 2 years
- **Stricter cloud filtering**: <20% cloud cover
- **Image limiting**: Best 50 images per analysis
- **Optimized resolution**: 100m scale for statistics
- **Efficient reducers**: Removed heavy percentile calculations

## 🎯 Use Cases

- **Geological Surveys**: Rapid mineral exploration
- **Environmental Monitoring**: Track mining activities
- **Research**: Academic and scientific studies
- **Resource Planning**: Identify potential mining sites
- **Compliance**: Verify legal mining boundaries

## 📝 API Endpoints

- `GET /` - Serve frontend application
- `GET /api/health` - Health check
- `POST /api/geocode` - Convert location to coordinates
- `POST /api/analyze` - Perform mineral analysis
- `POST /api/point-analysis` - Analyze specific point
- `GET /api/legal-mines` - Get legal mining database

## 🔐 Authentication

Google Earth Engine requires authentication. The application will guide you through the authentication process on first run.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- **Google Earth Engine**: Satellite imagery platform
- **ESA Sentinel-2**: Open satellite data
- **OpenStreetMap**: Base map tiles
- **Leaflet**: Mapping library

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Built with ❤️ for geological exploration and environmental monitoring**
