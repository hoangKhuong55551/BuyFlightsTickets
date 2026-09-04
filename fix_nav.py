with open('templates/partials/navbar.html', 'r', encoding='utf-8') as f:
    nav = f.read()

# Remove the messy append if it exists
nav = nav.replace('@\n<style>', '<style>')
nav = nav.replace('\n@', '')

css = """
<style>
  /* Mobile Support Sheet CSS */
  .mobile-support-backdrop {
    display: none; position: fixed; inset: 0; background: rgba(15, 31, 61, 0.4); 
    backdrop-filter: blur(2px); z-index: 9997; opacity: 0; transition: opacity 0.3s;
  }
  .mobile-support-overlay {
    display: none; /* Hidden by default on desktop */
  }
  
  @media (max-width: 900px) {
    .mobile-support-overlay {
      display: flex; position: fixed; bottom: 0; left: 0; right: 0; 
      background: white; border-top-left-radius: 24px; border-top-right-radius: 24px; 
      box-shadow: 0 -10px 40px rgba(0,0,0,0.15); z-index: 9998; 
      padding: 16px 20px 32px; flex-direction: column; gap: 8px; 
      transform: translateY(100%); transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
      padding-bottom: calc(32px + env(safe-area-inset-bottom));
    }
  }
  .mobile-support-handle {
    width: 40px; height: 5px; background: #cbd5e1; border-radius: 99px; margin: 0 auto 16px;
  }
  .mobile-support-item {
    display: flex; align-items: center; gap: 16px; padding: 14px 16px;
    background: #f8fafc; border-radius: 16px; border: 1px solid #f1f5f9;
    text-decoration: none !important; transition: background 0.2s;
  }
  .mobile-support-item:active { background: #e2e8f0; }
  .msi-icon {
    width: 40px; height: 40px; border-radius: 12px; background: white;
    display: flex; align-items: center; justify-content: center; color: #00B4D8;
    box-shadow: 0 4px 10px rgba(0,0,0,0.04); flex-shrink: 0;
  }
  .msi-text { display: flex; flex-direction: column; line-height: 1.3; }
  .msi-text strong { color: var(--navy-900); font-size: 0.95rem; font-weight: 700; }
  .msi-text span { color: #64748b; font-size: 0.75rem; }
  
  /* Show state */
  body.show-mobile-support { overflow: hidden; }
  body.show-mobile-support .mobile-support-backdrop { display: block; opacity: 1; }
  body.show-mobile-support .mobile-support-overlay { transform: translateY(0); }
</style>
"""

if '.mobile-support-overlay {' not in nav:
    nav += css

with open('templates/partials/navbar.html', 'w', encoding='utf-8') as f:
    f.write(nav)
