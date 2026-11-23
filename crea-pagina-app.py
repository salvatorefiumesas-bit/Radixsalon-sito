#!/usr/bin/env python3
"""Crea sul sito di Eurogestion le pagine legali di un'app (privacy, termini, cancellazione account).

Perché: negli store (Google Play, App Store) lo sviluppatore è Eurogestion, quindi l'indirizzo della
privacy deve aprire una pagina che indichi con chiarezza Eurogestion come sviluppatore, e non solo il salone.
Le pagine leggono gli stessi dati dell'app (Firestore): quando il titolare cambia i testi dal gestionale,
si aggiornano da sole. Le copie dei file (seed.js, config.js) vanno rigenerate quando cambiano nell'app.

Uso (dalla cartella di questo repository):
    python3 crea-pagina-app.py <cartella-repository-app> <nome-cartella> "<Nome app>"
Esempio:
    python3 crea-pagina-app.py ../Radici radici "Radici – Ambito Hair Studio"
Crea app/<nome-cartella>/ con: privacy.html, termini.html, cancella-account.html, seed.js, icon-192.png
(e config.js se l'app lo ha). Indirizzi da mettere negli store:
    https://eurogestionradix.it/app/<nome-cartella>/privacy.html   (e termini.html, cancella-account.html)
"""
import os, re, shutil, sys

QUI = os.path.dirname(os.path.abspath(__file__))
if len(sys.argv) != 4:
    sys.exit(__doc__)
sorgente, cartella, nome = os.path.abspath(sys.argv[1]), sys.argv[2], sys.argv[3]
if not re.fullmatch(r'[a-z0-9-]+', cartella):
    sys.exit('nome-cartella: solo minuscole, numeri e trattini')
dest = os.path.join(QUI, 'app', cartella)
os.makedirs(dest, exist_ok=True)

esc = lambda t: t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
BOX = ('<div style="border:1.5px solid var(--line);background:var(--surf);border-radius:16px;padding:12px 14px;margin:0 0 16px;font-size:.92rem">'
       'App <b>%s</b>, sviluppata e pubblicata da <b>Eurogestion S.A.S. di Di Fiore Rosa</b> (P.IVA 05812141215, Via Argine 572, 80147 Napoli) '
       'nell\'ambito del servizio <a href="https://eurogestionradix.it">Radix Salon</a>. Il titolare del trattamento dei dati degli utenti è l\'esercente '
       'indicato nell\'informativa; Eurogestion è responsabile del trattamento. Contatti: <a href="mailto:info@eurogestionradix.it">info@eurogestionradix.it</a>.</div>\n ') % esc(nome)
FOOTER = ('<footer>Questa pagina mostra i testi aggiornati che il titolare dell\'app pubblica nel gestionale. App sviluppata e pubblicata da '
          'Eurogestion S.A.S. di Di Fiore Rosa – servizio Radix Salon · <a href="https://eurogestionradix.it">eurogestionradix.it</a></footer>')

def una(s, vecchio, nuovo, nomefile):
    if s.count(vecchio) != 1:
        sys.exit('%s: non trovo (o trovo più volte) %r: la pagina dell\'app è cambiata, aggiornare questo script' % (nomefile, vecchio[:50]))
    return s.replace(vecchio, nuovo)

for pagina in ['privacy.html', 'termini.html', 'cancella-account.html']:
    h = open(os.path.join(sorgente, pagina), encoding='utf-8').read()
    h = una(h, '<main>', BOX + '<main>', pagina)
    h = re.sub(r'<footer>.*?</footer>', lambda m: FOOTER, h, count=1, flags=re.S)
    h = una(h, '<meta name="robots" content="index">',
            '<meta name="robots" content="index">\n<link rel="canonical" href="https://eurogestionradix.it/app/%s/%s">' % (cartella, pagina), pagina)
    open(os.path.join(dest, pagina), 'w', encoding='utf-8').write(h)

for f in ['seed.js', 'config.js', 'icon-192.png']:
    p = os.path.join(sorgente, f)
    if os.path.exists(p):
        shutil.copyfile(p, os.path.join(dest, f))
    elif f == 'seed.js':
        sys.exit('manca seed.js nella cartella dell\'app')
print('Pagine create in', dest)
print('Indirizzi per gli store: https://eurogestionradix.it/app/%s/privacy.html  (termini.html, cancella-account.html)' % cartella)
