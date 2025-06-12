import React, { useState } from "react";
import { Link } from "react-router-dom";
import { Home } from "lucide-react";
import LanguageToggle from "./ui/LanguageToggle";
import {
  API_URLS,
  translations,
  getStoredLanguage,
  setStoredLanguage,
} from "./constants";

import { useNavigate } from 'react-router-dom';

const AdminAuth = () => {
  const [language, setLanguage] = useState(getStoredLanguage());
  const t = translations[language];
  const toggleLanguage = () => {
    const newLanguage = language === "en" ? "tr" : "en";
    setLanguage(newLanguage);
    setStoredLanguage(newLanguage);
  };

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const navigate = useNavigate();

  const onSubmit = async (e) => {
    e.preventDefault();
    console.log("Submitted!");
    try {
      const response = await fetch(API_URLS.admin.auth, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username,
          password,
        }),
      });
      console.log(JSON.stringify(response));
      const data = await response.json();
      const accessToken = data["access_token"];
      localStorage.setItem("accessToken", accessToken);
      navigate("/admin/panel");
    } catch(error) {
      console.log(`Couldn’t authenticate: ${error}.`);
    }
    return false;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-white">
      <div className="max-w-4xl mx-auto p-4">
        {/* Header with navigation and language toggle */}
        <div className="flex justify-between items-center mb-8 pt-2">
          <Link to="/" className="text-gray-600 hover:text-gray-800">
            <Home size={24} />
          </Link>
          <LanguageToggle language={language} onToggle={toggleLanguage} />
        </div>

        {/* Title */}
        <h1 className="text-3xl font-bold mb-6 text-center">Admin</h1>

        <form method="POST" onSubmit={onSubmit}>
          <div className="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
            <div className="mb-4">
              <label
                className="block text-gray-700 text-sm font-bold md-2"
                htmlFor="username"
              >
                Username
              </label>
              <input
                className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                id="username"
                type="text"
                name="infinitive"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
              />
            </div>

            <div className="mb-4">
              <label
                className="block text-gray-700 text-sm font-bold md-2"
                htmlFor="password"
              >
                Password
              </label>
              <input
                className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                id="password"
                type="password"
                name="infinitive"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>

            <div className="text-center">
              <button
                className="flex-1 min-w-32 bg-blue-500 hover:bg-blue-600 active:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors duration-150 ease-in-out shadow-md hover:shadow-lg focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-opacity-50 disabled:opacity-50 disabled:cursor-not-allowed"
                type="submit"
              >
                <span className="block w-full text-center">Submit</span>
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  );
};

export default AdminAuth;
