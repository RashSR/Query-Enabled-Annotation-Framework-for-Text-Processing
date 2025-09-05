document.addEventListener('DOMContentLoaded', function() {
    function setupCollapsible(headerId, listId, label) {
        var header = document.getElementById(headerId);
        var list = document.getElementById(listId);
        var arrowSpan = header ? header.querySelector('span') : null;
        var expanded = false;
        if (header && list && arrowSpan) {
            header.addEventListener('click', function(e) {
                // Only toggle if the click is NOT on the Hinzufügen button
                if (e.target.classList.contains('add-annotation-btn') || e.target.classList.contains('add-error-btn') || e.target.classList.contains('add-spacy-btn')) {
                    return;
                }
                expanded = !expanded;
                if (expanded) {
                    list.style.display = '';
                    arrowSpan.innerHTML = arrowSpan.innerHTML.replace('▶', '▼');
                } else {
                    list.style.display = 'none';
                    arrowSpan.innerHTML = arrowSpan.innerHTML.replace('▼', '▶');
                }
            });
        }
    }
    setupCollapsible('annotation-header', 'annotation-list', 'Manuelle Annotationen');
    setupCollapsible('error-header', 'error-list', 'Fehlerliste');
    setupCollapsible('spacy-header', 'spacy-list', 'Linguistische Attribute');

    // Save button logic for annotation comments
    document.querySelectorAll('.save-annotation-btn').forEach(function(btn, idx) {
        btn.addEventListener('click', function() {
            var li = btn.closest('li');
            var input = li.querySelector('input[type="text"][name^="comment_"]');
            var comment = input ? input.value : '';
            // Get annotation_id from a data attribute (add this to your li in the template)
            var annotationId = li.getAttribute('data-annotation-id');
            var grund = li.querySelector('.annotation-grund') ? li.querySelector('.annotation-grund').textContent.trim() : '';
            var annotationText = li.querySelector('.annotation-text') ? li.querySelector('.annotation-text').textContent.trim() : '';
            var startPos = li.querySelector('.annotation-start') ? li.querySelector('.annotation-start').textContent.trim() : '';
            var endPos = li.querySelector('.annotation-end') ? li.querySelector('.annotation-end').textContent.trim() : '';
            btn.disabled = true;
            fetch('/update_annotation', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: 'annotation_id=' + encodeURIComponent(annotationId) +
                      '&new_comment=' + encodeURIComponent(comment) +
                      '&grund=' + encodeURIComponent(grund) +
                      '&annotation=' + encodeURIComponent(annotationText) +
                      '&start_pos=' + encodeURIComponent(startPos) +
                      '&end_pos=' + encodeURIComponent(endPos)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    btn.textContent = 'Gespeichert!';
                    btn.style.background = '#28a745';
                } else {
                    btn.textContent = 'Fehler!';
                    btn.style.background = '#dc3545';
                }
                setTimeout(function() {
                    btn.textContent = 'Speichern';
                    btn.style.background = '#0074D9';
                    btn.disabled = false;
                }, 1200);
            })
            .catch(() => {
                btn.textContent = 'Fehler!';
                setTimeout(function() { btn.textContent = 'Speichern'; btn.disabled = false; }, 1200);
            });
        });
    });

    // Delete button logic for annotation
    document.querySelectorAll('.delete-annotation-btn').forEach(function(btn) {
        btn.addEventListener('click', function() {
            var li = btn.closest('li');
            var annotationId = li.getAttribute('data-annotation-id');
            if (!annotationId) {
                alert('Annotation ID fehlt!');
                return;
            }
            btn.disabled = true;
            fetch('/delete_annotation', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: 'annotation_id=' + encodeURIComponent(annotationId)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    li.remove();
                } else {
                    btn.textContent = 'Fehler!';
                    setTimeout(function() { btn.textContent = 'Löschen'; btn.disabled = false; }, 1200);
                }
            })
            .catch(() => {
                btn.textContent = 'Fehler!';
                setTimeout(function() { btn.textContent = 'Löschen'; btn.disabled = false; }, 1200);
            });
        });
    });
});