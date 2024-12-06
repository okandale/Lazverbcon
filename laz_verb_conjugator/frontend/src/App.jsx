import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import VerbConjugator from './components/VerbConjugator';
import VerbList from './components/VerbList';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<VerbConjugator />} />
        <Route path="/verbs" element={<VerbList />} />
      </Routes>
    </Router>
  );
}

export default App;