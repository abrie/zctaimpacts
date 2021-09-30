import { useState, useEffect } from "react";
import axios from "axios";
import { ProgressBar } from "./ProgressBar";
import { Header } from "./HeaderFooter";
import { ImpactLabel, ImpactLabelParams } from "./ImpactLabel";
import {
  SearchInput,
  SearchHits,
  buildCountySearch,
  CountySearch,
} from "./Search";
import type {
  County,
  QueryCountyImpactsResponse,
  QueryCountyResponse,
} from "./Api";
import { Indicators } from "./Api";

export default function App() {
  const [showProgress, setShowProgress] = useState<boolean>(false);
  const [hits, setHits] = useState<County[]>([]);
  const [searchTerms, setSearchTerms] = useState<string>("");
  const [countySearch, setCountySearch] = useState<CountySearch | undefined>(
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

  async function loadCountyImpacts(county: County) {
    const data = {
      statefp: county.statefp,
      countyfp: county.countyfp,
      sampleSize: 50,
    };

    try {
      setShowProgress(true);
      setErrorMessage(undefined);
      const response = await axios.post<QueryCountyImpactsResponse>(
        "/query/county/impacts",
        data
      );
      setShowProgress(false);
      setImpacts((i) => [
        {
          industries: response.data.industries,
          indicators: Indicators,
          county: county,
        },
        ...i,
      ]);
    } catch (e: unknown) {
      setShowProgress(false);
      setErrorMessage(`${e}`);
    }
  }

  return (
    <div className="p-1 container flex flex-col h-screen max-h-screen mx-auto">
      <Header errorMessage={errorMessage} />
      <div className="flex flex-col flex-grow">
        <SearchInput setSearchTerms={(terms) => setSearchTerms(terms)} />
        <SearchHits
          selectCounty={(county) => loadCountyImpacts(county)}
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
    </div>
  );
}
