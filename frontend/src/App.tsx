import { useState, useEffect } from "react";
import axios from "axios";
import { ProgressBar } from "./ProgressBar";
import { ImpactLabel, ImpactLabelParams } from "./ImpactLabel";
import {
  SearchInput,
  SearchHits,
  buildCountySearch,
  CountySearch,
} from "./Search";
import {
  County,
  QueryCountyDetailsResponse,
  QueryCountyResponse,
  Indicators,
} from "./Api";

export default function App() {
  const [showProgress, setShowProgress] = useState<boolean>(false);
  const [hits, setHits] = useState<County[]>([]);
  const [searchTerms, setSearchTerms] = useState<string>("");
  const [countySearch, setCountySearch] = useState<CountySearch | undefined>(
    undefined
  );
  const [selectedCounty, selectCounty] = useState<County | undefined>(
    undefined
  );
  const [impacts, setImpacts] = useState<ImpactLabelParams[]>([]);
  const [errorMessage, setErrorMessage] = useState<string | undefined>(
    undefined
  );

  useEffect(() => {
    (async () => {
      const response = await axios.get<QueryCountyResponse>(
        "/query/county/all"
      );

      setCountySearch(buildCountySearch(response.data.results));
    })();
  }, []);

  useEffect(() => {
    if (countySearch && searchTerms) {
      setHits(countySearch.search(searchTerms));
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
          "/query/county/impacts",
          data
        );
        setShowProgress(false);
        setImpacts((i) => [
          {
            industries: response.data.industries,
            indicators: Indicators,
            county: selectedCounty,
          },
          ...i,
        ]);
      } catch (e: unknown) {
        setShowProgress(false);
        setErrorMessage(`${e}`);
      }
    })();
  }, [selectedCounty]);

  return (
    <div className="p-1 container flex flex-col h-screen max-h-screen mx-auto">
      <div className="flex flex-col flex-grow">
        <SearchInput setSearchTerms={(terms) => setSearchTerms(terms)} />
        <SearchHits
          selectCounty={(county) => selectCounty(county)}
          hits={hits}
        />
        <ProgressBar active={showProgress} />
        {impacts.map(({ industries, indicators, county }) => (
          <ImpactLabel
            industries={industries}
            indicators={indicators}
            county={county}
          />
        ))}
      </div>
      <div className="flex flex-col flex-grow-0 h-6 bg-gray-400 border-t-2 rounded-b-sm border-gray">
        <div className="flex flex-row items-center justify-between w-full pl-1 text-xs text-white">
          <div className="font-sans font-normal">
            <a href="https://github.com/abrie/zctaimpacts">
              https://github.com/abrie/zctaimpacts
            </a>
          </div>
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
