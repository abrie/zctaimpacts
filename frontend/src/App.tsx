import { useState, useEffect } from "react";
import { MapContainer, TileLayer, GeoJSON, useMapEvents } from "react-leaflet";
import { LatLngExpression } from "leaflet";
import axios from "axios";

const center: LatLngExpression = [33.813534, -84.403339];
export default function App() {
  const [layers, setLayers] = useState([]);
  const [status, setStatus] = useState("");

  function MyComponent() {
    const map = useMapEvents({
      dragend: async () => {
        const bounds = map.getBounds();
        const data = {
          x1: bounds.getWest(),
          y1: bounds.getNorth(),
          x2: bounds.getEast(),
          y2: bounds.getSouth(),
        };
        setStatus("Loading zipcode areas...");
        const response = await axios.post("/gis/zcta", data);
        setLayers(response.data.results);
        setStatus("");
      },
      click: () => {
        map.locate();
      },
      locationfound: (location) => {
        console.log("location found:", location);
      },
    });
    return null;
  }

  return (
    <div className="container mx-auto flex flex-col h-screen p-2">
      <MapContainer
        center={center}
        zoom={11}
        className="w-full h-full flex-grow"
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
        />
        <MyComponent />
        {layers.map(({ zipcode, geometry }) => (
          <GeoJSON key={zipcode} data={geometry} />
        ))}
      </MapContainer>
      <div className="flex-grow-0 h10 bg-gray-500 p-1 h-9 text-white">
        {status}
      </div>
    </div>
  );
}
