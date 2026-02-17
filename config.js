/**
 * Runtime Configuration for SpectraMining AI Frontend
 * This file manages API endpoint configuration for different environments
 */

window.__CONFIG__ = {
  // API Base URL - gets overridden by environment variables
  API_URL: (() => {
    // Check if running on localhost (development)
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
      return process.env.VITE_API_URL || 'http://localhost:5000/api';
    }
    
    // Production - use environment variable or fallback
    const apiUrl = process.env.VITE_API_URL || window.API_URL_OVERRIDE;
    
    if (!apiUrl) {
      console.warn('API URL not configured. Please set VITE_API_URL environment variable or window.API_URL_OVERRIDE');
    }
    
    return apiUrl || 'https://your-render-service-name.onrender.com/api';
  })(),
  
  // Get the configured API URL
  getApiUrl() {
    return this.API_URL;
  },
  
  // Check if API is properly configured
  isConfigured() {
    return this.API_URL && !this.API_URL.includes('your-render');
  },
  
  // Get API endpoint
  getEndpoint(path) {
    return `${this.API_URL}${path}`;
  }
};

// Log configuration status in development
if (window.location.hostname === 'localhost') {
  console.log('SpectraMining Config:', {
    apiUrl: window.__CONFIG__.API_URL,
    environment: 'development'
  });
}
