    // Dynamically populate Regel-ID dropdowns for Fehlerliste
    document.querySelectorAll('.error-ruleid-dropdown').forEach(function(select) {
        var current = select.getAttribute('data-current');
        fetch('/api/filter-values?type=error-ruleId')
            .then(r => r.json())
            .then(function(options) {
                select.innerHTML = '';
                options.forEach(function(opt) {
                    var option = document.createElement('option');
                    option.value = opt;
                    option.textContent = opt;
                    if (opt === current) option.selected = true;
                    select.appendChild(option);
                });
            });
    });
    // Save button logic for Fehlerliste (error list) elements
    document.querySelectorAll('.save-error-btn').forEach(function(btn) {
        btn.addEventListener('click', function() {
            var li = btn.closest('li');
            var errorId = li.getAttribute('data-id');
            if (!errorId) {
                alert('Fehler-ID fehlt!');
                return;
            }
            var categorySelect = li.querySelector('.error-category-dropdown');
            var category = categorySelect ? categorySelect.value : '';
            var startSpan = li.querySelector('.error-start');
            var endSpan = li.querySelector('.error-end');
            var ruleSelect = li.querySelector('.error-ruleid-dropdown');
            var start_pos = startSpan ? startSpan.textContent.trim() : '';
            var end_pos = endSpan ? endSpan.textContent.trim() : '';
            var rule_id = ruleSelect ? ruleSelect.value : '';
            btn.disabled = true;
            fetch('/update_error', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: 'id=' + encodeURIComponent(errorId) +
                      '&category=' + encodeURIComponent(category) +
                      '&start_pos=' + encodeURIComponent(start_pos) +
                      '&end_pos=' + encodeURIComponent(end_pos) +
                      '&rule_id=' + encodeURIComponent(rule_id)
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
                btn.style.background = '#dc3545';
                setTimeout(function() {
                    btn.textContent = 'Speichern';
                    btn.style.background = '#0074D9';
                    btn.disabled = false;
                }, 1200);
            });
        });
    });
    // Dynamically populate Kategorie dropdowns for Fehlerliste
    document.querySelectorAll('.error-category-dropdown').forEach(function(select) {
        var current = select.getAttribute('data-current');
        fetch('/api/filter-values?type=error-category')
            .then(r => r.json())
            .then(function(options) {
                select.innerHTML = '';
                options.forEach(function(opt) {
                    var option = document.createElement('option');
                    option.value = opt;
                    option.textContent = opt;
                    if (opt === current) option.selected = true;
                    select.appendChild(option);
                });
            });
    });

    // Helper to update header count and empty message for a list
    function updateHeaderCountAndEmpty(listId, headerSelector, itemClass, emptyMsg) {
        var list = document.getElementById(listId);
        var headerSpan = document.querySelector(headerSelector);
        var items = list ? list.querySelectorAll('.' + itemClass) : [];
        if (headerSpan) {
            // Extract label text before count
            var label = headerSpan.textContent.replace(/\(.*\).*/, '').trim();
            headerSpan.textContent = label + ' (' + items.length + ') ▶';
        }
        if (list && items.length === 0) {
            list.innerHTML = '<p style="color:#888;">' + emptyMsg + '</p>';
        }
    }

    // Delete button logic for spaCy matches
    document.querySelectorAll('.delete-spacy-btn').forEach(function(btn) {
        btn.addEventListener('click', function() {
            var li = btn.closest('li');
            var spacyId = li.getAttribute('data-id');
            if (!spacyId) {
                alert('spaCy-Match ID fehlt!');
                return;
            }
            btn.disabled = true;
            fetch('/delete_spacy_match', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: 'id=' + encodeURIComponent(spacyId)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    li.remove();
                    updateHeaderCountAndEmpty('spacy-list', '#spacy-header span', 'spacy-item', 'Keine linguistischen Attribute vorhanden.');
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

    // Delete button logic for Fehlerliste (error list) elements
    document.querySelectorAll('.delete-error-btn').forEach(function(btn) {
        btn.addEventListener('click', function() {
            var li = btn.closest('li');
            var errorId = li.getAttribute('data-id');
            if (!errorId) {
                alert('Fehler-ID fehlt!');
                return;
            }
            btn.disabled = true;
            fetch('/delete_error', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: 'id=' + encodeURIComponent(errorId)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    li.remove();
                    updateHeaderCountAndEmpty('error-list', '#error-header span', 'error-item', 'Keine Fehler vorhanden.');
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
document.addEventListener('DOMContentLoaded', function() {
    // Open 'Manuelle Annotationen' list if flag is set
    if (localStorage.getItem('openAnnotationListAfterReload')) {
        var annotationList = document.getElementById('annotation-list');
        var annotationHeader = document.getElementById('annotation-header');
        if (annotationList && annotationHeader) {
            annotationList.style.display = 'block';
            // Optionally update header arrow or state here
        }
        localStorage.removeItem('openAnnotationListAfterReload');
    }

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
            var annotationId = li.getAttribute('data-annotation-id');
            // Now get editable values from input fields
            var grundInput = li.querySelector('input.annotation-grund');
            var grund = grundInput ? grundInput.value : '';
            var annotationTextInput = li.querySelector('input.annotation-text');
            var annotationText = annotationTextInput ? annotationTextInput.value : '';
            var startPosInput = li.querySelector('input.annotation-start');
            var startPos = startPosInput ? startPosInput.value : '';
            var endPosInput = li.querySelector('input.annotation-end');
            var endPos = endPosInput ? endPosInput.value : '';
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
                    updateAnnotationHeaderCount();
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

    // Update annotation header counter
    function updateAnnotationHeaderCount() {
        var headerSpan = document.querySelector('#annotation-header span');
        var annotationItems = document.querySelectorAll('.annotation-item');
        var annotationList = document.getElementById('annotation-list');
        if (headerSpan) {
            headerSpan.textContent = 'Manuelle Annotationen (' + annotationItems.length + ') ▶';
        }
        // Show default message if no items left
        if (annotationList && annotationItems.length === 0) {
            annotationList.innerHTML = '<p style="color:#888;">Keine manuellen Annotationen vorhanden.</p>';
        }
    }

    // Selectable list items logic with checkbox (multi-select), but ignore dropdown interaction
    document.querySelectorAll('.selectable').forEach(function(item) {
        var checkbox = item.querySelector('.select-checkbox');
        item.addEventListener('click', function(e) {
            // Prevent toggle if clicking a button or a dropdown/select
            if (e.target.tagName === 'BUTTON' || e.target.tagName === 'SELECT') return;
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
                // Attach submit handler
                var manualForm = document.getElementById('manual-annotation-form');
                if (manualForm) {
                    manualForm.onsubmit = function(e) {
                        e.preventDefault();
                        var formData = new FormData(manualForm);
                        var messageId = window.message_id || document.getElementById('annotated-text').getAttribute('data-message-id');
                        if (messageId) {
                            formData.append('message_id', messageId);
                        }
                        var saveBtn = manualForm.querySelector('button[type="submit"]');
                        fetch('/save_annotation', {
                            method: 'POST',
                            body: formData
                        })
                        .then(response => response.json())
                        .then(data => {
                            if (data.success) {
                                saveBtn.style.background = '#28a745'; // green
                                saveBtn.textContent = 'Gespeichert!';
                                localStorage.setItem('openAnnotationListAfterReload', '1');
                                setTimeout(function() {
                                    window.location.reload();
                                }, 700);
                            } else {
                                saveBtn.style.background = '#dc3545'; // red
                                saveBtn.textContent = 'Fehler!';
                            }
                        })
                        .catch(() => {
                            saveBtn.style.background = '#dc3545'; // red
                            saveBtn.textContent = 'Fehler!';
                        });
                    };
                }
            }
        });
    }

    // Highlight selection in annotated-text and fill position field in form
    function setPositionFromSelection() {
        var annotatedText = document.getElementById('annotated-text');
        var form = document.getElementById('manual-annotation-form');
        if (!annotatedText || !form) return;
        annotatedText.addEventListener('mouseup', function() {
            var selection = window.getSelection();
            if (!selection || selection.rangeCount === 0) return;
            var range = selection.getRangeAt(0);
            if (!annotatedText.contains(range.commonAncestorContainer)) return;
            var selectedText = selection.toString();
            if (!selectedText) return;
            // Calculate offset relative to visible text only
            var fullText = annotatedText.textContent;
            var leadingWhitespaceMatch = fullText.match(/^\s*/);
            var leadingWhitespaceLength = leadingWhitespaceMatch ? leadingWhitespaceMatch[0].length : 0;
            var preRange = document.createRange();
            preRange.selectNodeContents(annotatedText);
            preRange.setEnd(range.startContainer, range.startOffset);
            var start = preRange.toString().length - leadingWhitespaceLength;
            var end = start + selectedText.length;
            var positionInput = document.getElementById('position');
            if (positionInput) {
                positionInput.value = start + '-' + end;
            }
            // Debug output
            var afterText = fullText.substring(end + leadingWhitespaceLength);
            console.log('Annotated text:', fullText);
            console.log('Selected text:', selectedText);
            console.log('Text after selection:', afterText);
            console.log('Leading whitespace length:', leadingWhitespaceLength);
            console.log('Start offset:', start);
            console.log('End offset:', end);
        });
    }

    // Attach after form is created
    function attachFormSelectionListener() {
        var formContainer = document.getElementById('add-annotation-form-container');
        var observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (document.getElementById('manual-annotation-form')) {
                    setPositionFromSelection();
                }
            });
        });
        observer.observe(formContainer, { childList: true });
    }
    attachFormSelectionListener();
});