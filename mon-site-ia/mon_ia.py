import os # Ajoute ça en haut

# Remplace tes lignes de config par celles-ci :


import feedparser
import ssl
import urllib.request
import json
import requests # La bibliothèque légère qu'on vient d'installer

# --- CONFIGURATION SUPABASE ---
# Remplace par tes vraies infos trouvées dans Supabase (Settings > API)
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
TABLE_NAME = "articles"

# Sécurité Windows
if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context

METIERS = {
    "Santé": ["médecin", "hôpital", "santé", "diagnostic", "imagerie", "patient", "chirurgie", "médical", "soins"],
    "Droit": ["avocat", "juridique", "loi", "justice", "contrat", "procès", "tribunal", "notaire", "jurisprudence"],
    "BTP": ["architecture", "construction", "bâtiment", "chantier", "urbanisme", "plan", "immobilier", "maçon"],
    "Éducation": ["école", "professeur", "élève", "apprentissage", "université", "cours", "pédagogie", "formation"],
    "Finance": ["banque", "bourse", "investissement", "comptabilité", "crypto", "trading", "économie", "audit"],
    "Marketing": ["publicité", "réseaux sociaux", "vente", "influence", "e-commerce", "client", "stratégie digitale"],
    "Agriculture": ["ferme", "agriculteur", "récolte", "élevage", "culture", "tracteur", "agronomie"]
}

def envoyer_a_supabase(article):
    endpoint = f"{SUPABASE_URL}/rest/v1/{TABLE_NAME}"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "resolution=merge-duplicates" # <--- Ajoute cette ligne magique !
    }
    # Pour que cela fonctionne, il faut que ta colonne "link" soit une "Unique Key" dans Supabase
    # Sinon, on peut simplement faire une recherche avant l'insert.
    
    try:
        response = requests.post(endpoint, headers=headers, json=article)
        if response.status_code == 201:
            print(f"✅ Enregistré : {article['title'][:50]}...")
        else:
            print(f"❌ Erreur Supabase : {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Erreur de connexion : {e}")

def classer_article(titre):
    titre_clean = titre.lower()
    for metier, mots_cles in METIERS.items():
        for mot in mots_cles:
            if mot in titre_clean: return metier
    return "Général"

def recuperer_et_sauvegarder():
    url = "https://www.lemonde.fr/pixels/rss_full.xml"
    print("🚀 Recherche et sauvegarde des news...")
    
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        flux = feedparser.parse(response.read())
        
        for entree in flux.entries[:15]:
            categorie = classer_article(entree.title)
            
            if categorie != "Général":
                nouvel_article = {
                    "title": entree.title,
                    "link": entree.link,
                    "category": categorie,
                    "summary": entree.get('summary', '')[:200] # On prend les 200 1ers caractères
                }
                envoyer_a_supabase(nouvel_article)

if __name__ == "__main__":
    recuperer_et_sauvegarder()