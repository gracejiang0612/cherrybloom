
// env-loader.js - Load environment variables in the browser
// This script should be included before config.js

(function() {
    // Load environment variables from a server endpoint or use a build process
    // For development, you can manually set the token here
    window.MAPBOX_ACCESS_TOKEN = 'pk.eyJ1IjoiZ3JhY2VqaWFuZzA2MTIiLCJhIjoiY21kcWRwcmphMDU1NDJpcHVycmRjdXdzcSJ9.buPPCMYEgXn2pWePJ3h5Sw';
    
    // For production, this should be loaded from your server
    // Example: fetch('/api/config').then(r => r.json()).then(config => {
    //     window.MAPBOX_ACCESS_TOKEN = config.mapboxToken;
    // });
})();
