import { State, County, Zipcode, Industry, Indicator } from "./Api";

export interface StateImpactLabelParams {
  type: "State";
  state: State;
  industries: Industry[];
  indicators: Indicator[];
}

export interface CountyImpactLabelParams {
  type: "County";
  county: County;
  industries: Industry[];
  indicators: Indicator[];
}

export interface ZipcodeImpactLabelParams {
  type: "Zipcode";
  zipcode: Zipcode;
  industries: Industry[];
  indicators: Indicator[];
}

export type ImpactLabelParams =
  | CountyImpactLabelParams
  | ZipcodeImpactLabelParams
  | StateImpactLabelParams;

interface ImpactLineParams {
  label: string;
  units: string | JSX.Element;
  value: number | string;
}

export function ImpactLabel(impactLabelParams: ImpactLabelParams): JSX.Element {
  switch (impactLabelParams.type) {
    case "County":
      return CountyImpactLabel(impactLabelParams);
    case "Zipcode":
      return ZipcodeImpactLabel(impactLabelParams);
    case "State":
      return StateImpactLabel(impactLabelParams);
  }
}

export function ZipcodeImpactLabel({
  zipcode,
  industries,
  indicators,
}: ZipcodeImpactLabelParams): JSX.Element {
  const totals: { indicator: Indicator; total: number }[] = indicators.map(
    (indicator) => {
      const total = industries.reduce((acc: number, industry: Industry) => {
        const impact = industry[indicator.Name] as number;
        return acc + impact;
      }, 0);
      return { indicator, total };
    }
  );

  return (
    <div className="inset-0">
      <div className="flex flex-col m-2 p-2 bg-white border-4 border-black">
        <div className="text-xs font-light pb-1">Community/Region Profile</div>
        <div className="text-lg font-extrabold border-b-8 pb-3 border-black">
          {zipcode.zipcode}
        </div>
        {totals.map(({ indicator, total }, idx: number) => (
          <ImpactLine
            key={idx}
            label={indicator.Name}
            units={indicator.Unit}
            value={indicator.formatter(total)}
          />
        ))}
      </div>
    </div>
  );
}
export function CountyImpactLabel({
  county,
  industries,
  indicators,
}: CountyImpactLabelParams): JSX.Element {
  const totals: { indicator: Indicator; total: number }[] = indicators.map(
    (indicator) => {
      const total = industries.reduce((acc: number, industry: Industry) => {
        const impact = industry[indicator.Name] as number;
        return acc + impact;
      }, 0);
      return { indicator, total };
    }
  );

  return (
    <div className="inset-0">
      <div className="flex flex-col m-2 p-2 bg-white border-4 border-black">
        <div className="text-xs font-light pb-1">Community/Region Profile</div>
        <div className="text-lg font-extrabold border-b-8 pb-3 border-black">
          {county.state_name}
        </div>
        <div className="border-b pb-1 border-black mb-2">
          <span className="text-sm font-bold pr-1">County:</span>
          <span className="text-sm font-light">{county.county_name}</span>
        </div>
        {totals.map(({ indicator, total }, idx: number) => (
          <ImpactLine
            key={idx}
            label={indicator.Name}
            units={indicator.Unit}
            value={indicator.formatter(total)}
          />
        ))}
      </div>
    </div>
  );
}

export function StateImpactLabel({
  state,
  industries,
  indicators,
}: StateImpactLabelParams): JSX.Element {
  const totals: { indicator: Indicator; total: number }[] = indicators.map(
    (indicator) => {
      const total = industries.reduce((acc: number, industry: Industry) => {
        const impact = industry[indicator.Name] as number;
        return acc + impact;
      }, 0);
      return { indicator, total };
    }
  );

  return (
    <div className="inset-0">
      <div className="flex flex-col m-2 p-2 bg-white border-4 border-black">
        <div className="text-xs font-light pb-1">Community/Region Profile</div>
        <div className="text-lg font-extrabold border-b-8 pb-3 border-black">
          {state.name}
        </div>
        <div className="border-b pb-1 border-black mb-2">
          <span className="text-sm font-bold pr-1">Entire State</span>
        </div>
        {totals.map(({ indicator, total }, idx: number) => (
          <ImpactLine
            key={idx}
            label={indicator.Name}
            units={indicator.Unit}
            value={indicator.formatter(total)}
          />
        ))}
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
