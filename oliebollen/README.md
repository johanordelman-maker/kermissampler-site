# De Oliebollen Bakkerij — klantenapp (klikbaar ontwerp v2.0)

Mobiele webapp voor de oliebollenkraam (Woonboulevard Veenendaal), opgebouwd naar het
voorbeeld van grote fastfood-apps: tabbalk met **Home · Sparen · Acties · Menu · Meer**,
punten sparen via een persoonlijke QR-code, acties activeren, beloningen inwisselen met een code,
en vooraf laten klaarzetten. Eigen huisstijl (bordeaux, goud, crème), eigen illustraties.

Live: https://johanordelman-maker.github.io/kermissampler-site/oliebollen/
Vorige versie (alleen spaarkaart): .../oliebollen/v1/

## Wat zit erin
- **Home**: actie van de week (hero), puntenstand met balk tot de volgende beloning, deals van de week, menu-teaser, uitleg sparen, open/gesloten.
- **Sparen**: persoonlijke QR + klantcode (OB-xxxx-xxxx), 10 punten per euro, 50 welkomstpunten bij de eerste scan, beloningen inwisselen → code B-xxxx met QR (30 dagen geldig), lijst "Mijn codes".
- **Acties**: kaarten met *Activeer* → code A-xxxx met QR, één keer te gebruiken.
- **Menu**: categorieën (oliebollen, krentenbollen, appelflappen, berlinerbollen, drinken) met **voorbeeldprijzen**, + en − knoppen, **Klaarzetten** met ophaaltijd → code K-xxxx; betalen bij de kraam.
- **Meer**: locatie + route, openingstijden (voorbeeld), meldingen-schakelaar, voornaam, privacy, kraam-modus, demo resetten.
- **Kraam-modus** (pincode, demo `1234`): klant scannen (camera via BarcodeDetector, Chrome/Android) of code tikken → bedrag kiezen → punten. Code inwisselen (beloning/actie/bestelling), lijst bestellingen (Opgehaald), nieuwe actie plaatsen.
- Offline-first (service worker), installeerbaar (manifest), geen externe scripts, geen tracking, geen cookies.

## Beperking van dit ontwerp
Alle gegevens staan in `localStorage` van **één toestel**. De kraam-modus kent dus alleen de klant
op hetzelfde toestel; punten, codes en acties gaan niet tussen telefoons heen en weer.
Ook pushberichten en echte bestellingen hebben een server nodig.

## Wat nodig is voor een echte versie
1. **Backend** (klanten, punten, codes, acties, bestellingen; pincode per medewerker; misbruikcontrole):
   - **Supabase gratis tier** (Postgres + auth + realtime, 500 MB) — voorkeur, makkelijkst.
   - **Firebase** Spark (gratis): Firestore + Auth + Cloud Messaging voor push.
   - **Cloudflare Workers + D1** (gratis tier) — goedkoopst op schaal, iets meer werk.
   - Of PocketBase op een eigen pc (gratis, maar die pc moet altijd aan staan).
   Kosten bij een kraam-volume blijven naar verwachting binnen de gratis tiers.
2. **Push**: Web Push (gratis) of Firebase Cloud Messaging.
3. **Android-shell**: Capacitor of een TWA (Trusted Web Activity, via Bubblewrap) om deze webapp als
   Play-app te verpakken; iOS via Capacitor. Store-accounts zijn er al (Kermis software).
4. **Kraam-toestel**: een goedkope Android-telefoon/tablet met camera bij de kassa (scannen werkt in Chrome).
5. Echte prijzen, tijden, acties en beloningen + privacyverklaring (AVG) zodra er een server is.
