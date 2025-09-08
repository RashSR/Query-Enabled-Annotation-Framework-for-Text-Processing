// Handles annotation box editing and saving
window.addEventListener('DOMContentLoaded', function() {
  const annotationBox = document.getElementById('annotation-box');
  if (annotationBox) {
    let lastValue = annotationBox.value;
    annotationBox.addEventListener('click', function() {
      if (annotationBox.hasAttribute('readonly')) {
        annotationBox.removeAttribute('readonly');
        annotationBox.focus();
      }
    });
    annotationBox.addEventListener('keydown', function(e) {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        annotationBox.blur();
      }
    });
    annotationBox.addEventListener('blur', function() {
      annotationBox.setAttribute('readonly', 'readonly');
      if (annotationBox.value !== lastValue) {
        fetch(window.location.pathname + '/annotation', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ annotation: annotationBox.value })
        }).then(r => {
          if (!r.ok) alert('Fehler beim Speichern!');
          else lastValue = annotationBox.value;
        });
      }
    });
  }

  // Handles add chat button
  const addChatBtn = document.getElementById('add-chat-btn');
  const chatFileInput = document.getElementById('chat-file-input');
  if (addChatBtn && chatFileInput) {
    addChatBtn.addEventListener('click', function() {
      chatFileInput.value = '';
      chatFileInput.click();
    });

    chatFileInput.addEventListener('change', function() {
      const file = chatFileInput.files[0];
      if (!file) return;
      if (file.type !== 'text/plain' && !file.name.endsWith('.txt')) {
        alert('Bitte wählen Sie eine .txt Datei aus!');
        return;
      }
      const authorId = addChatBtn.getAttribute('data-author-id') || window.location.pathname.split('/').pop();
      const formData = new FormData();
      formData.append('chat_file', file);
      fetch(`/profile/${authorId}/add_chat`, {
        method: 'POST',
        body: formData
      })
      .then(r => r.json())
      .then(data => {
        if (!data.success) {
          alert('Fehler beim Hinzufügen des Chats!');
          return;
        }
        // Show modal for author mapping
        if (data.extracted_authors && data.existing_authors) {
          showAuthorMappingModal(data.extracted_authors, data.existing_authors, function(selectedIds, relationship) {
            // Send mapping to backend (implement this route as needed)
            fetch(`/profile/${authorId}/map_chat_authors`, {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ mapping: selectedIds, extracted_authors: data.extracted_authors, relationship: relationship })
            })
            .then(r => r.json())
            .then(resp => {
              if (resp.task_id) {
                showProgressBar(resp.task_id);
              }
              if (!resp.success) {
                alert('Fehler beim Zuordnen der Autoren!');
              }
            });
          });
        }
      })
      .catch(() => {
        alert('Fehler beim Hinzufügen des Chats!');
      });
    });
  }

  // Modal for author mapping
  function showAuthorMappingModal(extractedAuthors, existingAuthors, onConfirm) {
    // Remove any existing modal
    document.getElementById('author-mapping-modal')?.remove();

    const modal = document.createElement('div');
    modal.id = 'author-mapping-modal';
    modal.style.position = 'fixed';
    modal.style.top = '0';
    modal.style.left = '0';
    modal.style.width = '100vw';
    modal.style.height = '100vh';
    modal.style.background = 'rgba(0,0,0,0.5)';
    modal.style.display = 'flex';
    modal.style.alignItems = 'center';
    modal.style.justifyContent = 'center';
    modal.style.zIndex = '9999';

    const card = document.createElement('div');
    card.style.background = '#fff';
    card.style.padding = '2rem';
    card.style.borderRadius = '8px';
    card.style.boxShadow = '0 2px 8px rgba(0,0,0,0.2)';
    card.style.minWidth = '320px';

    const title = document.createElement('h3');
    title.textContent = 'Teilnehmer zuordnen';
    card.appendChild(title);

    extractedAuthors.forEach((extracted, idx) => {
      const label = document.createElement('label');
      label.textContent = `Datei-Teilnehmer: ${extracted}`;
      label.style.display = 'block';
      label.style.marginTop = '1rem';
      card.appendChild(label);

      const select = document.createElement('select');
      select.name = `author_map_${idx}`;
      select.style.width = '100%';
      select.style.marginTop = '0.5rem';
      existingAuthors.forEach(author => {
        const option = document.createElement('option');
        option.value = author.id;
        option.textContent = author.name;
        select.appendChild(option);
      });
      card.appendChild(select);
    });

    // Add a single relationship textbox for all authors
    const relLabel = document.createElement('label');
    relLabel.textContent = 'Beziehung zwischen den Autoren:';
    relLabel.style.display = 'block';
    relLabel.style.marginTop = '1.5rem';
    card.appendChild(relLabel);

    const relInput = document.createElement('input');
    relInput.type = 'text';
    relInput.name = 'relationship';
    relInput.style.width = '100%';
    relInput.style.marginTop = '0.2rem';
    card.appendChild(relInput);

    const btnRow = document.createElement('div');
    btnRow.style.display = 'flex';
    btnRow.style.justifyContent = 'flex-end';
    btnRow.style.marginTop = '2rem';

    const confirmBtn = document.createElement('button');
    confirmBtn.textContent = 'Bestätigen';
    confirmBtn.style.padding = '0.5rem 1.5rem';
    confirmBtn.style.background = '#0074D9';
    confirmBtn.style.color = '#fff';
    confirmBtn.style.border = 'none';
    confirmBtn.style.borderRadius = '4px';
    confirmBtn.style.cursor = 'pointer';
    confirmBtn.onclick = function() {
      // Collect selected author IDs and relationship
      const selected = Array.from(card.querySelectorAll('select')).map(sel => sel.value);
      const relationship = relInput.value;
      document.body.removeChild(modal);
      onConfirm(selected, relationship);
    };
    btnRow.appendChild(confirmBtn);

    const cancelBtn = document.createElement('button');
    cancelBtn.textContent = 'Abbrechen';
    cancelBtn.style.marginLeft = '1rem';
    cancelBtn.style.padding = '0.5rem 1.5rem';
    cancelBtn.style.background = '#ccc';
    cancelBtn.style.color = '#333';
    cancelBtn.style.border = 'none';
    cancelBtn.style.borderRadius = '4px';
    cancelBtn.style.cursor = 'pointer';
    cancelBtn.onclick = function() {
      document.body.removeChild(modal);
    };
    btnRow.appendChild(cancelBtn);

    card.appendChild(btnRow);
    modal.appendChild(card);
    document.body.appendChild(modal);
  }

  // Progress bar logic
  function showProgressBar(taskId) {
    const modal = document.getElementById('analysis-progress-modal');
    const bar = document.getElementById('progress-bar');
    const text = document.getElementById('progress-text');
    modal.style.display = 'flex';

    function poll() {
      fetch('/progress/' + taskId)
        .then(res => res.json())
        .then(data => {
          let percent = Math.round((data.step / data.total) * 100);
          bar.style.width = percent + '%';
          text.textContent = `${percent}% – ${data.message || ''}`;
          // ETA formatting
          const etaElem = document.getElementById('progress-eta');
          if (typeof data.eta !== 'undefined' && !data.done) {
            let eta = Math.round(data.eta);
            let etaStr = '';
            if (eta > 59) {
              let min = Math.floor(eta / 60);
              let sec = eta % 60;
              etaStr = `${min}m${sec}s`;
            } else {
              etaStr = `${eta}s`;
            }
            etaElem.textContent = `Verbleibende Zeit: ${etaStr}`;
          } else {
            etaElem.textContent = '';
          }
          if (!data.done) {
            setTimeout(poll, 1000);
          } else {
            text.textContent = data.message || 'Analyse abgeschlossen!';
            etaElem.textContent = '';
            setTimeout(() => {
              modal.style.display = 'none';
              window.location.reload();
            }, 1500);
          }
        });
    }
    poll();
  }

  // Example usage after file upload and backend response:
  // showAuthorMappingModal(['Alice', 'Bob'], [{id:1,name:'Anna'},{id:2,name:'Bernd'}], function(selectedIds) {
  //   // selectedIds is an array of author IDs chosen by the user
  //   // Send to backend for mapping
  // });
});
