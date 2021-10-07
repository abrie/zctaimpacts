Notes on the experience of getting react-leaflet to work with Create React App
- yarn add bot 'react-leaflet' and 'leaflet'
- If using Typescript, yarn add @types/react-leaflet
- Add leaflet css <link> to the index.html page
- Set a default size for the map in index.css
- Use Craco and the Craco Babel Include plugin to properly handle the old Leaflet javascript. See craco.config.js for the relevant code. (@dealmore/craco-plugin-babel-include)
