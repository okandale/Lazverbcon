import { Home } from "lucide-react";
import { Link } from "react-router-dom";
import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import LanguageToggle from "../ui/LanguageToggle";
import {
  translations,
  getStoredLanguage,
  setStoredLanguage,
  verbTypeColors,
  API_URLS,
  regionColors,
} from "../constants";
import Skeleton from "@mui/material/Skeleton";
import Stack from "@mui/material/Stack";
import Chip from "@mui/material/Chip";

const VerbDetails = () => {
  const { verbID, verbType } = useParams();
  const [language, setLanguage] = useState(getStoredLanguage());
  const [isLoadingDetails, setIsLoadingDetails] = useState(false);
  const [verbDetails, setVerbDetails] = useState(null);

  const [isLoadingConjugations, setIsLoadingConjugations] = useState(false);
  const [conjugations, setConjugations] = useState(null);
  const toggleLanguage = () => {
    const newLanguage = language === "en" ? "tr" : "en";
    setLanguage(newLanguage);
    setStoredLanguage(newLanguage);
  };

  useEffect(() => {
    if (!verbID || !verbType) return;

    const fetchVerbDetails = async () => {
      setIsLoadingDetails(true);
      try {
        const response = await fetch(
          `${API_URLS.verbs.getDetails}/${verbID}/${verbType}`
        );
        const data = await response.json();
        setVerbDetails(data);
      } catch (error) {
        console.dir(error);
      } finally {
        setIsLoadingDetails(false);
      }
    };

    fetchVerbDetails();
  }, [verbID, verbType]);

  const conjugateVerb = async () => {
    try {
      setIsLoadingConjugations(true);
      const response = await fetch(`${API_URLS.verbs.conjugate}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          verb_id: verbID,
          verb_type: verbType,
          regions: ["FA", "HO", "PZ", "AS"],
          tense: "present",
        }),
      });
      const data = await response.json();
      setConjugations(data["conjugations"]);
    } catch (error) {
      console.log(error);
    } finally {
      setIsLoadingConjugations(false);
    }
  };

  return (
    <>
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-white">
        <div className="max-w-2xl mx-auto p-4">
          {/* Header section with language toggle */}
          <div className="flex justify-between items-center mb-8 pt-2">
            <Link to="/" className="text-gray-600 hover:text-gray-800">
              <Home size={24} />
            </Link>
            <LanguageToggle language={language} onToggle={toggleLanguage} />
          </div>
          {/* Title */}
          <h1 className="text-3xl font-bold mb-6 text-center">
            {translations[language].verbDetailsTitle}
          </h1>

          <div class="bg-orange-100 border border-orange-400 text-orange-700 px-4 py-3 rounded mb-5 text-center" role="alert">
            <span class="block sm:inline">Please bear in mind that this conjugator version may output inaccurate results.</span>
          </div>

          {isLoadingDetails && (
            <Stack spacing={1}>
              <div className="flex justify-center items-center">
                <Skeleton variant="rectangular" height={30} width={250} />
              </div>
              <Skeleton variant="rectangular" height={50} />
              <Skeleton variant="rectangular" height={300} />
              <Skeleton variant="rectangular" height={50} />
            </Stack>
          )}

          {!isLoadingDetails && verbDetails !== null && (
            <div className="text-center mb-6">
              <table class="min-w-full bg-white border">
                <tr>
                  <td>Infinitive Form</td>
                  <td>{verbDetails["infinitive_form"]}</td>
                </tr>
                <tr>
                  <td>Verb Type</td>
                  <td>
                    <Chip label={verbType} color={verbTypeColors[verbType]} />
                  </td>
                </tr>
                <tr>
                  <td>Regions</td>
                  <td>
                    {verbDetails["results"].map((result) => (
                      <Chip
                        key={result["region_code"]}
                        label={result["region_name"]}
                        color={regionColors[result["region_code"]]}
                      />
                    ))}
                  </td>
                </tr>
              </table>
              <button
                onClick={conjugateVerb}
                className="flex-1 min-w-32 bg-blue-500 hover:bg-blue-600 active:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors duration-150 ease-in-out shadow-md hover:shadow-lg focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-opacity-50 disabled:opacity-50 disabled:cursor-not-allowed mt-5"
              >
                Conjugate Present Form
              </button>
            </div>
          )}
          {!isLoadingConjugations && conjugations !== null && (
            <div className="grid grid-cols-2 gap-2">
              {Object.entries(conjugations).map(
                ([region, regionConjugations]) => (
                  <div className="bg-white p-2" key={region}>
                    <h2>{region}</h2>
                    <ul>
                      {regionConjugations.map((result) => (
                        <li>{result}</li>
                      ))}
                    </ul>
                  </div>
                )
              )}
            </div>
          )}
        </div>
      </div>
    </>
  );
};

export default VerbDetails;
