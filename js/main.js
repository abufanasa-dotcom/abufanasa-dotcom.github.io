'use strict';
(() => {
  const en = document.documentElement.lang === 'en';
  const themeButton = document.querySelector('.theme-toggle');
  const colorPreference = window.matchMedia('(prefers-color-scheme: dark)');
  const themeKey = 'aa-portfolio-theme';
  let themeOverride;
  try { themeOverride = window.localStorage.getItem(themeKey); } catch { /* Keep the control usable without storage. */ }
  if (themeOverride !== 'light' && themeOverride !== 'dark') themeOverride = null;
  const applyTheme = theme => {
    document.documentElement.setAttribute('data-theme', theme);
    const dark = theme === 'dark';
    document.querySelector('meta[name="theme-color"]')?.setAttribute('content', dark ? '#101923' : '#fafbfc');
    if (themeButton) {
      themeButton.setAttribute('aria-pressed', String(dark));
      themeButton.setAttribute('title', en
        ? (dark ? 'Switch to light theme' : 'Switch to dark theme')
        : (dark ? 'Helles Design aktivieren' : 'Dunkles Design aktivieren'));
    }
  };
  applyTheme(themeOverride || (colorPreference.matches ? 'dark' : 'light'));
  if (themeButton) {
    themeButton.hidden = false;
    themeButton.addEventListener('click', () => {
      themeOverride = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      applyTheme(themeOverride);
      try { window.localStorage.setItem(themeKey, themeOverride); } catch { /* In-page theme switching still works. */ }
    });
  }
  colorPreference.addEventListener('change', event => {
    if (!themeOverride) applyTheme(event.matches ? 'dark' : 'light');
  });
  window.addEventListener('storage', event => {
    if (event.key !== themeKey && event.key !== null) return;
    themeOverride = event.newValue === 'light' || event.newValue === 'dark' ? event.newValue : null;
    applyTheme(themeOverride || (colorPreference.matches ? 'dark' : 'light'));
  });

  const menu = document.querySelector('.menu-toggle');
  const nav = document.querySelector('#navigation');
  const desktop = window.matchMedia('(min-width: 961px)');
  const closeMenu = () => {
    nav?.classList.remove('open');
    menu?.setAttribute('aria-expanded', 'false');
  };
  // Navigation remains visible if JavaScript is unavailable.
  if (menu && nav) {
    menu.hidden = false;
    document.documentElement.classList.add('nav-ready');
    menu.addEventListener('click', () => {
      const open = menu.getAttribute('aria-expanded') !== 'true';
      menu.setAttribute('aria-expanded', String(open));
      nav.classList.toggle('open', open);
    });
    nav.addEventListener('click', event => {
      const anchor = event.target.closest('a');
      if (!anchor) return;
      const wasOpen = nav.classList.contains('open');
      closeMenu();
      // Move focus to the destination before hiding the focused mobile link.
      if (wasOpen) {
        const url = new URL(anchor.href, location.href);
        if (url.pathname === location.pathname && url.hash) {
          const target = document.getElementById(url.hash.slice(1));
          if (target) {
            target.setAttribute('tabindex', '-1');
            target.focus({ preventScroll: true });
          }
        }
      }
    });
    document.addEventListener('keydown', event => {
      if (event.key === 'Escape' && nav.classList.contains('open')) {
        closeMenu();
        menu.focus();
      }
    });
    document.addEventListener('click', event => {
      if (nav.classList.contains('open') && !nav.contains(event.target) && !menu.contains(event.target)) closeMenu();
    });
    desktop.addEventListener('change', event => { if (event.matches) closeMenu(); });
  }

  const dialog = document.querySelector('#chart-dialog');
  let chartTrigger;
  if (dialog && typeof dialog.showModal === 'function') {
    const enlarged = dialog.querySelector('img');
    const caption = dialog.querySelector('#chart-dialog-caption');
    document.querySelectorAll('[data-chart]').forEach(anchor => {
      anchor.addEventListener('click', event => {
        // Preserve normal modified-click behavior and the direct-image fallback.
        if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
        event.preventDefault();
        chartTrigger = anchor;
        enlarged.src = anchor.href; // Original PNG with all scientific detail.
        enlarged.alt = anchor.querySelector('img').alt;
        caption.textContent = anchor.closest('figure').querySelector('figcaption').textContent;
        dialog.showModal();
      });
    });
    dialog.querySelector('.dialog-close').addEventListener('click', () => dialog.close());
    dialog.addEventListener('click', event => {
      if (event.target !== dialog) return;
      const rect = dialog.getBoundingClientRect();
      if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) dialog.close();
    });
    // Escape and focus trapping are supplied by the native modal dialog.
    dialog.addEventListener('close', () => chartTrigger?.focus());
  }

  const contactDialog = document.querySelector('#contact-dialog');
  let contactTrigger;
  if (contactDialog && typeof contactDialog.showModal === 'function') {
    document.querySelectorAll('[data-contact]').forEach(anchor => {
      anchor.setAttribute('aria-haspopup', 'dialog');
      anchor.setAttribute('aria-controls', 'contact-dialog');
      anchor.addEventListener('click', event => {
        if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
        event.preventDefault();
        contactTrigger = anchor;
        const email = contactDialog.querySelector('.copy-email').dataset.email;
        const subject = anchor.dataset.subject || '';
        const gmail = new URL('https://mail.google.com/mail/');
        gmail.searchParams.set('view', 'cm');
        gmail.searchParams.set('fs', '1');
        gmail.searchParams.set('to', email);
        if (subject) gmail.searchParams.set('su', subject);
        contactDialog.querySelector('[data-gmail]').setAttribute('href', gmail.href);
        contactDialog.querySelector('[data-mail-app]').setAttribute('href', 'mailto:' + email + (subject ? '?subject=' + encodeURIComponent(subject) : ''));
        const subjectLine = contactDialog.querySelector('.contact-subject');
        subjectLine.textContent = (en ? 'Subject: ' : 'Betreff: ') + subject;
        subjectLine.hidden = !subject;
        contactDialog.querySelector('.copy-status').textContent = '';
        contactDialog.showModal();
      });
    });
    contactDialog.querySelector('.dialog-close').addEventListener('click', () => contactDialog.close());
    contactDialog.addEventListener('click', event => {
      if (event.target !== contactDialog) return;
      const rect = contactDialog.getBoundingClientRect();
      if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) contactDialog.close();
    });
    contactDialog.addEventListener('close', () => contactTrigger?.focus());
  }

  document.querySelector('.copy-email')?.addEventListener('click', async event => {
    const email = event.currentTarget.dataset.email;
    const status = document.querySelector('.copy-status');
    try {
      if (!navigator.clipboard?.writeText) throw new Error('Clipboard unavailable');
      await navigator.clipboard.writeText(email);
      status.textContent = en ? 'Email address copied.' : 'E-Mail-Adresse kopiert.';
    } catch {
      status.textContent = (en ? 'Please select and copy: ' : 'Bitte markieren und kopieren: ') + email;
    }
  });

  const language = document.querySelector('.language');
  const sections = [...document.querySelectorAll('main > section[id]')];
  const currentSection = () => {
    if (sections.length && window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 8) return sections.at(-1);
    return sections.filter(section => section.getBoundingClientRect().top <= 150).at(-1);
  };
  if (language) {
    const base = language.getAttribute('href').split('#')[0];
    const syncHash = () => { language.setAttribute('href', base + location.hash); };
    syncHash();
    window.addEventListener('hashchange', syncHash);
    // Scrolling need not change the URL; preserve the visible section on switch.
    language.addEventListener('click', () => {
      if (!sections.length) return;
      const current = currentSection();
      language.setAttribute('href', base + (current?.id && current.id !== 'top' ? '#' + current.id : ''));
    });
  }
  if (nav && sections.length && 'IntersectionObserver' in window) {
    const navLinks = [...nav.querySelectorAll('a')].filter(anchor => new URL(anchor.href, location.href).hash);
    const updateActive = () => {
      const current = currentSection();
      navLinks.forEach(anchor => {
        if (current && new URL(anchor.href, location.href).hash === '#' + current.id) anchor.setAttribute('aria-current', 'location');
        else anchor.removeAttribute('aria-current');
      });
    };
    const observer = new IntersectionObserver(updateActive, { rootMargin: '-80px 0px -60% 0px', threshold: 0 });
    sections.forEach(section => observer.observe(section));
    window.addEventListener('scroll', updateActive, { passive: true });
    updateActive();
  }
})();
