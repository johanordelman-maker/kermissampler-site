#!/usr/bin/env python3
"""Generate privacy and terms pages for Kermis apps. Run from repo root."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

APPS = {
    "kermissampler": {
        "title_nl": "Kermis Sampler",
        "title_en": "Kermis Sampler",
        "package": "nl.kermissampler.app",
    },
    "kermisbingo": {
        "title_nl": "Kermis Bingo",
        "title_en": "Kermis Bingo",
        "package": "nl.kermisbingo.app",
    },
    "opdekermis": {
        "title_nl": "Op de Kermis!",
        "title_en": "Op de Kermis!",
        "package": "nl.kermissoftware.opdekermis",
    },
}

PUBLISHER_NL = (
    "<strong>Johan C. Ordelman jr. V.O.F.</strong> "
    "(handelsnaam Kermis Software), Nederland"
)
PUBLISHER_EN = (
    "<strong>Johan C. Ordelman jr. V.O.F.</strong> "
    "(trading name Kermis Software), the Netherlands"
)
CONTACT = '<a href="mailto:johanordelman@gmail.com">johanordelman@gmail.com</a>'
DATE_NL = "24 oktober 2026"
DATE_EN = "24 October 2026"


def depth_path(depth: int, target: str) -> str:
    return ("../" * depth) + target


def legal_header(depth: int, app_key: str, page_type: str, lang: str) -> str:
    """depth=3: {privacy|voorwaarden}/{app}/{lang}/index.html"""
    home = depth_path(depth, "index.html")
    css = depth_path(depth, "styles.css")
    fav = depth_path(depth, "favicon.ico")
    fav32 = depth_path(depth, "assets/favicon-32.png")
    apple = depth_path(depth, "assets/apple-touch-icon.png")
    icon = depth_path(depth, "assets/icon-512.png")
    app = APPS[app_key]
    title_app = app["title_nl"] if lang == "nl" else app["title_en"]
    if page_type == "privacy":
        doc_nl, doc_en = "Privacyverklaring", "Privacy policy"
    else:
        doc_nl, doc_en = "Gebruiksvoorwaarden", "Terms of use"
    doc = doc_nl if lang == "nl" else doc_en
    hub_privacy = "../"
    other_lang = "en" if lang == "nl" else "nl"
    other_label = "English" if lang == "nl" else "Nederlands"
    other_href = f"../{other_lang}/"
    if page_type == "privacy":
        terms_href = depth_path(depth, f"voorwaarden/{app_key}/{lang}/")
    else:
        terms_href = depth_path(depth, f"privacy/{app_key}/{lang}/")
    terms_label_nl = "Gebruiksvoorwaarden" if page_type == "privacy" else "Privacyverklaring"
    terms_label_en = "Terms of use" if page_type == "privacy" else "Privacy policy"
    terms_label = terms_label_nl if lang == "nl" else terms_label_en
    skip = "Naar inhoud" if lang == "nl" else "Skip to content"
    home_label = "Home" if lang == "nl" else "Home"
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta name="description" content="{doc} — {title_app}" />
  <meta name="theme-color" content="#110E0C" />
  <link rel="alternate" hreflang="nl" href="../nl/" />
  <link rel="alternate" hreflang="en" href="../en/" />
  <title>{doc} — {title_app}</title>
  <link rel="icon" href="{fav}" sizes="any" />
  <link rel="icon" type="image/png" sizes="32x32" href="{fav32}" />
  <link rel="apple-touch-icon" href="{apple}" />
  <link rel="stylesheet" href="{css}" />
</head>
<body>
  <a class="skip" href="#main">{skip}</a>
  <header class="site-header">
    <div class="inner">
      <a class="brand" href="{home}">
        <img src="{icon}" width="40" height="40" alt="" />
        <span>Kermis Software</span>
      </a>
      <nav class="nav" aria-label="{'Hoofdmenu' if lang == 'nl' else 'Main'}">
        <a href="{home}">{home_label}</a>
        <a href="{hub_privacy}" aria-current="page">{doc}</a>
      </nav>
    </div>
  </header>
  <main id="main" class="policy-main">
    <nav class="lang-switch" aria-label="{'Taal' if lang == 'nl' else 'Language'}">
      <a href="{other_href}" hreflang="{other_lang}">{other_label}</a>
      <a href="{terms_href}">{terms_label}</a>
    </nav>
"""


def legal_footer(depth: int, lang: str) -> str:
    home = depth_path(depth, "index.html")
    footer_links = f"""
        <a href="../../../privacy/kermissampler/{lang}/">Kermis Sampler — privacy</a>
        <a href="../../../privacy/kermisbingo/{lang}/">Kermis Bingo — privacy</a>
        <a href="../../../privacy/opdekermis/{lang}/">Op de Kermis! — privacy</a>
"""
    if lang == "nl":
        copy = "© 2026 Johan C. Ordelman jr. V.O.F. · Deze site gebruikt geen trackers of cookies."
    else:
        copy = "© 2026 Johan C. Ordelman jr. V.O.F. · This site uses no trackers or cookies."
    return f"""
  </main>
  <footer class="site-footer">
    <div class="inner">
      <div>
        <strong>Johan C. Ordelman jr. V.O.F.</strong> · Kermis Software · Nederland / Netherlands<br />
        {CONTACT}
      </div>
      <div class="links links-legal">
        {footer_links}
        <a href="{home}">Kermis Sampler (home)</a>
      </div>
      <p class="muted" style="margin:0;font-size:0.8rem">{copy}</p>
    </div>
  </footer>
</body>
</html>
"""


def privacy_body(app_key: str, lang: str) -> str:
    pkg = APPS[app_key]["package"]
    if app_key == "kermissampler":
        return privacy_sampler(lang, pkg)
    if app_key == "kermisbingo":
        return privacy_bingo(lang, pkg)
    return privacy_opdekermis(lang, pkg)


def terms_body(app_key: str, lang: str) -> str:
    if app_key == "opdekermis":
        return terms_opdekermis(lang)
    return terms_generic(app_key, lang)


def privacy_sampler(lang: str, pkg: str) -> str:
    if lang == "nl":
        return f"""
    <p class="meta">{APPS['kermissampler']['title_nl']} · {pkg} · Laatst bijgewerkt: {DATE_NL}</p>
    <h1>Privacyverklaring</h1>
    <p>Deze verklaring geldt voor de Android- en iOS-app <strong>Kermis Sampler</strong> ({pkg}), een offline-first soundboard voor thuisgebruik. Verwerkingsverantwoordelijke: {PUBLISHER_NL}. Contact: {CONTACT}.</p>

    <h2>1. Welke gegevens worden verwerkt?</h2>
    <p><strong>Wij verzamelen geen persoonsgegevens op eigen servers.</strong> Er is geen account. De app bevat <strong>geen Google AdMob</strong>, <strong>geen analytics</strong> en <strong>geen tracking-SDK</strong> (geen Firebase Analytics, crashrapportage of advertentie-tracking naar ons).</p>
    <p>De app bewaart gegevens <em>alleen lokaal op uw toestel</em> (o.a. WebView-opslag / IndexedDB), bijvoorbeeld:</p>
    <ul>
      <li>instellingen (taal, uiterlijk, volume, mixer);</li>
      <li>soundboard-pads en gekoppelde lokale audiobestanden (URI’s waartoe u toegang geeft);</li>
      <li>afspeellijsten en wachtrijen die u importeert of plakt;</li>
      <li>optionele back-ups die u zelf exporteert;</li>
      <li>lokaal of de app is ontgrendeld na een store-aankoop.</li>
    </ul>

    <h2>2. Google Play, App Store en aankopen</h2>
    <p>In-app aankopen en abonnementen lopen via <strong>Google Play</strong> (Android) of de <strong>Apple App Store</strong> (iOS), o.a. product-id’s <code>full_unlock</code> (eenmalige volledige versie) en <code>disco_lijst_jaar</code> (jaarabonnement). Betaling en facturatie doen Google of Apple; wij ontvangen geen naam, adres, e-mail of betaalgegevens. De app vraagt de store alleen of de aankoop op uw account actief is en bewaart dat lokaal op het toestel.</p>
    <p><strong>Verwerker:</strong> Google (Google Play) of Apple (App Store), voor betaling en aankoopvalidatie.<br />
    <strong>Rechtsgrond:</strong> uitvoering van de overeenkomst (levering van de digitale inhoud) en, waar de store dat vereist, naleving van wettelijke verplichtingen.<br />
    <strong>Bewaartermijn:</strong> volgens het privacybeleid van Google of Apple; onze app bewaart alleen lokaal dat de app ontgrendeld is, tot u de app verwijdert of de opslag wist.</p>
    <p>Privacy Google: <a href="https://policies.google.com/privacy">policies.google.com/privacy</a>. Privacy Apple: <a href="https://www.apple.com/legal/privacy/">apple.com/legal/privacy</a>.</p>

    <h2>3. Microfoon en bestanden</h2>
    <p><strong>Microfoon</strong> — alleen als u de talk-over-functie gebruikt; het besturingssysteem vraagt dan toestemming. Audio wordt niet opgenomen of naar ons geüpload.</p>
    <p><strong>Bestanden</strong> — via de systeemkiezer wanneer u MP3/WAV of mappen kiest; alleen op het toestel.</p>

    <h2>4. Diensten van derden (internet)</h2>
    <p>Als u bepaalde functies gebruikt, maakt de app verbinding met diensten van derden. Wij sturen die partijen geen account bij ons door; zij kunnen bij die verbinding onder meer uw <strong>IP-adres</strong>, apparaat- en verbindingsgegevens en wat u zoekt of afspeelt verwerken volgens hun eigen beleid. Dit gebeurt alleen wanneer u de functie start:</p>
    <ul>
      <li><strong>YouTube en YouTube Music</strong> (zoeken en afspelen) — <a href="https://policies.google.com/privacy">privacybeleid Google/YouTube</a></li>
      <li><strong>Spotify</strong> (webspeler in de app) — <a href="https://www.spotify.com/legal/privacy-policy/">privacybeleid Spotify</a></li>
      <li><strong>Deezer</strong> (webspeler) — <a href="https://www.deezer.com/legal/privacy">privacybeleid Deezer</a></li>
      <li><strong>SoundCloud</strong> (webspeler) — <a href="https://soundcloud.com/pages/privacy">privacybeleid SoundCloud</a></li>
      <li><strong>Hugging Face</strong> (eenmalig downloaden van het Splitsen-model) — <a href="https://huggingface.co/privacy">privacybeleid Hugging Face</a></li>
    </ul>
    <p>Optioneel kan een openbare “lijst van vandaag”-CSV van een GitHub Gist worden opgehaald; daarvoor geldt het beleid van <a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement">GitHub</a>.</p>
    <p><strong>Rechtsgrond:</strong> uw keuze om de functie te gebruiken (uitvoering van de dienst die u start) en, voor de microfoon, uw toestemming via het besturingssysteem.<br />
    <strong>Bewaartermijn:</strong> bij ons niet op servers; bij derden volgens hun privacybeleid.</p>

    <h2>5. Rechten, klachten en contact</h2>
    <p>Omdat wij geen persoonsgegevens op servers bewaren, kunnen wij gegevens die alleen op uw toestel staan niet inzien of wissen; dat regelt u door de app te verwijderen of de app-opslag te wissen. Voor aankoopgegevens bij Google of Apple gelden hun privacy-instrumenten.</p>
    <p>U heeft rechten onder de AVG (o.a. inzage, rectificatie, verwijdering, beperking, bezwaar, dataportabiliteit) voor zover wij gegevens verwerken. Neem contact op via {CONTACT}. U kunt ook een klacht indienen bij de <a href="https://www.autoriteitpersoonsgegevens.nl/">Autoriteit Persoonsgegevens</a>.</p>

    <h2>6. Kinderen</h2>
    <p>De app is niet speciaal bedoeld voor kinderen. De app bevat geen advertenties en geen gepersonaliseerde advertenties.</p>
"""
    return f"""
    <p class="meta">{APPS['kermissampler']['title_en']} · {pkg} · Last updated: {DATE_EN}</p>
    <h1>Privacy policy</h1>
    <p>This notice applies to the Android and iOS app <strong>Kermis Sampler</strong> ({pkg}), an offline-first home soundboard. Controller: {PUBLISHER_EN}. Contact: {CONTACT}.</p>

    <h2>1. What data is processed?</h2>
    <p><strong>We do not collect personal data on our own servers.</strong> There is no account. The app includes <strong>no Google AdMob</strong>, <strong>no analytics</strong>, and <strong>no tracking SDK</strong> (no Firebase Analytics, crash reporting or ad tracking to us).</p>
    <p>The app stores data <em>only on your device</em> (including WebView storage / IndexedDB), for example:</p>
    <ul>
      <li>settings (language, appearance, volume, mixer);</li>
      <li>soundboard pads and local audio file references you grant;</li>
      <li>playlists and queues you import or paste;</li>
      <li>optional backups you export yourself;</li>
      <li>locally whether the app is unlocked after a store purchase.</li>
    </ul>

    <h2>2. Google Play, App Store and purchases</h2>
    <p>In-app purchases and subscriptions are handled by <strong>Google Play</strong> (Android) or the <strong>Apple App Store</strong> (iOS), including product IDs <code>full_unlock</code> (one-time full unlock) and <code>disco_lijst_jaar</code> (annual subscription). Google or Apple processes payment and billing; we never receive your name, address, email or payment details. The app only asks the store whether the purchase is active on your account and stores that locally on the device.</p>
    <p><strong>Processor:</strong> Google (Google Play) or Apple (App Store), for payment and purchase validation.<br />
    <strong>Legal basis:</strong> performance of a contract (delivery of digital content) and, where required by the store, compliance with legal obligations.<br />
    <strong>Retention:</strong> as described in Google’s or Apple’s privacy policy; our app only keeps local unlock state until you delete the app or clear its storage.</p>
    <p>Google privacy: <a href="https://policies.google.com/privacy">policies.google.com/privacy</a>. Apple privacy: <a href="https://www.apple.com/legal/privacy/">apple.com/legal/privacy</a>.</p>

    <h2>3. Microphone and files</h2>
    <p><strong>Microphone</strong> — only when you use talk-over; the operating system asks permission. Audio is not recorded or uploaded to us.</p>
    <p><strong>Files</strong> — via the system picker when you choose MP3/WAV files or folders; on-device only.</p>

    <h2>4. Third-party services (internet)</h2>
    <p>When you use certain features, the app connects to third-party services. We do not send those parties an account with us; they may process your <strong>IP address</strong>, device and connection data, and what you search or play, under their own policies. This only happens when you start the feature:</p>
    <ul>
      <li><strong>YouTube and YouTube Music</strong> (search and playback) — <a href="https://policies.google.com/privacy">Google/YouTube privacy policy</a></li>
      <li><strong>Spotify</strong> (in-app web player) — <a href="https://www.spotify.com/legal/privacy-policy/">Spotify privacy policy</a></li>
      <li><strong>Deezer</strong> (web player) — <a href="https://www.deezer.com/legal/privacy">Deezer privacy policy</a></li>
      <li><strong>SoundCloud</strong> (web player) — <a href="https://soundcloud.com/pages/privacy">SoundCloud privacy policy</a></li>
      <li><strong>Hugging Face</strong> (one-time download of the Splitsen model) — <a href="https://huggingface.co/privacy">Hugging Face privacy policy</a></li>
    </ul>
    <p>Optionally, a public “daily list” CSV may be fetched from a GitHub Gist; <a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement">GitHub’s privacy statement</a> applies.</p>
    <p><strong>Legal basis:</strong> your choice to use the feature (performance of the service you start) and, for the microphone, your consent via the operating system.<br />
    <strong>Retention:</strong> not on our servers; at third parties per their privacy policies.</p>

    <h2>5. Your rights, complaints and contact</h2>
    <p>Because we do not keep personal data on servers, we cannot access or erase data that exists only on your device; delete the app or clear its storage to remove that. For purchase data held by Google or Apple, use their privacy tools.</p>
    <p>You have GDPR rights (access, rectification, erasure, restriction, objection, portability) where we process data. Contact {CONTACT}. You may lodge a complaint with the <a href="https://www.autoriteitpersoonsgegevens.nl/">Dutch Data Protection Authority (Autoriteit Persoonsgegevens)</a>.</p>

    <h2>6. Children</h2>
    <p>The app is not specifically aimed at children. The app contains no ads and no personalised advertising.</p>
"""


def admob_section(lang: str, app_name: str) -> str:
    if lang == "nl":
        return f"""
    <h2>Beloningsadvertenties (Google AdMob)</h2>
    <p>In de gratis versie kunt u zelf een kort beloningsfilmpje starten (geen banners bij opstarten, tenzij anders in de app beschreven). <strong>Google AdMob</strong> verwerkt daarbij o.a.:</p>
    <ul>
      <li>het advertentie-ID van het toestel;</li>
      <li>het IP-adres;</li>
      <li>apparaattype en -gegevens;</li>
      <li>interacties met de advertentie (weergave, klik).</li>
    </ul>
    <p><strong>Doel:</strong> een advertentie tonen, meten en fraude/misbruik beperken.<br />
    <strong>Verwerker:</strong> Google (AdMob; op Android/iOS ook het User Messaging Platform voor toestemming; op iOS kan Apple’s App Tracking Transparency (ATT) gelden).<br />
    <strong>Rechtsgrond:</strong> uw <strong>toestemming</strong> (EU/VK) voordat gepersonaliseerde of meetbare advertentieverwerking plaatsvindt, via het toestemmingsformulier in de app.<br />
    <strong>Toestemming intrekken:</strong> in de app via het privacy-/advertentie-instellingenscherm (bij {app_name}: menu of instellingen → privacy &amp; reclame → wijzigen), en in de instellingen van uw toestel voor het advertentie-ID (Android: Google-account → advertenties; iOS: privacy → tracking / advertenties).<br />
    <strong>Bewaartermijn:</strong> volgens het <a href="https://policies.google.com/privacy">privacybeleid van Google</a> en <a href="https://support.google.com/admob/answer/6128543">AdMob-documentatie</a>; wij bewaren deze advertentiegegevens niet op eigen servers.</p>
    <p>Zonder toestemming of zonder start van het filmpje worden geen advertentiegegevens voor dat filmpje verwerkt. Wij verkopen geen gegevens.</p>
"""
    return f"""
    <h2>Rewarded ads (Google AdMob)</h2>
    <p>In the free version you can start a short rewarded video yourself (no banners on launch unless described otherwise in the app). <strong>Google AdMob</strong> may process:</p>
    <ul>
      <li>the device advertising ID;</li>
      <li>IP address;</li>
      <li>device type and characteristics;</li>
      <li>ad interactions (views, clicks).</li>
    </ul>
    <p><strong>Purpose:</strong> show an ad, measure it, and limit fraud/abuse.<br />
    <strong>Processor:</strong> Google (AdMob; on Android/iOS also the User Messaging Platform for consent; on iOS Apple’s App Tracking Transparency (ATT) may apply).<br />
    <strong>Legal basis:</strong> your <strong>consent</strong> (EU/UK) before personalised or measurable ad processing, via the in-app consent flow.<br />
    <strong>Withdraw consent:</strong> in the app via the privacy/ad settings screen (in {app_name}: menu or settings → privacy &amp; ads → change), and in your device settings for the advertising ID (Android: Google account → ads; iOS: Privacy → tracking / ads).<br />
    <strong>Retention:</strong> as set out in <a href="https://policies.google.com/privacy">Google’s privacy policy</a> and <a href="https://support.google.com/admob/answer/6128543">AdMob help</a>; we do not store this ad data on our own servers.</p>
    <p>Without consent or without starting the video, no ad data is processed for that video. We do not sell data.</p>
"""


def privacy_bingo(lang: str, pkg: str) -> str:
    admob = admob_section(lang, "Kermis Bingo")
    if lang == "nl":
        return f"""
    <p class="meta">Kermis Bingo · {pkg} · Laatst bijgewerkt: {DATE_NL}</p>
    <h1>Privacyverklaring</h1>
    <p>Deze verklaring geldt voor <strong>Kermis Bingo</strong> ({pkg}) op Android en iOS. Verwerkingsverantwoordelijke: {PUBLISHER_NL}. Contact: {CONTACT}.</p>

    <h2>1. Geen account, spel lokaal</h2>
    <p>Er is geen account en wij verzamelen geen naam of e-mailadres in de app. Trekken, kaarten en instellingen werken offline. Wat u invoert (trekking, rondes, kaartreeks, weergave, stem, optioneel logo) staat in lokale opslag op het toestel en gaat niet naar ons.</p>

    <h2>2. Google Play / App Store — eenmalige aankoop</h2>
    <p>De volledige versie is product-id <code>full_unlock</code> (eenmalig, via de store). Google of Apple verwerkt de betaling; wij zien geen betaalgegevens. De app controleert alleen of de aankoop actief is. <strong>Rechtsgrond:</strong> uitvoering van de overeenkomst. <strong>Bewaartermijn:</strong> bij Google/Apple volgens hun beleid; lokaal tot u de app verwijdert.</p>
{admob}
    <h2>3. Rechten en klachten</h2>
    <p>Voor spelgegevens op uw toestel kunt u de app verwijderen of opslag wissen. Voor advertentie- en aankoopgegevens bij Google of Apple gelden hun privacy-instrumenten. Vragen: {CONTACT}. Klacht bij de <a href="https://www.autoriteitpersoonsgegevens.nl/">Autoriteit Persoonsgegevens</a> is mogelijk.</p>

    <h2>4. Kinderen</h2>
    <p>De app is niet speciaal voor kinderen bedoeld. Zonder uw toestemming tonen wij geen gepersonaliseerde advertenties via AdMob.</p>
"""
    return f"""
    <p class="meta">Kermis Bingo · {pkg} · Last updated: {DATE_EN}</p>
    <h1>Privacy policy</h1>
    <p>This notice applies to <strong>Kermis Bingo</strong> ({pkg}) on Android and iOS. Controller: {PUBLISHER_EN}. Contact: {CONTACT}.</p>

    <h2>1. No account, local play</h2>
    <p>There is no account and we do not collect your name or email in the app. Drawing numbers and cards work offline. What you enter (draw, rounds, card series, display, voice, optional logo) stays in local storage on the device and is not sent to us.</p>

    <h2>2. Google Play / App Store — one-time purchase</h2>
    <p>The full version is product ID <code>full_unlock</code> (one-time, via the store). Google or Apple processes payment; we do not see payment details. The app only checks whether the purchase is active. <strong>Legal basis:</strong> performance of a contract. <strong>Retention:</strong> with Google/Apple per their policies; locally until you delete the app.</p>
{admob}
    <h2>3. Rights and complaints</h2>
    <p>For game data on your device, delete the app or clear storage. For ad and purchase data at Google or Apple, use their privacy tools. Questions: {CONTACT}. You may complain to the <a href="https://www.autoriteitpersoonsgegevens.nl/">Dutch Data Protection Authority</a>.</p>

    <h2>4. Children</h2>
    <p>The app is not specifically aimed at children. Without your consent we do not serve personalised ads via AdMob.</p>
"""


def privacy_opdekermis(lang: str, pkg: str) -> str:
    admob = admob_section(lang, "Op de Kermis!")
    if lang == "nl":
        return f"""
    <p class="meta">Op de Kermis! · {pkg} · Laatst bijgewerkt: {DATE_NL}</p>
    <h1>Privacyverklaring</h1>
    <p>Deze verklaring geldt voor de kermisgame <strong>Op de Kermis!</strong> ({pkg}) op Android en iOS. Verwerkingsverantwoordelijke: {PUBLISHER_NL}. Contact: {CONTACT}.</p>

    <h2>1. Geen account, voortgang lokaal</h2>
    <p>Er is geen account. Spelvoortgang en virtuele munten worden <strong>alleen lokaal op het toestel</strong> opgeslagen; wij ontvangen die gegevens niet op een server.</p>

    <h2>2. Aankopen via Google Play / App Store</h2>
    <p>In-app aankopen: <code>full_unlock</code>, <code>munten_25</code>, <code>munten_75</code>, <code>munten_200</code>. Betaling via Google Play Billing of StoreKit; wij zien geen betaalgegevens. Munten na aankoop worden lokaal bijgeschreven. <strong>Rechtsgrond:</strong> uitvoering van de overeenkomst. <strong>Bewaartermijn:</strong> store-gegevens bij Google/Apple; lokaal tot u de app verwijdert.</p>
{admob}
    <h2>3. Link naar kermis.nu</h2>
    <p>De app kan een knop tonen die <strong>kermis.nu</strong> in uw browser opent. Die website valt onder het eigen privacybeleid van kermis.nu; wij beheren die site niet en weten niet welke gegevens u daar achterlaat.</p>

    <h2>4. Rechten en klachten</h2>
    <p>Lokale gegevens wist u via de app of door verwijderen van de app. Voor AdMob en store-aankopen gelden de instrumenten van Google en Apple. Contact: {CONTACT}. Klacht: <a href="https://www.autoriteitpersoonsgegevens.nl/">Autoriteit Persoonsgegevens</a>.</p>

    <h2>5. Kinderen</h2>
    <p>De app is niet speciaal voor kinderen. Geen gepersonaliseerde advertenties zonder toestemming.</p>
"""
    return f"""
    <p class="meta">Op de Kermis! · {pkg} · Last updated: {DATE_EN}</p>
    <h1>Privacy policy</h1>
    <p>This notice applies to the fairground game <strong>Op de Kermis!</strong> ({pkg}) on Android and iOS. Controller: {PUBLISHER_EN}. Contact: {CONTACT}.</p>

    <h2>1. No account, local progress</h2>
    <p>There is no account. Game progress and virtual coins are stored <strong>only locally on the device</strong>; we do not receive that data on a server.</p>

    <h2>2. Purchases via Google Play / App Store</h2>
    <p>In-app products: <code>full_unlock</code>, <code>munten_25</code>, <code>munten_75</code>, <code>munten_200</code>. Payment via Google Play Billing or StoreKit; we do not see payment details. Coins are credited locally after purchase. <strong>Legal basis:</strong> performance of a contract. <strong>Retention:</strong> store data with Google/Apple; local until you delete the app.</p>
{admob}
    <h2>3. Link to kermis.nu</h2>
    <p>The app may open <strong>kermis.nu</strong> in your browser. That website has its own privacy policy; we do not operate it and do not know what data you provide there.</p>

    <h2>4. Rights and complaints</h2>
    <p>Clear local data by deleting the app. For AdMob and store purchases, use Google and Apple’s tools. Contact: {CONTACT}. Complaints: <a href="https://www.autoriteitpersoonsgegevens.nl/">Dutch Data Protection Authority</a>.</p>

    <h2>5. Children</h2>
    <p>The app is not specifically aimed at children. No personalised ads without consent.</p>
"""


def terms_generic(app_key: str, lang: str) -> str:
    app = APPS[app_key]
    name = app["title_nl"] if lang == "nl" else app["title_en"]
    pkg = app["package"]
    if lang == "nl":
        return f"""
    <p class="meta">{name} · {pkg} · Laatst bijgewerkt: {DATE_NL}</p>
    <h1>Gebruiksvoorwaarden</h1>
    <p>Deze voorwaarden gelden voor het gebruik van <strong>{name}</strong> ({pkg}), aangeboden door {PUBLISHER_NL}. Contact: {CONTACT}.</p>
    <h2>1. Gebruik</h2>
    <p>De app is bedoeld voor amusement en privégebruik. U gebruikt de app op eigen risico en in overeenstemming met de regels van Google Play of de App Store.</p>
    <h2>2. Aankopen</h2>
    <p>Betaalde functies worden via Google Play of de App Store afgerekend. Op die betalingen gelden de voorwaarden van Google of Apple. Digitale inhoud wordt geleverd na bevestiging door de store.</p>
    <h2>3. Aansprakelijkheid</h2>
    <p>Voor zover wettelijk toegestaan is onze aansprakelijkheid beperkt tot het bedrag dat u in de twaalf maanden voorafgaand aan de claim voor deze app via de store heeft betaald, met een maximum van € 50, tenzij dwingend recht anders voorschrijft. Wij zijn niet aansprakelijk voor indirecte schade of verlies van gegevens op uw toestel.</p>
    <h2>4. Toepasselijk recht</h2>
    <p>Op deze voorwaarden is Nederlands recht van toepassing. Geschillen worden voorgelegd aan de bevoegde rechter in Nederland, onverminderd uw rechten als consument.</p>
"""
    return f"""
    <p class="meta">{name} · {pkg} · Last updated: {DATE_EN}</p>
    <h1>Terms of use</h1>
    <p>These terms apply to <strong>{name}</strong> ({pkg}), offered by {PUBLISHER_EN}. Contact: {CONTACT}.</p>
    <h2>1. Use</h2>
    <p>The app is for entertainment and personal use. You use it at your own risk and in line with Google Play or App Store rules.</p>
    <h2>2. Purchases</h2>
    <p>Paid features are billed through Google Play or the App Store. Google or Apple’s terms apply to payment. Digital content is delivered after the store confirms the purchase.</p>
    <h2>3. Liability</h2>
    <p>Where permitted by law, our liability is limited to the amount you paid for this app via the store in the twelve months before the claim, up to € 50, unless mandatory law requires otherwise. We are not liable for indirect loss or loss of data on your device.</p>
    <h2>4. Governing law</h2>
    <p>These terms are governed by Dutch law. Disputes go to the competent courts in the Netherlands, without affecting your consumer rights.</p>
"""


def terms_opdekermis(lang: str) -> str:
    pkg = APPS["opdekermis"]["package"]
    if lang == "nl":
        return f"""
    <p class="meta">Op de Kermis! · {pkg} · Laatst bijgewerkt: {DATE_NL}</p>
    <h1>Gebruiksvoorwaarden</h1>
    <p>Deze voorwaarden gelden voor <strong>Op de Kermis!</strong> ({pkg}), aangeboden door {PUBLISHER_NL}. Contact: {CONTACT}.</p>
    <h2>1. Amusement, geen gokken</h2>
    <p>De game is entertainment. Er is geen echte gokinzet en geen uitbetaling van echt geld.</p>
    <h2>2. Virtuele munten</h2>
    <p>Munten in de app hebben <strong>geen geldwaarde</strong>, zijn niet inwisselbaar voor geld of goederen en kunnen niet worden uitbetaald. Munten en voortgang staan alleen lokaal op uw toestel.</p>
    <h2>3. Aankopen</h2>
    <p>Aankopen (o.a. <code>full_unlock</code>, muntenpakketten) lopen via Google Play of de App Store; hun voorwaarden gelden voor betaling en herstel.</p>
    <h2>4. Aansprakelijkheid en recht</h2>
    <p>Aansprakelijkheid is beperkt zoals toegestaan onder Nederlands recht (zie ook de algemene beperking in onze andere apps: maximaal het door u betaalde bedrag in de laatste twaalf maanden, tot € 50). Nederlands recht is van toepassing.</p>
"""
    return f"""
    <p class="meta">Op de Kermis! · {pkg} · Last updated: {DATE_EN}</p>
    <h1>Terms of use</h1>
    <p>These terms apply to <strong>Op de Kermis!</strong> ({pkg}), offered by {PUBLISHER_EN}. Contact: {CONTACT}.</p>
    <h2>1. Entertainment, not gambling</h2>
    <p>The game is for fun. There is no real-money wagering and no cash payouts.</p>
    <h2>2. Virtual coins</h2>
    <p>Coins have <strong>no monetary value</strong>, cannot be exchanged for cash or goods, and cannot be withdrawn. Coins and progress are stored only on your device.</p>
    <h2>3. Purchases</h2>
    <p>Purchases (e.g. <code>full_unlock</code>, coin packs) go through Google Play or the App Store; their terms apply.</p>
    <h2>4. Liability and law</h2>
    <p>Liability is limited as permitted under Dutch law (similar cap: amounts paid in the last twelve months, up to € 50). Dutch law applies.</p>
"""


def write_page(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def hub_page(app_key: str, page_type: str) -> str:
    depth = 2
    css = depth_path(depth, "styles.css")
    fav = depth_path(depth, "favicon.ico")
    icon = depth_path(depth, "assets/icon-512.png")
    home = depth_path(depth, "index.html")
    app = APPS[app_key]
    folder = "privacy" if page_type == "privacy" else "voorwaarden"
    return f"""<!DOCTYPE html>
<html lang="nl">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{app['title_nl']} — {folder}</title>
  <link rel="stylesheet" href="{css}" />
  <link rel="icon" href="{fav}" />
</head>
<body>
  <header class="site-header">
    <div class="inner">
      <a class="brand" href="{home}"><img src="{icon}" width="40" height="40" alt="" /><span>Kermis Software</span></a>
    </div>
  </header>
  <div class="legal-hub">
    <h1>{app['title_nl']} / {app['title_en']}</h1>
    <p class="muted">Kies een taal / Choose a language:</p>
    <ul>
      <li><a href="nl/">Nederlands — {folder}</a></li>
      <li><a href="en/">English — {folder if page_type == 'privacy' else 'terms'}</a></li>
    </ul>
  </div>
</body>
</html>
"""


def privacy_html_legacy() -> str:
    """Root privacy.html — Play Store URL compatibility, bilingual NL/EN."""
    nl = privacy_sampler("nl", APPS["kermissampler"]["package"])
    en = privacy_sampler("en", APPS["kermissampler"]["package"])
    return f"""<!DOCTYPE html>
<html lang="nl">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta name="description" content="Privacybeleid / Privacy Policy — Kermis Sampler (Kermis Software)" />
  <link rel="canonical" href="privacy/kermissampler/nl/" />
  <link rel="alternate" hreflang="nl" href="privacy/kermissampler/nl/" />
  <link rel="alternate" hreflang="en" href="privacy/kermissampler/en/" />
  <meta name="theme-color" content="#110E0C" />
  <title>Privacybeleid / Privacy Policy — Kermis Sampler</title>
  <link rel="icon" href="favicon.ico" sizes="any" />
  <link rel="icon" type="image/png" sizes="32x32" href="assets/favicon-32.png" />
  <link rel="apple-touch-icon" href="assets/apple-touch-icon.png" />
  <link rel="stylesheet" href="styles.css" />
</head>
<body>
  <a class="skip" href="#main">Naar inhoud / Skip to content</a>
  <header class="site-header">
    <div class="inner">
      <a class="brand" href="index.html">
        <img src="assets/icon-512.png" width="40" height="40" alt="" />
        <span>Kermis Sampler</span>
      </a>
      <nav class="nav" aria-label="Hoofdmenu">
        <a href="index.html">Home</a>
        <a href="privacy.html" aria-current="page">Privacy</a>
        <a href="voorwaarden/kermissampler/nl/" class="lang-nl">Gebruiksvoorwaarden</a>
        <a href="voorwaarden/kermissampler/en/" class="lang-en">Terms of use</a>
        <div class="lang-toggle" role="group" aria-label="Language / Taal">
          <button type="button" id="btn-nl" aria-pressed="true" data-lang="nl">NL</button>
          <button type="button" id="btn-en" aria-pressed="false" data-lang="en">EN</button>
        </div>
      </nav>
    </div>
  </header>
  <main id="main" class="policy-main">
    <div class="lang-nl">
{nl}
    </div>
    <div class="lang-en policy-lang-sep" lang="en">
{en}
    </div>
  </main>
  <footer class="site-footer">
    <div class="inner">
      <div>
        <strong>Johan C. Ordelman jr. V.O.F.</strong> · Kermis Software · Nederland / Netherlands<br />
        {CONTACT}
      </div>
      <div class="links links-legal">
        <a href="privacy/kermissampler/nl/">Kermis Sampler — privacy</a>
        <a href="privacy/kermisbingo/nl/">Kermis Bingo — privacy</a>
        <a href="privacy/opdekermis/nl/">Op de Kermis! — privacy</a>
        <a href="index.html">Home</a>
      </div>
      <p class="muted" style="margin:0;font-size:0.8rem">
        <span class="lang-nl">© 2026 Johan C. Ordelman jr. V.O.F. · Deze site gebruikt geen trackers of cookies.</span>
        <span class="lang-en">© 2026 Johan C. Ordelman jr. V.O.F. · This site uses no trackers or cookies.</span>
      </p>
    </div>
  </footer>
  <script src="lang.js"></script>
</body>
</html>
"""


def redirect_html(target: str, title: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="nl">
<head>
  <meta charset="utf-8" />
  <meta http-equiv="refresh" content="0; url={target}" />
  <link rel="canonical" href="{target}" />
  <title>{title}</title>
</head>
<body>
  <p><a href="{target}">{title}</a></p>
</body>
</html>
"""


def main() -> None:
    depth = 3  # privacy/app/lang/index.html
    for app_key in APPS:
        for page_type in ("privacy", "voorwaarden"):
            hub = ROOT / page_type / app_key / "index.html"
            write_page(hub, hub_page(app_key, page_type))
            for lang in ("nl", "en"):
                body_fn = privacy_body if page_type == "privacy" else terms_body
                html = (
                    legal_header(depth, app_key, page_type, lang)
                    + body_fn(app_key, lang)
                    + legal_footer(depth, lang)
                )
                out = ROOT / page_type / app_key / lang / "index.html"
                write_page(out, html)

    write_page(ROOT / "privacy.html", privacy_html_legacy())
    write_page(
        ROOT / "kermisbingo-privacy.html",
        redirect_html("privacy/kermisbingo/nl/", "Privacy — Kermis Bingo"),
    )
    print("Generated legal pages.")


if __name__ == "__main__":
    main()
