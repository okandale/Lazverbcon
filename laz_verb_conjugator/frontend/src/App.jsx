import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LoginPage from './components/login';
import VerbConjugator from './components/VerbConjugator';
import VerbList from './components/VerbList'; // Correct import

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LoginPage />} />
        <Route path="/conjugator" element={<VerbConjugator />} />
        <Route path="/verbs" element={<VerbList />} /> {/* New route */}
      </Routes>
    </Router>
  );
}

export default App;


