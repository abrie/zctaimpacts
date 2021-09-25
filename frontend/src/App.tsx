import { useState, useEffect } from "react";
import axios from "axios";
import { ProgressBar } from "./ProgressBar";
import { ImpactLabel } from "./ImpactLabel";
import lunr from "lunr";
import {
  County,
  CountyDetails,
  QueryCountyDetailsResponse,
  QueryCountyResponse,
} from "./Api";

export default function App() {
  const [showProgress, setShowProgress] = useState<boolean>(false);
  const [hits, setHits] = useState<County[]>([]);
  const [searchTerms, setSearchTerms] = useState<string>("");
  const [countySearch, setCountySearch] = useState<
    { index: lunr.Index; lookup: Record<string, County> } | undefined
  >(undefined);
  const [selectedCounty, selectCounty] = useState<County | undefined>(
    undefined
  );
  const [impacts, setImpacts] = useState<CountyDetails | undefined>(undefined);
  const [errorMessage, setErrorMessage] = useState<string | undefined>(
    undefined
  );

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

  useEffect(() => {
    (async () => {
      const response = await axios.get<QueryCountyResponse>(
        "/query/county/all"
      );

      const index = buildCountyIndex(response.data.results);
      const lookup = buildCountyLookup(response.data.results);
      setCountySearch({ index, lookup });
    })();
  }, []);

  useEffect(() => {
    if (countySearch && searchTerms) {
      setHits(
        countySearch.index
          .search(searchTerms)
          .map(({ ref }) => countySearch.lookup[ref])
      );
    }
  }, [searchTerms, countySearch]);

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

  function SearchBox(): JSX.Element {
    return (
      <div>
        <div>
          <input
            type="text"
            placeholder="County"
            onChange={(event) => setSearchTerms(event.target.value)}
            value={searchTerms}
          ></input>
        </div>
        <div
          id="hits"
          className="overflow-hidden overflow-scroll bg-gray-200 border border-black h-60"
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
      </div>
    );
  }

  return (
    <div className="container flex flex-col h-screen max-h-screen mx-auto">
      <div className="flex flex-col flex-grow">
        <SearchBox />
        <ImpactLabel countyDetails={impacts} />
      </div>
      <div className="flex flex-col flex-grow-0 h-6 bg-gray-400 border-t-2 rounded-b-sm border-gray">
        <ProgressBar active={showProgress} />
        <div className="flex flex-row items-center justify-between w-full pl-1 text-xs text-white">
          <div className="font-sans font-normal">County Impacts</div>
          {errorMessage && (
            <div className="px-2 font-bold bg-red-500">{errorMessage}</div>
          )}
          <div className="font-thin font-mono">
            [build#{process.env.REACT_APP_CI_RUN_NUMBER}]
          </div>
        </div>
      </div>
    </div>
  );
}
