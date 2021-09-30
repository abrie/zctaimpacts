import { County, Zipcode } from "./Api";
import lunr from "lunr";

export interface ZipcodeSearch {
  index: Zipcode[];
  search: (terms: string) => Zipcode[];
}

export function buildZipcodeSearch(documents: Zipcode[]): ZipcodeSearch {
  const index = documents;
  const search = (terms: string): Zipcode[] => {
    return index.filter((zipcode: Zipcode) =>
      zipcode.zipcode.startsWith(terms)
    );
  };

  return {
    index,
    search,
  };
}

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
  console.log("Building county index...");
  const index = lunr(function (this: lunr.Builder) {
    this.ref("geoid");
    this.field("county_name");
    this.field("state_name");

    documents.forEach(function (this: lunr.Builder, doc) {
      this.add(doc);
    }, this);
  });
  console.log("Done building county index.");
  return index;
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

interface CountySearchHitsParams {
  onSelect: (county: County) => void;
  hits: County[];
}

export function CountySearchHits({
  onSelect,
  hits,
}: CountySearchHitsParams): JSX.Element {
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
            onSelect({ ...hit });
          }}
        >
          {hit.county_name}, {hit.state_name}
        </div>
      ))}
    </div>
  );
}

interface ZipcodeSearchHitsParams {
  onSelect: (zipcode: Zipcode) => void;
  hits: Zipcode[];
}

export function ZipcodeSearchHits({
  onSelect,
  hits,
}: ZipcodeSearchHitsParams): JSX.Element {
  return (
    <div
      id="hits"
      className="overflow-hidden overflow-scroll bg-gray-200 border border-black max-h-40"
    >
      {hits.map((hit: Zipcode) => (
        <div
          className="cursor-pointer hover:bg-green-400"
          key={hit.geoid}
          onClick={() => {
            onSelect({ ...hit });
          }}
        >
          {hit.zipcode}
        </div>
      ))}
    </div>
  );
}
