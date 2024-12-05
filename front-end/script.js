// JavaScript code extracted from the HTML file

document.addEventListener("DOMContentLoaded", () => {
  setSize("medium");
  const themeToggle = document.getElementById("theme-toggle");

  const savedTheme = localStorage.getItem("theme");
  if (savedTheme) {
    document.body.classList.add(savedTheme);
    if (savedTheme === "dark-mode") {
      themeToggle.checked = true;
    }
  }

  updateSummary();

  themeToggle.addEventListener("change", () => {
    if (themeToggle.checked) {
      document.body.classList.add("dark-mode");
      localStorage.setItem("theme", "dark-mode");
    } else {
      document.body.classList.remove("dark-mode");
      localStorage.setItem("theme", "");
    }
    updateSummary();
  });
});

function showContent(sectionId) {
  const sections = document.querySelectorAll(".content-section");
  sections.forEach((section) => (section.style.display = "none"));
  document.getElementById(sectionId).style.display = "block";
}

function setSize(size) {
  document.body.classList.remove(
    "theme-small",
    "theme-medium",
    "theme-large",
    "theme-massive"
  );
  switch (size) {
    case "small":
      document.body.style.fontSize = "14px";
      break;
    case "medium":
      document.body.style.fontSize = "16px";
      break;
    case "large":
      document.body.style.fontSize = "18px";
      break;
    case "massive":
      document.body.style.fontSize = "20px";
      break;
  }
  if (size === "small") {
    document.body.classList.add("theme-small");
  } else if (size === "medium") {
    document.body.classList.add("theme-medium");
  } else if (size === "large") {
    document.body.classList.add("theme-large");
  } else if (size === "massive") {
    document.body.classList.add("theme-massive");
  }
}

function updateSummary() {
  const darkModeStatus = document.body.classList.contains("dark-mode")
    ? "On"
    : "Off";
  const sizeStatus = document.querySelector('input[name="value-radio"]:checked')
    ? document.querySelector('input[name="value-radio"]:checked').value
    : "Medium";
  const colorStatus = document.querySelector(
    'input[name="color-radio"]:checked'
  )
    ? document.querySelector('input[name="color-radio"]:checked').value
    : "Yellow";

  document.getElementById(
    "dark-mode-status"
  ).innerText = `Dark Mode: ${darkModeStatus}`;
  document.getElementById("size-status").innerText = `Size: ${sizeStatus}`;
  document.getElementById("color-status").innerText = `Color: ${colorStatus}`;
}

function setColorTheme(color) {
  document.body.classList.remove("theme-yellow", "theme-blue", "theme-red");

  switch (color) {
    case "yellow":
      document.documentElement.style.setProperty(
        "--text-hover-color",
        "#FAC921"
      );
      document.documentElement.style.setProperty(
        "--card-background-color",
        "#FAC921"
      );
      document.documentElement.style.setProperty("--input-focus", "#2d8cf0");
      break;
    case "blue":
      document.documentElement.style.setProperty(
        "--text-hover-color",
        "#2d8cf0"
      );
      document.documentElement.style.setProperty(
        "--card-background-color",
        "#2d8cf0"
      );
      document.documentElement.style.setProperty("--input-focus", "#FAC921");
      break;
    case "orange":
      document.documentElement.style.setProperty(
        "--text-hover-color",
        "#FF8C00"
      );
      document.documentElement.style.setProperty(
        "--card-background-color",
        "#FF8C00"
      );
      document.documentElement.style.setProperty("--input-focus", "#2d8cf0");
      break;
  }
  document.body.classList.add(`theme-${color}`);
  updateSummary();
}

function toggleMobileNav() {
  const mobileNav = document.getElementById("mobileNav");
  if (mobileNav.style.display === "none" || mobileNav.style.display === "") {
    mobileNav.style.display = "flex";
  } else {
    mobileNav.style.display = "none";
  }
}

async function submitJobDescription() {
  const jobDescription = document.getElementById("jobDescription").value;

  const response = await fetch(
    "https://matching-ai.gingerbreadmat.com/process",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ job_description: jobDescription }),
    }
  );

  const result = await response.json();
  document.getElementById("result").innerText = JSON.stringify(result, null, 2);
}
