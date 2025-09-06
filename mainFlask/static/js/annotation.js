document.addEventListener('DOMContentLoaded', function() {
    function setupCollapsible(headerId, listId, label) {
        var header = document.getElementById(headerId);
        var list = document.getElementById(listId);
        var arrowSpan = header ? header.querySelector('span') : null;
        var expanded = false;
        if (header && list && arrowSpan) {
            header.addEventListener('click', function(e) {
                // Prevent toggle if clicking the Hinzufügen button or header checkbox
                if (e.target.classList.contains('add-annotation-btn') ||
                    e.target.classList.contains('add-error-btn') ||
                    e.target.classList.contains('add-spacy-btn') ||
                    e.target.classList.contains('header-checkbox')) {
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

    // Selectable list items logic with checkbox (multi-select)
    document.querySelectorAll('.selectable').forEach(function(item) {
        var checkbox = item.querySelector('.select-checkbox');
        item.addEventListener('click', function(e) {
            if (e.target.tagName === 'BUTTON') return;
            var isSelected = item.classList.contains('selected');
            if (isSelected) {
                item.classList.remove('selected');
                if (checkbox) checkbox.checked = false;
            } else {
                item.classList.add('selected');
                if (checkbox) checkbox.checked = true;
            }
        });
        if (checkbox) {
            checkbox.addEventListener('click', function(e) {
                e.stopPropagation();
                var isSelected = item.classList.contains('selected');
                if (isSelected) {
                    item.classList.remove('selected');
                    checkbox.checked = false;
                } else {
                    item.classList.add('selected');
                    checkbox.checked = true;
                }
            });
        }
    });

    // Header checkbox logic for bulk select/deselect
    function setupHeaderCheckbox(headerClass, itemClass) {
        var headerCheckbox = document.querySelector('.' + headerClass);
        var items = document.querySelectorAll('.' + itemClass);
        if (headerCheckbox) {
            headerCheckbox.addEventListener('change', function() {
                var checked = headerCheckbox.checked;
                items.forEach(function(item) {
                    var cb = item.querySelector('.select-checkbox');
                    if (checked) {
                        item.classList.add('selected');
                        if (cb) cb.checked = true;
                    } else {
                        item.classList.remove('selected');
                        if (cb) cb.checked = false;
                    }
                });
            });
        }
        // Sync header checkbox if all/none selected
        function syncHeaderCheckbox() {
            var selectedCount = 0;
            items.forEach(function(item) {
                if (item.classList.contains('selected')) selectedCount++;
            });
            if (selectedCount === items.length && items.length > 0) {
                headerCheckbox.checked = true;
            } else {
                headerCheckbox.checked = false;
            }
        }
        items.forEach(function(item) {
            var cb = item.querySelector('.select-checkbox');
            if (cb) {
                cb.addEventListener('change', syncHeaderCheckbox);
            }
            item.addEventListener('click', syncHeaderCheckbox);
        });
    }
    setupHeaderCheckbox('annotation-header-checkbox', 'annotation-item');
    setupHeaderCheckbox('error-header-checkbox', 'error-item');
    setupHeaderCheckbox('spacy-header-checkbox', 'spacy-item');

    // Toggle highlight CSS for spans based on header checkbox or all items selected
    function setupSpanHighlight(headerClass, bodyClass, itemClass) {
        var headerCheckbox = document.querySelector('.' + headerClass);
        var items = document.querySelectorAll('.' + itemClass);
        function updateHighlight() {
            var allSelected = Array.from(items).length > 0 && Array.from(items).every(function(item) {
                return item.classList.contains('selected');
            });
            if ((headerCheckbox && headerCheckbox.checked) || allSelected) {
                document.body.classList.add(bodyClass);
            } else {
                document.body.classList.remove(bodyClass);
            }
        }
        if (headerCheckbox) {
            headerCheckbox.addEventListener('change', updateHighlight);
        }
        items.forEach(function(item) {
            item.addEventListener('click', updateHighlight);
            var cb = item.querySelector('.select-checkbox');
            if (cb) {
                cb.addEventListener('change', updateHighlight);
            }
        });
        // Initial state
        updateHighlight();
    }
    setupSpanHighlight('annotation-header-checkbox', 'show-annotation-highlight', 'annotation-item');
    setupSpanHighlight('error-header-checkbox', 'show-error-highlight', 'error-item');
    setupSpanHighlight('spacy-header-checkbox', 'show-pos-highlight', 'spacy-item');

    var addBtn = document.querySelector('.add-annotation-btn');
    var formContainer = document.getElementById('add-annotation-form-container');
    if (addBtn && formContainer) {
        addBtn.addEventListener('click', function() {
            if (formContainer.style.display === 'none' || !formContainer.innerHTML) {
                formContainer.innerHTML = `
                    <form id="manual-annotation-form" style="background:#e9ecef; padding:1em; border-radius:6px; box-shadow:0 2px 8px rgba(0,0,0,0.07);">
                        <div style="margin-bottom:0.7em;">
                            <label for="position" style="font-weight:bold;">Position:</label>
                            <input type="text" id="position" name="position" style="margin-left:1em; padding:0.3em; border-radius:3px; border:1px solid #ccc; width:6em;" required />
                        </div>
                        <div style="margin-bottom:0.7em;">
                            <label for="annotation" style="font-weight:bold;">Annotation:</label>
                            <input type="text" id="annotation" name="annotation" style="margin-left:1em; padding:0.3em; border-radius:3px; border:1px solid #ccc; width:12em;" required />
                        </div>
                        <div style="margin-bottom:0.7em;">
                            <label for="grund" style="font-weight:bold;">Grund:</label>
                            <input type="text" id="grund" name="grund" style="margin-left:1em; padding:0.3em; border-radius:3px; border:1px solid #ccc; width:12em;" />
                        </div>
                        <div style="margin-bottom:0.7em;">
                            <label for="kommentar" style="font-weight:bold;">Kommentar:</label>
                            <input type="text" id="kommentar" name="kommentar" style="margin-left:1em; padding:0.3em; border-radius:3px; border:1px solid #ccc; width:16em;" />
                        </div>
                        <button type="submit" style="background:#0074D9; color:white; border:none; border-radius:3px; padding:0.4em 1.2em; font-size:1em; cursor:pointer;">Speichern</button>
                        <button type="button" id="cancel-annotation-form" style="background:#dc3545; color:white; border:none; border-radius:3px; padding:0.4em 1.2em; font-size:1em; cursor:pointer; margin-left:1em;">Abbrechen</button>
                    </form>
                `;
                formContainer.style.display = 'block';
                document.getElementById('cancel-annotation-form').onclick = function() {
                    formContainer.style.display = 'none';
                    formContainer.innerHTML = '';
                };
            }
        });
    }
});