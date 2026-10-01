// Run before styles load to restore the visitor's chosen theme without a light flash.
(() => {
  let selected;
  try { selected = window.localStorage.getItem('aa-portfolio-theme'); } catch { /* Storage is optional. */ }
  const theme = selected === 'light' || selected === 'dark'
    ? selected
    : (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  document.documentElement.setAttribute('data-theme', theme);
  document.querySelector('meta[name="theme-color"]')?.setAttribute('content', theme === 'dark' ? '#101923' : '#fafbfc');
})();
