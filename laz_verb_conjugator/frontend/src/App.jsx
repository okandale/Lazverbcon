import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { createTheme, ThemeProvider } from "@mui/material/styles";

import VerbConjugator from "./components/VerbConjugator";
import VerbList from "./components/conjugator/VerbList";
import Classes from "./components/Classes";
import About from "./components/About";
import HomePage from "./components/Home";
import Resources from "./components/Resources";
import PhraseGuide from "./components/PhraseGuide";
import PazarPhrases from "./components/phrases/PazarPhrases";
import ArdesenPhrases from "./components/phrases/ArdesenPhrases";
import FindikliArhaviPhrases from "./components/phrases/FindikliArhaviPhrases";
import HopaPhrases from "./components/phrases/HopaPhrases";
import Keyboard from "./components/Keyboard";
import KeyboardWin from "./components/Keyboardwin";
import KeyboardPC from "./components/KeyboardPC";
import KeyboardMAC from "./components/KeyboardMAC";
import KeyboardAndr from "./components/KeyboardAndr";
import KeyboardiPhone from "./components/KeyboardiPhone";
import KeyboardMobile from "./components/KeyboardMobile";

import AdminAuth from "./components/AdminAuth";
import RequireAuth from "./components/RequireAuth";
import AdminPanel from "./components/AdminPanel";
import AdminLogout from "./components/AdminLogout";
import PickVerbForm from "./components/v2/PickVerbForm";
import VerbDetails from "./components/v2/VerbDetails";
import AdminManageVerbs from "./components/admin/AdminManageVerbs";
import AddVerb from "./components/admin/AddVerb";

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

          <Route path="/resources/phrase-guide" element={<PhraseGuide />} />
          <Route path="/resources/phrase-guide/pazar" element={<PazarPhrases />} />
          <Route path="/resources/phrase-guide/ardesen" element={<ArdesenPhrases />} />
          <Route
            path="/resources/phrase-guide/findikli-arhavi"
            element={<FindikliArhaviPhrases />}
          />
          <Route path="/resources/phrase-guide/hopa" element={<HopaPhrases />} />

          <Route path="/keyboard" element={<Keyboard />} />
          <Route path="/keyboard/windows" element={<KeyboardWin />} />
          <Route path="/keyboard/computer" element={<KeyboardPC />} />
          <Route path="/keyboard/mac" element={<KeyboardMAC />} />
          <Route path="/keyboard/android" element={<KeyboardAndr />} />
          <Route path="/keyboard/iphone" element={<KeyboardiPhone />} />
          <Route path="/keyboard/phone" element={<KeyboardMobile />} />

          <Route path="/pick-verb-form" element={<PickVerbForm />} />
          <Route path="/verbs/:id" element={<VerbDetails />} />

          <Route path="/admin/login" element={<AdminAuth />} />
          <Route path="/admin/logout" element={<AdminLogout />} />
          <Route
            path="/admin"
            element={
              <RequireAuth>
                <AdminPanel />
              </RequireAuth>
            }
          />
          <Route
            path="/admin/manage-verbs"
            element={
              <RequireAuth>
                <AdminManageVerbs />
              </RequireAuth>
            }
          />
          <Route
            path="/admin/add-verb"
            element={
              <RequireAuth>
                <AddVerb />
              </RequireAuth>
            }
          />
        </Routes>
      </Router>
    </ThemeProvider>
  );
}

export default App;