import { County, Zipcode, State } from "./Api";
import lunr from "lunr";
import { FaSearch } from "react-icons/fa";

export interface StateSearch {
  index: State[];
  search: (terms: string) => State[];
}

export function buildStateSearch(documents: State[]): StateSearch {
  const index = documents;
  const search = (terms: string): State[] => {
    return index.filter((state: State) =>
      state.name.toUpperCase().startsWith(terms.toUpperCase())
    );
  };

  return {
    index,
    search,
  };
}

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
  return index;
}

function buildCountyLookup(documents: County[]): Record<string, County> {
  return documents.reduce((acc, county) => {
    return { ...acc, [county.geoid]: county };
  }, {});
}

interface SearchParams {
  searchTerms: string;
  setSearchTerms: (terms: string) => void;
}

export function SearchInput({
  setSearchTerms,
  searchTerms,
}: SearchParams): JSX.Element {
  return (
    <div className="shadow flex rounded border">
      <span className="w-auto flex justify-end items-center text-gray-500 p-2">
        <FaSearch />
      </span>
      <input
        className="w-full p-2 border-0 "
        type="text"
        value={searchTerms}
        placeholder="Enter a County, State, or Zipcode"
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
  if (hits.length === 0) {
    return <></>;
  }
  return (
    <div className="ml-8 pl-2 overflow-hidden overflow-scroll bg-gray-200 max-h-40">
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
  if (hits.length === 0) {
    return <></>;
  }
  return (
    <div className="ml-8 pl-2 overflow-hidden overflow-scroll bg-gray-200 max-h-40">
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

interface StateSearchHitsParams {
  onSelect: (state: State) => void;
  hits: State[];
}

export function StateSearchHits({
  onSelect,
  hits,
}: StateSearchHitsParams): JSX.Element {
  if (hits.length === 0) {
    return <></>;
  }
  return (
    <div className="ml-8 pl-2 overflow-hidden overflow-scroll bg-gray-200 max-h-40">
      {hits.map((hit: State) => (
        <div
          className="cursor-pointer hover:bg-green-400"
          key={hit.geoid}
          onClick={() => {
            onSelect({ ...hit });
          }}
        >
          {hit.name}
        </div>
      ))}
    </div>
  );
}
