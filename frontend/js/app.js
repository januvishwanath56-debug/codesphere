// ─── Config ───
const API_BASE = window.API_BASE || 'http://localhost:8000';

// ─── Theme ───
const Theme = {
  init() {
    const saved = localStorage.getItem('theme') || 'dark';
    document.documentElement.setAttribute('data-theme', saved);
    this.updateIcon(saved);
  },
  toggle() {
    const current = document.documentElement.getAttribute('data-theme') || 'dark';
    const next = current === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('theme', next);
    this.updateIcon(next);
  },
  updateIcon(theme) {
    const btn = document.getElementById('theme-toggle');
    if (btn) btn.textContent = theme === 'dark' ? '☀️' : '🌙';
  }
};

// ─── Auth ───
const Auth = {
  getToken() { return localStorage.getItem('token'); },
  getUser() {
    const u = localStorage.getItem('user');
    return u ? JSON.parse(u) : null;
  },
  setSession(token, username) {
    localStorage.setItem('token', token);
    localStorage.setItem('user', JSON.stringify({ username }));
  },
  clearSession() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  },
  isLoggedIn() { return !!this.getToken(); },
  updateNav() {
    const user = this.getUser();
    const loginBtn = document.getElementById('nav-login');
    const userMenu = document.getElementById('nav-user');
    const usernameEl = document.getElementById('nav-username');
    if (user) {
      if (loginBtn) loginBtn.style.display = 'none';
      if (userMenu) userMenu.style.display = 'flex';
      if (usernameEl) usernameEl.textContent = user.username;
    } else {
      if (loginBtn) loginBtn.style.display = 'inline-flex';
      if (userMenu) userMenu.style.display = 'none';
    }
  }
};

// ─── API Client ───
const API = {
  async request(method, path, body) {
    const headers = { 'Content-Type': 'application/json' };
    const token = Auth.getToken();
    if (token) headers['Authorization'] = 'Bearer ' + token;
    const opts = { method: method, headers: headers };
    if (body) opts.body = JSON.stringify(body);
    const res = await fetch(API_BASE + path, opts);
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'Request failed');
    return data;
  },
  get(path) { return this.request('GET', path, null); },
  post(path, body) { return this.request('POST', path, body); },
};

// ─── Toast ───
const Toast = {
  container: null,
  init() {
    this.container = document.createElement('div');
    this.container.className = 'toast-container';
    document.body.appendChild(this.container);
  },
  show(msg, type, duration) {
    if (!this.container) this.init();
    duration = duration || 3000;
    const toast = document.createElement('div');
    toast.className = 'toast toast-' + (type || 'info');
    toast.textContent = msg;
    this.container.appendChild(toast);
    setTimeout(function() {
      toast.style.opacity = '0';
      toast.style.transition = 'opacity 0.3s';
      setTimeout(function() { toast.remove(); }, 300);
    }, duration);
  },
  success(msg) { this.show(msg, 'success'); },
  error(msg)   { this.show(msg, 'error'); },
  info(msg)    { this.show(msg, 'info'); },
};

// ─── Auth Modal ───
const AuthModal = {
  currentMode: 'login',

  show(mode) {
    mode = mode || 'login';
    this.currentMode = mode;

    // Remove existing modal if any
    const existing = document.getElementById('auth-modal');
    if (existing) existing.remove();

    const overlay = document.createElement('div');
    overlay.className = 'modal-overlay';
    overlay.id = 'auth-modal';

    const modal = document.createElement('div');
    modal.className = 'modal';

    // Header
    const header = document.createElement('div');
    header.style.cssText = 'display:flex;justify-content:space-between;align-items:center;margin-bottom:1.5rem;';

    const title = document.createElement('h2');
    title.className = 'modal-title';
    title.id = 'auth-title';
    title.style.margin = '0';
    title.textContent = mode === 'login' ? 'Welcome Back' : 'Create Account';

    const closeBtn = document.createElement('button');
    closeBtn.type = 'button';
    closeBtn.style.cssText = 'background:none;border:none;color:var(--text2);cursor:pointer;font-size:1.2rem;';
    closeBtn.textContent = '✕';
    closeBtn.addEventListener('click', function(e) { e.preventDefault(); AuthModal.hide(); });

    header.appendChild(title);
    header.appendChild(closeBtn);

    // Tabs
    const tabs = document.createElement('div');
    tabs.style.cssText = 'display:flex;gap:0.5rem;margin-bottom:1.5rem;';

    const loginTab = document.createElement('button');
    loginTab.type = 'button';
    loginTab.id = 'tab-login';
    loginTab.className = 'btn btn-sm ' + (mode === 'login' ? 'btn-primary' : 'btn-ghost');
    loginTab.textContent = 'Login';
    loginTab.addEventListener('click', function(e) { e.preventDefault(); AuthModal.switchTab('login'); });

    const regTab = document.createElement('button');
    regTab.type = 'button';
    regTab.id = 'tab-register';
    regTab.className = 'btn btn-sm ' + (mode === 'register' ? 'btn-primary' : 'btn-ghost');
    regTab.textContent = 'Register';
    regTab.addEventListener('click', function(e) { e.preventDefault(); AuthModal.switchTab('register'); });

    tabs.appendChild(loginTab);
    tabs.appendChild(regTab);

    const formContainer = document.createElement('div');
    formContainer.id = 'auth-form';

    modal.appendChild(header);
    modal.appendChild(tabs);
    modal.appendChild(formContainer);
    overlay.appendChild(modal);
    document.body.appendChild(overlay);

    overlay.addEventListener('click', function(e) {
      if (e.target === overlay) AuthModal.hide();
    });

    this.renderForm(mode);
  },

  hide() {
    const m = document.getElementById('auth-modal');
    if (m) m.remove();
  },

  switchTab(mode) {
    this.currentMode = mode;
    document.getElementById('auth-title').textContent = mode === 'login' ? 'Welcome Back' : 'Create Account';
    document.getElementById('tab-login').className = 'btn btn-sm ' + (mode === 'login' ? 'btn-primary' : 'btn-ghost');
    document.getElementById('tab-register').className = 'btn btn-sm ' + (mode === 'register' ? 'btn-primary' : 'btn-ghost');
    this.renderForm(mode);
  },

  renderForm(mode) {
    const container = document.getElementById('auth-form');
    container.innerHTML = '';

    const wrap = document.createElement('div');
    wrap.style.cssText = 'display:flex;flex-direction:column;gap:1rem;';

    // Username
    const uGroup = document.createElement('div');
    uGroup.className = 'input-group';
    uGroup.innerHTML = '<label class="input-label">Username</label>';
    const uInput = document.createElement('input');
    uInput.type = 'text';
    uInput.id = 'auth-username';
    uInput.className = 'input';
    uInput.placeholder = 'your_username';
    uGroup.appendChild(uInput);
    wrap.appendChild(uGroup);

    // Email (register only)
    if (mode === 'register') {
      const eGroup = document.createElement('div');
      eGroup.className = 'input-group';
      eGroup.innerHTML = '<label class="input-label">Email</label>';
      const eInput = document.createElement('input');
      eInput.type = 'email';
      eInput.id = 'auth-email';
      eInput.className = 'input';
      eInput.placeholder = 'you@example.com';
      eGroup.appendChild(eInput);
      wrap.appendChild(eGroup);
    }

    // Password
    const pGroup = document.createElement('div');
    pGroup.className = 'input-group';
    pGroup.innerHTML = '<label class="input-label">Password</label>';
    const pInput = document.createElement('input');
    pInput.type = 'password';
    pInput.id = 'auth-password';
    pInput.className = 'input';
    pInput.placeholder = '••••••••';
    pGroup.appendChild(pInput);
    wrap.appendChild(pGroup);

    // Submit button
    const submitBtn = document.createElement('button');
    submitBtn.type = 'button';  // CRITICAL
    submitBtn.className = 'btn btn-primary';
    submitBtn.style.cssText = 'width:100%;justify-content:center;margin-top:0.5rem;';
    submitBtn.textContent = mode === 'login' ? 'Sign In' : 'Create Account';
    submitBtn.addEventListener('click', function(e) {
      e.preventDefault();
      e.stopPropagation();
      if (mode === 'login') AuthModal.doLogin();
      else AuthModal.doRegister();
    });
    wrap.appendChild(submitBtn);

    container.appendChild(wrap);

    // Enter key on inputs
    [uInput, pInput].forEach(function(inp) {
      inp.addEventListener('keydown', function(e) {
        if (e.key === 'Enter') {
          e.preventDefault();
          if (mode === 'login') AuthModal.doLogin();
          else AuthModal.doRegister();
        }
      });
    });

    setTimeout(function() { uInput.focus(); }, 50);
  },

  async doLogin() {
    const username = (document.getElementById('auth-username').value || '').trim();
    const password = document.getElementById('auth-password').value || '';
    if (!username || !password) return Toast.error('Please fill all fields');
    try {
      const data = await API.post('/login', { username: username, password: password });
      Auth.setSession(data.token, data.username);
      AuthModal.hide();
      Toast.success('Welcome back, ' + data.username + '!');
      Auth.updateNav();
      if (window.onAuthSuccess) window.onAuthSuccess();
    } catch (e) {
      Toast.error(e.message);
    }
  },

  async doRegister() {
    const username = (document.getElementById('auth-username').value || '').trim();
    const email    = (document.getElementById('auth-email')    ? document.getElementById('auth-email').value.trim() : '');
    const password = document.getElementById('auth-password').value || '';
    if (!username || !email || !password) return Toast.error('Please fill all fields');
    try {
      const data = await API.post('/register', { username: username, email: email, password: password });
      Auth.setSession(data.token, data.username);
      AuthModal.hide();
      Toast.success('Account created! Welcome, ' + data.username + '!');
      Auth.updateNav();
      if (window.onAuthSuccess) window.onAuthSuccess();
    } catch (e) {
      Toast.error(e.message);
    }
  }
};

// ─── Navbar ───
function renderNavbar(activePage) {
  activePage = activePage || '';
  return '<nav class="navbar">' +
    '<a href="index.html" class="nav-logo">⟨/⟩ CodeSphere</a>' +
    '<ul class="nav-links">' +
      '<li><a href="problems.html" class="' + (activePage === 'problems' ? 'active' : '') + '">Problems</a></li>' +
      '<li><a href="playground.html" class="' + (activePage === 'playground' ? 'active' : '') + '">Playground</a></li>' +
    '</ul>' +
    '<div class="nav-actions">' +
      '<button type="button" class="theme-toggle" id="theme-toggle" title="Toggle theme">☀️</button>' +
      '<button type="button" class="btn btn-ghost btn-sm" id="nav-login">Sign In</button>' +
      '<div id="nav-user" style="display:none;align-items:center;gap:0.5rem;">' +
        '<span style="color:var(--text2);font-size:0.82rem;">👤 <span id="nav-username"></span></span>' +
        '<button type="button" class="btn btn-ghost btn-sm" id="nav-logout">Logout</button>' +
      '</div>' +
    '</div>' +
  '</nav>';
}

function logout() {
  Auth.clearSession();
  Auth.updateNav();
  Toast.info('Logged out');
  if (window.location.pathname.includes('problem-detail')) {
    window.location.href = 'problems.html';
  }
}

// ─── Init on DOM ready ───
document.addEventListener('DOMContentLoaded', function() {
  Theme.init();
  Toast.init();
  Auth.updateNav();

  // Wire navbar buttons AFTER they're injected into DOM
  // Use event delegation on document body so it works regardless of injection timing
  document.body.addEventListener('click', function(e) {
    if (e.target && e.target.id === 'theme-toggle') {
      e.preventDefault();
      Theme.toggle();
    }
    if (e.target && e.target.id === 'nav-login') {
      e.preventDefault();
      AuthModal.show('login');
    }
    if (e.target && e.target.id === 'nav-logout') {
      e.preventDefault();
      logout();
    }
  });
});
