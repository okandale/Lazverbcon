import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import VerbConjugator from "./components/VerbConjugator";
import VerbList from "./components/VerbList";
import Classes from "./components/Classes";
import About from "./components/About";
import HomePage from "./components/Home";
import Resources from "./components/Resources";
import AdminAuth from "./components/AdminAuth";
import RequireAuth from "./components/RequireAuth";
import AdminPanel from "./components/AdminPanel";
import AdminLogout from "./components/AdminLogout";
import PickVerbForm from "./components/v2/PickVerbForm";

import { createTheme, ThemeProvider } from "@mui/material/styles";
import VerbDetails from "./components/v2/VerbDetails";


const theme = createTheme({
  palette: {
    orange: {
      main: "#F57C00",
      contrastText: "#fff",
    },
    green: {
      main: "#388E3C",
      contrastText: "#fff",
    },
    blue: {
      main: "#1976D2",
      contrastText: "#fff",
    },
    purple: {
      main: "#7B1FA2",
      contrastText: "#fff",
    },
    red: {
      main: "#D32F2F",
      contrastText: "#fff",
    },
    teal: {
      main: "#00796B",
      contrastText: "#fff",
    },
    brown: {
      main: "#5D4037",
      contrastText: "#fff",
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <Router>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/conjugator" element={<VerbConjugator />} />
          <Route path="/verbs" element={<VerbList />} />
          <Route path="/events" element={<Classes />} />
          <Route path="/about" element={<About />} />
          <Route path="/resources" element={<Resources />} />
          <Route path="/admin" element={<AdminAuth />} />
          <Route
            path="/admin/panel"
            element={
              <RequireAuth>
                <AdminPanel />
              </RequireAuth>
            }
          />
          <Route
            path="/admin/logout"
            element={
              <RequireAuth>
                <AdminLogout />
              </RequireAuth>
            }
          />
          <Route path="/v2/verbs" element={<PickVerbForm />} />
          <Route path="/v2/verb/:verbID/:verbType" element = {<VerbDetails />} />
        </Routes>
      </Router>
    </ThemeProvider>
  );
}

export default App;
