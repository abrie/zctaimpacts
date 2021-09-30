interface HeaderParams {
  errorMessage: string | undefined;
}

export function Header({ errorMessage }: HeaderParams): JSX.Element {
  return (
    <details className="p-1 mb-2">
      <summary className="relative">
        <div className="absolute right-0 inline-flex flex-row justify-between left-5">
          <div className="">Community Impact Search</div>
          {errorMessage && (
            <div className="px-2 font-bold bg-red-500">{errorMessage}</div>
          )}
          <div className="font-mono font-thin">
            [build#{process.env.REACT_APP_CI_RUN_NUMBER}]
          </div>
        </div>
      </summary>
      <div className="text-sm ml-5 border-t-2 mt-1 p-4 text-justify">
        This web app was built for the{" "}
        <a
          className="underline"
          href="https://model.georgia.org/community/challenge/"
        >
          Sustainable Communities Web Challenge
        </a>{" "}
        hackathon in 2021. It generates a summary of direct environmental
        consequences due to industries within a county or zipcode. The summary
        format emulates a nutritional label found on food packaging.{" "}
        <a className="underline" href="https://github.com/abrie/zctaimpacts">
          {" "}
          Source code available here{" "}
        </a>
        .
      </div>
    </details>
  );
}
