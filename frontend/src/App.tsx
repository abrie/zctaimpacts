import { useState } from "react";
import { MapContainer, TileLayer, GeoJSON, useMapEvents } from "react-leaflet";
import { LatLngExpression, LeafletEventHandlerFnMap, Map } from "leaflet";
import { RiCollageLine } from "react-icons/ri";
import axios from "axios";

const providers = [
  {
    url: "https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png",
    attribution:
      '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
  },
  {
    url:
      "https://stamen-tiles-{s}.a.ssl.fastly.net/toner-lite/{z}/{x}/{y}{r}.png",
    attribution:
      '&copy; Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
  },
];

const activeProvider = 0;

const center: LatLngExpression = [33.813534, -84.403339];
const style = {
  fillColor: "green",
  weight: 1,
  opacity: 0.1,
  color: "red",
  dashArray: "1",
  fillOpacity: 0,
};

const highlightStyle = {
  weight: 5,
  color: "lightgreen",
  dashArray: "",
  fillOpacity: 0.5,
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
    setStatus("loading_zipcodes");
    const response = await axios.post("/query/zcta/mbr", data);
    setLayers(response.data.results);
    setStatus("idle");
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

  interface StatusProps {
    status: string;
  }

  function Status({ status }: StatusProps): JSX.Element {
    switch (status) {
      case "loading_zipcodes":
        return (
          <>
            <div>
              <RiCollageLine className="h-full align-middle animate-ping text-white" />
            </div>
            <div className="ml-2 align-middle text-mono text-sm">
              Mapping zipcodes
            </div>
          </>
        );
      default:
        return <></>;
    }
  }

  const eventHandlers: LeafletEventHandlerFnMap = {
    mouseover: (e: any) => {
      e.layer.setStyle(highlightStyle);
    },
    mouseout: (e: any) => {
      e.layer.setStyle(style);
    },
  };

  return (
    <div className="container flex flex-col h-screen p-2 mx-auto">
      <MapContainer
        center={center}
        zoom={11}
        className="flex-grow w-full h-full rounded-t-lg"
        whenCreated={(map) => loadVisibleZCTA(map)}
      >
        <TileLayer
          url={providers[activeProvider].url}
          attribution={providers[activeProvider].attribution}
        />
        <MapComponent />
        {layers.map(({ zipcode, geometry }) => (
          <GeoJSON
            key={zipcode}
            data={geometry}
            style={style}
            eventHandlers={eventHandlers}
          />
        ))}
      </MapContainer>
      <div className="flex flex-row flex-grow-0 h10 bg-gray-500 p-1 pl-5 border-t-2 border-gray h-9 text-white rounded-b-sm font-mono font-extralight">
        <Status status={status} />
      </div>
    </div>
  );
}
