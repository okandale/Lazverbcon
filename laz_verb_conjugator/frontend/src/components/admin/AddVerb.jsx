import { Link, useNavigate, useSearchParams } from "react-router-dom";
import { Home } from "lucide-react";
import LanguageToggle from "../ui/LanguageToggle";
import { getStoredLanguage, setStoredLanguage, API_URLS } from "../constants";
import { useEffect, useRef, useState } from "react";
import RegionSelector from "../v2/RegionSelector";

const AddVerb = () => {
  const [language, setLanguage] = useState(getStoredLanguage());
  const [canAddVerb, setCanAddVerb] = useState(false);
  const [infinitiveForm, setInfinitiveForm] = useState("");
  const [verbType, setVerbType] = useState("");
  const [thirdPersonForm, setThirdPersonForm] = useState("");
  const [turkishInfinitive, setTurkishInfinitive] = useState("");
  const [englishTranslation, setEnglisTranslation] = useState("");
  const toggleLanguage = () => {
    const newLanguage = language === "en" ? "tr" : "en";
    setLanguage(newLanguage);
    setStoredLanguage(newLanguage);
  };

  const [regions, setRegions] = useState([]);

  const onSelectedRegionsUpdate = (selectedRegions) => {
    console.log(selectedRegions);
    setRegions([...selectedRegions]);
  };

  const onAddVerbSubmit = async (event) => {
    event.preventDefault();
    const response = await fetch(`${API_URLS.admin.addVerb}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${localStorage.getItem("accessToken")}`
      },
      body: JSON.stringify({
        verb_infinitive: infinitiveForm,
        regions: regions,
        verb_type: verbType,
        third_person_form: thirdPersonForm,
        turkish_infinitive: turkishInfinitive,
        english_translation: englishTranslation,
      }),
    });
    try {
      const data = await response.json();
    } catch (error) {
      console.dir(error);
    }
    return false;
  };

  useEffect(() => {
    const canSendForm =
      infinitiveForm !== "" &&
      verbType !== "" &&
      englishTranslation !== "" &&
      turkishInfinitive != "" &&
      thirdPersonForm != "" &&
      regions.length !== 0;
    setCanAddVerb(canSendForm);
  }, [
    infinitiveForm,
    verbType,
    regions,
    englishTranslation,
    turkishInfinitive,
    thirdPersonForm,
  ]);

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
              value={infinitiveForm}
              onChange={(e) => setInfinitiveForm(e.target.value)}
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
              onChange={(e) => setVerbType(e.target.value)}
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
              value={thirdPersonForm}
              onChange={(e) => setThirdPersonForm(e.target.value)}
              className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div className="mt-2">
            <input
              type="text"
              value={turkishInfinitive}
              onChange={(e) => setTurkishInfinitive(e.target.value)}
              placeholder={"Turkish infinitive"}
              className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div className="mt-2">
            <input
              type="text"
              value={englishTranslation}
              onChange={(e) => setEnglisTranslation(e.target.value)}
              placeholder={"English translation"}
              className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div className="mt-2 text-center">
            <button
              type="submit"
              disabled={!canAddVerb}
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
