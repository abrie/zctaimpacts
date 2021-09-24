interface ImpactLineParams {
  label: string;
  units: string | JSX.Element;
  value: number | string;
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
