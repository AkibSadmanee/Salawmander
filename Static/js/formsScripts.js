function getTimestamp() {
  return new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
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
  const chatThread = document.getElementById('chat-thread');
  if (chatThread) {
    chatThread.appendChild(div);
    chatThread.scrollTop = chatThread.scrollHeight;
  }
}

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

function renderFormsSidebar(forms) {
  const formsListDiv = document.getElementById('forms-list');
  formsListDiv.innerHTML = ''; // Clear anything

  if (!forms.length) {
    formsListDiv.innerHTML = "<div style='color:#aaa;'>No forms found.</div>";
    return;
  }

  forms.forEach((form, index) => {
    const progress = typeof form.progress === "number" ? form.progress : 0;

    const formItem = document.createElement('div');
    formItem.classList.add('form-item');
    formItem.innerHTML = `
      <span>${form.form_name}</span>
      <div class="progress-container">
        <div class="progress-bar" style="width: ${progress}%;">${progress}%</div>
      </div>
    `;

    formItem.addEventListener('click', () => {
      showFormPopup(form);
    });

    formsListDiv.appendChild(formItem);
  });
}

async function showFormPopup(form) {
  const formModal = document.getElementById('form-modal');
  const formContent = document.getElementById('form-content');

  try {
    const response = await fetch('/get_html', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ form_name: form.form_name })
    });

    if (!response.ok) throw new Error('Failed to fetch form HTML');

    const html = await response.text();
    formContent.innerHTML = `
      <span class="close-button" id="form-close">&times;</span>
      ${html}
    `;

    // Close modal handler
    document.getElementById('form-close').addEventListener('click', () => {
      formModal.style.display = 'none';
    });

    const saveBtn = document.getElementById('save-form-btn');
    const formEl = document.querySelector('#form-content form');

    if (formEl && saveBtn) {
      const inputs = formEl.querySelectorAll('input');

      // Enable the Save button when any input changes
      inputs.forEach(input => {
        input.addEventListener('input', () => {
          saveBtn.disabled = false;
        });
      });

      saveBtn.addEventListener('click', async () => {
        const formData = new FormData(formEl);
        const formTitle = document.querySelector('#form-content h2')?.textContent?.trim();
        if (formTitle) {
          formData.append('form_name', formTitle);
        }

        const btnText = saveBtn.querySelector('.btn-text');
        const btnLoader = saveBtn.querySelector('.loader');
        if (btnText && btnLoader) {
          btnText.style.display = 'none';
          btnLoader.style.display = 'inline-block';
        }
        saveBtn.disabled = true;

        try {
          const response = await fetch('/save_html', {
            method: 'POST',
            body: formData
          });

          if (!response.ok) throw new Error('Failed to save form');

          const result = await response.json();
          appendBotMessageAnimated(result.message || "Form saved successfully!");
          formModal.style.display = 'none';
          window.location.href = '/form';

        } catch (err) {
          console.error("Error saving form:", err);
          alert("Failed to save the form.");
        } finally {
          // Hide spinner and restore button state
          if (btnText && btnLoader) {
            btnText.style.display = '';
            btnLoader.style.display = 'none';
          }
          saveBtn.disabled = true; // Disable again after save
        }
      });
    }

    // Show modal
    formModal.style.display = 'flex';

  } catch (error) {
    console.error("Error loading form:", error);
    alert("Failed to load the form. Please try again.");
  }
}


document.addEventListener("DOMContentLoaded", function () {
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

  const helpBtn = document.querySelector('.question');
  const aboutCard = document.getElementById('about-card');
  const aboutCloseBtn = document.getElementById('about-close-btn');

  helpBtn.addEventListener('click', () => {
    aboutCard.style.display = 'flex';
    Object.assign(aboutCard.style, {
      justifyContent: 'center',
      alignItems: 'center',
      position: 'fixed',
      left: 0,
      top: 0,
      width: '100vw',
      height: '100vh',
      backgroundColor: 'rgba(0,0,0,0.7)',
      zIndex: 1000
    });
  });

  aboutCloseBtn.addEventListener('click', () => aboutCard.style.display = 'none');
  window.addEventListener('click', (e) => {
    if (e.target === aboutCard) aboutCard.style.display = 'none';
  });
  document.addEventListener('keydown', (e) => {
    if (aboutCard.style.display === 'flex' && (e.key === 'Escape' || e.key === 'Esc')) {
      aboutCard.style.display = 'none';
    }
  });

  const chatThread = document.getElementById('chat-thread');
  const input = document.querySelector('.chat-input input');
  const sendBtn = document.querySelector('.chat-input button');

  function appendUserMessage(msg) {
    const timestamp = getTimestamp();
    const div = document.createElement('div');
    div.className = 'message user';
    div.innerHTML = `<div class="bubble user-bubble">${msg}</div><div class="timestamp">${timestamp}</div>`;
    chatThread.appendChild(div);
    chatThread.scrollTop = chatThread.scrollHeight;
  }

  function handleSend() {
  const message = input.value.trim();
  if (!message) return;

  appendUserMessage(message);
  input.value = '';

  const btnText = sendBtn.querySelector('.btn-text');
  const btnLoader = sendBtn.querySelector('.loader');
  if (btnText && btnLoader) {
    btnText.style.display = 'none';
    btnLoader.style.display = 'inline-block';
  }
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
      if (btnText && btnLoader) {
        btnText.style.display = '';
        btnLoader.style.display = 'none';
      }
      sendBtn.disabled = false;
    });
}


  sendBtn.addEventListener('click', handleSend);
  input.addEventListener('keydown', e => { if (e.key === 'Enter') handleSend(); });

  window.addEventListener('load', () => {
    if (Array.isArray(window.chatHistory)) {
      for (const msg of window.chatHistory) {
        if (msg.role === 'user') appendUserMessage(msg.content);
        else if (msg.role === 'salawmander') appendBotMessageAnimated(msg.content);
      }
    }

    const formsFromQuery = getFormsFromQuery();
    if (Array.isArray(formsFromQuery) && formsFromQuery.length) {
      renderFormsSidebar(formsFromQuery);
    } else if (Array.isArray(window.formsData)) {
      renderFormsSidebar(window.formsData);
    }
  });
});


// async function fetchDataAndGeneratePDF() {
//   try {
//     const response = await fetch('/get_data');
//     if (!response.ok) {
//       throw new Error('Network response was not ok');
//     }
//     const jsonData = await response.json();
//     generatePDF(jsonData);
//   } catch (error) {
//     console.error('Error fetching data:', error);
//   }
// }

// function generatePDF(dataList) {
//   const { jsPDF } = window.jspdf;
//   const doc = new jsPDF();

//   let yPosition = 10;

//   dataList.forEach((item, idx) => {
//     doc.text(`Form #${idx + 1}: ${item.form_name}`, 10, yPosition);
//     yPosition += 10;

//     // Print all key-value pairs except form_name
//     Object.entries(item).forEach(([key, value]) => {
//       if (key !== 'form_name') {
//         doc.text(`    ${key}: ${value}`, 10, yPosition);
//         yPosition += 8;
//       }
//     });

//     yPosition += 10; // Space between forms

//     // If yPosition gets close to bottom, add new page
//     if (yPosition > 270) {
//       doc.addPage();
//       yPosition = 10;
//     }
//   });

//   doc.save('forms.pdf');
// }

// // Call the function
// fetchDataAndGeneratePDF();
