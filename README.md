# 🐙 OCTOPUS — Application IA Multi-Générative

**OCTOPUS** interroge automatiquement plusieurs IA gratuites sans clé API (texte, image, vidéo, code) et synthétise les résultats via **Mistral 7B Instruct**.

## 🚀 Fonctionnalités

- Génération automatique multi-IA
- Synthèse via Mistral 7B (Hugging Face)
- Reconnaissance vocale + lecture vocale
- Traduction automatique (français, anglais, espagnol)
- Historique, favoris, statistiques
- Interface moderne et intuitive

## ⚙️ Utilisation locale

```bash
pip install -r requirements.txt
streamlit run app.py
```

## ☁️ Déploiement sur Streamlit Cloud

1. Déposer les fichiers sur un dépôt GitHub
2. Connecter votre GitHub à [Streamlit Cloud](https://share.streamlit.io)
3. Ajouter le token `HF_TOKEN` comme variable d’environnement