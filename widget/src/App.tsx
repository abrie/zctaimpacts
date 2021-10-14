import React, { useState, useEffect } from 'react';

interface AppProps {}

function App({}: AppProps) {
  // Create the count state.
  const [count, setCount] = useState(0);
  // Create the counter (+1 every second).
  useEffect(() => {
    const timer = setTimeout(() => setCount(count + 1), 1000);
    return () => clearTimeout(timer);
  }, [count, setCount]);
  // Return the App component.
  return (
    <div className="container bg-red-300 text-bold">
      <p>
        Page has been open for <code>{count}</code> seconds.
      </p>
    </div>
  );
}

export default App;
