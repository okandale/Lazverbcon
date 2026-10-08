const token =
  new URLSearchParams(location.hash.slice(1)).get("session") ||
  sessionStorage.getItem("laz-session");
if (token) sessionStorage.setItem("laz-session", token);
history.replaceState(null, "", "/");
const main = document.querySelector("#main"),
  dialog = document.querySelector("#dialog");
const notice = document.querySelector("#notice");
const state = {
  tab: "overview",
  offset: 0,
  entry: null,
  status: null,
  lastJob: null,
};
const esc = (x) =>
  String(x ?? "").replace(
    /[&<>"']/g,
    (c) =>
      ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[
        c
      ],
  );
const pretty = (x) => esc(JSON.stringify(x, null, 2));
const name = () => {
  const value = state.status.settings.actor?.trim();
  if (!value) {
    editActor();
    throw Error("Save your editor name, then try again.");
  }
  return value;
};
const notify = (text, error = false) => {
  notice.textContent = text;
  notice.className = error ? "error" : "";
  if (dialog.open && error) {
    let message = dialog.querySelector('[role="alert"]');
    if (!message) {
      message = document.createElement("p");
      message.setAttribute("role", "alert");
      message.className = "error";
      document.querySelector("#fields").prepend(message);
    }
    message.textContent = text;
    message.scrollIntoView({ block: "nearest" });
  }
};
async function api(path, body, method = "POST") {
  const response = await fetch("/api/" + path, {
    method: body === undefined ? "GET" : method,
    headers: {
      "X-Laz-Session": token || "",
      "Content-Type": "application/json",
    },
    body: body === undefined ? undefined : JSON.stringify(body),
  });
  const data = await response.json();
  if (!response.ok)
    throw Error(
      typeof data.detail === "string"
        ? data.detail
        : JSON.stringify(data.detail),
    );
  return data;
}
const run = (fn) => async (event) => {
  try {
    await fn(event);
  } catch (e) {
    notify(e.message, true);
  }
};
const button = (id, fn) => {
  const el = document.getElementById(id);
  if (el) el.onclick = run(fn);
};
const featuresText = (f) =>
  Object.entries(f)
    .filter(([, v]) => v !== false && v !== null && v !== "none")
    .map(([k, v]) => `${k.replaceAll("_", " ")}: ${v}`)
    .join(" · ");
const resultText = (v, empty = "Remove this request") =>
  v === null
    ? empty
    : v.status === "unsupported"
      ? `Unsupported: ${esc(v.reason)}`
      : v.forms
          .map(
            (f) =>
              `<strong>${esc(f.spelling)}</strong> <span class="pill">${esc(f.frame)}</span><br><span class="muted">Subject: ${esc(f.subject_pronoun) || "—"} · Object: ${esc(f.object_pronoun) || "—"}</span>`,
          )
          .join("<hr>");
function pager(total) {
  return `<div class="toolbar"><button id="prev" ${state.offset === 0 ? "disabled" : ""}>Previous</button><span>${total ? state.offset + 1 : 0}–${Math.min(state.offset + 100, total)} of ${total}</span><button id="next" ${state.offset + 100 >= total ? "disabled" : ""}>Next</button></div>`;
}
function pageButtons() {
  button("prev", async () => {
    state.offset = Math.max(0, state.offset - 100);
    await render();
  });
  button("next", async () => {
    state.offset += 100;
    await render();
  });
}
function modal(html, submit) {
  document.querySelector("#fields").innerHTML = html;
  document.querySelector("#editor").onsubmit = run(async (e) => {
    e.preventDefault();
    await submit(new FormData(e.target));
    dialog.close();
    await refresh();
  });
  dialog.showModal();
}
function updateActor() {
  const value = state.status.settings.actor?.trim();
  document.querySelector("#set-actor").textContent = value
    ? `Editor: ${value}`
    : "Set editor name";
}
function editActor() {
  if (dialog.open) return;
  modal(
    `<h2>Editor name</h2><p>Saved on this computer and recorded with your changes.</p><label>Your name<input name="actor" autocomplete="name" value="${esc(state.status.settings.actor || "")}" required></label>`,
    async (form) => {
      const value = form.get("actor").trim();
      if (!value) throw Error("Enter your name.");
      await api("settings", { ...state.status.settings, actor: value });
      notify("Editor name saved.");
    },
  );
  dialog.querySelector('[name="actor"]').focus();
}
button("set-actor", editActor);
button("close", () => dialog.close());
document.querySelectorAll("[data-tab]").forEach(
  (b) =>
    (b.onclick = run(async () => {
      state.tab = b.dataset.tab;
      state.offset = 0;
      await refresh();
    })),
);
button("stop", async () => {
  await api("shutdown", {});
  notify("App stopped. You can close this tab.");
  clearInterval(polling);
});
async function refresh() {
  state.status = await api("status");
  updateActor();
  await render();
}
async function render() {
  document
    .querySelectorAll("[data-tab]")
    .forEach((b) => b.classList.toggle("active", b.dataset.tab === state.tab));
  const s = state.status;
  if (state.tab === "overview") {
    main.innerHTML = `<h2>Your editing project</h2><div class="grid"><div class="card"><h3>${s.entries} verbs</h3><p>${s.records.toLocaleString()} approved grammatical requests</p></div><div class="card"><h3>${s.pending.toLocaleString()} proposals</h3><p>Pending changes are not published.</p></div><div class="card"><h3>Revision ${esc(s.revision)}</h3><p>Database and history stay on this computer.</p></div></div><div class="card"><h3>${s.entries ? "Workflow" : "Start a project"}</h3><ol>${!s.entries ? "<li>Import the original database once, or restore a current project backup in Backups.</li>" : ""}<li>Open a verb, edit forms or generate proposals.</li><li>Review changes before approving them.</li><li>Export and publish when ready.</li></ol>${!s.entries ? `<button id="seed" ${s.seed_available ? "" : "disabled"}>Import original database</button><p class="muted">One-time import of the original maintainer’s conjugations and pronouns. To continue an existing project, restore its current backup instead.</p>` : ""}<p>Project folder: <code>${esc(s.directory)}</code></p></div>`;
    button("seed", async () => {
      await api("seed", { actor: name() });
      notify("Baseline import started.");
    });
  } else if (state.tab === "entries") {
    if (state.entry) {
      await showRecords();
      return;
    }
    const rows = await api(
      "entries?q=" + encodeURIComponent(state.query || ""),
    );
    main.innerHTML = `<h2>Verbs</h2><div class="toolbar"><input id="search" aria-label="Search verbs" placeholder="Infinitive or meaning" value="${esc(state.query || "")}"><button id="search-go">Search</button><button id="new-entry">Add verb</button></div><div class="scroll"><table><thead><tr><th>Infinitive</th><th>Meaning</th><th>Class</th><th></th></tr></thead><tbody>${rows.map((e) => `<tr><td>${esc(e.infinitive)}</td><td>${esc(e.english)}<br>${esc(e.turkish)}</td><td>${esc(e.verb_class)}</td><td><button data-entry="${esc(e.id)}">Open</button></td></tr>`).join("")}</tbody></table></div>`;
    button("search-go", async () => {
      state.query = document.querySelector("#search").value;
      await render();
    });
    document.querySelector("#search").onkeydown = run(async (e) => {
      if (e.key === "Enter") {
        state.query = e.target.value;
        await render();
      }
    });
    button("new-entry", () => editEntry(null));
    document.querySelectorAll("[data-entry]").forEach(
      (b) =>
        (b.onclick = run(async () => {
          state.entry = rows.find((e) => e.id === b.dataset.entry);
          state.offset = 0;
          state.formQuery = "";
          state.formFilters = {};
          await render();
        })),
    );
  } else if (state.tab === "review") {
    const r = await api("proposals?offset=" + state.offset);
    main.innerHTML = `<h2>Review proposals</h2><p>Approval changes the master database. It does not publish the website.</p><div class="toolbar"><button id="select-all">Select this page</button><button id="approve" class="primary">Approve selected</button><button id="reject">Reject selected</button></div>${r.proposals.map((p) => `<article class="card"><label><input type="checkbox" data-proposal="${p.id}" ${p.conflict ? "disabled" : ""}> ${esc(p.entry_id)} · ${esc(p.actor)}</label><p class="muted">${esc(featuresText(p.features))}</p>${p.conflict ? '<p class="warning">Approved data changed. Reject this proposal and generate or edit again.</p>' : ""}<div class="grid"><section><h3>Approved</h3>${resultText(p.before, "No approved result")}</section><section><h3>Proposed</h3>${resultText(p.value)}</section></div><p>${esc(p.reason)}</p><small>Batch ${esc(p.batch)}</small>${p.conflict ? `<button data-reject="${p.id}">Reject stale proposal</button>` : ""}</article>`).join("") || "<p>No pending proposals.</p>"}${pager(r.total)}`;
    button("select-all", () =>
      document
        .querySelectorAll("[data-proposal]:not(:disabled)")
        .forEach((c) => (c.checked = true)),
    );
    for (const approve of [true, false])
      button(approve ? "approve" : "reject", async () => {
        const ids = [
          ...document.querySelectorAll("[data-proposal]:checked"),
        ].map((c) => c.dataset.proposal);
        await api("review", { ids, approve, actor: name() });
        notify(approve ? "Changes approved." : "Proposals rejected.");
        await refresh();
      });
    document.querySelectorAll("[data-reject]").forEach(
      (b) =>
        (b.onclick = run(async () => {
          await api("review", {
            ids: [b.dataset.reject],
            approve: false,
            actor: name(),
          });
          await refresh();
        })),
    );
    pageButtons();
  } else if (state.tab === "import") {
    main.innerHTML = `<h2>Import conjugations</h2><p>Files create review proposals. They never replace approved forms immediately.</p><div class="card"><input type="file" id="import-file" accept=".json,.csv"><label>Source or explanation<input id="import-reason" placeholder="Source and date"></label><button id="import-preview">Preview file</button><div id="import-result"></div></div><details><summary>File formats</summary><p>CSV: one alternative spelling per row. Repeated entry/feature combinations form one complete set of alternatives.</p><pre>entry_id,dialect,subject,object,tense,mood,derivation,applicative,causative,optional_preverb,optional_prefix,spelling,frame,subject_pronoun,object_pronoun,rule</pre><p>Blank object means no object; booleans are true/false. JSON is a list of requests:</p><pre>${pretty([{ entry_id: "verb-0026", features: { dialect: "AS", subject: "1sg" }, value: { status: "ok", forms: [{ spelling: "example", frame: "Ergative", subject_pronoun: "ma", object_pronoun: "" }], source: "Author review" } }])}</pre></details>`;
    button("import-preview", async () => {
      const file = document.querySelector("#import-file").files[0];
      if (!file) throw Error("Choose a file");
      if (file.size > 20 * 1024 * 1024)
        throw Error("Split imports into files under 20 MiB");
      const text = await file.text(),
        format = file.name.endsWith(".csv") ? "csv" : "json";
      const p = await api("import-preview", { text, format });
      document.querySelector("#import-result").innerHTML =
        `<p>${p.requests} grammatical requests. First ${p.sample.length}:</p><pre>${pretty(p.sample)}</pre><button id="import-confirm">Create review proposals</button>`;
      button("import-confirm", async () => {
        const r = await api("import", {
          text,
          format,
          actor: name(),
          reason: document.querySelector("#import-reason").value,
        });
        notify(`${r.proposals} proposals created.`);
        state.tab = "review";
        state.offset = 0;
        await refresh();
      });
    });
  } else if (state.tab === "history") {
    const rows = await api("history?offset=" + state.offset);
    main.innerHTML = `<div class="scroll"><table class="history-log" aria-label="Change history"><thead><tr><th scope="col">Date / time</th><th scope="col">Before</th><th scope="col">After</th></tr></thead><tbody>${rows.map((e) => `<tr><td><time datetime="${esc(e.created)}">${esc(new Date(e.created).toLocaleString())}</time>${["entry", "record"].includes(e.entity) ? `<button data-undo="${e.id}" title="Undo creates a new logged change and cannot overwrite later edits">Undo</button>` : ""}</td><td>${e.before_value ? `<pre>${pretty(JSON.parse(e.before_value))}</pre>` : "—"}</td><td>${e.after_value ? `<pre>${pretty(JSON.parse(e.after_value))}</pre>` : "—"}</td></tr>`).join("") || '<tr><td colspan="3">No changes yet.</td></tr>'}</tbody></table></div><div class="toolbar"><button id="prev" ${!state.offset ? "disabled" : ""}>Previous</button><button id="next" ${rows.length < 100 ? "disabled" : ""}>Next</button></div>`;
    document.querySelectorAll("[data-undo]").forEach(
      (b) =>
        (b.onclick = run(async () => {
          await api("undo", { id: Number(b.dataset.undo), actor: name() });
          notify("Change reversed.");
          await refresh();
        })),
    );
    pageButtons();
  } else if (state.tab === "backups") {
    const rows = await api("backups");
    main.innerHTML = `<h2>Backups and handover</h2><p>The latest 14 daily backups are kept. Manual and before-operation backups are retained. Choose an external backup folder in Settings.</p><button id="backup">Back up now</button><div class="card"><h3>Restore a project</h3><p>This replaces the current project with the selected backup, including its history. A backup of the current project is created first.</p><input type="file" id="restore-file" accept=".sqlite"><label><input type="checkbox" id="restore-confirm"> I want to replace this project with the selected backup.</label><button id="restore">Restore backup</button></div><table><tbody>${rows.map((r) => `<tr><td>${esc(r.name)}</td><td>${(r.bytes / 1024 / 1024).toFixed(1)} MiB</td><td><button data-download="${esc(r.name)}">Download</button></td></tr>`).join("")}</tbody></table>`;
    button("backup", async () => {
      const r = await api("backup", {});
      notify("Backup saved: " + r.path);
      await render();
    });
    document
      .querySelectorAll("[data-download]")
      .forEach(
        (b) => (b.onclick = run(() => download("backups", b.dataset.download))),
      );
    button("restore", async () => {
      const file = document.querySelector("#restore-file").files[0];
      if (!file || !document.querySelector("#restore-confirm").checked)
        throw Error("Choose a backup and confirm replacement.");
      const res = await fetch("/api/restore", {
        method: "POST",
        headers: {
          "X-Laz-Session": token,
          "X-Laz-Actor": encodeURIComponent(name()),
        },
        body: file,
      });
      const r = await res.json();
      if (!res.ok) throw Error(r.detail);
      state.entry = null;
      notify("Backup restored.");
      await refresh();
    });
  } else if (state.tab === "publish") {
    const rows = await api("exports");
    const settings = s.settings;
    main.innerHTML = `<h2>Publish approved data</h2><p>Export creates a fixed snapshot. GitHub publishing updates the release pointer; Cloudflare then builds the website. Draft proposals and history stay private.</p><button id="export" class="primary">Export approved snapshot</button><div class="card"><h3>Publish destination</h3><p>The website is the Cloudflare Pages project connected to this repository and branch. Set its domain in Cloudflare.</p><label>Repository<input id="repository" value="${esc(settings.repository || "")}" placeholder="owner/Lazverbcon"></label><label>Pages branch<input id="branch" value="${esc(settings.branch || "codex/static-export")}"></label><label>GitHub token<input type="password" id="github-token" autocomplete="off"></label><p class="muted">Use a fine-grained token with Contents read/write access to this public repository. The remake branch also needs Workflows read/write to create release tags at commits that change workflow files. Configure Pages once using the instructions in docs/admin-app.md. Tokens stay out of the project database and backups.</p><p id="credential-status" class="muted"></p>${s.credential_storage_available ? `<div class="toolbar"><button id="remember-token">Remember token on this computer</button><button id="forget-token">Forget saved token</button></div><p class="muted">Optional. Uses Windows Credential Manager for your Windows account on this computer.</p>` : ""}<label><input type="checkbox" id="publish-confirm"> I have reviewed the export and approve publishing to <span id="publish-destination"></span>.</label></div>${rows.map((r) => `<article class="card"><h3>Revision ${r.revision}</h3><p>${r.forms.toLocaleString()} forms · release ${esc(r.release)}</p><div class="toolbar"><button data-export-download="${esc(r.filename)}">Download ZIP</button><button data-preview="${esc(r.filename)}" ${s.preview_available ? "" : "disabled"}>Preview website</button><button data-publish="${esc(r.filename)}">Publish to GitHub</button></div></article>`).join("")}`;
    const destinationInputs = ["repository", "branch"].map((id) =>
      document.getElementById(id),
    );
    const updateDestination = () => {
      const [repository, branch] = destinationInputs.map((input) =>
        input.value.trim(),
      );
      document.querySelector("#publish-destination").textContent =
        repository && branch
          ? `${repository} (${branch})`
          : "the repository and branch above";
      document.querySelector("#publish-confirm").checked = false;
    };
    destinationInputs.forEach((input) =>
      input.addEventListener("input", updateDestination),
    );
    updateDestination();
    let credentialRequest = 0;
    let savedCredential = false;
    const loadCredential = async () => {
      const request = ++credentialRequest;
      savedCredential = false;
      const repository = document.querySelector("#repository").value.trim();
      const message = document.querySelector("#credential-status");
      const input = document.querySelector("#github-token");
      for (const id of ["remember-token", "forget-token"]) {
        const control = document.getElementById(id);
        if (control)
          control.disabled = !/^[A-Za-z0-9_.-]+\/[A-Za-z0-9_.-]+$/.test(
            repository,
          );
      }
      input.placeholder = "Paste a token";
      if (!s.credential_storage_available) {
        message.textContent =
          "Enter a token for each publication. Remembering tokens is available on Windows.";
        return;
      }
      if (!/^[A-Za-z0-9_.-]+\/[A-Za-z0-9_.-]+$/.test(repository)) {
        message.textContent = "Enter a repository to check for a saved token.";
        return;
      }
      message.textContent = "Checking for a saved token…";
      try {
        const result = await api(
          "github-credential?repository=" + encodeURIComponent(repository),
        );
        if (request !== credentialRequest || !message.isConnected) return;
        savedCredential = result.saved;
        message.textContent = savedCredential
          ? "Saved token available for this repository. Leave the field blank to use it."
          : "No token saved for this repository. Paste one to publish or remember it.";
        input.placeholder = savedCredential
          ? "Use saved token, or paste a replacement"
          : "Paste a token";
      } catch (error) {
        if (request === credentialRequest && message.isConnected)
          message.textContent = `${error.message}. You can still enter a token for this publication.`;
      }
    };
    document.querySelector("#repository").addEventListener("input", () => {
      document.querySelector("#github-token").value = "";
      void loadCredential();
    });
    button("remember-token", async () => {
      const input = document.querySelector("#github-token");
      const secret = input.value;
      input.value = "";
      await api("github-credential", {
        repository: document.querySelector("#repository").value.trim(),
        token: secret,
      });
      await loadCredential();
      notify(
        "Token saved in Windows Credential Manager. Saving does not publish the website.",
      );
    });
    button("forget-token", async () => {
      await api(
        "github-credential",
        {
          repository: document.querySelector("#repository").value.trim(),
        },
        "DELETE",
      );
      await loadCredential();
      notify(
        "Saved token removed from this computer. This does not revoke it on GitHub.",
      );
    });
    await loadCredential();
    button("export", async () => {
      await api("export", { actor: name() });
      notify("Export started.");
    });
    document.querySelectorAll("[data-preview]").forEach(
      (b) =>
        (b.onclick = run(async () => {
          await api("preview", { filename: b.dataset.preview });
          notify("Preparing preview. A link will appear here when ready.");
        })),
    );
    document
      .querySelectorAll("[data-export-download]")
      .forEach(
        (b) =>
          (b.onclick = run(() =>
            download("exports", b.dataset.exportDownload),
          )),
      );
    document.querySelectorAll("[data-publish]").forEach(
      (b) =>
        (b.onclick = run(async () => {
          if (!document.querySelector("#publish-confirm").checked)
            throw Error("Confirm publication first.");
          const input = document.querySelector("#github-token");
          const secret = input.value;
          if (!secret && !savedCredential)
            throw Error(
              "Enter a GitHub token or remember one for this repository.",
            );
          input.value = "";
          await api("publish", {
            filename: b.dataset.publish,
            actor: name(),
            token: secret,
            repository: document.querySelector("#repository").value.trim(),
            branch: document.querySelector("#branch").value.trim(),
          });
          notify("Publishing started.");
        })),
    );
  } else if (state.tab === "settings") {
    const v = s.settings;
    main.innerHTML = `<h2>Settings</h2><form id="settings" class="card"><label>Editor name<input name="actor" value="${esc(v.actor || "")}" autocomplete="name" required></label><label>Additional backup folder<input name="backup_directory" value="${esc(v.backup_directory || "")}" placeholder="For example a folder inside OneDrive or an external drive"></label><p>Completed backups are copied here. The live database stays in the local project folder.</p><label>GitHub repository<input name="repository" value="${esc(v.repository || "")}" placeholder="owner/repository"></label><label>Pages branch<input name="branch" value="${esc(v.branch || "codex/static-export")}"></label><button type="submit">Save settings</button></form><p>Project: <code>${esc(s.project)}</code><br>Data folder: <code>${esc(s.directory)}</code></p>`;
    document.querySelector("#settings").onsubmit = run(async (e) => {
      e.preventDefault();
      const value = Object.fromEntries(new FormData(e.target));
      value.actor = value.actor.trim();
      if (!value.actor) throw Error("Enter your name.");
      await api("settings", value);
      notify("Settings saved.");
      await refresh();
    });
  }
}
async function showRecords() {
  const e = state.entry;
  const r = await api(
    `records/${encodeURIComponent(e.id)}?offset=${state.offset}&q=${encodeURIComponent(state.formQuery || "")}&filters=${encodeURIComponent(JSON.stringify(state.formFilters || {}))}`,
  );
  main.innerHTML = `<button id="back">← Verbs</button><h2>${esc(e.infinitive)}</h2><p>${esc(e.english)} · ${esc(e.turkish)} · ${esc(e.verb_class)}</p><div class="toolbar"><button id="entry-edit">Edit verb</button><button id="new-form">Add conjugation</button><button id="generate">Generate proposals for this verb</button></div><p>Generated proposals never replace approved forms automatically.</p><div class="toolbar"><input id="form-search" placeholder="Find a spelling" aria-label="Find a spelling" value="${esc(state.formQuery || "")}"><button id="form-go">Search</button></div><details><summary>Filter grammatical features</summary><div class="grid">${Object.entries(
    state.status.dimensions,
  )
    .map(
      ([k, values]) =>
        `<label>${esc(k.replaceAll("_", " "))}<select data-filter="${k}"><option value="">Any</option>${values.map((v) => `<option value="${esc(JSON.stringify(v))}" ${state.formFilters && Object.hasOwn(state.formFilters, k) && state.formFilters[k] === v ? "selected" : ""}>${esc(v === null ? "No object" : String(v))}</option>`).join("")}</select></label>`,
    )
    .join(
      "",
    )}</div><button id="apply-filters">Apply filters</button><button id="clear-filters">Clear filters</button></details>${r.records.map((row, i) => `<article class="card"><p class="muted">${esc(featuresText(row.features))}</p>${resultText(row.value)}<details><summary>Source</summary><p>${esc(row.value.source || "Manual record")}</p></details><p><button data-edit="${i}">Edit</button> <button data-remove="${i}">Propose removal</button></p></article>`).join("")}${pager(r.total)}`;
  button("back", async () => {
    state.entry = null;
    state.offset = 0;
    await render();
  });
  button("entry-edit", () => editEntry(e));
  button("new-form", () => editForm(null));
  button("generate", async () => {
    await api("generate", { entry_id: e.id, actor: name() });
    notify("Generating proposals.");
  });
  button("apply-filters", async () => {
    state.formFilters = Object.fromEntries(
      [...document.querySelectorAll("[data-filter]")]
        .filter((input) => input.value !== "")
        .map((input) => [input.dataset.filter, JSON.parse(input.value)]),
    );
    state.offset = 0;
    await render();
  });
  button("clear-filters", async () => {
    state.formFilters = {};
    state.offset = 0;
    await render();
  });
  button("form-go", async () => {
    state.formQuery = document.querySelector("#form-search").value;
    state.offset = 0;
    await render();
  });
  document
    .querySelectorAll("[data-edit]")
    .forEach(
      (b) => (b.onclick = () => editForm(r.records[Number(b.dataset.edit)])),
    );
  document.querySelectorAll("[data-remove]").forEach(
    (b) =>
      (b.onclick = run(async () => {
        const row = r.records[Number(b.dataset.remove)];
        await api("proposal", {
          actor: name(),
          reason: "Proposed removal",
          items: [
            {
              entry_id: e.id,
              features: row.features,
              value: null,
              expected_hash: row.expected_hash,
            },
          ],
        });
        notify("Removal proposed. Approve it in Review.");
      })),
  );
  pageButtons();
}
function editEntry(e) {
  const initial = e || {
    id: "entry-" + crypto.randomUUID(),
    infinitive: "",
    english: "",
    turkish: "",
    verb_class: "TVE",
    source_row: 0,
    issues: [],
    variants: [],
  };
  modal(
    `<h2>${e ? "Edit" : "Add"} verb</h2><div class="grid">${["infinitive", "english", "turkish"].map((k) => `<label>${k}<input name="${k}" value="${esc(initial[k])}" ${k === "infinitive" ? "required" : ""}></label>`).join("")}<label>Class<select name="verb_class">${["IVD", "TVE", "TVM"].map((c) => `<option ${initial.verb_class === c ? "selected" : ""}>${c}</option>`).join("")}</select></label></div><label>Principal parts: one per line, followed by | and dialects<textarea name="variants" required placeholder="isinapams | AS,PZ,FA">${esc(initial.variants.map((p) => p.form + " | " + p.dialects.join(",")).join("\n"))}</textarea></label><p>Dialect codes: AS, PZ, FA, HO. Leave a principal part blank before | for a dialect with manually supplied forms only.</p><label>Explanation<input name="reason"></label>`,
    async (form) => {
      const value = {
        ...initial,
        ...Object.fromEntries(
          ["infinitive", "english", "turkish", "verb_class"].map((k) => [
            k,
            form.get(k),
          ]),
        ),
        variants: String(form.get("variants"))
          .split("\n")
          .filter((l) => l.trim())
          .map((l) => {
            const [word, ds = ""] = l.split("|");
            return {
              form: word.trim(),
              dialects: ds
                .split(",")
                .map((d) => d.trim())
                .filter(Boolean),
            };
          }),
      };
      state.entry = await api("entry", {
        entry: value,
        expected: e,
        actor: name(),
        reason: form.get("reason"),
      });
      state.tab = "entries";
      notify("Verb saved in change history.");
    },
  );
}
function editForm(row) {
  const e = state.entry;
  const f = row?.features || {
    dialect: e.variants.flatMap((p) => p.dialects)[0],
    subject: "1sg",
    object: null,
    tense: "present",
    mood: "indicative",
    derivation: "none",
    applicative: false,
    causative: "none",
    optional_preverb: false,
    optional_prefix: "none",
  };
  const forms = row?.value.forms || [
    {
      spelling: "",
      frame: { IVD: "Dative", TVE: "Ergative", TVM: "Nominative" }[
        e.verb_class
      ],
      subject_pronoun: "",
      object_pronoun: "",
      rule: "editorial",
    },
  ];
  modal(
    `<h2>${row ? "Edit" : "Add"} conjugation</h2><div class="grid">${Object.entries(
      state.status.dimensions,
    )
      .map(
        ([k, values]) =>
          `<label>${esc(k.replaceAll("_", " "))}<select name="${k}" ${row ? "disabled" : ""}>${values.map((v) => `<option value="${esc(JSON.stringify(v))}" ${v === f[k] ? "selected" : ""}>${esc(v === null ? "No object" : String(v))}</option>`).join("")}</select></label>`,
      )
      .join(
        "",
      )}</div>${row ? "<p>To change the grammatical analysis, add a new request and propose removal of this one.</p>" : ""}<label>Status<select name="status"><option value="ok">Forms available</option><option value="unsupported" ${row?.value.status === "unsupported" ? "selected" : ""}>Unsupported combination</option></select></label><div id="variants"></div><button type="button" id="add-variant">Add alternative spelling</button><label>Explanation / source<textarea name="reason" required></textarea></label>`,
    async (form) => {
      const fs = row
        ? f
        : Object.fromEntries(
            Object.keys(state.status.dimensions).map((k) => [
              k,
              JSON.parse(form.get(k)),
            ]),
          );
      const values = [...document.querySelectorAll(".variant")].map((v) =>
        Object.fromEntries(
          [...v.querySelectorAll("[data-field]")].map((input) => [
            input.dataset.field,
            input.value,
          ]),
        ),
      );
      await api("proposal", {
        actor: name(),
        reason: form.get("reason"),
        items: [
          {
            entry_id: e.id,
            features: fs,
            expected_hash: row?.expected_hash,
            value: {
              status: form.get("status"),
              forms: form.get("status") === "ok" ? values : [],
              reason: form.get("reason"),
              source: "Manual edit",
            },
          },
        ],
      });
      notify("Saved as a proposal. Review and approve it when ready.");
    },
  );
  const add = (value) => {
    const block = document.createElement("section");
    block.className = "variant";
    block.innerHTML = `<div class="grid">${["spelling", "subject_pronoun", "object_pronoun"].map((k) => `<label>${esc(k.replaceAll("_", " "))}<input data-field="${k}" value="${esc(value[k] || "")}"></label>`).join("")}<label>Frame<select data-field="frame">${["Dative", "Ergative", "Nominative"].map((x) => `<option ${value.frame === x ? "selected" : ""}>${x}</option>`).join("")}</select></label><input type="hidden" data-field="rule" value="${esc(value.rule || "editorial")}"></div><button type="button" class="remove">Remove alternative</button>`;
    block.querySelector(".remove").onclick = () => block.remove();
    document.querySelector("#variants").append(block);
  };
  forms.forEach(add);
  button("add-variant", () => add({ frame: forms[0]?.frame || "Ergative" }));
}
async function download(kind, filename) {
  const res = await fetch(
    `/api/download/${kind}/${encodeURIComponent(filename)}`,
    { headers: { "X-Laz-Session": token } },
  );
  if (!res.ok) throw Error("Download failed");
  const url = URL.createObjectURL(await res.blob()),
    a = document.createElement("a");
  a.href = url;
  a.download = filename;
  a.click();
  setTimeout(() => URL.revokeObjectURL(url), 30000);
}
async function poll() {
  try {
    const j = await api("job"),
      box = document.querySelector("#job");
    if (!j) {
      box.hidden = true;
      return;
    }
    if (j.state === "running") {
      box.hidden = false;
      box.textContent = `${j.name} · ${j.progress.toLocaleString()} processed `;
      if (j.name !== "Publish to GitHub") {
        const b = document.createElement("button");
        b.textContent = "Cancel";
        b.onclick = run(() => api("cancel", {}));
        box.append(b);
      }
    } else {
      box.hidden = true;
      if (state.lastJob !== j.id) {
        state.lastJob = j.id;
        notify(
          j.state === "failed"
            ? j.error
            : `${j.name} complete. ${JSON.stringify(j.result)}`,
          j.state === "failed",
        );
        await refresh();
        if (j.result?.preview_url) {
          const a = document.createElement("a");
          a.href = j.result.preview_url;
          a.target = "_blank";
          a.rel = "noopener";
          a.textContent = "Open website preview";
          notice.replaceChildren(a);
        }
      }
    }
  } catch {
    /* Launcher may have been stopped. */
  }
}
const polling = setInterval(poll, 2000);
try {
  state.status = await api("status");
  updateActor();
  await render();
  if (!state.status.settings.actor?.trim()) editActor();
} catch (e) {
  main.textContent = "Open this page using the Lazuri Admin launcher.";
  notify(e.message, true);
}
