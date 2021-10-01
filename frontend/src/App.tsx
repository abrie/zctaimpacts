import { useState, useEffect } from "react";
import axios from "axios";
import { ProgressBar } from "./ProgressBar";
import { Header } from "./HeaderFooter";
import { ImpactLabel, ImpactLabelParams } from "./ImpactLabel";
import {
  SearchInput,
  StateSearchHits,
  CountySearchHits,
  ZipcodeSearchHits,
  buildCountySearch,
  buildZipcodeSearch,
  buildStateSearch,
  CountySearch,
  ZipcodeSearch,
  StateSearch,
} from "./Search";
import type {
  State,
  County,
  Zipcode,
  QueryStateImpactsResponse,
  QueryCountyImpactsResponse,
  QueryZipcodeImpactsResponse,
  QueryCountyResponse,
  QueryZipcodeResponse,
  QueryStateResponse,
} from "./Api";
import { Indicators } from "./Api";

export default function App() {
  const [showProgress, setShowProgress] = useState<boolean>(false);
  const [stateHits, setStateHits] = useState<State[]>([]);
  const [countyHits, setCountyHits] = useState<County[]>([]);
  const [zipcodeHits, setZipcodeHits] = useState<Zipcode[]>([]);
  const [searchTerms, setSearchTerms] = useState<string>("");
  const [countySearch, setCountySearch] = useState<CountySearch | undefined>(
    undefined
  );
  const [zipcodeSearch, setZipcodeSearch] = useState<ZipcodeSearch | undefined>(
    undefined
  );
  const [stateSearch, setStateSearch] = useState<StateSearch | undefined>(
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
    (async () => {
      const response = await axios.get<QueryStateResponse>("/query/state/all");

      setStateSearch(buildStateSearch(response.data.results));
    })();
  }, []);

  useEffect(() => {
    (async () => {
      const response = await axios.get<QueryZipcodeResponse>(
        "/query/zipcode/all"
      );

      setZipcodeSearch(buildZipcodeSearch(response.data.results));
    })();
  }, []);

  useEffect(() => {
    if (countySearch && zipcodeSearch && stateSearch && searchTerms) {
      setStateHits(stateSearch.search(searchTerms));
      setCountyHits(countySearch.search(searchTerms));
      setZipcodeHits(zipcodeSearch.search(searchTerms));
    }
  }, [searchTerms, stateSearch, countySearch, zipcodeSearch]);

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
          type: "County",
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

  async function loadStateImpacts(state: State) {
    const data = {
      statefp: state.statefp,
      sampleSize: 50,
    };

    try {
      setShowProgress(true);
      setErrorMessage(undefined);
      const response = await axios.post<QueryStateImpactsResponse>(
        "/query/state/impacts",
        data
      );
      setShowProgress(false);
      setImpacts((i) => [
        {
          type: "State",
          industries: response.data.industries,
          indicators: Indicators,
          state: state,
        },
        ...i,
      ]);
    } catch (e: unknown) {
      setShowProgress(false);
      setErrorMessage(`${e}`);
    }
  }

  async function loadZipcodeImpacts(zipcode: Zipcode) {
    const data = {
      zipcode: zipcode.zipcode,
      sampleSize: 50,
    };

    try {
      setShowProgress(true);
      setErrorMessage(undefined);
      const response = await axios.post<QueryZipcodeImpactsResponse>(
        "/query/zipcode/impacts",
        data
      );
      setShowProgress(false);
      setImpacts((i) => [
        {
          type: "Zipcode",
          industries: response.data.industries,
          indicators: Indicators,
          zipcode: zipcode,
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
        <StateSearchHits
          onSelect={(state) => loadStateImpacts(state)}
          hits={stateHits}
        />
        <CountySearchHits
          onSelect={(county) => loadCountyImpacts(county)}
          hits={countyHits}
        />
        <ZipcodeSearchHits
          onSelect={(zipcode) => loadZipcodeImpacts(zipcode)}
          hits={zipcodeHits}
        />
        <ProgressBar active={showProgress} />
        {impacts.map((impactLabelParams: ImpactLabelParams) => (
          <ImpactLabel {...impactLabelParams} />
        ))}
      </div>
    </div>
  );
}
