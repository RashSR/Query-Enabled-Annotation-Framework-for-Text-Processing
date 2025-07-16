document.addEventListener('DOMContentLoaded', () => {

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
    const logicSel = clone.querySelector('select[name="logic_operator"]');
    logicSel.name = `logic_operator[${nodeIndex}]`;

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

  // Selection logic
  document.addEventListener('click', (e) => {
    // Delete logic (match button or child elements) FIRST
    if (e.target.closest('.delete-search-btn')) {
      const btn = e.target.closest('.delete-search-btn');
      const searchBar = btn.closest('.search-group');
      if (searchBar) {
        searchBar.remove();
      }
      return;
    }
    if (e.target.closest('.delete-complex-search-btn')) {
      const btn = e.target.closest('.delete-complex-search-btn');
      const complexBar = btn.closest('.complex-search-group');
      if (complexBar) {
        complexBar.remove();
        if (selectedNode && !document.body.contains(selectedNode)) selectedNode = null;
        // If no complex nodes remain, re-enable global add buttons
        if (document.querySelectorAll('.complex-search-group').length === 0) {
          restrictToComplex = false;
          updateGlobalAddButtons();
        }
      }
      return;
    }
    if (e.target.matches('.search-toggle')) {
      const cb = document.getElementById(e.target.dataset.toggleId);
      if (cb) {
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
      updateGlobalAddButtons();
    } else if (restrictToComplex && selectedNode && selectedNode.classList.contains('complex-search-group')) {
      createSearchBar(selectedNode);
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
      // After first complex node is created, restrict further adds
      restrictToComplex = true;
      updateGlobalAddButtons();
      return;
    }
    // If restrictToComplex is true, only allow as child of complex node
    if (selectedNode && selectedNode.classList.contains('complex-search-group')) {
      createComplexSearchBar(selectedNode);
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
    const left = ev.target.closest('select[name^="selected_type"]');
    if (!left) return;

    const group = left.closest('.search-group');
    const right = group?.querySelector('select[name^="selected_scope"]');
    const input = group?.querySelector('input[name^="keyword"]');
    if (!right || !input) return;

    /* enable/disable keyword input */
    if (left.value === 'word') {
      input.disabled = false;
    } else {
      input.value = '';
      input.disabled = true;
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