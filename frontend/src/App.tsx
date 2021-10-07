import { useState, useEffect } from "react";
import axios from "axios";
import { ProgressBar } from "./ProgressBar";
import { Header } from "./HeaderFooter";
import { ImpactLabel, ImpactLabelParams } from "./ImpactLabel";
import {
  Search,
  SearchHits,
  SearchInput,
  SearchHitsView,
  buildSearch,
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

const blankSearchHits = {
  states: [],
  counties: [],
  zipcodes: [],
};

export default function App() {
  const [showProgress, setShowProgress] = useState<boolean>(false);
  const [search, setSearch] = useState<Search | undefined>(undefined);
  const [searchHits, setSearchHits] = useState<SearchHits>(blankSearchHits);
  const [searchTerms, setSearchTerms] = useState<string>("");
  const [impacts, setImpacts] = useState<ImpactLabelParams[]>([]);
  const [errorMessage, setErrorMessage] = useState<string | undefined>(
    undefined
  );

  useEffect(() => {
    (async () => {
      const [
        countiesResponse,
        statesResponse,
        zipcodesResponse,
      ] = await Promise.all([
        axios.get<QueryCountyResponse>("/query/county/all"),
        axios.get<QueryStateResponse>("/query/state/all"),
        axios.get<QueryZipcodeResponse>("/query/zipcode/all"),
      ]);

      setSearch(
        buildSearch({
          counties: countiesResponse.data.results,
          zipcodes: zipcodesResponse.data.results,
          states: statesResponse.data.results,
        })
      );
    })();
  }, []);

  useEffect(() => {
    if (search && searchTerms) {
      setSearchHits(search.search(searchTerms));
    }
  }, [searchTerms, search]);

  function clearSearchBox() {
    setSearchTerms("");
    setSearchHits(blankSearchHits);
  }

  async function loadCountyImpacts(county: County) {
    const data = {
      statefp: county.statefp,
      countyfp: county.countyfp,
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
        {search ? (
          <SearchInput
            searchTerms={searchTerms}
            setSearchTerms={(terms) => setSearchTerms(terms)}
          />
        ) : (
          <div className="border border-black p-2 text-gray-500 bg-gray-50 rounded-md border-gray-400 font-bold">
            Downloading stuff to search...
          </div>
        )}
        <SearchHitsView
          hits={searchHits}
          onStateSelected={(val: State) => {
            clearSearchBox();
            loadStateImpacts(val);
          }}
          onCountySelected={(val: County) => {
            clearSearchBox();
            loadCountyImpacts(val);
          }}
          onZipcodeSelected={(val: Zipcode) => {
            clearSearchBox();
            loadZipcodeImpacts(val);
          }}
        />
        <ProgressBar active={showProgress} />
        {impacts.map((impactLabelParams: ImpactLabelParams) => (
          <ImpactLabel
            key={Math.floor(Math.random() * Number.MAX_SAFE_INTEGER)}
            {...impactLabelParams}
          />
        ))}
      </div>
    </div>
  );
}
