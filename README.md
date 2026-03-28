# NLP_3A

## Qui gère ce `git` ?

Le projet a été réalisé à deux, par Caroline Lebrun-Sabalot et Matéo Garbe. 
Comme requis, chacun des collaborateur a produit son propre rapport. 
Les rapports individuels sont disponibles dans le dossier correspondant. 


## Prérequis 
Si vous utilisez onyxia, paramétrez les paramètres minimaux et maximaux de RAM et de CPU à un niveau très élevé. 
Avant de commencer, lancez :

```bash
python3 -m venv mon_env
source env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

Puis 

```bash
pip install -e .
```

## Notes

Les identifiants des fichiers ont un sens : 
-EL137_L_1981_06_077_03_2_PF_01

EL = élections législatives
1981 = année de l'élection
06 = mois de l'élection ? 
077 = département
03 = circonscription
2 = 2ème tour
PF = profession de foi