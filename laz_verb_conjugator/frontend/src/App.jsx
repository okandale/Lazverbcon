import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LoginPage from './components/login';
import VerbConjugator from './components/VerbConjugator';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LoginPage />} />
        <Route path="/conjugator" element={<VerbConjugator />} />
      </Routes>
    </Router>
  );
}

export default App;