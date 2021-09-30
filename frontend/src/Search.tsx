import { County } from "./Api";
import lunr from "lunr";

export interface CountySearch {
  index: lunr.Index;
  lookup: Record<string, County>;
  search: (terms: string) => County[];
}

export function buildCountySearch(documents: County[]): CountySearch {
  const index = buildCountyIndex(documents);
  const lookup = buildCountyLookup(documents);
  const search = (terms: string): County[] =>
    index.search(terms).map(({ ref }) => lookup[ref]);

  return {
    index,
    lookup,
    search,
  };
}

function buildCountyIndex(documents: County[]): lunr.Index {
  return lunr(function (this: lunr.Builder) {
    this.ref("geoid");
    this.field("county_name");
    this.field("state_name");

    documents.forEach(function (this: lunr.Builder, doc) {
      this.add(doc);
    }, this);
  });
}

function buildCountyLookup(documents: County[]): Record<string, County> {
  return documents.reduce((acc, county) => {
    return { ...acc, [county.geoid]: county };
  }, {});
}

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
