function getFormsFromQuery() {
  const params = new URLSearchParams(window.location.search);
  const formsJson = params.get('forms');
  if (!formsJson) return [];
  try {
    return JSON.parse(decodeURIComponent(formsJson));
  } catch (e) {
    return [];
  }
}

// Render forms in the sidebar, replacing dummy ones
function renderFormsSidebar(forms) {
  const formsListDiv = document.getElementById('forms-list');
  formsListDiv.innerHTML = ''; // Clear anything

  if (!forms.length) {
    formsListDiv.innerHTML = "<div style='color:#aaa;'>No forms found.</div>";
    return;
  }

  forms.forEach(form => {
    // Default to 100% if progress isn't present
    const progress = typeof form.progress === "number" ? form.progress : 0;
    formsListDiv.innerHTML += `
      <div class="form-item">
        <span>${form.form_name}</span>
        <div class="progress-container">
          <div class="progress-bar" style="width: ${progress}%;">${progress}%</div>
        </div>
      </div>
    `;
  });
}

document.addEventListener("DOMContentLoaded", function() {
  // Theme toggle logic
  const toggleBtn = document.querySelector('.theme-toggle');
  const themeIcon = toggleBtn.querySelector('img');
  const isLight = document.body.classList.contains('light-mode');
  themeIcon.src = isLight ? 'static/images/darkmode.png' : 'static/images/lightmode.png';
  themeIcon.alt = isLight ? 'Switch to Dark Mode' : 'Switch to Light Mode';

  toggleBtn.addEventListener('click', function() {
    document.body.classList.toggle('light-mode');
    const isNowLight = document.body.classList.contains('light-mode');
    themeIcon.src = isNowLight ? 'static/images/darkmode.png' : 'static/images/lightmode.png';
    themeIcon.alt = isNowLight ? 'Switch to Dark Mode' : 'Switch to Light Mode';
    localStorage.setItem('theme', isNowLight ? 'light' : 'dark');
  });

  // Handle sidebar forms
  const forms = getFormsFromQuery();
  renderFormsSidebar(forms);
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


document.addEventListener("DOMContentLoaded", function() {
      // THEME TOGGLE
      const themeBtn = document.querySelector('.theme-toggle');
      const themeIcon = themeBtn.querySelector('img');
      const savedTheme = localStorage.getItem('theme');
      if (savedTheme === 'light') document.body.classList.add('light-mode');
      updateThemeIcon();

      themeBtn.addEventListener('click', () => {
        document.body.classList.toggle('light-mode');
        const isLight = document.body.classList.contains('light-mode');
        localStorage.setItem('theme', isLight ? 'light' : 'dark');
        updateThemeIcon();
      });

      function updateThemeIcon() {
        const isLight = document.body.classList.contains('light-mode');
        themeIcon.src = isLight ? 'static/images/darkmode.png' : 'static/images/lightmode.png';
        themeIcon.alt = isLight ? 'Switch to Dark Mode' : 'Switch to Light Mode';
      }

      // ABOUT CARD as HELP MODAL
      const helpBtn = document.querySelector('.question');
      const aboutCard = document.getElementById('about-card');
      const aboutCloseBtn = document.getElementById('about-close-btn');

      helpBtn.addEventListener('click', () => {
        aboutCard.style.display = 'flex';
        aboutCard.style.justifyContent = 'center';
        aboutCard.style.alignItems = 'center';
        aboutCard.style.position = 'fixed';
        aboutCard.style.left = 0;
        aboutCard.style.top = 0;
        aboutCard.style.width = '100vw';
        aboutCard.style.height = '100vh';
        aboutCard.style.backgroundColor = 'rgba(0,0,0,0.7)';
        aboutCard.style.zIndex = 1000;
      });

      aboutCloseBtn.addEventListener('click', () => aboutCard.style.display = 'none');
      window.addEventListener('click', (event) => {
        if (event.target === aboutCard) aboutCard.style.display = 'none';
      });

      // CHAT FUNCTIONALITY
      const chatThread = document.getElementById('chat-thread');
      const input = document.querySelector('.chat-input input');
      const sendBtn = document.querySelector('.chat-input button');

      function getTimestamp() {
        return new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
      }

      function appendUserMessage(msg) {
        const timestamp = getTimestamp();
        const div = document.createElement('div');
        div.className = 'message user';
        div.innerHTML = `<div class="bubble user-bubble">${msg}</div><div class="timestamp">${timestamp}</div>`;
        chatThread.appendChild(div);
        chatThread.scrollTop = chatThread.scrollHeight;
      }

      function appendBotMessageAnimated(msg) {
        const timestamp = getTimestamp();
        const div = document.createElement('div');
        div.className = 'message bot';
        div.innerHTML = `
          <img src="static/images/salawmanderlogo.png" alt="Bot" class="avatar" />
          <div>
            <div class="bubble bot-bubble">${msg}</div>
            <div class="timestamp">${timestamp}</div>
          </div>
        `;
        chatThread.appendChild(div);
        chatThread.scrollTop = chatThread.scrollHeight;
      }

      function renderFormsSidebar(forms) {
        const formsListDiv = document.getElementById('forms-list');
        formsListDiv.innerHTML = '';

        if (!forms.length) {
          formsListDiv.innerHTML = "<div style='color:#aaa;'>No forms found.</div>";
          return;
        }

        forms.forEach(form => {
          const progress = typeof form.progress === "number" ? form.progress : 0;
          formsListDiv.innerHTML += `
            <div class="form-item">
              <span>${form.form_name}</span>
              <div class="progress-container">
                <div class="progress-bar" style="width: ${progress}%;">${progress}%</div>
              </div>
            </div>
          `;
        });
      }

      function handleSend() {
        const message = input.value.trim();
        if (!message) return;
        appendUserMessage(message);
        input.value = '';
        sendBtn.disabled = true;

        fetch('/form-fill', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ query: message })
        })
        .then(res => res.json())
        .then(data => {
          appendBotMessageAnimated(data.message || "Sorry, I didn't understand that.");
          if (Array.isArray(data.forms)) {
            renderFormsSidebar(data.forms);
          }
        })
        .catch(() => {
          appendBotMessageAnimated("Sorry, something went wrong.");
        })
        .finally(() => {
          sendBtn.disabled = false;
        });
      }

      sendBtn.addEventListener('click', handleSend);
      input.addEventListener('keydown', e => { if (e.key === 'Enter') handleSend(); });

      // INITIAL LOAD
      window.addEventListener('load', () => {
        // Load chat history
        if (Array.isArray(window.chatHistory)) {
          for (const msg of window.chatHistory) {
            if (msg.role === 'user') appendUserMessage(msg.content);
            else if (msg.role === 'salawmander') appendBotMessageAnimated(msg.content);
          }
        }

        // Load form sidebar with progress
        if (Array.isArray(window.formsData)) {
          renderFormsSidebar(window.formsData);
        }
      });
    });


