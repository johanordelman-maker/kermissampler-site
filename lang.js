(function () {
  var root = document.documentElement;
  var btnNl = document.getElementById("btn-nl");
  var btnEn = document.getElementById("btn-en");
  if (!btnNl || !btnEn) return;

  function setLang(lang) {
    root.lang = lang === "en" ? "en" : "nl";
    btnNl.setAttribute("aria-pressed", lang === "nl" ? "true" : "false");
    btnEn.setAttribute("aria-pressed", lang === "en" ? "true" : "false");
    try { localStorage.setItem("ks-lang", root.lang); } catch (e) {}
  }

  btnNl.addEventListener("click", function () { setLang("nl"); });
  btnEn.addEventListener("click", function () { setLang("en"); });

  var saved = null;
  try { saved = localStorage.getItem("ks-lang"); } catch (e) {}
  if (saved === "en" || saved === "nl") setLang(saved);
  else setLang("nl");
})();
