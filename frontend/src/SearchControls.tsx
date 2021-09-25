import { County } from "./Api";

interface SearchParams {
  setSearchTerms: (terms: string) => void;
}

export function SearchInput({ setSearchTerms }: SearchParams): JSX.Element {
  return (
    <div>
      <input
        className="w-full"
        type="text"
        placeholder="...Search by County, State, or Zipcode"
        onChange={(event) => setSearchTerms(event.target.value)}
      ></input>
    </div>
  );
}

interface SearchHitsParams {
  selectCounty: (county: County) => void;
  hits: County[];
}

export function SearchHits({
  selectCounty,
  hits,
}: SearchHitsParams): JSX.Element {
  return (
    <div
      id="hits"
      className="overflow-hidden overflow-scroll bg-gray-200 border border-black max-h-40"
    >
      {hits.map((hit: County) => (
        <div
          className="cursor-pointer hover:bg-green-400"
          key={hit.geoid}
          onClick={() => {
            selectCounty({ ...hit });
          }}
        >
          {hit.county_name}, {hit.state_name}
        </div>
      ))}
    </div>
  );
}
