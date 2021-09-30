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
      This app generates a nutrition-style label describing direct environmental
      consequences of industries within a county.
    </details>
  );
}
