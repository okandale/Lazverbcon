import React from "react";
import type { Dialect, Response } from "../../api/client";
import { dialectNames, labels, names } from "../../i18n";
import type { Language } from "../../i18n";
import { restrictionText } from "../../restrictions";
const dialects = Object.keys(dialectNames) as Dialect[];

export function Results({
  data,
  language,
}: {
  data: Response;
  language: Language;
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
                    <th>{t.forms}</th>
                  </tr>
                </thead>
                <tbody>
                  {cells.flatMap((cell, i) =>
                    (cell.forms ?? []).map((form, j) => (
                      <tr key={`${i}-${j}`}>
                        <td>
                          {form.subject_pronoun}
                          <small>
                            {names[language][form.subject]}
                            {form.object && ` → ${form.object_pronoun}`}
                          </small>
                        </td>
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
      {errors.length > 0 && (
        <details className="issues">
          <summary>
            {t.unavailable} ({unavailable.length})
          </summary>
          <ul>
            {errors.map((e, i) => (
              <li key={i}>{e}</li>
            ))}
          </ul>
        </details>
      )}
    </>
  );
}
