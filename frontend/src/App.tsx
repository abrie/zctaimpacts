import { useState } from "react";
import { MapContainer, TileLayer, GeoJSON, useMapEvents } from "react-leaflet";
import { LatLngExpression, Map } from "leaflet";
import axios from "axios";

const center: LatLngExpression = [33.813534, -84.403339];
const style = {
  fillColor: "green",
  weight: 2,
  opacity: 0.5,
  color: "#555",
  dashArray: "1",
  fillOpacity: 0.1,
};
export default function App() {
  const [layers, setLayers] = useState([]);
  const [status, setStatus] = useState("");

  async function loadVisibleZCTA(map: Map) {
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
  }

  function MapComponent() {
    const map = useMapEvents({
      resize: () => {
        loadVisibleZCTA(map);
      },
      zoomend: () => {
        loadVisibleZCTA(map);
      },
      dragend: () => {
        loadVisibleZCTA(map);
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
        whenCreated={(map) => loadVisibleZCTA(map)}
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
        />
        <MapComponent />
        {layers.map(({ zipcode, geometry }) => (
          <GeoJSON key={zipcode} data={geometry} style={style} />
        ))}
      </MapContainer>
      <div className="flex-grow-0 h10 bg-gray-500 p-1 h-9 text-white">
        {status}
      </div>
    </div>
  );
}
