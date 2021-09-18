import { useState, useEffect } from "react";
import { CSSTransition } from "react-transition-group";
import { MapContainer, TileLayer, GeoJSON, useMapEvents } from "react-leaflet";
import {
  LatLngExpression,
  LeafletEventHandlerFnMap,
  LeafletMouseEvent,
  Map,
} from "leaflet";
import axios from "axios";
import { debounce } from "underscore";

const DEBOUNCE_TIME_MSEC = 1000;
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

interface ProgressBarParams {
  active: boolean;
}

function ProgressBar({ active }: ProgressBarParams): JSX.Element {
  return (
    <div className="overflow-hidden h-2 flex bg-white border-b border-t border-white">
      <CSSTransition
        in={active}
        timeout={999999}
        classNames={{
          enter: "w-0",
          enterActive: "w-full duration-long",
        }}
      >
        <div className="transition-all ease-linear shadow-none bg-yellow-500"></div>
      </CSSTransition>
    </div>
  );
}

export default function App() {
  const [layers, setLayers] = useState([]);
  const [showProgress, setShowProgress] = useState(false);
  const [loadedZip, setLoadedZip] = useState(undefined);

  useEffect(() => {
    (async () => {
      if (!loadedZip) {
        return;
      }
      const data = {
        zipcode: loadedZip,
      };
      const response = await axios.post("/query/zipcode", data);
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
    setShowProgress(true);
    const response = await axios.post("/query/zcta/mbr", data);
    setLayers(response.data.results);
    setShowProgress(false);
  }

  async function loadVisibleCounties(map: Map) {
    const bounds = map.getBounds();
    const data = {
      x1: bounds.getWest(),
      y1: bounds.getNorth(),
      x2: bounds.getEast(),
      y2: bounds.getSouth(),
    };
    setShowProgress(true);
    const response = await axios.post("/query/county/mbr", data);
    setLayers(response.data.results);
    setShowProgress(false);
  }

  function MapComponent() {
    const map = useMapEvents({
      resize: debounce(() => {
        loadVisibleCounties(map);
      }, DEBOUNCE_TIME_MSEC),
      zoomend: debounce(() => {
        loadVisibleCounties(map);
      }, DEBOUNCE_TIME_MSEC),
      dragend: debounce(() => {
        loadVisibleCounties(map);
      }, DEBOUNCE_TIME_MSEC),
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
    statefp: string,
    countyfp: string,
    geometry: GeoJSON.Geometry
  ): GeoJSON.Feature {
    return {
      type: "Feature",
      properties: {
        statefp,
        countyfp,
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
        whenCreated={(map) => loadVisibleCounties(map)}
      >
        <TileLayer
          url={providers[activeProvider].url}
          attribution={providers[activeProvider].attribution}
        />
        <MapComponent />
        {layers.map(({ statefp, countyfp, geometry }, idx) => (
          <GeoJSON
            key={idx}
            data={geometryToFeature(statefp, countyfp, geometry)}
            style={style}
            eventHandlers={eventHandlers}
          />
        ))}
      </MapContainer>
      <div className="flex flex-grow-0 h10 bg-gray-400 flex-col border-t-2 border-gray rounded-b-sm">
        <ProgressBar active={showProgress} />
        <div className="flex flex-row justify-between pl-1 w-full self-center">
          <div className="text-white font-normal font-sans text-xs">
            ZCTA Impacts
          </div>
          <div className="font-thin font-mono text-xs">
            [build#{process.env.REACT_APP_CI_RUN_NUMBER}]
          </div>
        </div>
      </div>
    </div>
  );
}
