/* book.js — reader interactivity (BCS v1.1 §D). Dependency-free, progressive
 * enhancement: everything works with JS off; the WeasyPrint PDF never relies on
 * this (print CSS force-opens solutions). Loads only on .reader pages. */
(function () {
  "use strict";
  var reader = document.querySelector(".reader");
  if (!reader) return; // non-reader page

  var toc = document.getElementById("book-toc");
  var tocLinks = toc ? Array.prototype.slice.call(toc.querySelectorAll("a[href^='#']")) : [];
  var units = Array.prototype.slice.call(reader.querySelectorAll(".unit, .opener, [id]")).filter(function (el) {
    return el.id;
  });
  var crumbCurrent = document.querySelector(".book-bar__crumbs .current");
  var progress = document.querySelector(".book-progress");
  var solutions = Array.prototype.slice.call(reader.querySelectorAll("details.solution"));

  // ---- cross-browser MediaQueryList listener ----
  function onMedia(mq, fn) {
    if (mq.addEventListener) mq.addEventListener("change", fn);
    else if (mq.addListener) mq.addListener(fn); // old Safari
  }

  // ---- scrollspy: exactly one .active ----
  var byId = {};
  tocLinks.forEach(function (a) {
    var id = decodeURIComponent(a.getAttribute("href").slice(1));
    byId[id] = a;
  });
  var activeId = null;
  function setActive(id) {
    if (id === activeId || !byId[id]) return;
    tocLinks.forEach(function (a) {
      a.classList.remove("active");
      a.removeAttribute("aria-current");
    });
    var link = byId[id];
    link.classList.add("active");
    link.setAttribute("aria-current", "true");
    activeId = id;
    if (crumbCurrent && link.dataset.crumbs) crumbCurrent.textContent = link.dataset.crumbs;
  }

  if ("IntersectionObserver" in window && tocLinks.length) {
    var io = new IntersectionObserver(
      function (entries) {
        // pick the topmost intersecting element with a TOC entry
        var best = null;
        entries.forEach(function (e) {
          if (e.isIntersecting && byId[e.target.id]) {
            if (!best || e.boundingClientRect.top < best.boundingClientRect.top) best = e;
          }
        });
        if (best) setActive(best.target.id);
        updateProgress();
      },
      { rootMargin: "-10% 0px -80% 0px", threshold: 0 }
    );
    units.forEach(function (u) {
      if (byId[u.id]) io.observe(u);
    });
  }

  // ---- reading progress rule (rAF-throttled) ----
  var ticking = false;
  function updateProgress() {
    if (!progress) return;
    var doc = document.documentElement;
    var scrollable = doc.scrollHeight - doc.clientHeight;
    var pct = scrollable > 0 ? (doc.scrollTop / scrollable) * 100 : 0;
    progress.style.width = Math.max(0, Math.min(100, pct)) + "%";
  }
  window.addEventListener(
    "scroll",
    function () {
      if (!ticking) {
        window.requestAnimationFrame(function () {
          updateProgress();
          ticking = false;
        });
        ticking = true;
      }
    },
    { passive: true }
  );
  updateProgress();

  // ---- unit-level prev/next (wraps across sections) ----
  var prevA = document.querySelector(".book-prev");
  var nextA = document.querySelector(".book-next");
  var navUnits = units.filter(function (u) {
    return byId[u.id];
  });
  function currentUnitIndex() {
    var y = document.documentElement.scrollTop + window.innerHeight * 0.2;
    var idx = 0;
    for (var i = 0; i < navUnits.length; i++) {
      if (navUnits[i].offsetTop <= y) idx = i;
    }
    return idx;
  }
  function wireNav() {
    if (!prevA || !nextA || !navUnits.length) return;
    function go(delta) {
      var i = currentUnitIndex() + delta;
      if (i < 0) i = 0;
      if (i > navUnits.length - 1) i = navUnits.length - 1;
      navUnits[i].scrollIntoView({ behavior: "smooth", block: "start" });
      setActive(navUnits[i].id);
      updateProgress();
    }
    prevA.addEventListener("click", function (e) {
      e.preventDefault();
      go(-1);
    });
    nextA.addEventListener("click", function (e) {
      e.preventDefault();
      go(1);
    });
    // disabled state at the ends
    function refreshEnds() {
      var i = currentUnitIndex();
      prevA.setAttribute("aria-disabled", i <= 0 ? "true" : "false");
      nextA.setAttribute("aria-disabled", i >= navUnits.length - 1 ? "true" : "false");
    }
    window.addEventListener("scroll", refreshEnds, { passive: true });
    refreshEnds();
  }
  wireNav();

  // ---- off-canvas TOC drawer < 992px ----
  var toggle = document.querySelector(".book-toc-toggle");
  var mqNarrow = window.matchMedia("(max-width: 991px)");
  if (toggle && toc) {
    toggle.addEventListener("click", function () {
      var open = toc.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    // close after choosing a destination on narrow screens
    tocLinks.forEach(function (a) {
      a.addEventListener("click", function () {
        if (mqNarrow.matches) {
          toc.classList.remove("open");
          toggle.setAttribute("aria-expanded", "false");
        }
      });
    });
  }

  // ---- expand / collapse all solutions (button injected into book-bar) ----
  if (solutions.length) {
    var navWrap = document.querySelector(".book-bar__nav");
    if (navWrap) {
      var toggleAll = document.createElement("a");
      toggleAll.href = "#";
      toggleAll.className = "book-expand-all";
      toggleAll.textContent = "Expand all";
      navWrap.insertBefore(toggleAll, navWrap.firstChild);
      toggleAll.addEventListener("click", function (e) {
        e.preventDefault();
        var anyClosed = solutions.some(function (d) {
          return !d.open;
        });
        solutions.forEach(function (d) {
          d.open = anyClosed;
        });
        toggleAll.textContent = anyClosed ? "Collapse all" : "Expand all";
      });
    }
  }

  // ---- force-open a #q-n-solution deep link (on load + before print) ----
  function openTargetSolution() {
    var h = decodeURIComponent(location.hash.slice(1));
    if (!h) return;
    var el = document.getElementById(h);
    if (el && el.tagName === "DETAILS") el.open = true;
    // also open a solution whose question is the target
    var sol = document.getElementById(h + "-solution");
    if (sol && sol.tagName === "DETAILS") sol.open = true;
  }
  openTargetSolution();
  window.addEventListener("hashchange", openTargetSolution);

  // browser "Save as PDF": open all, restore after (double-fire guarded)
  var printState = null;
  function beforePrint() {
    if (printState) return;
    printState = solutions.map(function (d) {
      return d.open;
    });
    solutions.forEach(function (d) {
      d.open = true;
    });
  }
  function afterPrint() {
    if (!printState) return;
    solutions.forEach(function (d, i) {
      d.open = printState[i];
    });
    printState = null;
  }
  window.addEventListener("beforeprint", beforePrint);
  window.addEventListener("afterprint", afterPrint);
  var mqPrint = window.matchMedia("print");
  onMedia(mqPrint, function (mq) {
    if (mq.matches) beforePrint();
    else afterPrint();
  });
})();
