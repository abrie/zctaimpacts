import { useState, useEffect, useRef } from "react";
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

const DEFAULT_CENTER: LatLngExpression = [33.813534, -84.403339];
const DEFAULT_ZOOM: number = 9;

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

interface QueryCountyDetailsResponse {
  industries: Industry[];
}

interface CountyDetails {
  industries: Industry[];
}

interface Industry {
  BEA_CODE: string;
  TOTAL_EMPLOYEES: number;
  TOTAL_ESTABLISHMENTS: number;
  TOTAL_PAYROLL: number;
  TOTAL_REVENUE: number;
  id: string;
  name: string;
}

interface County {
  statefp: string;
  countyfp: string;
  geoid: string;
  geometry: GeoJSON.Polygon;
}

interface QueryCountyResponse {
  results: County[];
}

function countyToFeature({
  statefp,
  countyfp,
  geometry,
}: County): GeoJSON.Feature {
  return {
    type: "Feature",
    properties: {
      statefp,
      countyfp,
    },
    geometry,
  };
}

interface CountyDetailsViewParams {
  countyDetails: CountyDetails | undefined;
}

function CountyDetailsView({
  countyDetails,
}: CountyDetailsViewParams): JSX.Element {
  if (!countyDetails) {
    return <></>;
  }
  return (
    <div className="absolute inset-0 overflow-hidden overflow-scroll">
      <div className="flex flex-col m-2 p-2 bg-white border-4 border-black">
        <div className="text-xs font-light pb-1">Community/Region Profile</div>
        <div className="text-lg font-extrabold border-b-8 pb-3 border-black">
          Georgia
        </div>
        <div className="border-b pb-1 border-black">
          <span className="text-sm font-bold pr-1">Counties:</span>
          <span className="text-sm font-light">Fulton</span>
        </div>
        <div></div>
      </div>
    </div>
  );
}

function ProgressBar({ active }: ProgressBarParams): JSX.Element {
  const nodeRef = useRef(null);
  return (
    <div className="flex h-2 overflow-hidden bg-white border-t border-b border-white">
      <CSSTransition
        nodeRef={nodeRef}
        in={active}
        timeout={999999}
        classNames={{
          enter: "w-0",
          enterActive: "w-full duration-long",
        }}
      >
        <div
          ref={nodeRef}
          className="bg-yellow-500 shadow-none transition-all ease-linear"
        ></div>
      </CSSTransition>
    </div>
  );
}

export default function App() {
  const [layers, setLayers] = useState<County[]>([]);
  const [showProgress, setShowProgress] = useState<boolean>(false);
  const [loadedCounty, setLoadedCounty] = useState<County | undefined>(
    undefined
  );
  const [loadedCountyDetails, setLoadedCountyDetails] = useState<
    CountyDetails | undefined
  >(undefined);
  const [errorMessage, setErrorMessage] = useState<string | undefined>(
    undefined
  );

  useEffect(() => {
    (async () => {
      if (!loadedCounty) {
        return;
      }
      const data = {
        statefp: loadedCounty.statefp,
        countyfp: loadedCounty.countyfp,
      };
      try {
        setShowProgress(true);
        setErrorMessage(undefined);
        const response = await axios.post<QueryCountyDetailsResponse>(
          "/query/county",
          data
        );
        setShowProgress(false);
        setLoadedCountyDetails({ industries: response.data.industries });
        console.log(response.data);
      } catch (e: unknown) {
        setShowProgress(false);
        setErrorMessage(`${e}`);
      }
    })();
  }, [loadedCounty]);

  async function loadVisibleCounties(map: Map) {
    const bounds = map.getBounds();
    const data = {
      x1: bounds.getWest(),
      y1: bounds.getNorth(),
      x2: bounds.getEast(),
      y2: bounds.getSouth(),
    };
    setShowProgress(true);
    setErrorMessage(undefined);
    try {
      const response = await axios.post<QueryCountyResponse>(
        "/query/county/mbr",
        data
      );
      setShowProgress(false);
      setLayers(response.data.results);
    } catch (e: unknown) {
      setShowProgress(false);
      setErrorMessage(`${e}`);
    }
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
      const { statefp, countyfp, geoid } = e.propagatedFrom.feature.properties;
      const geometry = e.propagatedFrom.feature.geometry;
      setLoadedCounty({ statefp, countyfp, geoid, geometry });
    },
  };

  return (
    <div className="container flex flex-col max-h-screen h-screen mx-auto">
      <div className="flex flex-grow flex-row">
        <MapContainer
          tap={false}
          center={DEFAULT_CENTER}
          zoom={DEFAULT_ZOOM}
          className="flex-grow"
          whenCreated={(map) => loadVisibleCounties(map)}
        >
          <TileLayer
            url={providers[activeProvider].url}
            attribution={providers[activeProvider].attribution}
          />
          <MapComponent />
          {layers.map((county: County) => (
            <GeoJSON
              key={county.geoid}
              data={countyToFeature(county)}
              style={style}
              eventHandlers={eventHandlers}
            />
          ))}
        </MapContainer>
        <div className="relative flex flex-col flex-grow-0 w-64 border-l-4 border-gray-200">
          <CountyDetailsView countyDetails={loadedCountyDetails} />
        </div>
      </div>
      <div className="flex flex-grow-0 h-20 bg-gray-400 flex-col border-t-2 border-gray rounded-b-sm">
        <ProgressBar active={showProgress} />
        <div className="flex flex-row justify-between pl-1 w-full items-center text-white text-xs">
          <div className="font-normal font-sans">County Impacts</div>
          {errorMessage && (
            <div className="bg-red-500 font-bold px-2">{errorMessage}</div>
          )}
          <div className="font-thin font-mono">
            [build#{process.env.REACT_APP_CI_RUN_NUMBER}]
          </div>
        </div>
      </div>
    </div>
  );
}
