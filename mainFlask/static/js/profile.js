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
      }).then(r => {
        if (r.ok) {
          location.reload();
        } else {
          alert('Fehler beim Hinzufügen des Chats!');
        }
      });
    });
  }
});
