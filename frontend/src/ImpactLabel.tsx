import { CountyDetails } from "./Api";

interface ImpactLineParams {
  label: string;
  units: string | JSX.Element;
  value: number | string;
}

interface ImpactLabelParams {
  countyDetails: CountyDetails | undefined;
}

export function ImpactLabel({ countyDetails }: ImpactLabelParams): JSX.Element {
  if (!countyDetails) {
    return <></>;
  }
  return (
    <div className="absolute inset-0 overflow-hidden overflow-scroll">
      <div className="flex flex-col m-2 p-2 bg-white border-4 border-black">
        <div className="text-xs font-light pb-1">Community/Region Profile</div>
        <div className="text-lg font-extrabold border-b-8 pb-3 border-black">
          {countyDetails.county.state_name}
        </div>
        <div className="border-b pb-1 border-black mb-2">
          <span className="text-sm font-bold pr-1">County:</span>
          <span className="text-sm font-light">
            {countyDetails.county.county_name}
          </span>
        </div>
        <ImpactLine
          label={"Global Warming Potential"}
          units={
            <span>
              kg co<sub>2</sub> eq
            </span>
          }
          value={Math.round(
            countyDetails.totals["impact potential/gcc/kg co2 eq"]
          )}
        ></ImpactLine>
        <ImpactLine
          label={"Ozone Depletion"}
          units={"kg CFC 11 eq"}
          value={countyDetails.totals[
            "impact potential/ozon/kg cfc11-eq"
          ].toFixed(3)}
        ></ImpactLine>
        <ImpactLine
          label={"Acidification"}
          units={
            <span>
              kg SO<sub>2</sub> eq
            </span>
          }
          value={countyDetails.totals[
            "impact potential/acid/kg so2-eq"
          ].toFixed(2)}
        ></ImpactLine>
        <ImpactLine
          label={"Eutrification"}
          units={"kg N eq"}
          value={countyDetails.totals["impact potential/eutr/kg n eq"].toFixed(
            2
          )}
        ></ImpactLine>
        <ImpactLine
          label={"Smog Formation"}
          units={
            <span>
              kg O<sub>3</sub> eq
            </span>
          }
          value={countyDetails.totals["impact potential/smog/kg o3 eq"].toFixed(
            2
          )}
        ></ImpactLine>
      </div>
    </div>
  );
}

export function ImpactLine({
  label,
  units,
  value,
}: ImpactLineParams): JSX.Element {
  return (
    <div className="flex flex-row border-b border-black mb-1 pb-1">
      <div className="whitespace-nowrap text-xs font-bold max-w-sm truncate overflow-hidden overflow-ellipsis mr-1">
        {label}
      </div>
      <div className="text-xs whitespace-nowrap">({units})</div>
      <div className="text-xs ml-auto">{value}</div>
    </div>
  );
}
