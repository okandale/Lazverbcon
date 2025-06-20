import { Link, useNavigate, useSearchParams } from "react-router-dom";
import { Home } from "lucide-react";
import LanguageToggle from "../ui/LanguageToggle";
import { getStoredLanguage, setStoredLanguage } from "../constants";
import { useEffect, useRef, useState } from "react";
import RegionSelector from "../v2/RegionSelector";

const AddVerb = () => {
  const [language, setLanguage] = useState(getStoredLanguage());
  const toggleLanguage = () => {
    const newLanguage = language === "en" ? "tr" : "en";
    setLanguage(newLanguage);
    setStoredLanguage(newLanguage);
  };

  const [regions, setRegions] = useState([]);

  const onSelectedRegionsUpdate = (selectedRegions) => {
    setRegions([...selectedRegions]);
  };

  const onAddVerbSubmit = (event) => {
    event.preventDefault();
    return false;
  }

  return (
    <div className="max-w-4xl mx-auto p-4">
      {/* Header with navigation and language toggle */}
      <div className="flex justify-between items-center mb-8 pt-2">
        <Link to="/" className="text-gray-600 hover:text-gray-800">
          <Home size={24} />
        </Link>
        <LanguageToggle language={language} onToggle={toggleLanguage} />
      </div>
      {/* Title */}
      <h1 className="text-3xl font-bold mb-6 text-center">Add a verb</h1>

      <div className="bg-white p-3 mb-3">
        <form method="POST" onSubmit={onAddVerbSubmit}>
          <div className="mt-2">
            <input
              type="text"
              placeholder={"Infinitive form"}
              className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div className="mt-2">
            Regions:
            <RegionSelector
              initialSelectedRegions={new Set()}
              onSelectedRegionsUpdate={onSelectedRegionsUpdate}
            />
          </div>

          <div className="mt-2">
            <select
              className=" appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline bg-white"
              name="verb_type"
            >
              <option value="">Verb type</option>
              <option value="nominative">Nominative</option>
              <option value="dative">Dative</option>
              <option value="ergative">Ergative</option>
            </select>
          </div>

          <div className="mt-2">
            <input
              type="text"
              placeholder={"3rd person form"}
              className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div className="mt-2">
            <input
              type="text"
              placeholder={"Turkish infinitive"}
              className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div className="mt-2">
            <input
              type="text"
              placeholder={"English translation"}
              className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div className="mt-2 text-center">
            <button
              type="submit"
              className="flex-1 min-w-32 bg-blue-500 hover:bg-blue-600 active:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors duration-150 ease-in-out shadow-md hover:shadow-lg focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-opacity-50 disabled:opacity-50 disabled:cursor-not-allowed mt-5"
            >
              Submit
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default AddVerb;
