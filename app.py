"""
SpectraMining AI - Backend API Server
Flask API for satellite-based mineral detection
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import ee
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import warnings
import logging
from datetime import datetime, timedelta
from ee_auth import initialize_earth_engine

warnings.filterwarnings('ignore')
logging.basicConfig(level=logging.INFO)

# Import legal mining sites database
from legal_mining_sites import LEGAL_MINING_AREAS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration
MY_PROJECT_ID = "spectramining"
geolocator = Nominatim(user_agent="spectramining_ai_pro_v6")

# Initialize Google Earth Engine with proper authentication
initialize_earth_engine()


def get_nearby_places(lat, lon, radius_km=5):
    """Get nearby points of interest"""
    try:
        query = f"{lat},{lon}"
        results = geolocator.reverse(query, exactly_one=False, language='en', addressdetails=True)
        
        nearby_places = []
        if results:
            for result in results[:10]:
                if hasattr(result, 'raw') and 'address' in result.raw:
                    address = result.raw['address']
                    place_name = None
                    place_type = None
                    
                    if 'mall' in address or 'shopping' in address.get('amenity', '').lower():
                        place_name = address.get('mall', address.get('shop', address.get('amenity')))
                        place_type = "Shopping"
                    elif 'school' in address or 'college' in address or 'university' in address:
                        place_name = address.get('school', address.get('college', address.get('university')))
                        place_type = "Education"
                    elif 'hospital' in address or 'clinic' in address:
                        place_name = address.get('hospital', address.get('clinic'))
                        place_type = "Healthcare"
                    elif 'hotel' in address or 'restaurant' in address:
                        place_name = address.get('hotel', address.get('restaurant'))
                        place_type = "Hospitality"
                    elif 'building' in address:
                        place_name = address.get('building')
                        place_type = "Landmark"
                    
                    if place_name and place_name not in [p['name'] for p in nearby_places]:
                        nearby_places.append({
                            'name': place_name,
                            'type': place_type,
                            'lat': result.latitude,
                            'lon': result.longitude
                        })
        
        return nearby_places[:5]
    except Exception as e:
        logging.error(f"Error getting nearby places: {e}")
        return []


def calculate_mineral_index(image, mineral_type):
    """Calculate mineral indices based on type"""
    if mineral_type == 'iron':
        return image.select('B4').divide(image.select('B2')).rename('iron_index')
    elif mineral_type == 'aluminum':
        return image.select('B11').divide(image.select('B12')).rename('aluminum_index')
    elif mineral_type == 'copper':
        red_green = image.select('B4').divide(image.select('B3'))
        nir_red = image.select('B8').divide(image.select('B4'))
        return red_green.multiply(nir_red).rename('copper_index')
    return None


def get_mineral_index_at_point(mineral_index_ee, lat, lon, mineral_name):
    """Get mineral index value at specific coordinates"""
    try:
        point = ee.Geometry.Point([lon, lat])
        sample = mineral_index_ee.sample(region=point, scale=10, geometries=True).first()
        if sample:
            mineral_value = sample.get(f'{mineral_name}_index').getInfo()
            return mineral_value
        return None
    except Exception as e:
        logging.error(f"Error getting mineral index: {e}")
        return None


def classify_location(lat, lon, mineral_coverage, mineral_name='iron'):
    """AI Classification based on proximity to legal mining areas"""
    search_point = (lat, lon)
    nearby_mines = []
    min_distance = float('inf')
    nearest_mine = None
    
    mineral_type_map = {
        'iron': 'Iron Ore',
        'aluminum': 'Bauxite/Aluminum',
        'copper': 'Copper'
    }
    
    target_mine_type = mineral_type_map.get(mineral_name, 'Iron Ore')
    
    for mine_name, (mine_lat, mine_lon, country, mine_type) in LEGAL_MINING_AREAS.items():
        if mine_type != target_mine_type:
            continue
            
        mine_point = (mine_lat, mine_lon)
        distance = geodesic(search_point, mine_point).kilometers
        
        if distance <= 10:
            nearby_mines.append({
                'name': mine_name,
                'distance': distance,
                'country': country,
                'type': mine_type
            })
        
        if distance < min_distance:
            min_distance = distance
            nearest_mine = mine_name
    
    if nearby_mines:
        classification = "Legal Mining Area"
        classification_type = "mining"
    else:
        mineral_display = mineral_name.capitalize()
        if mineral_coverage > 10:
            classification = f"Natural - High Potential {mineral_display} Deposits"
            classification_type = "high_potential"
        elif mineral_coverage > 3:
            classification = f"Natural - Moderate Potential {mineral_display} Deposits"
            classification_type = "moderate_potential"
        else:
            classification = f"Natural - Low {mineral_display} Signature"
            classification_type = "low_potential"
    
    return {
        'classification': classification,
        'classification_type': classification_type,
        'nearby_mines': nearby_mines,
        'min_distance': min_distance,
        'nearest_mine': nearest_mine
    }


@app.route('/')
def index():
    """API info endpoint"""
    return jsonify({
        'service': 'SpectraMining AI Backend',
        'version': '1.0',
        'status': 'running',
        'frontend': 'Deploy to Vercel separately'
    })


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'ee_initialized': True
    })


@app.route('/api/basemap', methods=['POST'])
def get_basemap():
    """Generate Sentinel-2 base map for given bounds"""
    try:
        data = request.json
        bounds = data.get('bounds')  # [[south, west], [north, east]]
        
        if not bounds:
            # Default global view
            bounds = [[-90, -180], [90, 180]]
        
        # Create geometry from bounds
        geometry = ee.Geometry.Rectangle(
            [bounds[0][1], bounds[0][0], bounds[1][1], bounds[1][0]]
        )
        
        # Get recent Sentinel-2 imagery (last 6 months)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=180)
        
        # Load global Sentinel-2 mosaic
        s2_collection = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED') \
            .filterDate(start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')) \
            .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 30)) \
            .select(['B4', 'B3', 'B2'])
        
        # Create median composite
        s2_mosaic = s2_collection.median()
        
        # Visualization parameters for true color
        vis_params = {
            'bands': ['B4', 'B3', 'B2'],
            'min': 0,
            'max': 3000,
            'gamma': 1.4
        }
        
        # Generate map tiles
        map_id = s2_mosaic.visualize(**vis_params).getMapId()
        
        return jsonify({
            'success': True,
            'tile_url': map_id['tile_fetcher'].url_format,
            'mapid': map_id['mapid']
        })
    
    except Exception as e:
        logging.error(f"Basemap error: {e}")
        return jsonify({'error': str(e)}), 500



@app.route('/api/geocode', methods=['POST'])
def geocode():
    """Geocode a location string to coordinates"""
    try:
        data = request.json
        location_str = data.get('location')
        
        if not location_str:
            return jsonify({'error': 'Location parameter required'}), 400
        
        location = geolocator.geocode(location_str)
        
        if not location:
            return jsonify({'error': 'Location not found'}), 404
        
        return jsonify({
            'latitude': location.latitude,
            'longitude': location.longitude,
            'address': location.address,
            'raw': location.raw
        })
    
    except Exception as e:
        logging.error(f"Geocoding error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/analyze', methods=['POST'])
def analyze_location():
    """Main analysis endpoint - processes satellite imagery and detects minerals"""
    try:
        data = request.json
        lat = float(data.get('latitude'))
        lon = float(data.get('longitude'))
        mineral_type = data.get('mineral_type', 'iron')
        
        # Define area of interest
        point = ee.Geometry.Point([lon, lat])
        roi = point.buffer(10000)  # 10km radius
        
        # Date range - last 1 year (Faster)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)
        
        # Load Sentinel-2 imagery
        collection = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED') \
            .filterBounds(roi) \
            .filterDate(start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')) \
            .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)) \
            .sort('CLOUDY_PIXEL_PERCENTAGE') \
            .limit(50)
        
        num_images = collection.size().getInfo()
        
        if num_images == 0:
            return jsonify({'error': 'No clear satellite images found for this location'}), 404
        
        # Create median composite
        median_image = collection.median().clip(roi)
        
        # Calculate mineral index
        mineral_index = calculate_mineral_index(median_image, mineral_type)
        
        # Calculate statistics (Optimized scale)
        stats = mineral_index.reduceRegion(
            reducer=ee.Reducer.mean().combine(
                ee.Reducer.stdDev(), '', True
            ),
            geometry=roi,
            scale=100,  # Optimized scale
            maxPixels=1e9
        ).getInfo()
        
        # Dynamic threshold
        mean_val = stats.get(f'{mineral_type}_index_mean', 1.5)
        std_val = stats.get(f'{mineral_type}_index_stdDev', 0.3)
        threshold = mean_val + (0.5 * std_val)
        
        # Calculate coverage percentage (Optimized scale)
        threshold_mask = mineral_index.gt(threshold)
        coverage_stats = threshold_mask.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=roi,
            scale=100,  # Optimized scale
            maxPixels=1e9
        ).getInfo()
        
        coverage_percent = coverage_stats.get(f'{mineral_type}_index', 0) * 100
        
        # Classify location
        classification_result = classify_location(lat, lon, coverage_percent, mineral_type)
        
        # Get nearby places
        nearby_places = get_nearby_places(lat, lon)
        
        # Generate map tile URLs with mineral-specific palettes
        vis_params_true_color = {
            'bands': ['B4', 'B3', 'B2'],
            'min': 0,
            'max': 3000,
            'gamma': 1.4
        }
        
        # Mineral-specific color palettes
        mineral_palettes = {
            'iron': ['#ffb3b3', '#ff9999', '#ff6b6b', '#ee5a6f', '#d63447', '#8b0000'],
            'aluminum': ['#b8f3ef', '#6ee7df', '#4ecdc4', '#44a3a0', '#2d8b85', '#1a5653'],
            'copper': ['#ffd8a8', '#ffb86c', '#ffa94d', '#ff8c42', '#e67700', '#b35900']
        }
        
        vis_params_mineral = {
            'min': threshold - 0.5,
            'max': threshold + 2.0,
            'palette': mineral_palettes.get(mineral_type, mineral_palettes['iron'])
        }
        
        vis_params_false_color = {
            'bands': ['B8', 'B4', 'B3'],
            'min': 0,
            'max': 3000,
            'gamma': 1.4
        }
        
        true_color_tile = median_image.visualize(**vis_params_true_color).getMapId()
        mineral_tile = mineral_index.visualize(**vis_params_mineral).getMapId()
        false_color_tile = median_image.visualize(**vis_params_false_color).getMapId()
        
        return jsonify({
            'success': True,
            'location': {
                'latitude': lat,
                'longitude': lon
            },
            'mineral_type': mineral_type,
            'num_images': num_images,
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'statistics': stats,
            'threshold': threshold,
            'coverage_percent': coverage_percent,
            'classification': classification_result,
            'nearby_places': nearby_places,
            'map_tiles': {
                'true_color': {
                    'url': true_color_tile['tile_fetcher'].url_format,
                    'mapid': true_color_tile['mapid']
                },
                'mineral_index': {
                    'url': mineral_tile['tile_fetcher'].url_format,
                    'mapid': mineral_tile['mapid']
                },
                'false_color': {
                    'url': false_color_tile['tile_fetcher'].url_format,
                    'mapid': false_color_tile['mapid']
                }
            }
        })
    
    except Exception as e:
        logging.error(f"Analysis error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/point-analysis', methods=['POST'])
def point_analysis():
    """Analyze mineral content at a specific point"""
    try:
        data = request.json
        lat = float(data.get('latitude'))
        lon = float(data.get('longitude'))
        center_lat = float(data.get('center_latitude'))
        center_lon = float(data.get('center_longitude'))
        mineral_type = data.get('mineral_type', 'iron')
        
        # Calculate distance from center
        distance = geodesic((lat, lon), (center_lat, center_lon)).kilometers
        
        if distance > 10:
            return jsonify({'error': 'Point outside analysis radius (10km)'}), 400
        
        # Define area of interest around center
        center_point = ee.Geometry.Point([center_lon, center_lat])
        roi = center_point.buffer(10000)
        
        # Load and process imagery (Optimized)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)
        
        collection = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED') \
            .filterBounds(roi) \
            .filterDate(start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')) \
            .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)) \
            .sort('CLOUDY_PIXEL_PERCENTAGE') \
            .limit(50)
        
        median_image = collection.median().clip(roi)
        mineral_index = calculate_mineral_index(median_image, mineral_type)
        
        # Get value at point (Optimized scale)
        mineral_value = get_mineral_index_at_point(mineral_index, lat, lon, mineral_type)
        
        if mineral_value is None:
            return jsonify({'error': 'Could not retrieve mineral index'}), 500
        
        return jsonify({
            'success': True,
            'latitude': lat,
            'longitude': lon,
            'distance_from_center': distance,
            'mineral_value': mineral_value,
            'mineral_type': mineral_type
        })
    
    except Exception as e:
        logging.error(f"Point analysis error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/legal-mines', methods=['GET'])
def get_legal_mines():
    """Get all legal mining areas"""
    mineral_type = request.args.get('mineral_type')
    country = request.args.get('country')
    
    mines = []
    for name, (lat, lon, mine_country, mine_type) in LEGAL_MINING_AREAS.items():
        if mineral_type and mine_type != mineral_type:
            continue
        if country and mine_country != country:
            continue
        
        mines.append({
            'name': name,
            'latitude': lat,
            'longitude': lon,
            'country': mine_country,
            'type': mine_type
        })
    
    return jsonify({
        'total': len(mines),
        'mines': mines
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
