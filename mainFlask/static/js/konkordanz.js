document.addEventListener('DOMContentLoaded', () => {
  // Show/hide custom number input for range dropdowns
  document.addEventListener('change', function(e) {
    if (e.target.matches('select.range-select')) {
      const select = e.target;
      const customInput = select.parentElement.querySelector('.custom-range-input');
      if (!customInput) return;
      if (select.value === 'custom') {
        customInput.style.display = 'inline-block';
        customInput.required = true;
      } else {
        customInput.style.display = 'none';
        customInput.required = false;
        customInput.value = '';
      }
    }
  });

  // On form submit, if custom is selected, copy the custom value to the token_range field
  document.querySelector('form')?.addEventListener('submit', function(ev) {
    document.querySelectorAll('select.range-select').forEach(function(select) {
      if (select.value === 'custom') {
        const customInput = select.parentElement.querySelector('.custom-range-input');
        if (customInput && customInput.value) {
          // Set the select's value to the custom value for submission
          select.value = customInput.value;
        }
      }
    });
  });
  // Show/hide range dropdown for AND nodes in dynamic complex search
  document.addEventListener('change', function(e) {
    if (e.target.matches('select[name="logic_operator"], select[name^="logic_operator["]')) {
      const select = e.target;
      const parent = select.closest('.complex-search-group');
      if (!parent) return;
      let label = parent.querySelector('.token-range-label');
      if (!label) return;
      const rangeDropdown = label.querySelector('select[name="token_range"]');
      if (select.value === 'AND') {
        label.style.display = '';
      } else {
        label.style.display = 'none';
        if (rangeDropdown) rangeDropdown.value = 'None';
      }
    }
  });

  /* ───────── Hide/show “recipient” column ───────── */
  const toggleRecipient = document.getElementById('toggle-recipient');
  if (toggleRecipient) {
    toggleRecipient.addEventListener('change', function () {
      const col = 3;
      const display = this.checked ? '' : 'none';
      document
        .querySelectorAll(`table th:nth-child(${col + 1}), table td:nth-child(${col + 1})`)
        .forEach(el => el.style.display = display);
    });
  }

  /* ───────── References & state ───────── */
  const template  = document.getElementById('search-template');
  const complexTemplate = document.getElementById('complex-search-template');
  const container = document.getElementById('extra-search-fields');
  // Use global add buttons
  const globalAddBtn    = document.getElementById('global-add-search-btn');
  const globalAddComplexBtn = document.getElementById('global-add-complex-search-btn');

  let toggleIndex = 1;
let nodeCounter = 0;

  // Track complex search groups
  // No longer needed: complexGroups

  /* ───────── Helpers ───────── */

  // --- On page load, re-enable right dropdowns if left dropdown has a value ---
  async function restoreRightDropdowns() {
    document.querySelectorAll('.search-group').forEach(async group => {
      const left = group.querySelector('select[name^="selected_type"]');
      const right = group.querySelector('select[name^="selected_scope"]');
      // Save the current value before repopulating
      const prevValue = right ? right.value : null;
      if (left && right && left.value) {
        try {
          const resp = await fetch(`/api/filter-values?type=${encodeURIComponent(left.value)}`);
          if (!resp.ok) throw new Error(await resp.text());
          const items = await resp.json();
          right.innerHTML = '';
          addEmptyOption(right);
          right.disabled = items.length === 0;
          items.forEach(v => {
            const opt = document.createElement('option');
            opt.value = opt.textContent = v;
            right.appendChild(opt);
          });
          // Restore the previous value if present in the new options
          if (prevValue && Array.from(right.options).some(opt => opt.value === prevValue)) {
            right.value = prevValue;
          }
        } catch (err) {
          console.error(err);
        }
      }
    });
  }

  // Store selected value in data attribute before form submit
  document.querySelector('form')?.addEventListener('submit', () => {
    document.querySelectorAll('.search-group').forEach(group => {
      const right = group.querySelector('select[name^="selected_scope"]');
      if (right) right.dataset.selectedValue = right.value;
    });
  });

  // Call restore on page load
  restoreRightDropdowns();

  function addEmptyOption(select) {
    if (!select || select.querySelector('option[value=""]')) return;
    const empty = document.createElement('option');
    empty.value = '';
    empty.textContent = '— Please select —';
    select.insertBefore(empty, select.firstChild);
    select.value = '';
    select.disabled = true;
  }

  function createSearchBar() {
    const frag  = template.content.cloneNode(true);
    const clone = frag.querySelector('.search-group');
    if (!clone) return console.error('Template missing .search-group');

    // --- left, right dropdowns ---
    const leftSel  = clone.querySelector('select[name="selected_type"]');
    const rightSel = clone.querySelector('select[name="selected_scope"]');

    // --- keyword input (grab ONCE!) ---
    const keywordInput = clone.querySelector('input[name="keyword"]');

    // Hierarchical index logic
    let parentIndex = '';
    if (arguments.length && arguments[0]) {
      const parent = arguments[0];
      parentIndex = parent.dataset.nodeIndex;
    }
    // Find next child index for this parent
    let childNum = 0;
    if (parentIndex) {
      // Count children for this parent
      const groupContainer = arguments[0].querySelector('.grouped-searches');
      childNum = groupContainer ? groupContainer.children.length : 0;
    } else {
      // Root level
      childNum = container.querySelectorAll('.search-group').length;
    }
    let nodeIndex = parentIndex ? `${parentIndex}.${childNum}` : `${childNum}`;
    clone.dataset.nodeIndex = nodeIndex;

    // Use nodeIndex for field names
    keywordInput.name = `keyword[${nodeIndex}]`;
    leftSel.name      = `selected_type[${nodeIndex}]`;
    rightSel.name     = `selected_scope[${nodeIndex}]`;

    clone.querySelectorAll('.hidden-toggle').forEach(cb => {
      const base = cb.name.replace('[]', '');
      cb.name = `${base}[${nodeIndex}]`;
    });


    /* keyword starts disabled */
    keywordInput.disabled = true;
    // Also visually disable the icons
    clone.querySelectorAll('.search-toggle').forEach(t => t.classList.add('disabled-toggle'));

    /* unique IDs for toggle spans */
    const types = ['case_sensitive', 'whole_word', 'use_regex'];
    clone.querySelectorAll('.hidden-toggle').forEach((cb, i) => {
      const id = `${types[i]}_${toggleIndex}`;
      cb.id = id;
      clone.querySelectorAll('.search-toggle')[i].dataset.toggleId = id;
    });
    toggleIndex++;

    addEmptyOption(rightSel);
    // If called with a parent, add to its grouped-searches and indent
    if (arguments.length && arguments[0]) {
      const parent = arguments[0];
      let groupContainer = parent.querySelector('.grouped-searches');
      clone.style.marginLeft = '2rem';
      groupContainer.appendChild(clone);
    } else {
      container.appendChild(clone);
    }
  }

  /* ───────── Initial setup ───────── */

  // Add complex search bar logic
  function createComplexSearchBar(parent) {
    const frag = complexTemplate.content.cloneNode(true);
    const clone = frag.querySelector('.complex-search-group');
    if (!clone) return console.error('Template missing .complex-search-group');
    // Show range dropdown by default for AND nodes
    const logicSelect = clone.querySelector('select[name="logic_operator"]');
    const tokenLabel = clone.querySelector('.token-range-label');
    const rangeDropdown = tokenLabel ? tokenLabel.querySelector('select[name="token_range"]') : null;
    if (logicSelect && tokenLabel && logicSelect.value === 'AND') {
      tokenLabel.style.display = '';
    }
    // Set default value to 'None' (Message)
    if (rangeDropdown) {
      rangeDropdown.value = 'None';
    }
    // Hierarchical index logic
    let parentIndex = '';
    if (parent) {
      parentIndex = parent.dataset.nodeIndex;
    }
    // Find next child index for this parent
    let childNum = 0;
    if (parentIndex) {
      const groupContainer = parent.querySelector('.grouped-searches');
      childNum = groupContainer ? groupContainer.children.length : 0;
    } else {
      childNum = container.querySelectorAll('.complex-search-group').length;
    }
    let nodeIndex = parentIndex ? `${parentIndex}.${childNum}` : `${childNum}`;
    clone.dataset.nodeIndex = nodeIndex;

    // Set field name for logic operator
    logicSelect.name = `logic_operator[${nodeIndex}]`;

    if (parent) {
      let groupContainer = parent.querySelector('.grouped-searches');
      clone.style.marginLeft = '2rem';
      groupContainer.appendChild(clone);
    } else {
      container.appendChild(clone);
      clone.style.marginLeft = '0';
    }
    // Auto-select the new complex node
    setTimeout(() => selectNode(clone), 0);
  }

  /* ───────── Delegated clicks ───────── */
  let selectedNode = null;

  // Selection logic and add child search buttons
  document.addEventListener('click', (e) => {
    // Delete logic (match button or child elements) FIRST
    if (e.target.closest('.delete-search-btn')) {
      const btn = e.target.closest('.delete-search-btn');
      const searchBar = btn.closest('.search-group');
      if (searchBar) {
        // If the deleted node is selected, clear selection
        if (selectedNode === searchBar) {
          selectedNode.classList.remove('selected');
          selectedNode = null;
        }
        // Check if parent is a NOT complex node and still selected
        const parentComplex = searchBar.parentElement.closest('.complex-search-group');
        searchBar.remove();
        // Show global add buttons if all search bars are deleted
        const numSimple = container.querySelectorAll('.search-group').length;
        const numComplex = container.querySelectorAll('.complex-search-group').length;
        if (numSimple === 0 && numComplex === 0) {
          document.getElementById('global-add-buttons').style.display = '';
        }
        if (parentComplex && parentComplex === selectedNode) {
          // Re-enable the simple search button if NOT node is selected
          updateGlobalAddButtons();
        } else {
          updateGlobalAddButtons();
        }
      }
      return;
    }
    if (e.target.closest('.delete-complex-search-btn')) {
      const btn = e.target.closest('.delete-complex-search-btn');
      const complexBar = btn.closest('.complex-search-group');
      if (complexBar) {
        // If the deleted node is selected, clear selection
        if (selectedNode === complexBar) {
          selectedNode.classList.remove('selected');
          selectedNode = null;
        }
        complexBar.remove();
        // Show global add buttons if all search bars are deleted
        const numSimple = container.querySelectorAll('.search-group').length;
        const numComplex = container.querySelectorAll('.complex-search-group').length;
        if (numSimple === 0 && numComplex === 0) {
          document.getElementById('global-add-buttons').style.display = '';
        }
        // If no complex nodes remain, re-enable global add buttons
        if (document.querySelectorAll('.complex-search-group').length === 0) {
          restrictToComplex = false;
        }
        updateGlobalAddButtons();
      }
      return;
    }
    // --- Add child complex search ---
    if (e.target.closest('.add-complex-search-btn')) {
      const btn = e.target.closest('.add-complex-search-btn');
      const complexBar = btn.closest('.complex-search-group');
      if (complexBar) {
        createComplexSearchBar(complexBar);
        updateGlobalAddButtons();
      }
      return;
    }
    // --- Add child simple search ---
    if (e.target.closest('.add-simple-search-btn')) {
      const btn = e.target.closest('.add-simple-search-btn');
      const complexBar = btn.closest('.complex-search-group');
      if (complexBar) {
        createSearchBar(complexBar);
        updateGlobalAddButtons();
      }
      return;
    }
    if (e.target.matches('.search-toggle')) {
      const cb = document.getElementById(e.target.dataset.toggleId);
      // Find the associated input (keyword textbox) in the same .search-group
      const searchGroup = e.target.closest('.search-group');
      const input = searchGroup ? searchGroup.querySelector('input[name^="keyword"]') : null;
      if (cb && input && !input.disabled) {
        cb.checked = !cb.checked;
        e.target.classList.toggle('active', cb.checked);
      }
      return;
    }
    // Select only complex search node on click (after delete/icon logic)
    if (e.target.closest('.complex-search-group')) {
      selectNode(e.target.closest('.complex-search-group'));
      return;
    }
  });

  function selectNode(node) {
    if (selectedNode) selectedNode.classList.remove('selected');
    selectedNode = node;
    selectedNode.classList.add('selected');
  }



  // --- Enable/disable global add buttons based on selection and state ---
  let restrictToComplex = false;
  function updateGlobalAddButtons() {
    const numSimple = container.querySelectorAll('.search-group').length;
    const numComplex = container.querySelectorAll('.complex-search-group').length;
    // If no simple and no complex, both enabled
    if (numSimple === 0 && numComplex === 0) {
      globalAddBtn.disabled = false;
      globalAddComplexBtn.disabled = false;
      globalAddBtn.classList.remove('disabled');
      globalAddComplexBtn.classList.remove('disabled');
      globalAddBtn.style.opacity = '';
      globalAddComplexBtn.style.opacity = '';
      globalAddBtn.style.cursor = '';
      globalAddComplexBtn.style.cursor = '';
      restrictToComplex = false;
      return;
    }
    // If only one simple at root, disable both
    if (numSimple === 1 && numComplex === 0) {
      globalAddBtn.disabled = true;
      globalAddComplexBtn.disabled = true;
      globalAddBtn.classList.add('disabled');
      globalAddComplexBtn.classList.add('disabled');
      globalAddBtn.style.opacity = '0.5';
      globalAddComplexBtn.style.opacity = '0.5';
      globalAddBtn.style.cursor = 'not-allowed';
      globalAddComplexBtn.style.cursor = 'not-allowed';
      restrictToComplex = false;
      return;
    }
    // If restrictToComplex is not set, but a complex node exists, set it
    if (numComplex > 0 && !restrictToComplex) restrictToComplex = true;

    // Special logic for NOT complex search
    if (selectedNode && selectedNode.classList.contains('complex-search-group')) {
      const logicDropdown = selectedNode.querySelector('select[name^="logic_operator"]');
      if (logicDropdown && logicDropdown.value === 'NOT') {
        // Only allow one simple search as child
        const groupContainer = selectedNode.querySelector('.grouped-searches');
        const numChildren = groupContainer ? groupContainer.children.length : 0;
        // Enable simple search button only if no child exists
        if (numChildren === 0) {
          globalAddBtn.disabled = false;
          globalAddBtn.classList.remove('disabled');
          globalAddBtn.style.opacity = '1';
          globalAddBtn.style.cursor = 'pointer';
        } else {
          globalAddBtn.disabled = true;
          globalAddBtn.classList.add('disabled');
          globalAddBtn.style.opacity = '0.5';
          globalAddBtn.style.cursor = 'not-allowed';
        }
        // Always disable complex search button
        globalAddComplexBtn.disabled = true;
        globalAddComplexBtn.classList.add('disabled');
        globalAddComplexBtn.style.opacity = '0.5';
        globalAddComplexBtn.style.cursor = 'not-allowed';
        return;
      }
    }

    // If restrictToComplex, use the previous logic
    if (restrictToComplex) {
      if (selectedNode && selectedNode.classList.contains('complex-search-group')) {
        globalAddBtn.disabled = false;
        globalAddComplexBtn.disabled = false;
        globalAddBtn.classList.remove('disabled');
        globalAddComplexBtn.classList.remove('disabled');
        globalAddBtn.style.opacity = '1';
        globalAddComplexBtn.style.opacity = '1';
        globalAddBtn.style.cursor = 'pointer';
        globalAddComplexBtn.style.cursor = 'pointer';
      } else {
        globalAddBtn.disabled = true;
        globalAddComplexBtn.disabled = true;
        globalAddBtn.classList.add('disabled');
        globalAddComplexBtn.classList.add('disabled');
        globalAddBtn.style.opacity = '0.5';
        globalAddComplexBtn.style.opacity = '0.5';
        globalAddBtn.style.cursor = 'not-allowed';
        globalAddComplexBtn.style.cursor = 'not-allowed';
      }
      return;
    }
    // Fallback: disable both
    globalAddBtn.disabled = true;
    globalAddComplexBtn.disabled = true;
    globalAddBtn.classList.add('disabled');
    globalAddComplexBtn.classList.add('disabled');
    globalAddBtn.style.opacity = '0.5';
    globalAddComplexBtn.style.opacity = '0.5';
    globalAddBtn.style.cursor = 'not-allowed';
    globalAddComplexBtn.style.cursor = 'not-allowed';
  }

  // Initial state: enabled
  updateGlobalAddButtons();

  // Global add buttons
  globalAddBtn.addEventListener('click', () => {
    // Only allow at root if no simple/complex exists
    const numSimple = container.querySelectorAll('.search-group').length;
    const numComplex = container.querySelectorAll('.complex-search-group').length;
    if (numSimple === 0 && numComplex === 0) {
      createSearchBar();
      document.getElementById('global-add-buttons').style.display = 'none';
      updateGlobalAddButtons();
    } else if (restrictToComplex && selectedNode && selectedNode.classList.contains('complex-search-group')) {
      createSearchBar(selectedNode);
      document.getElementById('global-add-buttons').style.display = 'none';
      updateGlobalAddButtons();
    }
  });
  globalAddComplexBtn.addEventListener('click', () => {
    // If restrictToComplex is false, allow adding at root or as child
    if (!restrictToComplex) {
      if (selectedNode && selectedNode.classList.contains('complex-search-group')) {
        createComplexSearchBar(selectedNode);
      } else {
        createComplexSearchBar();
      }
      document.getElementById('global-add-buttons').style.display = 'none';
      // After first complex node is created, restrict further adds
      restrictToComplex = true;
      updateGlobalAddButtons();
      return;
    }
    // If restrictToComplex is true, only allow as child of complex node
    if (selectedNode && selectedNode.classList.contains('complex-search-group')) {
      createComplexSearchBar(selectedNode);
      document.getElementById('global-add-buttons').style.display = 'none';
    }
  });

  // Update buttons on node selection
  function selectNode(node) {
    if (selectedNode) selectedNode.classList.remove('selected');
    selectedNode = node;
    selectedNode.classList.add('selected');
    updateGlobalAddButtons();
  }

  // Also update on click outside (deselect), but ignore clicks on global add buttons
  document.addEventListener('click', (e) => {
    const isAddBtn = e.target.closest('#global-add-search-btn') || e.target.closest('#global-add-complex-search-btn');
    if (isAddBtn) return;
    if (!e.target.closest('.complex-search-group') && !e.target.closest('.search-group')) {
      if (selectedNode) selectedNode.classList.remove('selected');
      selectedNode = null;
      updateGlobalAddButtons();
    }
  });

  /* ───────── Main change handler ───────── */
  container.addEventListener('change', async (ev) => {
    // Logic operator change: prevent invalid NOT
    if (ev.target.matches('select[name^="logic_operator"]')) {
      const dropdown = ev.target;
      const complexNode = dropdown.closest('.complex-search-group');
      const groupContainer = complexNode.querySelector('.grouped-searches');
      const children = Array.from(groupContainer.children);
      const numChildren = children.length;
      const hasComplexChild = children.some(child => child.classList.contains('complex-search-group'));
      const prevValue = dropdown.dataset.prevValue || 'AND';
      if (dropdown.value === 'NOT' && (numChildren > 1 || hasComplexChild)) {
        alert('Ein NOT-Knoten darf nur eine einfache Suche als Kind haben.');
        dropdown.value = prevValue;
        return;
      }
      // Save current value for future revert
      dropdown.dataset.prevValue = dropdown.value;
      updateGlobalAddButtons();
      return;
    }

    const left = ev.target.closest('select[name^="selected_type"]');
    if (!left) return;

    const group = left.closest('.search-group');
    const right = group?.querySelector('select[name^="selected_scope"]');
    const input = group?.querySelector('input[name^="keyword"]');
    if (!right || !input) return;

    /* enable/disable keyword input and toggle icon style */
    const toggles = group.querySelectorAll('.search-toggle');
    if (left.value === 'word') {
      input.disabled = false;
      toggles.forEach(t => t.classList.remove('disabled-toggle'));
    } else {
      input.value = '';
      input.disabled = true;
      toggles.forEach(t => t.classList.add('disabled-toggle'));
    }

    if (!left.value) {
      right.innerHTML = '<option value="" selected>— Please select —</option>';
      right.disabled  = true;
      return;
    }

    try {
      const resp  = await fetch(`/api/filter-values?type=${encodeURIComponent(left.value)}`);
      if (!resp.ok) throw new Error(await resp.text());
      const items = await resp.json();

      right.innerHTML = '';
      addEmptyOption(right);
      right.disabled = items.length === 0;

      items.forEach(v => {
        const opt = document.createElement('option');
        opt.value = opt.textContent = v;
        right.appendChild(opt);
      });
    } catch (err) {
      console.error(err);
      alert('Fehler beim Laden der Werte');
    }
  });

  /* ───────── Restore toggle button states on page load ───────── */
  document.querySelectorAll('.hidden-toggle').forEach(cb => {
    if (cb.checked) {
      const toggleSpan = document.querySelector(`.search-toggle[data-toggle-id="${cb.id}"]`);
      if (toggleSpan) {
        toggleSpan.classList.add('active');
      }
    }
  });

});