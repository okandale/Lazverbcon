<<<<<<< HEAD
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import VerbConjugator from './components/VerbConjugator';
import VerbList from './components/VerbList';
import Classes from './components/Classes';
import About from './components/About';
import HomePage from './components/Home';
import Resources from './components/Resources';
import Keyboard from './components/Keyboard';
import KeyboardWin from './components/Keyboardwin';       
import KeyboardPC from './components/KeyboardPC';
import KeyboardMAC from './components/KeyboardMAC';
import KeyboardAndr from './components/KeyboardAndr';
import KeyboardiPhone from './components/KeyboardiPhone';
import KeyboardMobile from './components/KeyboardMobile';
=======
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

>>>>>>> dev
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
<<<<<<< HEAD
        <Route path="/keyboard" element={<Keyboard />} />
        <Route path="/keyboard/windows" element={<KeyboardWin />} />
        <Route path="/keyboard/computer" element={<KeyboardPC />} />
        <Route path="/keyboard/mac" element={<KeyboardMAC />} />
        <Route path="/keyboard/android" element={<KeyboardAndr />} />
        <Route path="/keyboard/iphone" element={<KeyboardiPhone />} />
        <Route path="/keyboard/phone" element={<KeyboardMobile />} />
=======
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
>>>>>>> dev
      </Routes>
    </Router>
  );
}

export default App;
