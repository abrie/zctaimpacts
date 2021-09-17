import { useState, useEffect } from "react";
import { CSSTransition } from "react-transition-group";
import { MapContainer, TileLayer, GeoJSON, useMapEvents } from "react-leaflet";
import {
  LatLngExpression,
  LeafletEventHandlerFnMap,
  LeafletMouseEvent,
  Map,
} from "leaflet";
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
  opacity: 0.15,
  color: "blue",
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
  const [isLoading, setIsLoading] = useState(false);
  const [loadedZip, setLoadedZip] = useState(undefined);

  useEffect(() => {
    (async () => {
      if (!loadedZip) {
        return;
      }
      const data = {
        zipcode: loadedZip,
      };
      setStatus("loading_zipcode");
      const response = await axios.post("/query/zipcode", data);
      console.log(response.data.results);
      setStatus("idle");
    })();
  }, [loadedZip]);

  async function loadVisibleZCTA(map: Map) {
    const bounds = map.getBounds();
    const data = {
      x1: bounds.getWest(),
      y1: bounds.getNorth(),
      x2: bounds.getEast(),
      y2: bounds.getSouth(),
    };
    setStatus("loading_zipcodes");
    setIsLoading(true);
    const response = await axios.post("/query/zcta/mbr", data);
    setLayers(response.data.results);
    setIsLoading(false);
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

  const eventHandlers: LeafletEventHandlerFnMap = {
    mouseover: (e: LeafletMouseEvent) => {
      e.target.setStyle(highlightStyle);
    },
    mouseout: (e: LeafletMouseEvent) => {
      e.target.setStyle(style);
    },
    click: (e: LeafletMouseEvent) => {
      setLoadedZip(e.propagatedFrom.feature.properties.zipcode);
    },
  };

  function geometryToFeature(
    zipcode: string,
    geometry: GeoJSON.Geometry
  ): GeoJSON.Feature {
    return {
      type: "Feature",
      properties: {
        zipcode,
      },
      geometry,
    };
  }

  return (
    <div className="container flex flex-col h-screen p-2 mx-auto">
      <MapContainer
        tap={false}
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
            data={geometryToFeature(zipcode, geometry)}
            style={style}
            eventHandlers={eventHandlers}
          />
        ))}
      </MapContainer>
      <div className="flex flex-grow-0 h10 bg-gray-400 flex-col justify-center align-middle p-1 pl-5 border-t-2 border-gray h-9 text-white rounded-b-sm font-mono font-extralight">
        <div className="w-full">
          <div className="overflow-hidden h-full mb-1 text-xs flex rounded bg-blue-200 border-1 border-white ">
            <CSSTransition
              in={isLoading}
              timeout={10000}
              classNames={{
                enter: "w-0",
                enterActive: "w-full duration-long",
                exit: "duration-75 w-0",
              }}
            >
              <div className="transition-all ease-linear shadow-none flex flex-col text-center whitespace-nowrap text-white justify-center bg-blue-500"></div>
            </CSSTransition>
          </div>
        </div>
      </div>
    </div>
  );
}
