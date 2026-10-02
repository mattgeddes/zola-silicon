/* zola-biz — progressive enhancement only. Every feature here has a working
   no-JS fallback, so the site is fully usable if this file fails to load. */
(function () {
  "use strict";

  var root = document.documentElement;

  /* ---------------------------------------------------------------------
     Colour theme
     Stores an explicit choice only. With nothing stored, the CSS media query
     follows the operating system, which is what most visitors expect.
     --------------------------------------------------------------------- */
  var STORAGE_KEY = "theme";

  function currentTheme() {
    if (root.dataset.theme) return root.dataset.theme;
    return window.matchMedia("(prefers-color-scheme: dark)").matches
      ? "dark"
      : "light";
  }

  var toggle = document.getElementById("theme-toggle");
  if (toggle) {
    var syncLabel = function () {
      var next = currentTheme() === "dark" ? "light" : "dark";
      var text = "Switch to " + next + " theme";
      toggle.setAttribute("aria-label", text);
      toggle.setAttribute("title", text);
    };

    toggle.addEventListener("click", function () {
      var next = currentTheme() === "dark" ? "light" : "dark";
      root.dataset.theme = next;
      try {
        localStorage.setItem(STORAGE_KEY, next);
      } catch (e) {
        /* private mode: the choice still applies for this page view */
      }
      syncLabel();
    });

    /* Follow OS changes, but only while the visitor has no stored preference. */
    if (window.matchMedia) {
      var mq = window.matchMedia("(prefers-color-scheme: dark)");
      var onChange = function () {
        if (!root.dataset.theme) syncLabel();
      };
      if (mq.addEventListener) mq.addEventListener("change", onChange);
      else if (mq.addListener) mq.addListener(onChange);
    }

    syncLabel();
  }

  /* ---------------------------------------------------------------------
     Mobile navigation
     --------------------------------------------------------------------- */
  var navButton = document.getElementById("nav-toggle");
  var nav = document.getElementById("site-nav");

  if (navButton && nav) {
    var setNav = function (open) {
      nav.dataset.open = open ? "true" : "false";
      navButton.setAttribute("aria-expanded", open ? "true" : "false");
    };

    navButton.addEventListener("click", function () {
      setNav(nav.dataset.open !== "true");
    });

    /* Escape closes the menu and returns focus to the button. */
    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && nav.dataset.open === "true") {
        setNav(false);
        navButton.focus();
      }
    });

    /* Following a link should close the menu before the page navigates. */
    nav.addEventListener("click", function (event) {
      if (event.target.closest("a") && nav.dataset.open === "true") {
        setNav(false);
      }
    });

    var desktop = window.matchMedia("(min-width: 62em)");
    var onBreakpoint = function () {
      if (desktop.matches) setNav(false);
    };
    if (desktop.addEventListener) desktop.addEventListener("change", onBreakpoint);
    else if (desktop.addListener) desktop.addListener(onBreakpoint);
  }

  /* ---------------------------------------------------------------------
     Header shadow once the page has scrolled
     --------------------------------------------------------------------- */
  var header = document.getElementById("site-header");
  if (header) {
    var ticking = false;
    var updateHeader = function () {
      header.dataset.scrolled = window.scrollY > 8 ? "true" : "false";
      ticking = false;
    };
    window.addEventListener(
      "scroll",
      function () {
        if (!ticking) {
          ticking = true;
          window.requestAnimationFrame(updateHeader);
        }
      },
      { passive: true }
    );
    updateHeader();
  }

  /* ---------------------------------------------------------------------
     Newsletter form — demo only
     There is no backend in a static site. This keeps the visitor on the page
     and explains what to do next, rather than posting nowhere.
     Wire it to your provider (or set the form's action) before going live.
     --------------------------------------------------------------------- */
  var forms = document.querySelectorAll("[data-newsletter]");
  Array.prototype.forEach.call(forms, function (form) {
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      var note = form.querySelector("[data-newsletter-note]");
      var field = form.querySelector('input[type="email"]');
      if (!note) return;
      if (!field || !field.value) {
        note.textContent = "Please enter your email address.";
        return;
      }
      note.textContent = "This is a demo form — point it at your mailing list provider.";
      form.reset();
    });
  });
})();