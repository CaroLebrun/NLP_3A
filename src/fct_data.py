import zipfile
from pathlib import Path
import pandas as pd

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