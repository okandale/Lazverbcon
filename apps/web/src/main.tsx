import React from "react";
import { createRoot } from "react-dom/client";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { Site } from "./site/Site";
import "./style.css";
import "./site/site.css";

const client = new QueryClient({
  defaultOptions: { queries: { retry: 1, staleTime: 60_000 } },
});
createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <QueryClientProvider client={client}>
      <Site />
    </QueryClientProvider>
  </React.StrictMode>,
);
