/* nav.js: builds the in-page TOC from h2 headings and adds anchor links. No external dependencies. */
(function () {
  "use strict";
  function slugify(text, used) {
    var base = "s-" + text.trim().toLowerCase()
      .replace(/[^֐-׿a-z0-9]+/g, "-")
      .replace(/^-+|-+$/g, "");
    var slug = base, i = 2;
    while (used[slug]) { slug = base + "-" + i++; }
    used[slug] = true;
    return slug;
  }
  document.addEventListener("DOMContentLoaded", function () {
    var tocHost = document.querySelector("nav.toc[data-auto]");
    var heads = document.querySelectorAll("main h2");
    var used = {};
    heads.forEach(function (h) {
      if (!h.id) { h.id = slugify(h.textContent, used); }
    });
    if (tocHost && heads.length > 1) {
      var ol = document.createElement("ol");
      heads.forEach(function (h) {
        var li = document.createElement("li");
        var a = document.createElement("a");
        a.href = "#" + h.id;
        a.textContent = h.textContent;
        li.appendChild(a);
        ol.appendChild(li);
      });
      var t = document.createElement("div");
      t.className = "toc-title";
      t.textContent = "בפרק הזה";
      tocHost.appendChild(t);
      tocHost.appendChild(ol);
    }
  });
})();
