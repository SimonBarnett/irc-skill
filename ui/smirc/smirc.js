(function () {
  "use strict";

  const DEMO = window.SMIRC_DEMO !== false;

  const state = {
    buffers: {},
    activeId: null,
    channelUsers: {},
  };

  function bufferId(kind, name) {
    return kind === "dm" ? "dm:" + name : "chan:" + name;
  }

  function seedDemo() {
    const channels = ["#bobiverse", "#smirc-ui", "#demo"];
    channels.forEach((ch) => {
      const id = bufferId("chan", ch);
      state.buffers[id] = {
        id,
        kind: "chan",
        name: ch,
        lines: [{ who: "system", text: "Demo buffer (no live IRC)." }],
      };
      state.channelUsers[ch] = ["alice", "bob", "chair"];
    });
    state.activeId = bufferId("chan", "#demo");
    state.buffers[state.activeId].lines.push({
      who: "alice",
      text: "Layout: channels left, tabs bottom, users right.",
    });
  }

  function el(id) {
    return document.getElementById(id);
  }

  function renderChannels() {
    const ul = el("channel-list");
    ul.innerHTML = "";
    Object.values(state.buffers)
      .filter((b) => b.kind === "chan")
      .sort((a, b) => a.name.localeCompare(b.name))
      .forEach((b) => {
        const li = document.createElement("li");
        const btn = document.createElement("button");
        btn.type = "button";
        btn.className = "channel" + (state.activeId === b.id ? " active" : "");
        btn.textContent = b.name;
        btn.addEventListener("click", () => focusBuffer(b.id));
        li.appendChild(btn);
        ul.appendChild(li);
      });
  }

  function renderTabs() {
    const ul = el("tab-list");
    ul.innerHTML = "";
    Object.values(state.buffers).forEach((b) => {
      const li = document.createElement("li");
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "tab" + (state.activeId === b.id ? " active" : "");
      btn.textContent = b.kind === "dm" ? "@" + b.name : b.name;
      btn.addEventListener("click", () => focusBuffer(b.id));
      li.appendChild(btn);
      ul.appendChild(li);
    });
  }

  function renderLog() {
    const buf = state.buffers[state.activeId];
    if (!buf) return;
    el("chat-title").textContent = buf.kind === "dm" ? "DM " + buf.name : buf.name;
    const log = el("chat-log");
    log.innerHTML = "";
    buf.lines.forEach((line) => {
      const div = document.createElement("div");
      div.className = "line";
      if (line.imageUrl) {
        div.innerHTML =
          '<span class="meta">' +
          escapeHtml(line.who) +
          '</span> [image: ' +
          escapeHtml(line.text) +
          '] <img alt="" src="' +
          line.imageUrl +
          '" style="max-width:120px;max-height:80px;display:block;margin-top:4px" />';
      } else {
        div.innerHTML =
          '<span class="meta">' + escapeHtml(line.who) + "</span> " + escapeHtml(line.text);
      }
      log.appendChild(div);
    });
    log.scrollTop = log.scrollHeight;
    renderToolbar(buf);
  }

  function renderToolbar(buf) {
    let bar = document.querySelector(".smirc-toolbar");
    if (!bar) {
      bar = document.createElement("div");
      bar.className = "smirc-toolbar";
      el("chat-form").before(bar);
    }
    bar.innerHTML = "";
    if (buf.kind !== "dm") {
      bar.style.display = "none";
      return;
    }
    bar.style.display = "flex";
    const seal = document.createElement("button");
    seal.type = "button";
    seal.textContent = "SEAL";
    seal.title = "Live wire UNKNOWN — use irc_seal.py + agentic-compose";
    seal.addEventListener("click", () => appendSystem(buf.id, "SEAL: stub (UNKNOWN live wire)."));
    const file = document.createElement("button");
    file.type = "button";
    file.textContent = "File";
    file.title = "Live wire UNKNOWN — use irc_filexfer.py offer";
    file.addEventListener("click", () =>
      appendSystem(buf.id, "File offer: stub (UNKNOWN live wire).")
    );
    const gate = document.createElement("span");
    gate.className = "gate";
    gate.textContent = "DM tools → agentic_irc (env creds)";
    bar.append(seal, file, gate);
  }

  function appendSystem(id, text) {
    const buf = state.buffers[id];
    if (!buf) return;
    buf.lines.push({ who: "system", text: text });
    if (state.activeId === id) renderLog();
  }

  function renderUsers() {
    const ul = el("user-list");
    ul.innerHTML = "";
    const buf = state.buffers[state.activeId];
    const ch = buf && buf.kind === "chan" ? buf.name : "#demo";
    const users = state.channelUsers[ch] || [];
    const tpl = el("tpl-user-row");
    users.forEach((nick) => {
      const node = tpl.content.cloneNode(true);
      node.querySelector(".smirc-user-nick").textContent = nick;
      node.querySelector(".smirc-btn-dm").addEventListener("click", () => openDm(nick));
      ul.appendChild(node);
    });
  }

  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function focusBuffer(id) {
    if (!state.buffers[id]) return;
    state.activeId = id;
    renderChannels();
    renderTabs();
    renderLog();
    renderUsers();
  }

  function openDm(nick) {
    const id = bufferId("dm", nick);
    if (!state.buffers[id]) {
      state.buffers[id] = {
        id,
        kind: "dm",
        name: nick,
        lines: [{ who: "system", text: "DM demo (SEAL/File stubs on toolbar)." }],
      };
    }
    focusBuffer(id);
  }

  function sendMessage(text) {
    const buf = state.buffers[state.activeId];
    if (!buf || !text.trim()) return;
    buf.lines.push({ who: "you", text: text.trim() });
    renderLog();
  }

  function setupDrop() {
    const zone = el("image-drop");
    function accept(file) {
      if (!file || !file.type.startsWith("image/")) return;
      window.__smircLastDrop = { name: file.name, type: file.type, size: file.size };
      const url = URL.createObjectURL(file);
      const buf = state.buffers[state.activeId];
      buf.lines.push({ who: "you", text: file.name, imageUrl: url });
      renderLog();
    }
    zone.addEventListener("dragover", (e) => {
      e.preventDefault();
      zone.classList.add("dragover");
    });
    zone.addEventListener("dragleave", () => zone.classList.remove("dragover"));
    zone.addEventListener("drop", (e) => {
      e.preventDefault();
      zone.classList.remove("dragover");
      const file = e.dataTransfer.files && e.dataTransfer.files[0];
      accept(file);
    });
  }

  el("chat-form").addEventListener("submit", (e) => {
    e.preventDefault();
    const input = el("chat-input");
    sendMessage(input.value);
    input.value = "";
  });

  if (DEMO) seedDemo();
  setupDrop();
  renderChannels();
  renderTabs();
  renderLog();
  renderUsers();
})();
