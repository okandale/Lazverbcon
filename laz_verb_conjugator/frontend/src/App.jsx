import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import VerbConjugator from './components/VerbConjugator';
import VerbList from './components/VerbList';
import Classes from './components/Classes';
import About from './components/About';
import HomePage from './components/Home';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/conjugator" element={<VerbConjugator />} />
        <Route path="/verbs" element={<VerbList />} />
        <Route path="/classes" element={<Classes />} />
        <Route path="/about" element={<About />} />
      </Routes>
    </Router>
  );
}

export default App;