async function fetchEmails() {
  const list = document.getElementById("emailList");

  // Show skeleton loaders
  list.innerHTML = `
    <div class="skeleton-card"><div class="sk sk-line sk-w80"></div><div class="sk sk-line sk-w50 sk-mt"></div><div class="sk sk-block"></div></div>
    <div class="skeleton-card"><div class="sk sk-line sk-w60"></div><div class="sk sk-line sk-w40 sk-mt"></div><div class="sk sk-block"></div></div>
    <div class="skeleton-card"><div class="sk sk-line sk-w70"></div><div class="sk sk-line sk-w55 sk-mt"></div><div class="sk sk-block"></div></div>
  `;

  // Reset stats to loading state
  ["emailCount", "highCount", "actionCount"].forEach(id => {
    document.getElementById(id).textContent = "—";
  });

  try {
    const res = await fetch("/emails/");
    if (!res.ok) throw new Error("Request failed");
    const data = await res.json();
    renderStats(data);
    renderList(data);
  } catch (err) {
    list.innerHTML = `
      <div class="empty">
        <div class="empty-icon">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
            <circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>
          </svg>
        </div>
        Could not load emails.<br>Check your connection and try again.
      </div>`;
  }
}

function renderStats(emails) {
  const emailCount  = emails.length;
  const highCount   = emails.filter(e => e.urgency === "high").length;
  const actionCount = emails.filter(e => e.action && e.action !== "none").length;

  animateNumber("emailCount",  emailCount);
  animateNumber("highCount",   highCount);
  animateNumber("actionCount", actionCount);
}

function animateNumber(id, target) {
  const el = document.getElementById(id);
  const duration = 600;
  const start = performance.now();
  function step(now) {
    const t = Math.min((now - start) / duration, 1);
    el.textContent = Math.round(easeOut(t) * target);
    if (t < 1) requestAnimationFrame(step);
  }
  requestAnimationFrame(step);
}

function easeOut(t) { return 1 - Math.pow(1 - t, 3); }

function getInitials(email) {
  const name = (email || "").split("@")[0].replace(/[._-]/g, " ");
  const words = name.trim().split(/\s+/);
  return words.slice(0, 2).map(w => w[0] || "").join("").toUpperCase() || "?";
}

function renderList(emails) {
  const list = document.getElementById("emailList");

  if (!emails.length) {
    list.innerHTML = `
      <div class="empty">
        <div class="empty-icon">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
            <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/>
          </svg>
        </div>
        No work emails found.
      </div>`;
    return;
  }

  list.innerHTML = emails.map((email, i) => {
    const urgency  = email.urgency || "low";
    const from     = email.from_email || "";
    const initials = getInitials(from);

    const tasksHtml = (email.tasks && email.tasks.length)
      ? email.tasks.map(t => `
          <div class="task">
            <div class="task-dot"></div>
            <span>${escapeHtml(t.task_text)}</span>
          </div>`).join("")
      : `<div class="task"><div class="task-dot" style="opacity:.3"></div><span style="color:var(--muted)">No tasks extracted.</span></div>`;

    return `
      <article class="card" style="animation-delay:${Math.min(i * 0.07, 0.35)}s">
        <div class="card-header">
          <div class="card-meta">
            <div class="subject">${escapeHtml(email.subject || "(No subject)")}</div>
            <div class="from">
              <div class="from-avatar">${escapeHtml(initials)}</div>
              <div class="from-email">${escapeHtml(from)}</div>
            </div>
          </div>
          <div class="pill ${urgency}">${escapeHtml(urgency)}</div>
        </div>
        ${email.summary ? `<div class="summary">${escapeHtml(email.summary)}</div>` : ""}
        <div>
          <div class="tasks-label">Extracted tasks</div>
          <div class="tasks">${tasksHtml}</div>
        </div>
      </article>`;
  }).join("");
}

function escapeHtml(text) {
  return String(text)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

document.getElementById("refreshBtn").addEventListener("click", fetchEmails);
fetchEmails();