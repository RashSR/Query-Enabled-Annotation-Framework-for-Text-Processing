document.addEventListener('DOMContentLoaded', function() {
  var addBtn = document.querySelector('.add-author-btn');
  var modal = document.getElementById('add-author-modal');
  var cancelBtn = document.getElementById('cancel-add-author');
  addBtn.addEventListener('click', function() {
    modal.style.display = 'flex';
  });
  cancelBtn.addEventListener('click', function() {
    modal.style.display = 'none';
    document.getElementById('add-author-form').reset();
  });
  document.getElementById('add-author-form').onsubmit = function(e) {
    e.preventDefault();
    var name = document.getElementById('author-name').value;
    var age = document.getElementById('author-age').value;
    var gender = document.getElementById('author-gender').value;
    var first_language = document.getElementById('author-first-language').value;
    var languages = document.getElementById('author-languages').value;
    var region = document.getElementById('author-region').value;
    var job = document.getElementById('author-job').value;
    fetch('/add_author', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name: name,
        age: age,
        gender: gender,
        first_language: first_language,
        languages: languages,
        region: region,
        job: job
      })
    })
    .then(response => response.json())
    .then(data => {
      if (data.success && data.author_id) {
        modal.style.display = 'none';
        this.reset();
        window.location.href = '/profile/' + data.author_id;
      } else {
        alert('Fehler beim Speichern!');
      }
    })
    .catch(() => {
      alert('Fehler beim Speichern!');
    });
  };

  // Author delete logic
  document.querySelectorAll('.delete-author-btn').forEach(function(btn) {
    btn.addEventListener('click', function() {
      var authorId = btn.getAttribute('data-author-id');
      if (!authorId) return;
      if (!confirm('Autor wirklich löschen?')) return;
      fetch('/delete_author', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ author_id: authorId })
      })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          window.location.href = '/profile';
        } else {
          alert('Fehler beim Löschen!');
        }
      })
      .catch(() => {
        alert('Fehler beim Löschen!');
      });
    });
  });
});