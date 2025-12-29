function login() {
  const user = document.getElementById("userid").value;
  const pass = document.getElementById("password").value;

  fetch("https://mywebsite.onrender.com/login")
", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      username: user,
      password: pass
    })
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      document.getElementById("loginPage").classList.add("hidden");
      document.getElementById("mainPage").classList.remove("hidden");
      showSection("contact");
    } else {
      alert("Invalid username or password");
    }
  })
  .catch(() => {
    alert("Server error. Is backend running?");
  });
}
document.addEventListener("DOMContentLoaded", function () {

  function handleForm(formId, url, successMsg) {
    const form = document.getElementById(formId);
    if (!form) return;

    form.addEventListener("submit", function (e) {
      e.preventDefault();

      const data = Object.fromEntries(new FormData(this));

      fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
      })
      .then(res => res.json())
      .then(() => {
        alert(successMsg);
        this.reset();
      })
      .catch(() => alert("Server error"));
    });
  }

  handleForm("contactForm", "https://mywebsite.onrender.com/contact", "Contact form submitted!");
  handleForm("queryForm", "https://mywebsite.onrender.com/query", "Query submitted!");
  handleForm("feedbackForm", "https://mywebsite.onrender.com/feedback", "Feedback submitted!");

});

// LOGOUT
function logout() {
  document.getElementById("mainPage").classList.add("hidden");
  document.getElementById("loginPage").classList.remove("hidden");
  document.querySelectorAll("form").forEach(f => f.reset());
}

// SHOW SECTION
function showSection(sectionId) {
  const sections = document.querySelectorAll(".section");
  sections.forEach(sec => sec.classList.add("hidden"));
  document.getElementById(sectionId).classList.remove("hidden");
}

// FORM SUBMIT
function submitForm(event, type) {
  event.preventDefault();
  alert(type + " form submitted successfully!");
  event.target.reset();
  document.getElementById('success-message').hidden = false;
  setTimeout(() => {
    document.getElementById('success-message').hidden = true;
  }, 2000);
}

// HAMBURGER MENU TOGGLE
function toggleMenu() {
  document.getElementById("nav-links").classList.toggle("active");
}
function loadAdminData(type) {
  const title = document.getElementById("admin-title");
  const tableDiv = document.getElementById("admin-table");

  title.innerText = "Loading...";

  fetch(`https://mywebsite.onrender.com/view-${type}`)
    .then(res => res.json())
    .then(data => {
      title.innerText = type.toUpperCase() + " DATA";

      if (data.length === 0) {
        tableDiv.innerHTML = "<p>No records yet</p>";
        return;
      }

      let table = "<table><tr>";

      // headers
      Object.keys(data[0]).forEach(key => {
        table += `<th>${key}</th>`;
      });

      table += "</tr>";

      // rows
      data.forEach(row => {
        table += "<tr>";
        Object.values(row).forEach(val => {
          table += `<td>${val}</td>`;
        });
        table += "</tr>";
      });

      table += "</table>";
      tableDiv.innerHTML = table;
    });
}

