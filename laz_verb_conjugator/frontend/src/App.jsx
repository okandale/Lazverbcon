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

function App() {
  return (
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
      </Routes>
    </Router>
  );
}

export default App;
