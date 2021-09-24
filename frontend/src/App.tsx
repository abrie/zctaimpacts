import { useState, useEffect } from "react";
import { MapContainer, TileLayer, GeoJSON, useMapEvents } from "react-leaflet";
import {
  LatLngExpression,
  LeafletEventHandlerFnMap,
  LeafletMouseEvent,
  Map,
} from "leaflet";
import axios from "axios";
import { debounce } from "underscore";
import { ProgressBar } from "./ProgressBar";
import { TileProviders } from "./TileProviders";
import { ImpactLabel } from "./ImpactLabel";
import {
  County,
  CountyDetails,
  QueryCountyDetailsResponse,
  QueryCountyResponse,
} from "./Api";

const DEBOUNCE_TIME_MSEC = 1000;
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

function countyToFeature({
  statefp,
  countyfp,
  county_name,
  state_name,
  geometry,
}: County): GeoJSON.Feature {
  return {
    type: "Feature",
    properties: {
      statefp,
      countyfp,
      county_name,
      state_name,
    },
    geometry,
  };
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
        setLoadedCountyDetails({
          industries: response.data.industries,
          totals: response.data.totals,
          county: loadedCounty,
        });
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
      const {
        statefp,
        countyfp,
        county_name,
        state_name,
        geoid,
      } = e.propagatedFrom.feature.properties;
      const geometry = e.propagatedFrom.feature.geometry;
      setLoadedCounty({
        statefp,
        countyfp,
        county_name,
        state_name,
        geoid,
        geometry,
      });
    },
  };

  return (
    <div className="container flex flex-col max-h-screen h-screen mx-auto">
      <div className="flex flex-grow flex-row">
        <MapContainer
          tap={false}
          center={DEFAULT_CENTER}
          zoom={DEFAULT_ZOOM}
          scrollWheelZoom={false}
          className="flex-grow"
          whenCreated={(map) => loadVisibleCounties(map)}
        >
          <TileLayer
            url={TileProviders[activeProvider].url}
            attribution={TileProviders[activeProvider].attribution}
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
          <ImpactLabel countyDetails={loadedCountyDetails} />
        </div>
      </div>
      <div className="flex flex-grow-0 h-6 bg-gray-400 flex-col border-t-2 border-gray rounded-b-sm">
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
