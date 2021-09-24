import { County } from "./Api";

export const CountyStyle = {
  normal: {
    fillColor: "green",
    weight: 1,
    opacity: 0.15,
    color: "blue",
    dashArray: "1",
    fillOpacity: 0,
  },
  highlight: {
    weight: 5,
    color: "lightgreen",
    dashArray: "",
    fillOpacity: 0.5,
  },
};

export function countyToFeature({
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
