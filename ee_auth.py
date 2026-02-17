"""
Earth Engine Authentication Module for Render Deployment
Handles service account authentication for Render environment
"""

import json
import os
import ee
import logging
import tempfile

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def initialize_earth_engine():
    """
    Initialize Earth Engine with credentials from Render environment
    Supports both service account JSON and default project initialization
    """
    try:
        # Check for credentials JSON from environment variable
        credentials_json = os.getenv('GOOGLE_APPLICATION_CREDENTIALS_JSON')
        
        if credentials_json:
            try:
                # Parse and validate JSON
                creds_dict = json.loads(credentials_json)
                
                # Create temporary file for credentials
                with tempfile.NamedTemporaryFile(
                    mode='w',
                    suffix='.json',
                    delete=False
                ) as f:
                    json.dump(creds_dict, f)
                    credentials_path = f.name
                
                # Authenticate with service account
                credentials = ee.ServiceAccountCredentials(
                    email=creds_dict.get('client_email'),
                    key_file=credentials_path
                )
                ee.Initialize(credentials, project=creds_dict.get('project_id'))
                
                logger.info(f"✓ Earth Engine initialized with service account: {creds_dict.get('client_email')}")
                return True
                
            except json.JSONDecodeError as e:
                logger.warning(f"Invalid JSON in GOOGLE_APPLICATION_CREDENTIALS_JSON: {e}")
                # Continue with fallback
        
        # Fallback: try default initialization with project
        try:
            ee.Initialize(project='spectramining')
            logger.info("✓ Earth Engine initialized with default project 'spectramining'")
            return True
        except:
            # Last fallback: try without specifying project
            ee.Initialize()
            logger.info("✓ Earth Engine initialized with default settings")
            return True
            
    except Exception as e:
        logger.error(f"✗ Earth Engine initialization failed: {e}")
        logger.error("Earth Engine API features will not be available")
        logger.error("To fix: Set GOOGLE_APPLICATION_CREDENTIALS_JSON environment variable on Render")
        return False


def check_earth_engine_status():
    """Check if Earth Engine is properly initialized"""
    try:
        # Try a simple EE operation
        ee.List([1, 2, 3]).getInfo()
        return True
    except Exception as e:
        logger.error(f"Earth Engine status check failed: {e}")
        return False
