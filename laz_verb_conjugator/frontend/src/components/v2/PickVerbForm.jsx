import { useState, useRef, useEffect } from "react";
import { Link } from "react-router-dom";
import LanguageToggle from "../ui/LanguageToggle";
import { Home } from "lucide-react";
import {
  translations,
  getStoredLanguage,
  setStoredLanguage,
  API_URLS,
} from "../constants";
import Skeleton from "@mui/material/Skeleton";
import Stack from "@mui/material/Stack";
import Chip from "@mui/material/Chip";
import { useSearchParams } from "react-router-dom";
import Pagination from "../ui/Pagination";
import { useNavigate } from "react-router-dom";

const PickVerbForm = () => {
  const navigate = useNavigate();

  const [language, setLanguage] = useState(getStoredLanguage());
  const [searchTerm, setSearchTerm] = useState("");
  const searchInputRef = useRef(null);
  const [isLoadingVerbs, setIsLoadingVerbs] = useState(true);
  const [verbs, setVerbs] = useState([]);
  const [verbCount, setVerbCount] = useState(0);
  const [totalPages, setTotalPages] = useState(0);
  const [searchParams, setSearchParams] = useSearchParams();
  const page = parseInt(searchParams.get("page")) || 1;

  const toggleLanguage = () => {
    const newLanguage = language === "en" ? "tr" : "en";
    setLanguage(newLanguage);
    setStoredLanguage(newLanguage);
  };

  const handlePageChange = (newPage) => {
    setSearchParams({ page: newPage });
  };

  const handleVerbClick = (verb) => {
    console.dir(verb);
    navigate(`/v2/verb/${verb["verb_id"]}/${verb["verb_type"]}`);
  };

  const fetchVerbsList = async () => {
    setIsLoadingVerbs(true);
    const response = await fetch(
      `${API_URLS.verbs.list}?page=${page}&pattern=${searchTerm}`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      }
    );
    const data = await response.json();
    setVerbs(data.results);
    setVerbCount(data.count);
    setTotalPages(data.pages);
    setIsLoadingVerbs(false);
  };

  useEffect(() => {
    fetchVerbsList();
  }, [page]);

  useEffect(() => {
    handlePageChange(1);
    fetchVerbsList();
  }, [searchTerm]);

  const columnTitles = {
    en: {
      laz: "Laz Infinitive",
      presentBase: "Present Base",
      verbType: "Verb Type",
      turkish: "Turkish Verb",
      english: "English",
    },
    tr: {
      laz: "Lazuri",
      presentBase: "3. şahıs",
      verbType: "Fiil türü",
      turkish: "Türkçe",
      english: "İngilizce",
    },
  };

  const verbTypeColors = {
    ergative: "blue",
    nominative: "orange",
    dative: "green",
  };

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
      <h1 className="text-3xl font-bold mb-6 text-center">
        {translations[language].verbsListTitle}
      </h1>

      <div className="mb-6">
        <input
          ref={searchInputRef}
          type="text"
          placeholder={"Search for a verb…"}
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      <div className="overflow-x-auto">
        {isLoadingVerbs && (
          <Stack spacing={1}>
            <div className="flex justify-center items-center">
              <Skeleton variant="rectangular" height={30} width={250} />
            </div>
            <Skeleton variant="rectangular" height={50} />
            <Skeleton variant="rectangular" height={300} />
            <Skeleton variant="rectangular" height={50} />
          </Stack>
        )}
        {!isLoadingVerbs && (
          <>
            <div className="text-center mb-6">
              <p className="text-xl text-gray-600">{`There are ${verbCount} verbs listed so far.`}</p>
            </div>
            <div className="bg-white p-3 mb-3">
              <Pagination
                currentPage={page}
                totalPages={totalPages}
                onPageChange={handlePageChange}
              />
            </div>
            <table className="min-w-full bg-white border">
              <thead>
                <tr>
                  <th className="py-2 px-4 border-b">
                    {columnTitles[language].laz}
                  </th>
                  <th className="py-2 px-4 border-b">
                    {columnTitles[language].presentBase}
                  </th>
                  <th className="py-2 px-4 border-b">
                    {columnTitles[language].verbType}
                  </th>
                  <th className="py-2 px-4 border-b">
                    {columnTitles[language].turkish}
                  </th>
                  <th className="py-2 px-4 border-b">
                    {columnTitles[language].english}
                  </th>
                </tr>
              </thead>
              <tbody>
                {verbs.map((verb) => {
                  return (
                    <tr
                      key={verb}
                      onClick={() => handleVerbClick(verb)}
                      className="hover:bg-blue-50 cursor-pointer transition-colors duration-150"
                    >
                      <td className="border px-4 py-2">
                        {verb["infinitive_form"]}
                      </td>
                      <td className="border px-4 py-2">{verb["verb_root"]}</td>
                      <td className="border px-4 py-2 text-center">
                        <Chip
                          label={verb["verb_type"]}
                          color={verbTypeColors[verb["verb_type"]]}
                        />
                      </td>
                      <td className="border px-4 py-2">
                        {verb["turkish_verb"]}
                      </td>
                      <td className="border px-4 py-2">
                        {verb["english_translation"]}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
            <div className="bg-white p-3 mt-3">
              <Pagination
                currentPage={page}
                totalPages={totalPages}
                onPageChange={handlePageChange}
              />
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default PickVerbForm;
