import feedparser
import ssl
import urllib.request
import json
import requests
import os

# CONFIGURATION
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
TABLE_NAME = "articles"

# SÉCURITÉ SSL
if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context

METIERS = {
    "Santé": ["le", "médecin", "hôpital", "santé", "diagnostic", "imagerie", "patient", "chirurgie", "médical", "soins", "cancer", "clinique"],
    "Droit": ["avocat", "juridique", "loi", "justice", "contrat", "procès", "tribunal", "notaire", "jurisprudence", "magistrat"],
    "BTP": ["architecture", "construction", "bâtiment", "chantier", "urbanisme", "plan", "immobilier", "maçon", "travaux"],
    "Éducation": ["école", "professeur", "élève", "apprentissage", "université", "cours", "pédagogie", "formation", "lycée", "collège"],
    "Finance": ["banque", "bourse", "investissement", "comptabilité", "crypto", "trading", "économie", "audit", "fiscal"],
    "Marketing": ["publicité", "réseaux sociaux", "vente", "influence", "e-commerce", "client", "stratégie digitale", "seo", "branding"],
    "Agriculture": ["ferme", "agriculteur", "récolte", "élevage", "culture", "tracteur", "agronomie", "vigne", "paysan"]
}

SOURCES = [
    "https://www.lemonde.fr/pixels/rss_full.xml",
    "https://www.actuia.com/actualite/intelligence-artificielle/feed/",
    "https://intelligence-artificielle.com/feed/",
    "https://www.zdnet.fr/feeds/rss/actualites/intelligence-artificielle-3900003001.htm"
]

def envoyer_a_supabase(article):
    endpoint = f"{SUPABASE_URL}/rest/v1/{TABLE_NAME}"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "resolution=merge-duplicates" 
    }
    try:
        response = requests.post(endpoint, headers=headers, json=article)
        if response.status_code in [200, 201]:
            print(f"✅ Enregistré : {article['title'][:50]}...")
        else:
            print(f"ℹ️ Déjà présent : {article['title'][:30]}...")
    except Exception as e:
        print(f"❌ Erreur réseau : {e}")

def classer_article(titre):
    titre_clean = titre.lower()
    for metier, mots_cles in METIERS.items():
        for mot in mots_cles:
            if mot in titre_clean:
                return metier
    return "Général"

def executer_le_robot():
    print(f"🚀 Robot en marche...")
    for url in SOURCES:
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                flux = feedparser.parse(response.read())
                for entree in flux.entries[:20]:
                    categorie = classer_article(entree.title)
                    if categorie != "Général":
                        article = {
                            "title": entree.title,
                            "link": entree.link,
                            "category": categorie,
                            "summary": entree.get('summary', '')[:250]
                        }
                        envoyer_a_supabase(article)
        except Exception as e:
            print(f"⚠️ Erreur sur la source {url}: {e}")

if __name__ == "__main__":
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("❌ Erreur : Clés manquantes dans GitHub Secrets.")
    else:
        executer_le_robot()
