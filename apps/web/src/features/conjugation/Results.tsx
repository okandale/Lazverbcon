import React from "react";
import type { Dialect, Request, Response } from "../../api/client";
import { dialectNames, labels, names } from "../../i18n";
import type { Language } from "../../i18n";
import { restrictionText } from "../../restrictions";
const dialects = Object.keys(dialectNames) as Dialect[];

export function Results({
  data,
  language,
  object = null,
}: {
  data: Response;
  language: Language;
  object?: Request["object"];
}) {
  const t = labels[language];
  const unavailable = data.cells.filter((c) => c.status !== "ok");
  const errors = [
    ...new Set(
      unavailable.map((c) =>
        restrictionText(c.reason ?? c.status, c.message, language),
      ),
    ),
  ];
  return (
    <>
      <div className="dialect-results">
        {dialects.map((d) => {
          const cells = data.cells.filter(
            (c) => c.features.dialect === d && c.status === "ok",
          );
          return cells.length ? (
            <div className="dialect-card" key={d}>
              <h3>
                <span>{d === "AS" ? "AŞ" : d}</span>
                {dialectNames[d]}
              </h3>
              <table>
                <thead>
                  <tr>
                    <th>{t.subject}</th>
                    {object != null && <th>{t.object}</th>}
                    <th>{t.forms}</th>
                  </tr>
                </thead>
                <tbody>
                  {cells.flatMap((cell, i) =>
                    (cell.forms ?? []).map((form, j) => (
                      <tr key={`${i}-${j}`}>
                        <td>
                          <span lang="lzz">{form.subject_pronoun}</span>{" "}
                          <small>{names[language][form.subject]}</small>
                        </td>
                        {object != null && (
                          <td>
                            {form.object
                              ? names[language][form.object]
                              : t.none}
                          </td>
                        )}
                        <td lang="lzz">{form.spelling}</td>
                      </tr>
                    )),
                  )}
                </tbody>
              </table>
            </div>
          ) : null;
        })}
      </div>
      {!data.cells.some((c) => c.status === "ok") && <p>{t.noForms}</p>}
      {errors.length > 0 &&
        (!data.cells.some((c) => c.status === "ok") ||
          unavailable.some((c) => c.status === "error")) && (
          <div className="selection-notes">
            <ul>
              {errors.map((e, i) => (
                <li key={i}>{e}</li>
              ))}
            </ul>
          </div>
        )}
    </>
  );
}
