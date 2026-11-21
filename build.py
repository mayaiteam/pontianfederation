#!/usr/bin/env python3
"""Builds the static draft site into ./dist from the content below.
Run: python3 build.py   (no dependencies). Every text has an English and a Greek version.
"""
import os, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(HERE, "dist")

def t(en, el, tag="span"):
    return f'<{tag} lang="en">{en}</{tag}><{tag} lang="el">{el}</{tag}>'

NAV = [
    ("index.html", "Home", "Αρχική"),
    ("about.html", "About", "Ποιοι είμαστε"),
    ("associations.html", "Member Associations", "Σωματεία-Μέλη"),
    ("events.html", "Events", "Εκδηλώσεις"),
    ("news.html", "News", "Νέα"),
    ("contact.html", "Contact", "Επικοινωνία"),
]

def page(fname, title_en, title_el, body):
    nav = "".join(
        f'<li><a href="{h}"{" aria-current=\"page\"" if h == fname else ""}>{t(en, el)}</a></li>'
        for h, en, el in NAV)
    site_en = "Federation of Pontian Associations of Australia"
    site_el = "Ομοσπονδία Ποντιακών Σωματείων Αυστραλίας"
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title_en} · {site_en}</title>
<meta name="title-en" content="{title_en} · {site_en}">
<meta name="title-el" content="{title_el} · {site_el}">
<meta name="description" content="The Federation of Pontian Associations of Australia, est. 1989, unites Pontian Greek associations across Australia.">
<link rel="icon" href="assets/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans:wght@400;500;600;700&family=Noto+Serif:wght@500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<div class="top"><div class="wrap">
  <span>{t("Est. 1989 · Uniting Pontian Hellenism in Australia", "Ιδρύθηκε το 1989 · Ενώνοντας τον Ποντιακό Ελληνισμό της Αυστραλίας")}</span>
  <span class="langs"><button data-lang="en" aria-pressed="true">EN</button><button data-lang="el" aria-pressed="false">ΕΛ</button></span>
</div></div>
<header class="site"><div class="wrap">
  <a class="brand" href="index.html"><img src="assets/logo-sm.png" alt="Federation logo"><span><b>{t(site_en, site_el)}</b><small>{t("Ομοσπονδία Ποντιακών Σωματείων Αυστραλίας", "Federation of Pontian Associations of Australia")}</small></span></a>
  <button class="menu-btn" aria-expanded="false">{t("Menu", "Μενού")}</button>
  <nav class="main"><ul>{nav}</ul></nav>
</div></header>
<main>
{body}
</main>
<footer class="site"><div class="wrap">
  <div class="cols">
    <div class="brandf"><img src="assets/logo-sm.png" alt=""><div><b style="color:#fff">{t(site_en, site_el)}</b><br>{t("The national body of Pontian Greek associations in Australia since 1989.", "Το εθνικό όργανο των Ποντιακών Σωματείων της Αυστραλίας από το 1989.")}</div></div>
    <div><h4>{t("Explore", "Πλοήγηση")}</h4><ul>{"".join(f'<li><a href="{h}">{t(en, el)}</a></li>' for h, en, el in NAV[1:])}</ul></div>
    <div><h4>{t("Connect", "Επικοινωνία")}</h4><ul><li><a href="contact.html">{t("Contact us", "Επικοινωνήστε μαζί μας")}</a></li><li><a href="mailto:info@pontos.org.au">info@pontos.org.au</a></li><li><a href="https://www.instagram.com/pontian_federation_aus_/" target="_blank" rel="noopener">Instagram</a></li><li><a href="https://www.facebook.com/federation.pontian.associations.australia" target="_blank" rel="noopener">Facebook</a></li></ul></div>
  </div>
  <div class="fine">© 2026 {t(site_en, site_el)}. {t("Draft site for review.", "Πρόχειρη έκδοση προς έγκριση.")}</div>
</div></footer>
<script src="assets/site.js"></script>
</body>
</html>'''

import json, glob, html as _html
from datetime import date as _date

def load(path):
    with open(os.path.join(HERE, "content", path), encoding="utf-8") as fh:
        return json.load(fh)

def esc(x):
    return _html.escape(x or "", quote=True)

def paras(text):
    return "".join(f"<p>{esc(p.strip())}</p>" for p in (text or "").split("\n\n") if p.strip())

MONTHS_EN = ["January","February","March","April","May","June","July","August","September","October","November","December"]
MONTHS_EL = ["Ιανουάριος","Φεβρουάριος","Μάρτιος","Απρίλιος","Μάιος","Ιούνιος","Ιούλιος","Αύγουστος","Σεπτέμβριος","Οκτώβριος","Νοέμβριος","Δεκέμβριος"]

def month_label(iso):
    d = _date.fromisoformat(str(iso)[:10])
    return t(f"{MONTHS_EN[d.month-1]} {d.year}", f"{MONTHS_EL[d.month-1]} {d.year}")

ASSOCIATIONS = load("associations.json")["associations"]
COMMITTEE_DATA = load("committee.json")
COMMITTEE = COMMITTEE_DATA["members"]
NEWS_LIST = sorted((json.load(open(f, encoding="utf-8")) for f in glob.glob(os.path.join(HERE, "content", "news", "*.json"))),
                   key=lambda n: str(n["date"]), reverse=True)
EVENT_LIST = sorted((json.load(open(f, encoding="utf-8")) for f in glob.glob(os.path.join(HERE, "content", "events", "*.json"))),
                    key=lambda e: e.get("order", 99))

def assoc_card(a):
    where = " · ".join(x for x in (esc(a.get("city")), esc(a.get("state"))) if x) or "—"
    link = (f'<p><a href="{esc(a["website"])}" target="_blank" rel="noopener">{t("Visit website", "Ιστοσελίδα")} →</a></p>'
            if a.get("website") else "")
    return f'<div class="card"><div class="meta">{where}</div><h3>{t(esc(a["name_en"]), esc(a["name_el"]))}</h3>{link}</div>'

def person_card(m):
    city = f' · {esc(m["city"])}' if m.get("city") else ""
    return f'<div class="card"><b>{esc(m["name"])}</b><span>{t(esc(m["role_en"]), esc(m["role_el"]))}{city}</span></div>'

def event_card(e):
    link = (f'<p><a href="{esc(e["link"])}" target="_blank" rel="noopener">{t("Details &amp; tickets", "Πληροφορίες &amp; εισιτήρια")} →</a></p>'
            if e.get("link") else "")
    return (f'<div class="card"><div class="meta">{t(esc(e["when_en"]), esc(e["when_el"]))}</div>'
            f'<h3>{t(esc(e["title_en"]), esc(e["title_el"]))}</h3><p>{t(esc(e["description_en"]), esc(e["description_el"]))}</p>{link}</div>')

def news_teaser(n):
    return (f'<div class="card"><div class="meta">{month_label(n["date"])}</div><h3>{t(esc(n["title_en"]), esc(n["title_el"]))}</h3>'
            f'<p><a href="news.html">{t("Read more", "Περισσότερα")} →</a></p></div>')

def news_article(n):
    return (f'<article class="card" style="margin-bottom:22px"><div class="meta">{month_label(n["date"])}</div>'
            f'<h2>{t(esc(n["title_en"]), esc(n["title_el"]))}</h2>'
            f'<div lang="en">{paras(n["body_en"])}</div><div lang="el">{paras(n["body_el"])}</div></article>')

HOME = f'''
<section class="hero"><div class="wrap">
  <div>
    <div class="eyebrow">{t("Since 1989", "Από το 1989")}</div>
    <h1>{t("Keeping the spirit of Pontos alive in Australia", "Κρατάμε ζωντανή την ψυχή του Πόντου στην Αυστραλία")}</h1>
    <p class="lead">{t("The Federation of Pontian Associations of Australia brings together Pontian Greek associations from Perth to Sydney to preserve our language, music, dance and faith, to honour the memory of the Pontian Genocide, and to pass our heritage to the next generation.",
      "Η Ομοσπονδία Ποντιακών Σωματείων Αυστραλίας ενώνει τα ποντιακά σωματεία από το Πέρθ έως το Σύδνεϋ, για να διαφυλάξουμε τη διάλεκτο, τη μουσική, τους χορούς και την πίστη μας, να τιμούμε τη μνήμη της Γενοκτονίας των Ποντίων και να παραδώσουμε την κληρονομιά μας στη νέα γενιά.")}</p>
    <div class="btns"><a class="btn solid" href="events.html">{t("Upcoming events", "Επερχόμενες εκδηλώσεις")}</a><a class="btn ghost" href="associations.html">{t("Find your local association", "Βρείτε το σωματείο σας")}</a></div>
  </div>
  <img src="assets/logo.png" alt="Federation of Pontian Associations of Australia logo">
</div></section>

<section class="block"><div class="wrap">
  <div class="statrow">
    <div><div class="stat">1989</div><p>{t("Year founded", "Έτος ίδρυσης")}</p></div>
    <div><div class="stat">9</div><p>{t("Member associations", "Σωματεία-μέλη")}</p></div>
    <div><div class="stat">5</div><p>{t("States &amp; territories", "Πολιτείες &amp; επικράτειες")}</p></div>
    <div><div class="stat">~800</div><p>{t("Guests at Synapantema 2026", "Καλεσμένοι στο Συναπάντημα 2026")}</p></div>
  </div>
</div></section>

<section class="block alt"><div class="wrap feature">
  <div>
    <span class="state">{t("NEXT SYNAPANTEMA", "ΕΠΟΜΕΝΟ ΣΥΝΑΠΑΝΤΗΜΑ")}</span>
    <h2 style="margin-top:12px">{t("Synapantema 2027 · Canberra", "Συναπάντημα 2027 · Καμπέρα")}</h2>
    <p>{t("Our flagship national gathering moves to a different state each year. After a sold-out Synapantema in Sydney in April 2026, the 2027 gathering will be hosted in Canberra, followed by Perth in 2028.",
      "Η κορυφαία πανελλαδική μας συνάντηση φιλοξενείται κάθε χρόνο σε διαφορετική πολιτεία. Μετά το Συναπάντημα του Σύδνεϋ τον Απρίλιο του 2026, το 2027 θα φιλοξενηθεί στην Καμπέρα και το 2028 στο Πέρθ.")}</p>
    <a class="btn ghost light" href="events.html">{t("See all events", "Όλες οι εκδηλώσεις")}</a>
  </div>
  <div class="panel">
    <h3>{t("What happens at Synapantema", "Τι περιλαμβάνει το Συναπάντημα")}</h3>
    <ul>
      <li>{t("Opening night parakath with live lyra", "Παρακάθ’ με ζωντανή λύρα")}</li>
      <li>{t("Grand dinner dance with performers from every state", "Μεγάλος χορός με χορευτικά από όλες τις πολιτείες")}</li>
      <li>{t("Divine Liturgy and cultural workshops", "Θεία Λειτουργία και πολιτιστικά εργαστήρια")}</li>
      <li>{t("Youth networking and the Federation awards", "Συνάντηση νεολαίας και βραβεύσεις της Ομοσπονδίας")}</li>
    </ul>
  </div>
</div></section>

<section class="block"><div class="wrap">
  <h2>{t("What we do", "Τι κάνουμε")}</h2>
  <div class="grid g3" style="margin-top:20px">
    <div class="card"><h3>{t("Culture &amp; heritage", "Πολιτισμός &amp; παράδοση")}</h3><p>{t("Supporting dance groups, lyra players and the Pontic dialect through our member associations.", "Στηρίζουμε χορευτικά, λυράρηδες και την ποντιακή διάλεκτο μέσα από τα σωματεία-μέλη μας.")}</p></div>
    <div class="card"><h3>{t("Remembrance &amp; recognition", "Μνήμη &amp; αναγνώριση")}</h3><p>{t("Commemorating the Genocide of the Pontian Greeks every 19 May and working with parliaments across Australia for its recognition.", "Τιμούμε κάθε 19 Μαΐου τη Γενοκτονία των Ελλήνων του Πόντου και εργαζόμαστε με τα κοινοβούλια της Αυστραλίας για την αναγνώρισή της.")}</p></div>
    <div class="card"><h3>{t("Youth", "Νεολαία")}</h3><p>{t("A decade-long youth development effort that is bringing a new generation into Federation leadership.", "Μια δεκαετής προσπάθεια για τη νεολαία που φέρνει μια νέα γενιά στη διοίκηση της Ομοσπονδίας.")}</p></div>
  </div>
</div></section>

<section class="block alt"><div class="wrap">
  <h2>{t("Latest news", "Τελευταία νέα")}</h2>
  <div class="grid g3" style="margin-top:20px">
    {"".join(news_teaser(n) for n in NEWS_LIST[:3])}
  </div>
</div></section>
'''

ABOUT = f'''
<div class="pagehead"><div class="wrap"><h1>{t("About the Federation", "Η Ομοσπονδία")}</h1>
<p>{t("The national voice of Pontian Hellenism in Australia since 1989.", "Η εθνική φωνή του Ποντιακού Ελληνισμού στην Αυστραλία από το 1989.")}</p></div></div>
<section class="block"><div class="wrap feature">
  <div>
    <h2>{t("Our story", "Η ιστορία μας")}</h2>
    <p>{t("Founded in 1989, the Federation of Pontian Associations of Australia unites the Pontian Greek associations of New South Wales, Victoria, South Australia, Western Australia and the ACT. Together we keep alive the culture of Pontos, the Black Sea homeland of our ancestors, and honour the memory of the 353,000 Pontian Greeks who perished in the Genocide of 1916–1923.",
       "Η Ομοσπονδία Ποντιακών Σωματείων Αυστραλίας ιδρύθηκε το 1989 και ενώνει τα ποντιακά σωματεία της Νέας Νότιας Ουαλίας, της Βικτώριας, της Νότιας Αυστραλίας, της Δυτικής Αυστραλίας και της Επικράτειας Πρωτεύουσας. Μαζί κρατάμε ζωντανό τον πολιτισμό του Πόντου, της πατρογονικής μας γης στον Εύξεινο Πόντο, και τιμούμε τη μνήμη των 353.000 Ποντίων που χάθηκαν στη Γενοκτονία του 1916–1923.")}</p>
    <p>{t("Each year the Federation brings the community together at Synapantema, holds its Annual General Meeting in a different state, and advocates for the recognition of the Genocides of the Hellenes, Armenians and Assyrians.",
       "Κάθε χρόνο η Ομοσπονδία συγκεντρώνει την ομογένεια στο Συναπάντημα, πραγματοποιεί τη Γενική της Συνέλευση σε διαφορετική πολιτεία και αγωνίζεται για την αναγνώριση των Γενοκτονιών των Ελλήνων, των Αρμενίων και των Ασσυρίων.")}</p>
  </div>
  <img src="assets/logo.png" alt="" style="max-width:320px;margin:0 auto">
</div></section>
<section class="block alt"><div class="wrap">
  <h2>{t("Our mission", "Η αποστολή μας")}</h2>
  <div class="grid g3" style="margin-top:20px">
    <div class="card"><h3>{t("Unite", "Ενότητα")}</h3><p>{t("Bring Pontian associations across Australia together under one national body.", "Ενώνουμε τα ποντιακά σωματεία της Αυστραλίας κάτω από ένα εθνικό όργανο.")}</p></div>
    <div class="card"><h3>{t("Preserve", "Διατήρηση")}</h3><p>{t("Protect the dialect, music, dance and Orthodox traditions of Pontos.", "Διαφυλάσσουμε τη διάλεκτο, τη μουσική, τους χορούς και τις ορθόδοξες παραδόσεις του Πόντου.")}</p></div>
    <div class="card"><h3>{t("Remember", "Μνήμη")}</h3><p>{t("Seek justice and recognition for the Genocide of the Pontian Greeks.", "Διεκδικούμε δικαίωση και αναγνώριση για τη Γενοκτονία των Ελλήνων του Πόντου.")}</p></div>
  </div>
</div></section>
<section class="block"><div class="wrap">
  <h2>{t("Executive Committee " + esc(COMMITTEE_DATA["term"]), "Διοικητικό Συμβούλιο " + esc(COMMITTEE_DATA["term"]))}</h2>
  <p class="note">{t("Draft: names taken from press reports of the August 2025 AGM. Please confirm before publishing.", "Πρόχειρο: τα ονόματα προέρχονται από δημοσιεύματα για τη Γενική Συνέλευση του Αυγούστου 2025. Παρακαλούμε επιβεβαιώστε πριν από τη δημοσίευση.")}</p>
  <div class="people" style="margin-top:20px">
    {"".join(person_card(m) for m in COMMITTEE)}
  </div>
</div></section>
'''

ASSOC = f'''
<div class="pagehead"><div class="wrap"><h1>{t("Member Associations", "Σωματεία-Μέλη")}</h1>
<p>{t("Nine associations across Australia make up the Federation. Get involved with the one nearest you.", "Εννέα σωματεία σε όλη την Αυστραλία αποτελούν την Ομοσπονδία. Γίνετε μέλος σε αυτό που βρίσκεται πιο κοντά σας.")}</p></div></div>
<section class="block"><div class="wrap">
  <div class="grid g3">
    {"".join(assoc_card(x) for x in ASSOCIATIONS)}
  </div>
</div></section>
'''

EVENTS = f'''
<div class="pagehead"><div class="wrap"><h1>{t("Events", "Εκδηλώσεις")}</h1>
<p>{t("National gatherings, commemorations and feast days of the Pontian community in Australia.", "Πανελλαδικές συναντήσεις, μνημόσυνα και γιορτές της ποντιακής ομογένειας στην Αυστραλία.")}</p></div></div>
<section class="block"><div class="wrap">
  <h2>{t("Coming up", "Προσεχώς")}</h2>
  <div class="grid g2" style="margin-top:20px">
    {"".join(event_card(e) for e in EVENT_LIST)}
  </div>
</div></section>
<section class="block alt"><div class="wrap">
  <h2>{t("Synapantema hosts", "Διοργανώτριες πόλεις του Συναπαντήματος")}</h2>
  <div class="grid g3" style="margin-top:20px">
    <div class="card"><div class="meta">2026</div><h3>{t("Sydney", "Σύδνεϋ")}</h3><p>{t("24–27 April · nearly 800 guests", "24–27 Απριλίου · σχεδόν 800 καλεσμένοι")}</p></div>
    <div class="card"><div class="meta">2027</div><h3>{t("Canberra", "Καμπέρα")}</h3><p>{t("Dates to be announced", "Θα ανακοινωθεί")}</p></div>
    <div class="card"><div class="meta">2028</div><h3>{t("Perth", "Πέρθ")}</h3><p>{t("Dates to be announced", "Θα ανακοινωθεί")}</p></div>
  </div>
</div></section>
'''

NEWS = f'''
<div class="pagehead"><div class="wrap"><h1>{t("News", "Νέα")}</h1>
<p>{t("Updates from the Federation and our member associations.", "Ενημερώσεις από την Ομοσπονδία και τα σωματεία-μέλη.")}</p></div></div>
<section class="block"><div class="wrap" style="max-width:820px">
  {"".join(news_article(n) for n in NEWS_LIST)}
</div></section>
'''

CONTACT = f'''
<div class="pagehead"><div class="wrap"><h1>{t("Contact", "Επικοινωνία")}</h1>
<p>{t("Questions about the Federation, Synapantema or joining a member association? Send us a message.", "Ερωτήσεις για την Ομοσπονδία, το Συναπάντημα ή την εγγραφή σε σωματείο; Στείλτε μας μήνυμα.")}</p></div></div>
<section class="block"><div class="wrap feature" style="align-items:start">
  <form class="contact" onsubmit="event.preventDefault();this.querySelector('.ok').hidden=false">
    <label>{t("Name", "Όνομα")}<input required name="name"></label>
    <label>{t("Email", "Email")}<input required type="email" name="email"></label>
    <label>{t("Topic", "Θέμα")}<select name="topic"><option>{t("General enquiry", "Γενική ερώτηση")}</option><option>Synapantema</option><option>{t("Media", "Μέσα ενημέρωσης")}</option><option>{t("Sponsorship", "Χορηγίες")}</option></select></label>
    <label>{t("Message", "Μήνυμα")}<textarea required name="message"></textarea></label>
    <button class="btn solid" type="submit">{t("Send message", "Αποστολή")}</button>
    <p class="note ok" hidden>{t("Thank you. (Draft: the form is not connected yet.)", "Ευχαριστούμε. (Πρόχειρο: η φόρμα δεν είναι ακόμη συνδεδεμένη.)")}</p>
  </form>
  <div class="panel" style="background:var(--dark);color:#EDE2C6;border-radius:14px;padding:32px">
    <h3 style="color:var(--gold)">{t("Federation office", "Γραφείο Ομοσπονδίας")}</h3>
    <p>Email: <a style="color:#fff" href="mailto:info@pontos.org.au">info@pontos.org.au</a><br>{t("Postal address to confirm", "Ταχυδρομική διεύθυνση προς επιβεβαίωση")}</p>
    <h3 style="color:var(--gold);margin-top:24px">{t("Follow us", "Ακολουθήστε μας")}</h3>
    <p><a style="color:#fff" href="https://www.instagram.com/pontian_federation_aus_/" target="_blank" rel="noopener">Instagram · @pontian_federation_aus_</a><br><a style="color:#fff" href="https://www.facebook.com/federation.pontian.associations.australia" target="_blank" rel="noopener">Facebook</a></p>
  </div>
</div></section>
'''

PAGES = [
    ("index.html", "Home", "Αρχική", HOME),
    ("about.html", "About", "Ποιοι είμαστε", ABOUT),
    ("associations.html", "Member Associations", "Σωματεία-Μέλη", ASSOC),
    ("events.html", "Events", "Εκδηλώσεις", EVENTS),
    ("news.html", "News", "Νέα", NEWS),
    ("contact.html", "Contact", "Επικοινωνία", CONTACT),
]

if __name__ == "__main__":
    shutil.rmtree(DIST, ignore_errors=True)
    shutil.copytree(os.path.join(HERE, "src", "assets"), os.path.join(DIST, "assets"))
    for f, en, el, body in PAGES:
        with open(os.path.join(DIST, f), "w", encoding="utf-8") as fh:
            fh.write(page(f, en, el, body))
    print("built", len(PAGES), "pages into", DIST)
