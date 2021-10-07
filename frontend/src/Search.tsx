import { County, Zipcode, State } from "./Api";
import lunr from "lunr";
import { FaSearch } from "react-icons/fa";

export interface SearchHits {
  states: State[];
  zipcodes: Zipcode[];
  counties: County[];
}

export interface Search {
  search: (terms: string) => SearchHits;
}

interface StateSearch {
  index: State[];
  search: (terms: string) => State[];
}

interface BuildSearchParams {
  states: State[];
  counties: County[];
  zipcodes: Zipcode[];
}

export function buildSearch({
  states,
  counties,
  zipcodes,
}: BuildSearchParams): Search {
  const stateSearch = buildStateSearch(states);
  const countySearch = buildCountySearch(counties);
  const zipcodeSearch = buildZipcodeSearch(zipcodes);
  return {
    search: (terms: string) => {
      return {
        states: stateSearch.search(terms),
        counties: countySearch.search(terms),
        zipcodes: zipcodeSearch.search(terms),
      };
    },
  };
}

function buildStateSearch(documents: State[]): StateSearch {
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

interface ZipcodeSearch {
  index: Zipcode[];
  search: (terms: string) => Zipcode[];
}

function buildZipcodeSearch(documents: Zipcode[]): ZipcodeSearch {
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

interface CountySearch {
  index: lunr.Index;
  lookup: Record<string, County>;
  search: (terms: string) => County[];
}

function buildCountySearch(documents: County[]): CountySearch {
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

export interface SearchHitsViewParams {
  hits: SearchHits;
  onStateSelected: (val: State) => void;
  onCountySelected: (val: County) => void;
  onZipcodeSelected: (val: Zipcode) => void;
}

export function SearchHitsView({
  hits,
  onStateSelected,
  onCountySelected,
  onZipcodeSelected,
}: SearchHitsViewParams): JSX.Element {
  return (
    <>
      <StateSearchHits hits={hits.states} onSelect={onStateSelected} />
      <CountySearchHits hits={hits.counties} onSelect={onCountySelected} />
      <ZipcodeSearchHits hits={hits.zipcodes} onSelect={onZipcodeSelected} />
    </>
  );
}

interface CountySearchHitsParams {
  onSelect: (county: County) => void;
  hits: County[];
}

function CountySearchHits({
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

function ZipcodeSearchHits({
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

function StateSearchHits({
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
