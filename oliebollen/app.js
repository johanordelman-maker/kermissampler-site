/* De Oliebollen Bakkerij — klantenapp (klikbaar ontwerp v2.0)
   Alles lokaal in localStorage. Geen server, geen tracking. */
(function () {
  "use strict";
  const KEY = "oliebollen-app-v2";
  const PIN = "1234";                 // demo-pin; echte versie: per medewerker, op de server
  const PUNTEN_PER_EURO = 10;
  const WELKOMSTBONUS = 50;
  const TZ = "Europe/Amsterdam";

  /* ---------- voorbeelddata ---------- */
  const TIJDEN = [ // 0 = zondag (voorbeeld)
    ["Zondag", "11:00", "20:00"], ["Maandag", "11:00", "20:00"], ["Dinsdag", "11:00", "20:00"],
    ["Woensdag", "11:00", "20:00"], ["Donderdag", "11:00", "20:00"], ["Vrijdag", "11:00", "21:00"], ["Zaterdag", "11:00", "21:00"]
  ];
  const MENU = [
    { cat: "Oliebollen", items: [
      { id: "ob1", naam: "Oliebol naturel", sub: "Per stuk, met poedersuiker", prijs: 1.50, ill: "bol" },
      { id: "ob5", naam: "Zak van 5 oliebollen", sub: "Naturel", prijs: 6.50, ill: "zak" },
      { id: "ob10", naam: "Zak van 10 oliebollen", sub: "Naturel, de favoriet", prijs: 12.00, ill: "zak" },
      { id: "obap", naam: "Oliebol appel-rozijn", sub: "Met stukjes appel", prijs: 1.95, ill: "krent" }
    ]},
    { cat: "Krentenbollen", items: [
      { id: "kb1", naam: "Krentenbol", sub: "Per stuk, rijk gevuld", prijs: 1.75, ill: "krent" },
      { id: "kb10", naam: "Zak van 10 krentenbollen", sub: "Met krenten en rozijnen", prijs: 13.50, ill: "zak" }
    ]},
    { cat: "Appelflappen", items: [
      { id: "af1", naam: "Appelflap", sub: "Bladerdeeg, appel en kaneel", prijs: 2.25, ill: "flap" },
      { id: "abg", naam: "Appelbeignet", sub: "Appelschijf in beslag", prijs: 2.25, ill: "beignet" }
    ]},
    { cat: "Berlinerbollen", items: [
      { id: "bb1", naam: "Berlinerbol slagroom", sub: "Gevuld met verse slagroom", prijs: 2.75, ill: "berliner" },
      { id: "bb2", naam: "Berlinerbol vanille", sub: "Gevuld met vanillecrème", prijs: 2.75, ill: "berliner" }
    ]},
    { cat: "Drinken", items: [
      { id: "kof", naam: "Koffie", sub: "Vers gezet", prijs: 2.50, ill: "beker" },
      { id: "cho", naam: "Warme chocolademelk", sub: "Met of zonder slagroom", prijs: 2.75, ill: "beker" }
    ]}
  ];
  const BELONINGEN = [
    { id: "r-bol", titel: "Gratis oliebol", punten: 100, ill: "bol" },
    { id: "r-kof", titel: "Gratis koffie", punten: 120, ill: "beker" },
    { id: "r-flap", titel: "Gratis appelflap", punten: 150, ill: "flap" },
    { id: "r-ber", titel: "Gratis berlinerbol", punten: 180, ill: "berliner" },
    { id: "r-zak", titel: "Gratis zak van 5 oliebollen", punten: 450, ill: "zak" }
  ];
  function eindeWeek() {
    const d = new Date(); const dag = d.getDay(); d.setDate(d.getDate() + ((7 - dag) % 7));
    return isoDag(d);
  }
  function voorbeeldActies() {
    return [
      { id: "a-week", titel: "10 oliebollen + gratis appelflap", tekst: "Koop een zak van 10 en krijg er een appelflap bij. Alleen met de app.", tot: eindeWeek(), ill: "zak", voorbeeld: true, hero: true },
      { id: "a-kof", titel: "Koffie voor € 1", tekst: "Bij elke zak van 5 of 10 oliebollen.", tot: eindeWeek(), ill: "beker", voorbeeld: true },
      { id: "a-ber", titel: "2e berlinerbol halve prijs", tekst: "Neem er twee, de tweede is voor de helft.", tot: eindeWeek(), ill: "berliner", voorbeeld: true },
      { id: "a-oud", titel: "Oudjaar zonder rij", tekst: "Laat je bestelling klaarzetten via Menu en haal hem op zonder wachten.", tot: new Date().getFullYear() + "-12-31", ill: "bol", voorbeeld: true }
    ];
  }

  /* ---------- hulpjes ---------- */
  function isoDag(d) { return d.toLocaleDateString("en-CA", { timeZone: TZ }); }
  function nu() { // uur, minuut en weekdag in Amsterdam
    const p = new Intl.DateTimeFormat("en-GB", { timeZone: TZ, hour: "2-digit", minute: "2-digit", weekday: "short", hourCycle: "h23" }).formatToParts(new Date());
    const g = (t) => p.find((x) => x.type === t).value;
    const wd = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"].indexOf(g("weekday"));
    return { u: +g("hour"), m: +g("minute"), wd };
  }
  const $ = (id) => document.getElementById(id);
  function esc(s) { return String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c])); }
  function euro(n) { return "€ " + n.toFixed(2).replace(".", ","); }
  function rnd(n) { const b = new Uint32Array(1); crypto.getRandomValues(b); return b[0] % n; }
  function cijfers(k) { let s = ""; for (let i = 0; i < k; i++) s += rnd(10); return s; }
  function datumNL(iso) { return new Date(iso + "T12:00:00").toLocaleDateString("nl-NL", { weekday: "short", day: "numeric", month: "long" }); }
  function minuten(t) { const [h, m] = t.split(":").map(Number); return h * 60 + m; }

  /* ---------- opslag ---------- */
  function nieuw() {
    return {
      klant: { id: "OB-" + cijfers(4) + "-" + cijfers(4), naam: "", punten: 0, totaal: 0, eersteScan: false },
      codes: [], acties: voorbeeldActies(), mand: {}, meldingen: false,
      kraam: { dag: isoDag(new Date()), punten: 0, ingewisseld: 0 }
    };
  }
  function laad() {
    try {
      const o = JSON.parse(localStorage.getItem(KEY) || "null");
      if (o && o.klant && o.klant.id) {
        // voorbeeldacties steeds verversen (datums lopen mee), eigen acties houden
        const eigen = (o.acties || []).filter((a) => !a.voorbeeld);
        o.acties = eigen.concat(voorbeeldActies());
        if (o.kraam.dag !== isoDag(new Date())) o.kraam = { dag: isoDag(new Date()), punten: 0, ingewisseld: 0 };
        o.mand = o.mand || {};
        return o;
      }
    } catch (e) { /* kapotte opslag: opnieuw beginnen */ }
    return nieuw();
  }
  let data = laad();
  function bewaar() { try { localStorage.setItem(KEY, JSON.stringify(data)); } catch (e) {} }
  bewaar();

  /* ---------- illustraties (eigen SVG) ---------- */
  let gid = 0;
  function ill(soort, px) {
    const g = "g" + (++gid);
    const size = px || 56;
    const bolGrad = `<radialGradient id="${g}" cx="36%" cy="30%" r="72%"><stop offset="0" stop-color="#F7DFA3"/><stop offset=".45" stop-color="#C97B2A"/><stop offset="1" stop-color="#6E3510"/></radialGradient>`;
    const suiker = `<g fill="#FFFDF6" opacity=".95"><circle cx="38" cy="32" r="2.4"/><circle cx="47" cy="28" r="2"/><circle cx="56" cy="31" r="2.6"/><circle cx="62" cy="38" r="1.8"/><circle cx="43" cy="40" r="1.6"/><circle cx="52" cy="38" r="2"/><circle cx="34" cy="42" r="1.8"/></g>`;
    let body = "";
    if (soort === "bol") body = `<circle cx="50" cy="54" r="34" fill="url(#${g})"/>${suiker}`;
    else if (soort === "krent") body = `<circle cx="50" cy="54" r="34" fill="url(#${g})"/><g fill="#3A1A0C"><ellipse cx="38" cy="58" rx="3.4" ry="2.4"/><ellipse cx="58" cy="64" rx="3" ry="2.2"/><ellipse cx="62" cy="50" rx="3" ry="2"/><ellipse cx="46" cy="72" rx="2.8" ry="2"/><ellipse cx="32" cy="70" rx="2.6" ry="1.8"/></g>${suiker}`;
    else if (soort === "berliner") body = `<ellipse cx="50" cy="56" rx="38" ry="30" fill="url(#${g})"/><path d="M14 56c10 7 62 7 72 0v6c-10 8-62 8-72 0z" fill="#FFF6E4"/><circle cx="50" cy="60" r="4" fill="#C0392B"/><g fill="#FFFDF6"><circle cx="40" cy="38" r="2"/><circle cx="55" cy="35" r="2.3"/><circle cx="64" cy="42" r="1.7"/></g>`;
    else if (soort === "flap") body = `<path d="M12 74 50 16 88 74q-38 12-76 0z" fill="url(#${g})" stroke="#8a4a15" stroke-width="2" stroke-linejoin="round"/><path d="M32 58h36M38 48h24" stroke="#F7DFA3" stroke-width="3" stroke-linecap="round" opacity=".8"/><g fill="#FFFDF6"><circle cx="46" cy="36" r="2"/><circle cx="56" cy="44" r="2.2"/><circle cx="40" cy="62" r="1.8"/></g>`;
    else if (soort === "beignet") body = `<circle cx="50" cy="54" r="34" fill="url(#${g})"/><circle cx="50" cy="54" r="12" fill="#F3E4C6"/><circle cx="50" cy="54" r="12" fill="none" stroke="#9c5a1c" stroke-width="2"/><g fill="#FFFDF6"><circle cx="34" cy="40" r="2"/><circle cx="64" cy="38" r="2.4"/><circle cx="70" cy="62" r="1.8"/></g>`;
    else if (soort === "beker") body = `<path d="M26 30h44l-5 54H31z" fill="#FFF8EA" stroke="#6B1523" stroke-width="3" stroke-linejoin="round"/><rect x="24" y="24" width="48" height="9" rx="3" fill="#6B1523"/><rect x="29" y="48" width="38" height="16" fill="#C9A227"/><path d="M42 18c0-5 6-5 6-10M52 18c0-5 6-5 6-10" stroke="#a37b68" stroke-width="2.5" fill="none" stroke-linecap="round"/>`;
    else if (soort === "zak") body = `<path d="M22 34h56l-6 54H28z" fill="#E9CC93" stroke="#a5793a" stroke-width="2"/><path d="M22 34l6-8h44l6 8" fill="#d9b878" stroke="#a5793a" stroke-width="2"/><circle cx="38" cy="30" r="13" fill="url(#${g})"/><circle cx="60" cy="28" r="14" fill="url(#${g})"/><circle cx="49" cy="22" r="12" fill="url(#${g})"/><rect x="34" y="54" width="32" height="16" rx="3" fill="#6B1523"/><text x="50" y="66" font-size="10" font-family="Georgia,serif" text-anchor="middle" fill="#E8D08A">vers</text>`;
    return `<svg viewBox="0 0 100 100" width="${size}" height="${size}" aria-hidden="true"><defs>${bolGrad}</defs>${body}</svg>`;
  }

  /* ---------- QR ---------- */
  function qrSvg(tekst) {
    const q = qrcode(0, "M"); q.addData(tekst); q.make();
    return q.createSvgTag({ cellSize: 4, margin: 0, scalable: true });
  }

  /* ---------- navigatie ---------- */
  const SCHERMEN = ["home", "sparen", "acties", "menu", "meer"];
  function toon(naam) {
    if (!SCHERMEN.includes(naam)) naam = "home";
    SCHERMEN.forEach((s) => $("s-" + s).classList.toggle("aan", s === naam));
    document.querySelectorAll("#tabbalk button").forEach((b) => {
      if (b.dataset.naar === naam) b.setAttribute("aria-current", "page"); else b.removeAttribute("aria-current");
    });
    $("mand-balk").hidden = naam !== "menu" || mandAantal() === 0;
    window.scrollTo(0, 0);
    if (location.hash !== "#" + naam) history.replaceState(null, "", "#" + naam);
    teken();
  }
  document.addEventListener("click", (e) => {
    const n = e.target.closest("[data-naar]");
    if (n) { toon(n.dataset.naar); return; }
    const s = e.target.closest("[data-sluit]");
    if (s) sluitVenster(s.closest(".venster"));
  });
  window.addEventListener("hashchange", () => toon(location.hash.slice(1)));

  function openVenster(id) { $(id).classList.add("aan"); }
  function sluitVenster(v) { if (v) v.classList.remove("aan"); if (v && v.id === "v-code") teken(); }
  document.querySelectorAll(".venster").forEach((v) => v.addEventListener("click", (e) => { if (e.target === v) sluitVenster(v); }));
  document.addEventListener("keydown", (e) => {
    if (e.key !== "Escape") return;
    const open = document.querySelector(".venster.aan");
    if (open) sluitVenster(open); else if ($("kraam").classList.contains("aan")) kraamUit();
  });

  function toast(t) {
    const el = $("toast"); el.textContent = t; el.classList.add("aan");
    clearTimeout(toast.t); toast.t = setTimeout(() => el.classList.remove("aan"), 2400);
  }

  /* ---------- open / dicht ---------- */
  function openStatus() {
    const n = nu(); const [, van, tot] = TIJDEN[n.wd]; const m = n.u * 60 + n.m;
    if (m >= minuten(van) && m < minuten(tot)) return { open: true, tekst: "Nu open tot " + tot };
    if (m < minuten(van)) return { open: false, tekst: "Gesloten · vandaag open om " + van };
    const morgen = TIJDEN[(n.wd + 1) % 7];
    return { open: false, tekst: "Gesloten · morgen open om " + morgen[1] };
  }

  /* ---------- codes ---------- */
  function maakCode(prefix) {
    let c; do { c = prefix + "-" + cijfers(4); } while (data.codes.some((x) => x.code === c));
    return c;
  }
  function toonCode(c) {
    const soort = { beloning: "Beloning", actie: "Actie", bestelling: "Klaarzetten" }[c.soort];
    $("vc-soort").textContent = soort;
    $("vc-titel").textContent = c.titel;
    $("vc-sub").textContent = c.soort === "bestelling"
      ? c.regels.map((r) => r.n + "× " + r.naam).join(", ") + " · ophalen " + c.tijd
      : "Laat deze code scannen of zien bij de kraam.";
    $("vc-qr").innerHTML = qrSvg("OLIEBOL:" + c.code);
    $("vc-code").textContent = c.code;
    $("vc-geldig").textContent = c.status === "gebruikt" ? "Al gebruikt" : "Geldig t/m " + datumNL(c.tot);
    openVenster("v-code");
  }

  /* ---------- tekenen ---------- */
  function volgendeBeloning() {
    const p = data.klant.punten;
    return BELONINGEN.find((b) => b.punten > p) || null;
  }
  function geldigeActies() {
    const vandaag = isoDag(new Date());
    return data.acties.filter((a) => a.tot >= vandaag);
  }
  function actieCode(a) { return data.codes.find((c) => c.soort === "actie" && c.ref === a.id); }

  function teken() {
    const k = data.klant, n = nu();
    const uur = n.u;
    const groet = uur < 12 ? "Goedemorgen" : uur < 18 ? "Goedemiddag" : "Goedenavond";
    $("groet").textContent = groet + (k.naam ? ", " + k.naam : "") + "!";
    const st = openStatus();
    $("open-chip").textContent = st.open ? "Open" : "Gesloten";
    $("open-chip").classList.toggle("dicht", !st.open);
    $("meer-status").textContent = st.tekst + " (voorbeeldtijden)";

    // hero
    const hero = geldigeActies().find((a) => a.hero) || geldigeActies()[0];
    if (hero) {
      $("hero").hidden = false;
      $("hero-titel").textContent = hero.titel;
      $("hero-sub").textContent = hero.tekst;
      $("hero-beeld").innerHTML = ill(hero.ill || "bol", 190);
      const hc = actieCode(hero);
      $("hero-knop").textContent = hc ? (hc.status === "gebruikt" ? "Gebruikt" : "Toon mijn code") : "Activeer actie";
      $("hero-knop").onclick = () => activeer(hero);
    } else $("hero").hidden = true;

    // spaarstand
    $("home-punten").textContent = k.punten;
    const vb = volgendeBeloning();
    const vorige = BELONINGEN.filter((b) => b.punten <= k.punten).pop();
    if (vb) {
      const basis = vorige ? vorige.punten : 0;
      $("home-balk").style.width = Math.max(3, Math.round(((k.punten - basis) / (vb.punten - basis)) * 100)) + "%";
      $("home-volgende").textContent = (vorige ? "Je kunt al een " + vorige.titel.toLowerCase().replace("gratis ", "gratis ") + " halen! " : "") +
        "Nog " + (vb.punten - k.punten) + " punten tot " + vb.titel.toLowerCase();
    } else { $("home-balk").style.width = "100%"; $("home-volgende").textContent = "Je kunt alles inwisselen. Smullen!"; }

    // home deals
    $("home-deals").innerHTML = geldigeActies().map((a) => {
      const c = actieCode(a);
      return `<button type="button" class="deal-mini" data-actie="${esc(a.id)}">
        <div class="beeld">${ill(a.ill || "bol", 78)}</div>
        <b>${esc(a.titel)}</b><small>t/m ${esc(datumNL(a.tot))}</small>
        ${c ? `<span class="badge${c.status === "gebruikt" ? " grijs" : ""}">${c.status === "gebruikt" ? "Gebruikt" : "Geactiveerd"}</span>` : a.voorbeeld ? `<span class="chip-vb" style="align-self:flex-start">Voorbeeld</span>` : ""}
      </button>`;
    }).join("");
    $("home-menu").innerHTML = MENU.flatMap((c) => c.items.slice(0, 1)).concat([MENU[0].items[2]]).map((i) =>
      `<button type="button" class="prod-mini" data-naar="menu">${ill(i.ill, 64)}<b>${esc(i.naam)}</b><small>${euro(i.prijs)} · vb.</small></button>`).join("");

    // sparen
    $("klantcode").textContent = k.id;
    if (!$("klant-qr").dataset.voor || $("klant-qr").dataset.voor !== k.id) {
      $("klant-qr").innerHTML = qrSvg("OLIEBOL:" + k.id); $("klant-qr").dataset.voor = k.id;
    }
    $("spaar-punten").textContent = k.punten;
    $("spaar-totaal").textContent = "Totaal gespaard: " + k.totaal + " punten · " + PUNTEN_PER_EURO + " punten per euro";
    $("beloningen").innerHTML = BELONINGEN.map((b) => {
      const kan = k.punten >= b.punten;
      return `<div class="item"><div class="ill">${ill(b.ill, 52)}</div>
        <div class="tx"><b>${esc(b.titel)}</b><small><span class="prijs-pt">${b.punten} punten</span>${kan ? "" : " · nog " + (b.punten - k.punten)}</small></div>
        <button type="button" class="knop knop-klein" data-beloning="${b.id}" ${kan ? "" : "disabled"}>Inwisselen</button></div>`;
    }).join("");
    const mijn = data.codes.filter((c) => c.soort !== "actie").slice().reverse();
    $("mijn-codes").innerHTML = mijn.length ? mijn.map((c) =>
      `<div class="item${c.status === "gebruikt" ? " gebruikt" : ""}"><div class="tx"><b>${esc(c.titel)}</b>
        <small>${esc(c.code)} · ${c.status === "gebruikt" ? "gebruikt" : "nog te gebruiken"}</small></div>
        ${c.status === "open" ? `<button type="button" class="knop knop-klein" data-toon="${esc(c.code)}">Toon</button>` : ""}</div>`).join("")
      : `<p class="leeg">Nog geen codes. Wissel punten in of laat iets klaarzetten.</p>`;

    // acties
    const acties = geldigeActies();
    $("actie-lijst").innerHTML = acties.length ? acties.map((a) => {
      const c = actieCode(a);
      const knop = c ? (c.status === "gebruikt" ? `<button class="knop" disabled>Gebruikt</button>` : `<button type="button" class="knop" data-actie="${esc(a.id)}">Toon mijn code</button>`)
        : `<button type="button" class="knop" data-actie="${esc(a.id)}">Activeer</button>`;
      return `<article class="actie"><div class="band">${a.voorbeeld ? `<span class="label-goud">Voorbeeld</span>` : `<span class="label-goud">Nieuw</span>`}${ill(a.ill || "bol", 110)}</div>
        <div class="lijf"><h3>${esc(a.titel)}</h3><p>${esc(a.tekst)}</p><p class="klein">Geldig t/m ${esc(datumNL(a.tot))}</p>
        ${c && c.status === "open" ? `<span class="badge">Geactiveerd · ${esc(c.code)}</span>` : ""}${knop}</div></article>`;
    }).join("") : `<p class="leeg">Er lopen nu geen acties.</p>`;

    // menu
    if (!$("menu-chips").children.length) {
      $("menu-chips").innerHTML = MENU.map((c, i) => `<button type="button" data-cat="cat-${i}" class="${i === 0 ? "aan" : ""}">${esc(c.cat)}</button>`).join("");
    }
    $("menu-lijst").innerHTML = MENU.map((c, i) => `<h2 class="cat-kop" id="cat-${i}">${esc(c.cat)}</h2><div class="lijst">` +
      c.items.map((it) => {
        const n = data.mand[it.id] || 0;
        return `<div class="item"><div class="ill">${ill(it.ill, 56)}</div><div class="tx"><b>${esc(it.naam)}</b><small>${esc(it.sub)}</small>
          <span class="prijs">${euro(it.prijs)}</span> <span class="chip-vb">vb.</span></div>
          <div class="teller-rij">${n ? `<button type="button" class="min" data-min="${it.id}" aria-label="Eén minder">−</button><span class="aantal">${n}</span>` : ""}
          <button type="button" class="plus" data-plus="${it.id}" aria-label="${esc(it.naam)} toevoegen">+</button></div></div>`;
      }).join("") + `</div>`).join("");
    const aantal = mandAantal();
    $("mand-aantal").textContent = aantal + (aantal === 1 ? " artikel" : " artikelen");
    $("mand-totaal").textContent = euro(mandSom());
    $("mand-balk").hidden = !$("s-menu").classList.contains("aan") || aantal === 0;

    // meer
    $("tijden").innerHTML = [1, 2, 3, 4, 5, 6, 0].map((d) => `<li class="${d === n.wd ? "vandaag" : ""}"><span>${TIJDEN[d][0]}</span><span>${TIJDEN[d][1]} – ${TIJDEN[d][2]}</span></li>`).join("");
    $("set-meldingen").checked = !!data.meldingen;
    if (document.activeElement !== $("set-naam")) $("set-naam").value = k.naam;
  }

  /* ---------- acties en beloningen (klant) ---------- */
  function activeer(a) {
    let c = actieCode(a);
    if (!c) {
      c = { code: maakCode("A"), soort: "actie", ref: a.id, titel: a.titel, tot: a.tot, status: "open", gemaakt: Date.now() };
      data.codes.push(c); bewaar(); toast("Actie geactiveerd");
    }
    toonCode(c);
  }
  function wisselIn(id) {
    const b = BELONINGEN.find((x) => x.id === id);
    if (!b || data.klant.punten < b.punten) return;
    if (!confirm(b.titel + " inwisselen voor " + b.punten + " punten?")) return;
    data.klant.punten -= b.punten;
    const t = new Date(); t.setDate(t.getDate() + 30);
    const c = { code: maakCode("B"), soort: "beloning", ref: b.id, titel: b.titel, punten: b.punten, tot: isoDag(t), status: "open", gemaakt: Date.now() };
    data.codes.push(c); bewaar(); toonCode(c);
  }
  document.addEventListener("click", (e) => {
    const a = e.target.closest("[data-actie]");
    if (a) { const ac = data.acties.find((x) => x.id === a.dataset.actie); if (ac) activeer(ac); return; }
    const b = e.target.closest("[data-beloning]");
    if (b) { wisselIn(b.dataset.beloning); return; }
    const t = e.target.closest("[data-toon]");
    if (t) { const c = data.codes.find((x) => x.code === t.dataset.toon); if (c) toonCode(c); return; }
    const p = e.target.closest("[data-plus]");
    if (p) { data.mand[p.dataset.plus] = (data.mand[p.dataset.plus] || 0) + 1; bewaar(); teken(); return; }
    const m = e.target.closest("[data-min]");
    if (m) { const k = m.dataset.min; data.mand[k] = Math.max(0, (data.mand[k] || 0) - 1); if (!data.mand[k]) delete data.mand[k]; bewaar(); teken(); return; }
    const c = e.target.closest("[data-cat]");
    if (c) {
      document.querySelectorAll("#menu-chips button").forEach((x) => x.classList.toggle("aan", x === c));
      $(c.dataset.cat).scrollIntoView({ behavior: "smooth", block: "start" });
    }
  });

  /* ---------- mand / klaarzetten ---------- */
  function alleItems() { return MENU.flatMap((c) => c.items); }
  function mandRegels() { return Object.entries(data.mand).map(([id, n]) => { const it = alleItems().find((x) => x.id === id); return it ? { id, n, naam: it.naam, prijs: it.prijs } : null; }).filter(Boolean); }
  function mandAantal() { return mandRegels().reduce((s, r) => s + r.n, 0); }
  function mandSom() { return mandRegels().reduce((s, r) => s + r.n * r.prijs, 0); }
  function ophaalTijden() {
    const n = nu(); const [, van, tot] = TIJDEN[n.wd];
    const lijst = [];
    let start = Math.max(n.u * 60 + n.m + 15, minuten(van));
    start = Math.ceil(start / 15) * 15;
    for (let t = start; t <= minuten(tot) - 15; t += 15) lijst.push("vandaag " + String(Math.floor(t / 60)).padStart(2, "0") + ":" + String(t % 60).padStart(2, "0"));
    if (!lijst.length) { const mo = TIJDEN[(n.wd + 1) % 7]; for (let t = minuten(mo[1]); t <= minuten(mo[1]) + 120; t += 15) lijst.push("morgen " + String(Math.floor(t / 60)).padStart(2, "0") + ":" + String(t % 60).padStart(2, "0")); }
    return lijst.slice(0, 16);
  }
  $("mand-balk").addEventListener("click", () => {
    $("mand-regels").innerHTML = mandRegels().map((r) => `<div class="mand-regel"><span>${r.n}× ${esc(r.naam)}</span><b>${euro(r.n * r.prijs)}</b></div>`).join("");
    $("mand-tijd").innerHTML = ophaalTijden().map((t) => `<option>${t}</option>`).join("");
    $("mand-som").textContent = euro(mandSom());
    openVenster("v-mand");
  });
  $("btn-bestel").addEventListener("click", () => {
    const regels = mandRegels(); if (!regels.length) return;
    const tijd = $("mand-tijd").value;
    const dag = new Date(); if (tijd.startsWith("morgen")) dag.setDate(dag.getDate() + 1);
    const c = { code: maakCode("K"), soort: "bestelling", titel: "Klaarzetten · " + euro(mandSom()), regels: regels.map((r) => ({ n: r.n, naam: r.naam })), tijd, tot: isoDag(dag), status: "open", gemaakt: Date.now() };
    data.codes.push(c); data.mand = {}; bewaar();
    sluitVenster($("v-mand")); teken(); toonCode(c);
  });

  /* ---------- meer ---------- */
  $("set-meldingen").addEventListener("change", (e) => {
    data.meldingen = e.target.checked; bewaar();
    toast(data.meldingen ? "Meldingen aan (echte pushberichten komen met de echte app)" : "Meldingen uit");
  });
  $("set-naam").addEventListener("input", (e) => { data.klant.naam = e.target.value.trim().slice(0, 30); bewaar(); });
  $("set-naam").addEventListener("change", teken);
  $("btn-reset").addEventListener("click", () => {
    if (!confirm("Alles wissen en opnieuw beginnen? Je punten en codes zijn dan weg.")) return;
    data = nieuw(); bewaar(); $("klant-qr").dataset.voor = ""; toon("home"); toast("Opnieuw begonnen");
  });

  /* ---------- kraam-modus ---------- */
  $("btn-kraam").addEventListener("click", () => { $("pin-in").value = ""; $("pin-fout").hidden = true; openVenster("v-pin"); setTimeout(() => $("pin-in").focus(), 60); });
  $("pin-ok").addEventListener("click", () => {
    if ($("pin-in").value.trim() === PIN) { sluitVenster($("v-pin")); kraamAan(); }
    else { $("pin-fout").hidden = false; $("pin-in").select(); }
  });
  $("pin-in").addEventListener("keydown", (e) => { if (e.key === "Enter") $("pin-ok").click(); });

  let gekozenKlant = null;
  function kraamAan() { $("kraam").classList.add("aan"); $("kraam").setAttribute("aria-hidden", "false"); kraamTab("klant"); tekenKraam(); }
  function kraamUit() { stopCam(); $("kraam").classList.remove("aan"); $("kraam").setAttribute("aria-hidden", "true"); gekozenKlant = null; $("klant-gevonden").hidden = true; teken(); }
  $("kraam-uit").addEventListener("click", kraamUit);
  function kraamTab(t) {
    stopCam();
    document.querySelectorAll(".kraam-tabs button").forEach((b) => b.classList.toggle("aan", b.dataset.kt === t));
    document.querySelectorAll(".kt").forEach((k) => k.classList.toggle("aan", k.id === "kt-" + t));
    tekenKraam();
  }
  document.querySelectorAll(".kraam-tabs button").forEach((b) => b.addEventListener("click", () => kraamTab(b.dataset.kt)));
  function tekenKraam() {
    $("kraam-stat").textContent = "Vandaag: " + data.kraam.punten + " pt · " + data.kraam.ingewisseld + "× in";
    $("bedragen").innerHTML = [1.5, 5, 6.5, 10, 12, 20].map((b) => `<button type="button" data-bedrag="${b}">${euro(b)}<small>+${Math.floor(b * PUNTEN_PER_EURO)} pt</small></button>`).join("");
    const open = data.codes.filter((c) => c.soort === "bestelling" && c.status === "open");
    $("best-lijst").innerHTML = open.length ? open.map((c) => `<div class="item"><div class="tx"><b>${esc(c.code)} · ${esc(c.tijd)}</b>
      <small>${c.regels.map((r) => esc(r.n + "× " + r.naam)).join("<br>")}</small></div>
      <button type="button" class="knop knop-klein" data-opgehaald="${esc(c.code)}">Opgehaald</button></div>`).join("")
      : `<p class="leeg">Geen bestellingen om klaar te zetten.</p>`;
    if (gekozenKlant) { $("kg-code").textContent = gekozenKlant.id; $("kg-punten").textContent = gekozenKlant.punten + " punten" + (gekozenKlant.eersteScan ? "" : " · eerste scan: +" + WELKOMSTBONUS + " bonus"); }
  }
  function zoekKlant(code) {
    code = String(code || "").trim().toUpperCase().replace(/^OLIEBOL:/, "");
    if (/^\d{8}$/.test(code)) code = "OB-" + code.slice(0, 4) + "-" + code.slice(4);
    if (code === data.klant.id) {
      gekozenKlant = data.klant; $("klant-gevonden").hidden = false; $("klant-melding").textContent = ""; tekenKraam();
    } else {
      gekozenKlant = null; $("klant-gevonden").hidden = true;
      $("klant-melding").textContent = code ? "Onbekende klantcode. (In deze demo kent de kraam alleen de klant op dit toestel.)" : "";
    }
  }
  function geefPunten(bedrag) {
    if (!gekozenKlant || !(bedrag > 0)) return;
    let pt = Math.floor(bedrag * PUNTEN_PER_EURO + 1e-9);
    let extra = "";
    if (!gekozenKlant.eersteScan) { pt += WELKOMSTBONUS; gekozenKlant.eersteScan = true; extra = " (incl. " + WELKOMSTBONUS + " welkomstbonus)"; }
    gekozenKlant.punten += pt; gekozenKlant.totaal += pt; data.kraam.punten += pt; bewaar();
    $("klant-melding").textContent = "+" + pt + " punten" + extra + " · klant heeft nu " + gekozenKlant.punten;
    $("bedrag-in").value = ""; tekenKraam();
  }
  $("btn-klant-zoek").addEventListener("click", () => zoekKlant($("klant-in").value));
  $("klant-in").addEventListener("keydown", (e) => { if (e.key === "Enter") zoekKlant(e.target.value); });
  $("btn-demo-klant").addEventListener("click", () => { $("klant-in").value = data.klant.id; zoekKlant(data.klant.id); });
  $("btn-bedrag").addEventListener("click", () => geefPunten(parseFloat(String($("bedrag-in").value).replace(",", "."))));
  $("kraam").addEventListener("click", (e) => {
    const b = e.target.closest("[data-bedrag]"); if (b) { geefPunten(parseFloat(b.dataset.bedrag)); return; }
    const o = e.target.closest("[data-opgehaald]");
    if (o) { const c = data.codes.find((x) => x.code === o.dataset.opgehaald); if (c) { c.status = "gebruikt"; data.kraam.ingewisseld++; bewaar(); tekenKraam(); toast("Bestelling " + c.code + " opgehaald"); } return; }
    const ok = e.target.closest("[data-bevestig]");
    if (ok) {
      const c = data.codes.find((x) => x.code === ok.dataset.bevestig);
      if (c && c.status === "open") { c.status = "gebruikt"; data.kraam.ingewisseld++; bewaar(); tekenKraam();
        $("code-resultaat").innerHTML = `<div class="resultaat goed">✓ ${esc(c.code)} ingewisseld: ${esc(c.titel)}</div>`; $("code-in").value = ""; }
    }
  });
  function controleerCode(v) {
    v = String(v || "").trim().toUpperCase().replace(/^OLIEBOL:/, "").replace(/\s/g, "");
    if (/^[ABK]\d{4}$/.test(v)) v = v[0] + "-" + v.slice(1);
    const c = data.codes.find((x) => x.code === v);
    const r = $("code-resultaat");
    if (!c) { r.innerHTML = `<div class="resultaat fout">Code ${esc(v || "?")} niet gevonden.</div>`; return; }
    if (c.status !== "open") { r.innerHTML = `<div class="resultaat fout">${esc(c.code)} is al gebruikt.</div>`; return; }
    if (c.tot < isoDag(new Date())) { r.innerHTML = `<div class="resultaat fout">${esc(c.code)} is verlopen.</div>`; return; }
    const wat = c.soort === "bestelling" ? c.regels.map((x) => esc(x.n + "× " + x.naam)).join(", ") + " · " + esc(c.tijd) : esc(c.titel);
    r.innerHTML = `<div class="resultaat goed">Geldig: ${wat}<button type="button" class="knop" data-bevestig="${esc(c.code)}">${c.soort === "bestelling" ? "Opgehaald" : "Inwisselen bevestigen"}</button></div>`;
  }
  $("btn-code").addEventListener("click", () => controleerCode($("code-in").value));
  $("code-in").addEventListener("keydown", (e) => { if (e.key === "Enter") controleerCode(e.target.value); });
  $("btn-na").addEventListener("click", () => {
    const titel = $("na-titel").value.trim(), tekst = $("na-tekst").value.trim(), tot = $("na-tot").value;
    if (!titel || !tekst || !tot) { $("na-melding").textContent = "Vul titel, uitleg en datum in."; return; }
    data.acties.unshift({ id: "e-" + Date.now(), titel, tekst, tot, ill: "bol", voorbeeld: false, hero: false });
    bewaar(); $("na-titel").value = ""; $("na-tekst").value = "";
    $("na-melding").textContent = "Geplaatst. Klanten zien hem onder Acties.";
  });

  /* camera-scan met de ingebouwde BarcodeDetector (Chrome op Android) */
  let stream = null, lus = 0;
  function stopCam() {
    cancelAnimationFrame(lus); lus = 0;
    if (stream) { stream.getTracks().forEach((t) => t.stop()); stream = null; }
    ["cam", "cam2"].forEach((id) => $(id).classList.remove("aan"));
  }
  async function startCam(videoId, opResultaat, meldId) {
    stopCam();
    if (!("BarcodeDetector" in window) || !navigator.mediaDevices) {
      if (meldId) $(meldId).textContent = "Scannen werkt niet in deze browser. Tik de code in."; else toast("Scannen werkt hier niet. Tik de code in.");
      return;
    }
    try {
      stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } });
      const v = $(videoId); v.srcObject = stream; v.classList.add("aan"); await v.play();
      const det = new BarcodeDetector({ formats: ["qr_code"] });
      const stap = async () => {
        if (!stream) return;
        try { const r = await det.detect(v); if (r.length) { stopCam(); opResultaat(r[0].rawValue); return; } } catch (e) {}
        lus = requestAnimationFrame(stap);
      };
      stap();
    } catch (e) { stopCam(); toast("Geen toegang tot de camera"); }
  }
  $("btn-cam").addEventListener("click", () => startCam("cam", (w) => { $("klant-in").value = w.replace(/^OLIEBOL:/, ""); zoekKlant(w); }, "klant-melding"));
  $("btn-cam2").addEventListener("click", () => startCam("cam2", (w) => { $("code-in").value = w.replace(/^OLIEBOL:/, ""); controleerCode(w); }));

  /* ---------- start ---------- */
  toon(location.hash.slice(1) || "home");
  if ("serviceWorker" in navigator && location.protocol === "https:") navigator.serviceWorker.register("sw.js").catch(() => {});
})();
