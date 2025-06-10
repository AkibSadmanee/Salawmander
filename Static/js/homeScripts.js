function toggleTheme() {
  document.body.classList.toggle('light-mode');
  const icon = document.getElementById('theme-icon');
  if (document.body.classList.contains('light-mode')) {
    icon.src = 'static/images/darkmode.png';
    icon.alt = 'Switch to Dark Mode';
    localStorage.setItem('theme', 'light');
  } else {
    icon.src = 'static/images/lightmode.png';
    icon.alt = 'Switch to Light Mode';
    localStorage.setItem('theme', 'dark');
  }
}

document.addEventListener("DOMContentLoaded", function() {
    const chatForm = document.querySelector(".chat-input");
    const userInput = document.getElementById("user-input");
    const sendBtn = document.getElementById("send-btn");
    const btnText = sendBtn.querySelector(".btn-text");
    const btnLoader = sendBtn.querySelector(".loader");

    chatForm.addEventListener("submit", async function(e) {
        e.preventDefault();
        const message = userInput.value.trim();
        if (!message) return;

        // --- Show loader, hide text, disable button ---
        btnText.style.display = "none";
        btnLoader.style.display = "inline-block";
        sendBtn.disabled = true;

        try {
            const response = await fetch("/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ query: message })
            });

            if (response.ok) {
                const data = await response.json();
                if (data.forms) {
                    showConfirmationCard(data.forms, data.query); // new function below
                }
            } else {
                alert("Error processing your request.");
            }
        } finally {
            // --- Restore button after request ---
            btnText.style.display = "";
            btnLoader.style.display = "none";
            sendBtn.disabled = false;
            userInput.value = "";
        }
    }); 

  function showConfirmationCard(forms, userQuery) {
    const card = document.getElementById("confirm-card");
    const cardContent = card.querySelector('.card');
    const h3 = cardContent.querySelector('h3');
    const btnContainer = card.querySelector('.card-btns');
    const ul = document.getElementById("forms-list");

    // Remove previous elements
    cardContent.querySelectorAll('.no-match, .ok-btn, .match-section, .confirm-question').forEach(el => el.remove());
    ul.innerHTML = "";

    // Only forms with a non-empty form_name
    const validForms = forms.filter(form => form.form_name && form.form_name.trim() !== "");

    if (validForms.length === 0) {
        ul.style.display = "none";
        if (btnContainer) btnContainer.style.display = "none";

        // No match message
        const noMatch = document.createElement('div');
        noMatch.className = 'no-match';
        noMatch.textContent = "No matching forms were found for your query.";
        cardContent.insertBefore(noMatch, btnContainer);

        // Okay button
        const okBtn = document.createElement('button');
        okBtn.className = 'ok-btn';
        okBtn.textContent = 'Okay';
        okBtn.onclick = function() {
            card.style.display = "none";
        };
        cardContent.appendChild(okBtn);

    } else {
        ul.style.display = "";
        if (btnContainer) btnContainer.style.display = ""; // Show Proceed/Cancel

        // --- Match section (header + list) ---
        const matchSection = document.createElement('div');
        matchSection.className = 'match-section';

        const header = document.createElement('p');
        header.className = 'match-header';
        header.textContent = "We found the following relevant forms:";
        matchSection.appendChild(header);

        validForms.forEach(form => {
            const li = document.createElement("li");
            li.textContent = form.form_name;
            ul.appendChild(li);
        });
        matchSection.appendChild(ul);

        cardContent.insertBefore(matchSection, btnContainer);

        // --- Confirm question (below list, above buttons) ---
        const confirmQ = document.createElement('p');
        confirmQ.className = 'confirm-question';
        confirmQ.textContent = "Are you sure you want to proceed with these forms?";
        cardContent.insertBefore(confirmQ, btnContainer);

        // Button handlers
        document.getElementById("proceed-btn").onclick = function() {
          // Only include the valid forms
          const validForms = forms.filter(form => form.form_name && form.form_name.trim() !== "");
          const formsParam = encodeURIComponent(JSON.stringify(validForms));
          window.location.href = `/form?forms=${formsParam}`;
        };
        document.getElementById("cancel-btn").onclick = function() {
            card.style.display = "none";
        };
    }
    card.style.display = "flex"; // Show the modal
}




});


const aboutCard = document.getElementById('about-card');
const aboutCardInner = aboutCard.querySelector('.card');
const aboutCloseBtn = document.getElementById('about-close-btn');

// Show the modal
document.querySelector('.question').addEventListener('click', function() {
  aboutCard.style.display = 'flex';
});

// Click outside to close
aboutCard.addEventListener('mousedown', function(e) {
  if (!aboutCardInner.contains(e.target)) {
    aboutCard.style.display = 'none';
  }
});

// Close button
aboutCloseBtn.addEventListener('click', function() {
  aboutCard.style.display = 'none';
});

// Esc key closes modal
document.addEventListener('keydown', function(e) {
  if (aboutCard.style.display === 'flex' && (e.key === 'Escape' || e.key === 'Esc')) {
    aboutCard.style.display = 'none';
  }
});


