import Chip from "@mui/material/Chip";
import { verbTypeColors } from "../constants";

const VerbsTable = ({ language, verbs, onVerbClick }) => {
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

  return (
    <>
      <table className="min-w-full bg-white border">
        <thead>
          <tr>
            <th className="py-2 px-4 border-b">{columnTitles[language].laz}</th>
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
                onClick={() => onVerbClick(verb)}
                className="hover:bg-blue-50 cursor-pointer transition-colors duration-150"
              >
                <td className="border px-4 py-2">{verb["infinitive_form"]}</td>
                <td className="border px-4 py-2">{verb["verb_root"]}</td>
                <td className="border px-4 py-2 text-center">
                  <Chip
                    label={verb["verb_type"]}
                    color={verbTypeColors[verb["verb_type"]]}
                  />
                </td>
                <td className="border px-4 py-2">{verb["turkish_verb"]}</td>
                <td className="border px-4 py-2">
                  {verb["english_translation"]}
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </>
  );
};

export default VerbsTable;
