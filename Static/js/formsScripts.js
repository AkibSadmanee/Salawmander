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