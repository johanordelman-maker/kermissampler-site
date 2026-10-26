#!/usr/bin/env python3
"""Generate privacy and terms pages for Kermis apps. Run from repo root."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

APPS = {
    "kermissampler": {
        "title_nl": "Kermis Sampler",
        "title_en": "Kermis Sampler",
        "package": "nl.kermissampler.app",
        # Support address of Kermis Sampler (Johan, 25-10-2026; catch-all forward).
        "email": "kermissampler@ordelman.net",
    },
    "kermisbingo": {
        "title_nl": "Kermis Bingo",
        "title_en": "Kermis Bingo",
        "package": "nl.kermisbingo.app",
        # Support address of Kermis Bingo (catch-all forward, 26-10-2026).
        "email": "kermisbingo@ordelman.net",
    },
    "opdekermis": {
        "title_nl": "Op de Kermis!",
        "title_en": "Op de Kermis!",
        "package": "nl.kermissoftware.opdekermis",
        # Support address of Op de Kermis! (catch-all forward, 26-10-2026).
        "email": "opdekermis@ordelman.net",
    },
}

# Maker name shown on the site is Kermis Software; the legal entity stays named.
PUBLISHER_NL = (
    "<strong>Kermis Software</strong> "
    "(handelsnaam van Johan C. Ordelman jr. V.O.F.)"
)
PUBLISHER_EN = (
    "<strong>Kermis Software</strong> "
    "(trade name of Johan C. Ordelman jr. V.O.F.)"
)
KVK = "98595407"
ADDRESS = "Terbregsehof 48, 3062 CP Rotterdam"
DATE_NL = "25 oktober 2026"
DATE_EN = "25 October 2026"
AP_LINK_NL = '<a href="https://www.autoriteitpersoonsgegevens.nl/">Autoriteit Persoonsgegevens</a>'
AP_LINK_EN = (
    '<a href="https://www.autoriteitpersoonsgegevens.nl/">'
    "Dutch Data Protection Authority (Autoriteit Persoonsgegevens)</a>"
)
GOOGLE_PRIVACY = '<a href="https://policies.google.com/privacy">policies.google.com/privacy</a>'
APPLE_PRIVACY = '<a href="https://www.apple.com/legal/privacy/">apple.com/legal/privacy</a>'


def t(lang: str, nl: str, en: str) -> str:
    return nl if lang == "nl" else en


def contact(app_key: str) -> str:
    """Mail link with the support address of this app."""
    email = APPS[app_key]["email"]
    return f'<a href="mailto:{email}">{email}</a>'


def app_name(app_key: str, lang: str) -> str:
    return APPS[app_key]["title_nl" if lang == "nl" else "title_en"]


def meta_line(app_key: str, lang: str) -> str:
    pkg = APPS[app_key]["package"]
    updated = t(lang, f"Laatst bijgewerkt: {DATE_NL}", f"Last updated: {DATE_EN}")
    return f'    <p class="meta">{app_name(app_key, lang)} · {pkg} · {updated}</p>\n'


# --- Gedeelde blokken (audit 25-10-2026, teksten A-F) -----------------------


def company_section(lang: str, app_key: str) -> str:
    """A: bedrijfsgegevens, op alle pagina's."""
    return t(
        lang,
        f"""
    <h2>Wie zijn wij</h2>
    <p>Deze app is van {PUBLISHER_NL}, {ADDRESS}, Nederland. KvK-nummer {KVK}. Contact: {contact(app_key)}.</p>
""",
        f"""
    <h2>Who we are</h2>
    <p>This app is provided by {PUBLISHER_EN}, {ADDRESS}, the Netherlands. Chamber of Commerce (KvK) number {KVK}. Contact: {contact(app_key)}.</p>
""",
    )


def purchases_section(lang: str, app_key: str) -> str:
    """B: aankopen, terugbetaling en herroeping, in alle voorwaarden."""
    gp = '<a href="https://play.google.com/store/account">play.google.com/store/account</a>'
    ap = '<a href="https://reportaproblem.apple.com/">reportaproblem.apple.com</a>'
    return t(
        lang,
        f"""
    <h2>Aankopen, terugbetaling en herroeping</h2>
    <p>Aankopen in de app lopen via Google Play of de Apple App Store. Betaling, facturering en terugbetaling regelen zij volgens hun eigen voorwaarden. Een terugbetaling vraag je aan via Google Play ({gp} → Bestelgeschiedenis) of via Apple ({ap}).</p>
    <p>Digitale inhoud krijg je direct na de aankoop. Bij het kopen geef je uitdrukkelijk toestemming om meteen te leveren en verklaar je dat je daarmee afziet van het herroepingsrecht van 14 dagen (art. 6:230p BW). Je wettelijke rechten bij een gebrek blijven altijd gelden. Werkt een aankoop niet, mail ons dan via {contact(app_key)}; we helpen je.</p>
""",
        f"""
    <h2>Purchases, refunds and right of withdrawal</h2>
    <p>In-app purchases are processed by Google Play or the Apple App Store. They handle payment, invoicing and refunds under their own terms. To request a refund, use Google Play ({gp} → Order history) or Apple ({ap}).</p>
    <p>Digital content is delivered immediately after purchase. When you buy, you expressly consent to immediate delivery and acknowledge that you thereby lose your 14-day right of withdrawal (Article 16(m) of Directive 2011/83/EU; Article 6:230p of the Dutch Civil Code). Your statutory rights in case of a defect always remain. If a purchase does not work, email us at {contact(app_key)} and we will help you.</p>
""",
    )


def subscription_section(lang: str) -> str:
    """C: jaarabonnement Disco's lijst (alleen Kermis Sampler)."""
    return t(
        lang,
        """
    <h2>Abonnement Disco’s lijst</h2>
    <p>Disco’s lijst is een jaarabonnement dat automatisch verlengt, tenzij je het uiterlijk 24 uur voor het einde van de periode opzegt in Google Play of de App Store (Abonnementen). Na opzeggen blijft het actief tot het einde van de betaalde periode.</p>
""",
        """
    <h2>Disco’s lijst subscription</h2>
    <p>Disco’s lijst is an annual subscription that renews automatically unless you cancel it at least 24 hours before the end of the current period in Google Play or the App Store (Subscriptions). After cancelling, it stays active until the end of the paid period.</p>
""",
    )


APPLE_STD_EULA = "https://www.apple.com/legal/internet-services/itunes/dev/stdeula/"


def eula_section(lang: str) -> str:
    """Kermis Sampler: these terms are the EULA; Apple's standard EULA applies to App Store purchases (App Review 3.1.2, iOS build 58)."""
    link = f'<a href="{APPLE_STD_EULA}">{APPLE_STD_EULA}</a>'
    return t(
        lang,
        f"""
    <h2>Licentieovereenkomst (EULA)</h2>
    <p>Deze gebruiksvoorwaarden zijn de licentieovereenkomst voor eindgebruikers (End User License Agreement, EULA) van Kermis Sampler.</p>
    <p>Koop je in de app via Apple (de eenmalige aankoop Volledige versie of het jaarabonnement Disco’s lijst), dan geldt daarnaast de standaard licentieovereenkomst van Apple: {link}</p>
""",
        f"""
    <h2>Licence agreement (EULA)</h2>
    <p>These terms of use are the end user licence agreement (EULA) of Kermis Sampler.</p>
    <p>If you buy in the app through Apple (the one-time purchase Full version or the annual subscription Disco’s lijst), Apple’s standard licence agreement applies as well: {link}</p>
""",
    )


def rights_section(lang: str, app_key: str) -> str:
    """Notice-and-takedown (Kermis Sampler, Johan 25-10-2026); same text as the app (licRights)."""
    return t(
        lang,
        f"""    <h2>Rechten van anderen</h2>
    <p>We hebben ons best gedaan om alle rechthebbenden te achterhalen. Alle merken en geluiden zijn eigendom van hun respectieve eigenaren. Vind je dat materiaal in deze app inbreuk maakt op jouw rechten? Mail dan naar {contact(app_key)} met uitleg en bewijs. We nemen zo snel mogelijk contact met je op en verwijderen het materiaal indien nodig.</p>

""",
        f"""    <h2>Rights of others</h2>
    <p>We have done our best to trace all rights holders. All trademarks and sounds are the property of their respective owners. Do you believe material in this app infringes your rights? Email {contact(app_key)} with an explanation and proof. We will contact you as soon as possible and remove the material if necessary.</p>

""",
    )


def coins_section(lang: str) -> str:
    """D: virtuele munten (Op de Kermis!)."""
    return t(
        lang,
        """
    <h2>Munten</h2>
    <p>Munten zijn alleen spelmunten. Ze hebben geen geldwaarde, je kunt ze niet inwisselen, overdragen of terugbetaald krijgen (behalve als de wet dat verplicht), en je kunt er geen echte prijzen mee winnen. Gekochte munten worden direct bijgeschreven en zijn verbruikbaar. Ze staan alleen op je toestel, dus je raakt ze kwijt als je de app verwijdert of de appgegevens wist. Alleen de Volledige versie kun je herstellen via ‘Aankoop herstellen’.</p>
""",
        """
    <h2>Coins</h2>
    <p>Coins are in-game coins only. They have no monetary value; you cannot exchange, transfer or get a refund for them (unless the law requires it), and you cannot win real prizes with them. Purchased coins are credited immediately and are consumable. They are stored only on your device, so you lose them if you delete the app or clear its app data. Only the Full version can be restored, via ‘Restore purchase’ (‘Aankoop herstellen’).</p>
""",
    )


def delete_data_section(lang: str, with_ads: bool, app_key: str) -> str:
    """E: gegevens verwijderen en je rechten (Bingo, Op de Kermis!; Sampler zonder advertentiedeel)."""
    if lang == "nl":
        ads = ""
        if with_ads:
            ads = f"""
      <li><strong>Toestemming voor advertenties intrekken of wijzigen:</strong> in de app via Instellingen → <em>Privacy-instellingen</em>.</li>
      <li><strong>Advertentie-ID resetten:</strong> Android: Instellingen → Google → Advertenties; iPhone: Instellingen → Privacy en beveiliging → Tracking.</li>
      <li>Hoe Google advertentiegegevens gebruikt: <a href="https://policies.google.com/technologies/ads">policies.google.com/technologies/ads</a>.</li>"""
        return f"""
    <h2>Je gegevens verwijderen en je rechten</h2>
    <ul>
      <li><strong>Alles op je toestel wissen:</strong> verwijder de app of wis de appgegevens. Wij bewaren geen gegevens op eigen servers, dus daarmee is alles weg.</li>{ads}
    </ul>
    <p>Je hebt onder de AVG recht op inzage, rectificatie, verwijdering, beperking, bezwaar en overdraagbaarheid, voor zover wij gegevens van je verwerken. Mail daarvoor naar {contact(app_key)}; we reageren binnen 30 dagen. Je kunt ook een klacht indienen bij de {AP_LINK_NL}.</p>
"""
    ads = ""
    if with_ads:
        ads = """
      <li><strong>Withdraw or change ad consent:</strong> in the app via Settings → <em>Privacy-instellingen</em> (privacy settings).</li>
      <li><strong>Reset your advertising ID:</strong> Android: Settings → Google → Ads; iPhone: Settings → Privacy &amp; Security → Tracking.</li>
      <li>How Google uses advertising data: <a href="https://policies.google.com/technologies/ads">policies.google.com/technologies/ads</a>.</li>"""
    return f"""
    <h2>Deleting your data and your rights</h2>
    <ul>
      <li><strong>Erase everything on your device:</strong> delete the app or clear its app data. We do not keep data on our own servers, so this removes everything.</li>{ads}
    </ul>
    <p>Under the GDPR you have the right of access, rectification, erasure, restriction, objection and data portability, to the extent we process your data. Email {contact(app_key)}; we respond within 30 days. You can also lodge a complaint with the {AP_LINK_EN}.</p>
"""


def camera_section(lang: str) -> str:
    """F: voorcamera in de schiettent (Op de Kermis!)."""
    return t(
        lang,
        """
    <h2>Camera (kermisfoto)</h2>
    <p>In de schiettent kun je een kermisfoto maken met de voorcamera. De app vraagt daar eerst toestemming voor. De foto blijft op je toestel, wordt niet geüpload en wij zien hem niet. Weiger je de toestemming, dan speel je gewoon zonder foto.</p>
""",
        """
    <h2>Camera (fairground photo)</h2>
    <p>In the shooting gallery you can take a fairground photo with the front camera. The app asks for your permission first. The photo stays on your device, is not uploaded and we never see it. If you decline, you simply play without a photo.</p>
""",
    )


def store_purchase_section(app_key: str, lang: str) -> str:
    """Privacy: welke aankoopgegevens via Google Play / App Store lopen."""
    products = {
        "kermissampler": t(
            lang,
            "<code>full_unlock</code> (eenmalige volledige versie) en <code>disco_lijst_jaar</code> (jaarabonnement)",
            "<code>full_unlock</code> (one-time full version) and <code>disco_lijst_jaar</code> (annual subscription)",
        ),
        "kermisbingo": t(
            lang,
            "<code>full_unlock</code> (eenmalige volledige versie)",
            "<code>full_unlock</code> (one-time full version)",
        ),
        "opdekermis": t(
            lang,
            "<code>full_unlock</code> (Volledige versie) en de muntpakketten <code>munten_25</code>, <code>munten_75</code> en <code>munten_200</code>",
            "<code>full_unlock</code> (Full version) and the coin packs <code>munten_25</code>, <code>munten_75</code> and <code>munten_200</code>",
        ),
    }[app_key]
    return t(
        lang,
        f"""
    <h2>Aankopen via Google Play en de App Store</h2>
    <p>In-app aankopen lopen via <strong>Google Play</strong> (Android) of de <strong>Apple App Store</strong> (iOS): {products}. Google of Apple verwerkt betaling en facturering; wij krijgen geen naam, adres, e-mailadres of betaalgegevens. De app vraagt de store alleen of een aankoop actief is en bewaart dat lokaal op je toestel.</p>
    <p><strong>Verwerker:</strong> Google of Apple, voor betaling en aankoopcontrole. <strong>Rechtsgrond:</strong> uitvoering van de overeenkomst (levering van de digitale inhoud). <strong>Bewaartermijn:</strong> bij Google of Apple volgens hun beleid ({GOOGLE_PRIVACY}, {APPLE_PRIVACY}); in de app tot je hem verwijdert of de appgegevens wist.</p>
""",
        f"""
    <h2>Purchases via Google Play and the App Store</h2>
    <p>In-app purchases are handled by <strong>Google Play</strong> (Android) or the <strong>Apple App Store</strong> (iOS): {products}. Google or Apple processes payment and billing; we never receive your name, address, email address or payment details. The app only asks the store whether a purchase is active and stores that locally on your device.</p>
    <p><strong>Processor:</strong> Google or Apple, for payment and purchase validation. <strong>Legal basis:</strong> performance of a contract (delivery of digital content). <strong>Retention:</strong> at Google or Apple under their policies ({GOOGLE_PRIVACY}, {APPLE_PRIVACY}); in the app until you delete it or clear its app data.</p>
""",
    )


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


def legal_footer(depth: int, lang: str, app_key: str) -> str:
    home = depth_path(depth, "index.html")
    footer_links = f"""
        <a href="../../../privacy/kermissampler/{lang}/">Kermis Sampler — privacy</a>
        <a href="../../../privacy/kermisbingo/{lang}/">Kermis Bingo — privacy</a>
        <a href="../../../privacy/opdekermis/{lang}/">Op de Kermis! — privacy</a>
"""
    if lang == "nl":
        copy = "© 2026 Kermis Software · Deze site gebruikt geen trackers of cookies."
    else:
        copy = "© 2026 Kermis Software · This site uses no trackers or cookies."
    return f"""
  </main>
  <footer class="site-footer">
    <div class="inner">
      <div>
        <strong>Johan C. Ordelman jr. V.O.F.</strong> · Kermis Software · {ADDRESS} · Nederland / Netherlands · KvK {KVK}<br />
        {contact(app_key)}
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



def admob_section(lang: str) -> str:
    return t(
        lang,
        f"""
    <h2>Beloningsfilmpjes (Google AdMob)</h2>
    <p>In de gratis versie kun je zelf een kort beloningsfilmpje starten. Er zijn geen banners en geen filmpjes bij het opstarten. <strong>Google AdMob</strong> verwerkt daarbij onder meer:</p>
    <ul>
      <li>het advertentie-ID van je toestel;</li>
      <li>je IP-adres;</li>
      <li>apparaattype en -gegevens;</li>
      <li>interacties met de advertentie (weergave, klik).</li>
    </ul>
    <p><strong>Doel:</strong> een advertentie tonen, meten en fraude of misbruik beperken.<br />
    <strong>Verwerker:</strong> Google (AdMob en het User Messaging Platform voor toestemming; op iOS geldt ook Apple’s App Tracking Transparency).<br />
    <strong>Rechtsgrond:</strong> je <strong>toestemming</strong> (EU/VK), die de app vraagt vóór gepersonaliseerde of meetbare advertentieverwerking.<br />
    <strong>Bewaartermijn:</strong> volgens het {GOOGLE_PRIVACY.replace('>policies.google.com/privacy<', '>privacybeleid van Google<')}; wij bewaren deze advertentiegegevens niet op eigen servers.</p>
    <p>Zonder toestemming of zonder dat je een filmpje start, worden voor dat filmpje geen advertentiegegevens verwerkt. Wij verkopen geen gegevens.</p>
""",
        f"""
    <h2>Rewarded videos (Google AdMob)</h2>
    <p>In the free version you can choose to start a short rewarded video. There are no banners and no videos on launch. <strong>Google AdMob</strong> processes, among other things:</p>
    <ul>
      <li>your device’s advertising ID;</li>
      <li>your IP address;</li>
      <li>device type and characteristics;</li>
      <li>ad interactions (views, clicks).</li>
    </ul>
    <p><strong>Purpose:</strong> showing and measuring an ad and limiting fraud or abuse.<br />
    <strong>Processor:</strong> Google (AdMob and the User Messaging Platform for consent; on iOS, Apple’s App Tracking Transparency also applies).<br />
    <strong>Legal basis:</strong> your <strong>consent</strong> (EU/UK), which the app asks for before any personalised or measurable ad processing.<br />
    <strong>Retention:</strong> as set out in {GOOGLE_PRIVACY.replace('>policies.google.com/privacy<', '>Google’s privacy policy<')}; we do not store this ad data on our own servers.</p>
    <p>Without consent, or if you do not start a video, no ad data is processed for that video. We do not sell data.</p>
""",
    )


def privacy_sampler(lang: str) -> str:
    key = "kermissampler"
    if lang == "nl":
        body = f"""
    <h1>Privacyverklaring</h1>
    <p>Deze verklaring geldt voor de Android- en iOS-app <strong>Kermis Sampler</strong> ({APPS[key]['package']}), een soundboard voor thuisgebruik. Verwerkingsverantwoordelijke: {PUBLISHER_NL}.</p>
{company_section(lang, key)}
    <h2>Welke gegevens worden verwerkt?</h2>
    <p><strong>Wij verzamelen geen persoonsgegevens op eigen servers.</strong> Er is geen account. De app bevat <strong>geen advertenties</strong>, <strong>geen analytics</strong> en <strong>geen tracking-SDK</strong> (geen Firebase Analytics, crashrapportage of advertentietracking).</p>
    <p>De app bewaart gegevens <em>alleen op je toestel</em> (onder meer WebView-opslag / IndexedDB), bijvoorbeeld:</p>
    <ul>
      <li>instellingen (taal, uiterlijk, volume, mixer);</li>
      <li>soundboard-pads en gekoppelde lokale audiobestanden waartoe je toegang geeft;</li>
      <li>afspeellijsten en wachtrijen die je importeert of plakt;</li>
      <li>back-ups die je zelf exporteert;</li>
      <li>of de app na een store-aankoop is ontgrendeld.</li>
    </ul>
{store_purchase_section(key, lang)}
    <h2>Microfoon en bestanden</h2>
    <p><strong>Microfoon</strong>: alleen als je de talk-over-functie gebruikt; het besturingssysteem vraagt dan toestemming. Audio wordt niet opgenomen of naar ons geüpload.</p>
    <p><strong>Bestanden</strong>: via de systeemkiezer als je MP3/WAV-bestanden of mappen kiest; alleen op het toestel.</p>

    <h2>Diensten van derden (internet)</h2>
    <p>Bij sommige functies maakt de app verbinding met diensten van derden. Zij kunnen daarbij onder meer je <strong>IP-adres</strong>, apparaat- en verbindingsgegevens en wat je zoekt of afspeelt verwerken volgens hun eigen beleid. Dat gebeurt alleen als je de functie start:</p>
    <ul>
      <li><strong>YouTube en YouTube Music</strong> (zoeken en afspelen): <a href="https://policies.google.com/privacy">privacybeleid Google/YouTube</a></li>
      <li><strong>Spotify</strong> (webspeler in de app): <a href="https://www.spotify.com/legal/privacy-policy/">privacybeleid Spotify</a></li>
      <li><strong>Deezer</strong> (webspeler): <a href="https://www.deezer.com/legal/privacy">privacybeleid Deezer</a></li>
      <li><strong>SoundCloud</strong> (webspeler): <a href="https://soundcloud.com/pages/privacy">privacybeleid SoundCloud</a></li>
      <li><strong>Hugging Face</strong> (eenmalig downloaden van het Splitsen-model): <a href="https://huggingface.co/privacy">privacybeleid Hugging Face</a></li>
      <li><strong>GitHub</strong>: bij <strong>Lijst van vandaag</strong> (Disco’s lijst) haalt de app een CSV op van <code>gist.githubusercontent.com</code>: <a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement">privacybeleid GitHub</a></li>
    </ul>
    <p><strong>Rechtsgrond:</strong> je keuze om de functie te gebruiken (uitvoering van de dienst die je start) en, voor de microfoon, je toestemming via het besturingssysteem. <strong>Bewaartermijn:</strong> bij ons niet op servers; bij derden volgens hun privacybeleid.</p>

    <h2>Multiplayer (WebRTC)</h2>
    <p>Voor multiplayer gebruikt de app <strong>WebRTC</strong>. Om de verbinding op te zetten raadpleegt de app STUN-servers van <strong>Google</strong> (<code>stun.l.google.com</code>) en <strong>Cloudflare</strong> (<code>stun.cloudflare.com</code>); die zien daarbij je <strong>IP-adres</strong>. Zie het <a href="https://policies.google.com/privacy">privacybeleid van Google</a> en het <a href="https://www.cloudflare.com/privacypolicy/">privacybeleid van Cloudflare</a>.</p>
    <p>De audio-/datasessie loopt daarna <strong>rechtstreeks tussen de apparaten</strong> (peer-to-peer). Het andere apparaat ziet daardoor ook je IP-adres, en jij dat van de ander. Wij ontvangen die sessie niet op een eigen server.</p>
{delete_data_section(lang, with_ads=False, app_key=key)}
    <h2>Kinderen</h2>
    <p>De app is niet speciaal bedoeld voor kinderen en bevat geen advertenties.</p>
"""
    else:
        body = f"""
    <h1>Privacy policy</h1>
    <p>This policy applies to the Android and iOS app <strong>Kermis Sampler</strong> ({APPS[key]['package']}), a soundboard for home use. Controller: {PUBLISHER_EN}.</p>
{company_section(lang, key)}
    <h2>What data is processed?</h2>
    <p><strong>We do not collect personal data on our own servers.</strong> There is no account. The app contains <strong>no ads</strong>, <strong>no analytics</strong> and <strong>no tracking SDK</strong> (no Firebase Analytics, crash reporting or ad tracking).</p>
    <p>The app stores data <em>only on your device</em> (including WebView storage / IndexedDB), for example:</p>
    <ul>
      <li>settings (language, appearance, volume, mixer);</li>
      <li>soundboard pads and the local audio files you give access to;</li>
      <li>playlists and queues you import or paste;</li>
      <li>backups you export yourself;</li>
      <li>whether the app has been unlocked after a store purchase.</li>
    </ul>
{store_purchase_section(key, lang)}
    <h2>Microphone and files</h2>
    <p><strong>Microphone</strong>: only when you use talk-over; the operating system asks for permission. Audio is not recorded or uploaded to us.</p>
    <p><strong>Files</strong>: via the system picker when you choose MP3/WAV files or folders; on the device only.</p>

    <h2>Third-party services (internet)</h2>
    <p>Some features connect to third-party services. They may process your <strong>IP address</strong>, device and connection data, and what you search for or play, under their own policies. This only happens when you start the feature:</p>
    <ul>
      <li><strong>YouTube and YouTube Music</strong> (search and playback): <a href="https://policies.google.com/privacy">Google/YouTube privacy policy</a></li>
      <li><strong>Spotify</strong> (in-app web player): <a href="https://www.spotify.com/legal/privacy-policy/">Spotify privacy policy</a></li>
      <li><strong>Deezer</strong> (web player): <a href="https://www.deezer.com/legal/privacy">Deezer privacy policy</a></li>
      <li><strong>SoundCloud</strong> (web player): <a href="https://soundcloud.com/pages/privacy">SoundCloud privacy policy</a></li>
      <li><strong>Hugging Face</strong> (one-time download of the Splitsen model): <a href="https://huggingface.co/privacy">Hugging Face privacy policy</a></li>
      <li><strong>GitHub</strong>: <strong>Lijst van vandaag</strong> (Disco’s lijst) fetches a CSV from <code>gist.githubusercontent.com</code>: <a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement">GitHub privacy statement</a></li>
    </ul>
    <p><strong>Legal basis:</strong> your choice to use the feature (performance of the service you start) and, for the microphone, your consent via the operating system. <strong>Retention:</strong> not on our servers; at third parties under their privacy policies.</p>

    <h2>Multiplayer (WebRTC)</h2>
    <p>Multiplayer uses <strong>WebRTC</strong>. To set up the connection, the app contacts STUN servers operated by <strong>Google</strong> (<code>stun.l.google.com</code>) and <strong>Cloudflare</strong> (<code>stun.cloudflare.com</code>), which see your <strong>IP address</strong>. See <a href="https://policies.google.com/privacy">Google’s privacy policy</a> and <a href="https://www.cloudflare.com/privacypolicy/">Cloudflare’s privacy policy</a>.</p>
    <p>The audio/data session then runs <strong>directly between the devices</strong> (peer-to-peer), so the other device can see your IP address and you can see theirs. We do not receive that session on our own servers.</p>
{delete_data_section(lang, with_ads=False, app_key=key)}
    <h2>Children</h2>
    <p>The app is not specifically aimed at children and contains no ads.</p>
"""
    return meta_line(key, lang) + body


def privacy_bingo(lang: str) -> str:
    key = "kermisbingo"
    if lang == "nl":
        body = f"""
    <h1>Privacyverklaring</h1>
    <p>Deze verklaring geldt voor <strong>Kermis Bingo</strong> ({APPS[key]['package']}) op Android en iOS. Verwerkingsverantwoordelijke: {PUBLISHER_NL}.</p>
{company_section(lang, key)}
    <h2>Geen account, spel lokaal</h2>
    <p>Er is geen account en de app vraagt niet om je naam of e-mailadres. Trekken, kaarten en instellingen werken offline. Wat je invoert (trekking, rondes, kaartreeks, weergave, stem, eventueel een logo) staat in lokale opslag op je toestel en gaat niet naar ons.</p>
{store_purchase_section(key, lang)}{admob_section(lang)}{delete_data_section(lang, with_ads=True, app_key=key)}
    <h2>Kinderen</h2>
    <p>De app is niet speciaal bedoeld voor kinderen. Zonder je toestemming tonen we geen gepersonaliseerde advertenties.</p>
"""
    else:
        body = f"""
    <h1>Privacy policy</h1>
    <p>This policy applies to <strong>Kermis Bingo</strong> ({APPS[key]['package']}) on Android and iOS. Controller: {PUBLISHER_EN}.</p>
{company_section(lang, key)}
    <h2>No account, local play</h2>
    <p>There is no account and the app does not ask for your name or email address. Drawing numbers, cards and settings work offline. What you enter (draw, rounds, card series, display, voice, optionally a logo) stays in local storage on your device and is not sent to us.</p>
{store_purchase_section(key, lang)}{admob_section(lang)}{delete_data_section(lang, with_ads=True, app_key=key)}
    <h2>Children</h2>
    <p>The app is not specifically aimed at children. Without your consent we do not show personalised ads.</p>
"""
    return meta_line(key, lang) + body


def privacy_opdekermis(lang: str) -> str:
    key = "opdekermis"
    if lang == "nl":
        body = f"""
    <h1>Privacyverklaring</h1>
    <p>Deze verklaring geldt voor de kermisgame <strong>Op de Kermis!</strong> ({APPS[key]['package']}) op Android en iOS. Verwerkingsverantwoordelijke: {PUBLISHER_NL}.</p>
{company_section(lang, key)}
    <h2>Geen account, voortgang lokaal</h2>
    <p>Er is geen account. Spelvoortgang, munten en je verzameling staan <strong>alleen op je toestel</strong>; wij ontvangen die gegevens niet op een server.</p>
{camera_section(lang)}{store_purchase_section(key, lang)}{admob_section(lang)}
    <h2>Link naar kermis.nu</h2>
    <p>De app heeft een knop die <strong>kermis.nu</strong> in je browser opent. Die website heeft een eigen privacybeleid; wij beheren die site niet en weten niet welke gegevens je daar achterlaat.</p>
{delete_data_section(lang, with_ads=True, app_key=key)}
    <h2>Leeftijd</h2>
    <p>Op de Kermis! is bedoeld voor spelers van 13 jaar en ouder en is niet op kinderen gericht. Zonder je toestemming tonen we geen gepersonaliseerde advertenties.</p>
"""
    else:
        body = f"""
    <h1>Privacy policy</h1>
    <p>This policy applies to the fairground game <strong>Op de Kermis!</strong> ({APPS[key]['package']}) on Android and iOS. Controller: {PUBLISHER_EN}.</p>
{company_section(lang, key)}
    <h2>No account, progress stays local</h2>
    <p>There is no account. Game progress, coins and your collection are stored <strong>only on your device</strong>; we do not receive that data on a server.</p>
{camera_section(lang)}{store_purchase_section(key, lang)}{admob_section(lang)}
    <h2>Link to kermis.nu</h2>
    <p>The app has a button that opens <strong>kermis.nu</strong> in your browser. That website has its own privacy policy; we do not operate it and do not know what data you leave there.</p>
{delete_data_section(lang, with_ads=True, app_key=key)}
    <h2>Age</h2>
    <p>Op de Kermis! is intended for players aged 13 and over and is not directed at children. Without your consent we do not show personalised ads.</p>
"""
    return meta_line(key, lang) + body


PRIVACY_BODIES = {
    "kermissampler": privacy_sampler,
    "kermisbingo": privacy_bingo,
    "opdekermis": privacy_opdekermis,
}


def privacy_body(app_key: str, lang: str) -> str:
    return PRIVACY_BODIES[app_key](lang)


def terms_body(app_key: str, lang: str) -> str:
    """Eén opbouw voor alle voorwaarden; app-specifieke blokken (C, D) waar ze horen."""
    name = app_name(app_key, lang)
    pkg = APPS[app_key]["package"]
    if lang == "nl":
        intro = f"""
    <h1>Gebruiksvoorwaarden</h1>
    <p>Deze voorwaarden gelden voor het gebruik van <strong>{name}</strong> ({pkg}).</p>
"""
        use = """
    <h2>Gebruik</h2>
    <p>De app is bedoeld voor amusement en privégebruik. Je gebruikt de app in overeenstemming met de regels van Google Play of de App Store.</p>
"""
        if app_key == "opdekermis":
            use += """
    <h2>Amusement, geen gokken</h2>
    <p>De game is entertainment. Er is geen inzet van echt geld en er wordt nooit echt geld of een echte prijs uitgekeerd.</p>
"""
        tail = """
    <h2>Aansprakelijkheid</h2>
    <p>Voor zover de wet dat toestaat, is onze aansprakelijkheid beperkt tot het bedrag dat je in de twaalf maanden vóór de claim voor deze app via de store hebt betaald, met een maximum van € 50. Wij zijn niet aansprakelijk voor indirecte schade of verlies van gegevens op je toestel. Dwingend consumentenrecht gaat altijd voor.</p>
    <h2>Toepasselijk recht</h2>
    <p>Op deze voorwaarden is Nederlands recht van toepassing. Geschillen worden voorgelegd aan de bevoegde rechter in Nederland, onverminderd je rechten als consument.</p>
"""
    else:
        intro = f"""
    <h1>Terms of use</h1>
    <p>These terms apply to your use of <strong>{name}</strong> ({pkg}).</p>
"""
        use = """
    <h2>Use</h2>
    <p>The app is intended for entertainment and personal use. You use it in line with the rules of Google Play or the App Store.</p>
"""
        if app_key == "opdekermis":
            use += """
    <h2>Entertainment, not gambling</h2>
    <p>The game is entertainment. There is no real-money wagering, and no real money or real prizes are ever paid out.</p>
"""
        tail = """
    <h2>Liability</h2>
    <p>To the extent permitted by law, our liability is limited to the amount you paid for this app through the store in the twelve months before the claim, up to a maximum of € 50. We are not liable for indirect loss or for loss of data on your device. Mandatory consumer law always takes precedence.</p>
    <h2>Governing law</h2>
    <p>These terms are governed by Dutch law. Disputes are submitted to the competent court in the Netherlands, without prejudice to your rights as a consumer.</p>
"""
    if app_key == "kermissampler":
        intro = intro.replace("<h1>Gebruiksvoorwaarden</h1>", "<h1>Gebruiksvoorwaarden (EULA)</h1>").replace(
            "<h1>Terms of use</h1>", "<h1>Terms of Use (EULA)</h1>"
        )
        intro += eula_section(lang)
    extra = ""
    if app_key == "opdekermis":
        extra += coins_section(lang)
    extra += purchases_section(lang, app_key)
    if app_key == "kermissampler":
        extra += subscription_section(lang)
        extra += rights_section(lang, app_key)
    return meta_line(app_key, lang) + intro + company_section(lang, app_key) + use + extra + tail



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
    nl = privacy_sampler("nl")
    en = privacy_sampler("en")
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
        <strong>Johan C. Ordelman jr. V.O.F.</strong> · Kermis Software · {ADDRESS} · Nederland / Netherlands · KvK {KVK}<br />
        {contact("kermissampler")}
      </div>
      <div class="links links-legal">
        <a href="privacy/kermissampler/nl/">Kermis Sampler — privacy</a>
        <a href="privacy/kermisbingo/nl/">Kermis Bingo — privacy</a>
        <a href="privacy/opdekermis/nl/">Op de Kermis! — privacy</a>
        <a href="index.html">Home</a>
      </div>
      <p class="muted" style="margin:0;font-size:0.8rem">
        <span class="lang-nl">© 2026 Kermis Software · Deze site gebruikt geen trackers of cookies.</span>
        <span class="lang-en">© 2026 Kermis Software · This site uses no trackers or cookies.</span>
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
                    + legal_footer(depth, lang, app_key)
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
