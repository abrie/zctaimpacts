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
import { CountyStyle, countyToFeature } from "./Map";

const DEBOUNCE_TIME_MSEC = 1000;
const activeProvider = 0;

const DEFAULT_CENTER: LatLngExpression = [33.813534, -84.403339];
const DEFAULT_ZOOM: number = 9;

export default function App() {
  const [layers, setLayers] = useState<County[]>([]);
  const [showProgress, setShowProgress] = useState<boolean>(false);
  const [selectedCounty, selectCounty] = useState<County | undefined>(
    undefined
  );
  const [impacts, setImpacts] = useState<CountyDetails | undefined>(undefined);
  const [errorMessage, setErrorMessage] = useState<string | undefined>(
    undefined
  );

  useEffect(() => {
    (async () => {
      if (!selectedCounty) {
        return;
      }
      const data = {
        statefp: selectedCounty.statefp,
        countyfp: selectedCounty.countyfp,
      };
      try {
        setShowProgress(true);
        setErrorMessage(undefined);
        const response = await axios.post<QueryCountyDetailsResponse>(
          "/query/county",
          data
        );
        setShowProgress(false);
        setImpacts({
          industries: response.data.industries,
          totals: response.data.totals,
          county: selectedCounty,
        });
      } catch (e: unknown) {
        setShowProgress(false);
        setErrorMessage(`${e}`);
      }
    })();
  }, [selectedCounty]);

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
      e.target.setStyle(CountyStyle.highlight);
    },
    mouseout: (e: LeafletMouseEvent) => {
      e.target.setStyle(CountyStyle.normal);
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
      selectCounty({
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
              style={CountyStyle.normal}
              eventHandlers={eventHandlers}
            />
          ))}
        </MapContainer>
        <div className="relative flex flex-col flex-grow-0 w-64 border-l-4 border-gray-200">
          <ImpactLabel countyDetails={impacts} />
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
