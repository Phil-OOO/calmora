/**
 * Calmora - Main JavaScript
 * Shared utilities and interactions
 */

// ── Range Slider Live Value Display ──────────────────────────────
document.querySelectorAll('input[type="range"]').forEach(slider => {
  const display = document.getElementById(slider.id + '_display');
  if (display) {
    display.textContent = slider.value;
    slider.addEventListener('input', () => { display.textContent = slider.value; });
  }
});

// ── Habit Toggle (AJAX) ──────────────────────────────────────────
document.querySelectorAll('.habit-toggle-btn').forEach(btn => {
  btn.addEventListener('click', async () => {
    const habitId = btn.dataset.habitId;
    const token = document.querySelector('meta[name="csrf-token"]')?.content || '';
    
    const resp = await fetch(`/habits/toggle/${habitId}`, {
      method: 'POST',
      headers: { 'X-CSRFToken': token, 'Content-Type': 'application/json' }
    });
    const data = await resp.json();
    
    const icon = btn.querySelector('i');
    const streakEl = document.getElementById(`streak-${habitId}`);
    
    if (data.completed) {
      btn.classList.remove('btn-outline-success');
      btn.classList.add('btn-success');
      if (icon) icon.className = 'bi bi-check-circle-fill';
    } else {
      btn.classList.remove('btn-success');
      btn.classList.add('btn-outline-success');
      if (icon) icon.className = 'bi bi-circle';
    }
    
    if (streakEl) streakEl.textContent = data.streak;
  });
});

// ── Journal Favorite Toggle ──────────────────────────────────────
document.querySelectorAll('.favorite-btn').forEach(btn => {
  btn.addEventListener('click', async () => {
    const entryId = btn.dataset.entryId;
    const token = document.querySelector('meta[name="csrf-token"]')?.content || '';
    
    const resp = await fetch(`/journal/toggle-favorite/${entryId}`, {
      method: 'POST',
      headers: { 'X-CSRFToken': token }
    });
    const data = await resp.json();
    
    const icon = btn.querySelector('i');
    if (data.favorited) {
      icon.className = 'bi bi-heart-fill text-danger';
    } else {
      icon.className = 'bi bi-heart text-muted';
    }
  });
});

// ── Word Count for Journal Editor ────────────────────────────────
const journalContent = document.getElementById('content');
const wordCountEl = document.getElementById('wordCount');
if (journalContent && wordCountEl) {
  journalContent.addEventListener('input', () => {
    const words = journalContent.value.trim().split(/\s+/).filter(w => w).length;
    wordCountEl.textContent = words;
  });
}

// ── Auto-save indicator (visual only) ───────────────────────────
const forms = document.querySelectorAll('.auto-save-form');
forms.forEach(form => {
  const indicator = document.getElementById('autoSaveIndicator');
  let timer;
  form.querySelectorAll('input, textarea, select').forEach(input => {
    input.addEventListener('input', () => {
      if (indicator) indicator.textContent = 'Unsaved changes…';
      clearTimeout(timer);
    });
  });
});

// ── Tooltip init ─────────────────────────────────────────────────
document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(el => {
  new bootstrap.Tooltip(el);
});

// ── Smooth card hover (optional enhancement) ─────────────────────
document.querySelectorAll('.stat-card').forEach(card => {
  card.addEventListener('mouseenter', () => card.style.transition = 'all .2s ease');
});

// ── Delete confirm ───────────────────────────────────────────────
document.querySelectorAll('[data-confirm]').forEach(btn => {
  btn.addEventListener('click', e => {
    if (!confirm(btn.dataset.confirm || 'Are you sure?')) {
      e.preventDefault();
    }
  });
});