Notes on the experience of getting react-leaflet to work with Create React App
- Install both 'react-leaflet' and 'leaflet'
- Add leaflet css <link> to the index.html page
- Set a default size for the map in index.css
- Use Craco and the Craco Babel Include plugin to properly handle the old Leaflet javascript. See craco.config.js for the relevant code.
