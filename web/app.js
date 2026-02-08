async function loadConfig() {
  const res = await fetch("/api/config");
  const data = await res.json();

  const root = document.getElementById("app");
  root.innerHTML = "";

  for (const device in data) {
    const d = document.createElement("div");
    d.innerHTML = `<h2>${device}</h2>`;
    root.appendChild(d);

    for (const entity in data[device]) {
      const e = data[device][entity];

      const row = document.createElement("div");
      row.innerHTML = `
        <label>
          <input type="checkbox" ${e.enabled ? "checked" : ""}>
          ${entity}
        </label>
        <input value="${e.name}">
      `;

      row.querySelector("input[type=checkbox]").onchange = ev =>
        update(device, entity, { enabled: ev.target.checked });

      row.querySelector("input[type=text]").onchange = ev =>
        update(device, entity, { name: ev.target.value });

      d.appendChild(row);
    }
  }
}

async function update(device, entity, payload) {
  await fetch(`/api/config/${device}/${entity}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
}

loadConfig();
