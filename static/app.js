document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("[data-password-toggle]").forEach(btn => {
    btn.addEventListener("click", () => {
      const input = btn.parentElement.querySelector("input");
      input.type = input.type === "password" ? "text" : "password";
      btn.textContent = input.type === "password" ? "◉" : "○";
    });
  });

  const input = document.getElementById("fileInput");
  const zone = document.getElementById("dropzone");
  const title = document.getElementById("fileTitle");
  const subtitle = document.getElementById("fileSubtitle");
  const form = document.getElementById("uploadForm");
  const button = document.getElementById("uploadButton");

  if (!input) return;
  const showFile = file => {
    if (!file) return;
    title.textContent = file.name;
    subtitle.textContent = `${(file.size / 1024 / 1024).toFixed(2)} MB selected`;
  };
  input.addEventListener("change", () => showFile(input.files[0]));
  ["dragenter","dragover"].forEach(type => zone.addEventListener(type, e => {
    e.preventDefault(); zone.classList.add("dragging");
  }));
  ["dragleave","drop"].forEach(type => zone.addEventListener(type, e => {
    e.preventDefault(); zone.classList.remove("dragging");
  }));
  zone.addEventListener("drop", e => {
    if (e.dataTransfer.files.length) { input.files = e.dataTransfer.files; showFile(input.files[0]); }
  });
  form.addEventListener("submit", () => {
    button.disabled = true;
    button.querySelector("span").textContent = "Uploading securely…";
  });
});