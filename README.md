# OCTOPUS 🐙

OCTOPUS est une application IA tout-en-un qui combine automatiquement plusieurs IA gratuites sans clé API pour générer du texte, du code, des images et des vidéos. Elle synthétise ensuite les meilleures réponses via Mistral 7B Instruct (Hugging Face).

## Fonctionnalités
- Génération multi-IA automatique
- Synthèse des résultats avec Mistral 7B
- Traduction automatique
- Micro intégré (si disponible localement)
- Interface multilingue 🇫🇷 🇬🇧 🇪🇸
- Historique, favoris, statistiques, partage

## Lancement local
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Déploiement sur Streamlit Cloud
1. Poussez ce repo sur GitHub
2. Connectez Streamlit Cloud à ce dépôt
3. Dans `Settings > Secrets`, ajoutez :
   - `HF_TOKEN`: votre clé Hugging Face
