import zipfile
from pathlib import Path
import pandas as pd
import nltk
from nltk.corpus import stopwords
import re


nltk.download('stopwords')
STOP_WORDS = set(stopwords.words('french'))

# FONCTION MAIN


def raw_data_cleaning(path_meta, path_zip):
    # lecture metdonnées
    metadonnees = pd.read_csv("data/archelect_search.zip", compression="zip")

    # decompression et creation dict.
    texts = extract_texts_from_zips("data/text_files")

    # merge avec métadonnées
    meta_et_texts = meta_et_texts = pd.merge(
        metadonnees,
        texts,
        on="id",
        how="right")

    # nettoyage stopwords
    meta_et_texts['text'] = meta_et_texts['text'].apply(clean_text)
    meta_et_texts['texte_clean'] = meta_et_texts['text'].apply(stopwords_and_punctuation_cleaning)
    meta_et_texts.drop_duplicates(inplace=True)

    # format
    meta_et_texts['annee'] = pd.to_datetime(meta_et_texts['date'], errors='coerce').dt.year

    return meta_et_texts


# SOUS-FONCTIONS
def extract_texts_from_zips(base_dir: str) -> pd.DataFrame:
    """
    Parcourt tous les fichiers ZIP dans `base_dir` (y compris les sous-dossiers),
    extrait tous les fichiers .txt et retourne un DataFrame avec les colonnes :
        - id : nom du fichier sans dossier ni extension
        - text : contenu du fichier
        - zip_path : chemin du ZIP original
    """
    base_dir = Path(base_dir)
    all_texts = []

    for zip_path in base_dir.rglob("*.zip"):
        print(f"Traitement de {zip_path}")
        try:
            with zipfile.ZipFile(zip_path, "r") as z:
                # Liste tous les fichiers .txt valides
                txt_files = [f for f in z.namelist() if f.endswith(".txt")]
                txt_files = [f for f in txt_files if not f.startswith("__MACOSX")]

                for file in txt_files:
                    try:
                        with z.open(file) as f:
                            text_content = f.read().decode("utf-8")
                            filename = Path(file).stem
                            all_texts.append({
                                "id": filename,
                                "text": text_content,
                                "zip_path": str(zip_path)
                            })
                    except Exception as e:
                        print(f"Erreur lecture {file} dans {zip_path}: {e}")
        except Exception as e:
            print(f"Erreur ouverture ZIP {zip_path}: {e}")

    df = pd.DataFrame(all_texts)
    print(f"Nombre total de documents extraits : {len(df)}")
    return df


def stopwords_and_punctuation_cleaning(text):
    text = str(text).lower()
    # enlever chiffres
    text = re.sub(r'\d+', '', text)    
    # normaliser espaces
    text = re.sub(r'\s+', ' ', text)
    # garder les apostrophes
    text = re.sub(r"[^\w\s']", '', text)
    words = []
    for w in text.split():
        # gérer les mots avec apostrophe (ex: l'école)
        if "'" in w:
            parts = w.split("'")
            for p in parts:
                if p and p not in STOP_WORDS:
                    words.append(p)
        else:
            if w not in STOP_WORDS:
                words.append(w)

    return ' '.join(words)



def clean_text(text: str) -> str:
    """
    Nettoie une chaîne de caractères pour préparer les données pour BERT.

    Transformations appliquées :
    - Remplace les sauts de ligne (\\n) par un espace
    - Supprime les caractères carrés (■, □, ▪, ▫, etc.)
    - Remplace '- ' par '' (pour recoller les mots coupés)
    - Supprime le point entre deux chiffres (3.000 → 3000)

    Args:
        text: Chaîne de caractères à nettoyer

    Returns:
        Chaîne nettoyée
    """
    if not isinstance(text, str):
        return text

    text = text.replace('\n', ' ')
    text = re.sub(r'[\u25A0-\u25FF■□▪▫▬▮]', '', text)
    text = text.replace('- ', '')
    text = re.sub(r'(?<=\d)\.(?=\d)', '', text)
    text = re.sub(r' +', ' ', text).strip()
    text = re.sub(r'sciences\s*po', '', text, flags=re.IGNORECASE)
    text = re.sub(r'fonds\s*cevipof', '', text, flags=re.IGNORECASE)
    text = text.replace('/', ' ')
    # corriger toutes les apostrophes "cassées"
    text = re.sub(r"\\+'", "'", text)   # gère \', \\', \\\' etc.

    # supprimer les backslashes restants
    text = re.sub(r"\\+", " ", text)
    text = text.replace("\\\'", "'")
    text = re.sub(r'\s+', ' ', text).strip() #espaces parasites
    
    return text
