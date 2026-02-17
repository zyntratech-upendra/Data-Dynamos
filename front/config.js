window.__CONFIG__ = {
  API_URL:
    window.location.hostname === 'localhost'
      ? 'http://localhost:5000/api'
      : 'https://data-dynamos-5tdq.onrender.com/api',

  getApiUrl() {
    return this.API_URL;
  },

  isConfigured() {
    return true;
  },

  getEndpoint(path) {
    return `${this.API_URL}${path}`;
  }
};
