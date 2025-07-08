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
  const container = document.getElementById('extra-search-fields');
  const addBtn    = document.getElementById('add-search-btn');

  let toggleIndex = 1;
  let barIndex    = 0;

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

    /* index field names */
    keywordInput.name = `keyword[${barIndex}]`;
    leftSel.name      = `selected_type[${barIndex}]`;
    rightSel.name     = `selected_scope[${barIndex}]`;

    clone.querySelectorAll('.hidden-toggle').forEach(cb => {
      const base = cb.name.replace('[]', '');
      cb.name = `${base}[${barIndex}]`;
    });
    barIndex++;

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
    container.appendChild(clone);
  }

  /* ───────── Initial setup ───────── */

  if (!document.querySelector('.search-group')) {
      createSearchBar();
  }                   // one bar on load
  addBtn.addEventListener('click', createSearchBar);

  /* ───────── Delegated clicks ───────── */
  document.addEventListener('click', (e) => {
    if (e.target.matches('.delete-search-btn')) {
      e.target.closest('.search-group')?.remove();
      return;
    }
    if (e.target.matches('.search-toggle')) {
      const cb = document.getElementById(e.target.dataset.toggleId);
      if (cb) {
        cb.checked = !cb.checked;
        e.target.classList.toggle('active', cb.checked);
      }
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