function toggleTheme() {
  document.body.classList.toggle('light-mode');
  const icon = document.getElementById('theme-icon');
  if (document.body.classList.contains('light-mode')) {
    icon.src = 'static/images/lightmode.png';
    icon.alt = 'Switch to Dark Mode';
    localStorage.setItem('theme', 'light');
  } else {
    icon.src = 'static/images/darkmode.png';
    icon.alt = 'Switch to Light Mode';
    localStorage.setItem('theme', 'dark');
  }
}

document.addEventListener("DOMContentLoaded", function() {
  const savedTheme = localStorage.getItem('theme');
  if (savedTheme === 'light') {
    document.body.classList.add('light-mode');
    const icon = document.getElementById('theme-icon');
    icon.src = 'static/images/lightmode.png';
    icon.alt = 'Switch to Dark Mode';
  }

  const chatForm = document.querySelector(".chat-input");
  const userInput = document.getElementById("user-input");
  const sendBtn = chatForm.querySelector("button");
  const sendText = sendBtn.textContent; // Keep "Send" to restore later

  chatForm.addEventListener("submit", async function(e) {
    e.preventDefault();
    const message = userInput.value.trim();
    if (!message) return;

    // Disable button and show loader
    sendBtn.disabled = true;
    sendBtn.innerHTML = `<span class="loader"></span>`;

    try {
      const response = await fetch("/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: message })
      });

      if (response.ok) {
        const data = await response.json();
        if (data.redirect) {
          window.location.href = data.redirect;
        }
        // Optionally, handle response data here
      } else {
        alert("Error processing your request.");
      }
    } catch (err) {
      alert("Network error.");
    }

    // Restore button and clear input
    sendBtn.disabled = false;
    sendBtn.textContent = sendText;
    userInput.value = "";
  });
});
