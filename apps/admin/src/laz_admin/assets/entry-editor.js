const dialects = {
  AS: "Ardeşen (AŞ)",
  PZ: "Pazar (PZ)",
  FA: "Fındıklı · Arhavi (FA)",
  HO: "Hopa (HO)",
};
const esc = (value) =>
  String(value ?? "").replace(
    /[&<>"']/g,
    (c) =>
      ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[
        c
      ],
  );

export function presentBases(container, initial) {
  const add = (part = { form: "", dialects: [] }) => {
    const row = document.createElement("section");
    row.className = "variant present-base";
    row.innerHTML = `<label>Present base<input data-base value="${esc(part.form)}" placeholder="For example, isinapams"></label><fieldset><legend>Dialects for this base</legend><div class="dialect-checks">${Object.entries(
      dialects,
    )
      .map(
        ([code, label]) =>
          `<label><input type="checkbox" value="${code}" ${part.dialects.includes(code) ? "checked" : ""}>${label}</label>`,
      )
      .join("")}</div></fieldset><button type="button">Remove base</button>`;
    row.querySelector("button").onclick = () => row.remove();
    container.append(row);
  };
  (initial.length ? initial : [{ form: "", dialects: [] }]).forEach(add);
  return {
    add: () => add(),
    read: () =>
      [...container.querySelectorAll(".present-base")]
        .map((row) => ({
          form: row.querySelector("[data-base]").value.trim(),
          dialects: [...row.querySelectorAll("input:checked")].map(
            (input) => input.value,
          ),
        }))
        .filter((part) => part.form || part.dialects.length),
  };
}

export function generationOptions(initial, dimensions) {
  return new Promise((resolve) => {
    const dialog = document.createElement("dialog");
    dialog.innerHTML = `<form><h2>Generation exceptions</h2><label><input type="checkbox" name="preverb-lookalike" ${initial.preverb_lookalike ? "checked" : ""}> Looks like a preverb, but isn't</label><p>Treat the beginning as part of the stem when generating forms. Use only for a confirmed exception, such as oǩoru.</p><h3>Do not generate these combinations</h3><p>Choose the features to exclude in each row. Every selection in a row must match. Separate rows exclude additional combinations.</p><p>For example, Present + Indicative reserves those combinations for manual entry. Approved forms are kept and will still be published.</p><div class="exclusions"></div><button type="button" data-add>Add exclusion</button><p role="alert" class="error"></p><footer><button type="button" data-cancel>Cancel</button><button type="submit">Apply options</button></footer></form>`;
    const label = (key) =>
      ({
        tense: "Tense / aspect",
        mood: "Mood",
        derivation: "Derivation",
        dialect: "Dialect",
        subject: "Subject",
        object: "Object",
        applicative: "Applicative",
        causative: "Causative",
        optional_prefix: "Optional preverb",
      })[key];
    const fields = (keys) =>
      keys
        .map(
          (key) =>
            `<label>${label(key)}<select data-feature="${key}"><option value="">Any</option>${dimensions[key].map((value) => `<option value="${esc(JSON.stringify(value))}">${esc(value === null ? "No object" : String(value).replaceAll("_", " "))}</option>`).join("")}</select></label>`,
        )
        .join("");
    const add = (rule = {}) => {
      const row = document.createElement("section");
      row.className = "variant";
      row.innerHTML = `<div class="grid">${fields(["tense", "mood", "derivation", "dialect"])}</div><details><summary>Persons and markers</summary><div class="grid">${fields(["subject", "object", "applicative", "causative", "optional_prefix"])}</div></details><button type="button">Remove exclusion</button>`;
      for (const [key, value] of Object.entries(rule)) {
        row.querySelector(`[data-feature="${key}"]`).value =
          JSON.stringify(value);
      }
      if (
        [
          "subject",
          "object",
          "applicative",
          "causative",
          "optional_prefix",
        ].some((key) => Object.hasOwn(rule, key))
      )
        row.querySelector("details").open = true;
      row.querySelector("button").onclick = () => row.remove();
      dialog.querySelector(".exclusions").append(row);
    };
    initial.excluded_combinations.forEach(add);
    dialog.querySelector("[data-add]").onclick = () =>
      add({ tense: "present", mood: "indicative", derivation: "none" });
    dialog.querySelector("[data-cancel]").onclick = () => dialog.close();
    let result = null;
    dialog.querySelector("form").onsubmit = (event) => {
      event.preventDefault();
      const rows = [...dialog.querySelectorAll(".exclusions > section")].map(
        (row) =>
          Object.fromEntries(
            [...row.querySelectorAll("select")]
              .filter((select) => select.value !== "")
              .map((select) => [
                select.dataset.feature,
                JSON.parse(select.value),
              ]),
          ),
      );
      if (rows.some((row) => !Object.keys(row).length)) {
        dialog.querySelector('[role="alert"]').textContent =
          "Choose at least one feature for every exclusion, or remove the empty row.";
        return;
      }
      result = {
        preverb_lookalike: dialog.querySelector('[name="preverb-lookalike"]')
          .checked,
        excluded_combinations: rows,
      };
      dialog.close();
    };
    dialog.onclose = () => {
      dialog.remove();
      resolve(result);
    };
    document.body.append(dialog);
    dialog.showModal();
  });
}
