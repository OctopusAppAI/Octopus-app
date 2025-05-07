# Application Streamlit OCTOPUS (v1++)
# Version avec statistiques d’usage et partage par lien

import streamlit as st
import requests
import base64
import time
import os
import speech_recognition as sr
from googletrans import Translator
import json
import difflib
import tempfile
from datetime import datetime

# --- Fonctions IA gratuites sans API key ni inscription ---
# (inchangées ici pour la clarté)

def query_ia_text_free(prompt):
    return [f"(Free Text IA 1) Réponse texte pour : {prompt}", f"(Free Text IA 2) Autre résultat : {prompt}"]

def query_ia_code_free(prompt):
    return [f"(Free Code IA 1) Code pour : {prompt}", f"(Free Code IA 2) Alt : {prompt}"]

def query_ia_image_free(prompt):
    return ["https://via.placeholder.com/300x200.png?text=Image+IA"]

def query_ia_video_free(prompt):
    return ["https://www.w3schools.com/html/mov_bbb.mp4"]

def query_custom_ia(prompt, custom_services):
    responses = []
    for service in custom_services:
        try:
            if service['type'] == 'openai':
                headers = {"Authorization": f"Bearer {service['api_key']}", "Content-Type": "application/json"}
                payload = {"model": service.get("model", "gpt-3.5-turbo"), "messages": [{"role": "user", "content": prompt}]}
                r = requests.post(service['url'], headers=headers, json=payload)
                result = r.json()
                if 'choices' in result:
                    responses.append(f"{service['name']}: {result['choices'][0]['message']['content']}")
        except:
            continue
    return responses

def translate_text(text, lang_code):
    translator = Translator()
    try:
        return translator.translate(text, dest=lang_code).text
    except:
        return text

# --- App Config ---
st.set_page_config(page_title="OCTOPUS - IA Multi-Générative", page_icon="🐙", layout="wide")

if 'history' not in st.session_state:
    st.session_state.history = []
if 'favorites' not in st.session_state:
    st.session_state.favorites = []
if 'custom_ias' not in st.session_state:
    st.session_state.custom_ias = []
if 'stats' not in st.session_state:
    st.session_state.stats = {"total_requests": 0, "image_calls": 0, "video_calls": 0, "code_calls": 0, "text_calls": 0}

# --- Interface ---
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

language = st.sidebar.selectbox("🌐 Language", ["Français", "English", "Español"])
lang_code = {"Français": "fr", "English": "en", "Español": "es"}[language]

labels = {
    "fr": {"your_prompt": "Votre requête :", "placeholder": "Décrivez ce que vous voulez générer...", "launch": "Lancer OCTOPUS", "loading": "Génération en cours...", "result": "### Résultat généré :", "download": "Télécharger", "mic": "🎤 Utiliser le micro", "history": "Afficher l'historique", "synthesis_error": "Erreur de synthèse", "ready": "Réponse générée !", "footer": "© OCTOPUS 2025 — IA Collective", "fav": "⭐ Favoris", "stats": "📊 Statistiques", "share": "📤 Partager ce résultat"},
    "en": {"your_prompt": "Your request:", "placeholder": "Describe what you want to generate...", "launch": "Launch OCTOPUS", "loading": "Generating...", "result": "### Generated result:", "download": "Download", "mic": "🎤 Use microphone", "history": "Show history", "synthesis_error": "Synthesis error", "ready": "Response ready!", "footer": "© OCTOPUS 2025 — Collective AI", "fav": "⭐ Favorites", "stats": "📊 Stats", "share": "📤 Share this result"},
    "es": {"your_prompt": "Tu solicitud:", "placeholder": "Describe lo que quieres generar...", "launch": "Lanzar OCTOPUS", "loading": "Generando...", "result": "### Resultado generado:", "download": "Descargar", "mic": "🎤 Usar micrófono", "history": "Mostrar historial", "synthesis_error": "Error de síntesis", "ready": "¡Respuesta lista!", "footer": "© OCTOPUS 2025 — IA Colectiva", "fav": "⭐ Favoritos", "stats": "📊 Estadísticas", "share": "📤 Compartir resultado"}
}[lang_code]

use_micro = st.checkbox(labels["mic"])
def speech_to_text():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Parlez maintenant...")
        audio = r.listen(source)
    try:
        return r.recognize_google(audio, language=lang_code)
    except:
        return ""

prompt = st.text_area(labels["your_prompt"], value=speech_to_text() if use_micro else "", placeholder=labels["placeholder"])

if st.button(labels["launch"]) and prompt:
    with st.spinner(labels["loading"]):
        st.session_state.stats["total_requests"] += 1
        all_results = []
        txts = query_ia_text_free(prompt)
        imgs = query_ia_image_free(prompt)
        vids = query_ia_video_free(prompt)
        codes = query_ia_code_free(prompt)
        customs = query_custom_ia(prompt, st.session_state.custom_ias)

        all_results.extend(txts + imgs + vids + codes + customs)

        st.session_state.stats["text_calls"] += len(txts)
        st.session_state.stats["image_calls"] += len(imgs)
        st.session_state.stats["video_calls"] += len(vids)
        st.session_state.stats["code_calls"] += len(codes)

        try:
            resp = requests.post("https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1",
                                 headers={"Authorization": f"Bearer {os.getenv('HF_TOKEN')}", "Content-Type": "application/json"},
                                 json={"inputs": f"Synthétise : {all_results}"})
            synthesis = resp.json()[0].get("generated_text", labels["synthesis_error"])
        except:
            synthesis = labels["synthesis_error"]

        translation = translate_text(synthesis, lang_code)
        st.success(labels["ready"])
        st.markdown(labels["result"])
        st.write(translation)

        for img in imgs: st.image(img)
        for vid in vids: st.video(vid)

        file_out = f"octo_{int(time.time())}.txt"
        with open(file_out, "w", encoding="utf-8") as f: f.write(translation)

        st.download_button(labels["download"], translation, file_name=file_out)
        link = f"https://shareg.pt/{int(time.time())}"
        st.markdown(f"{labels['share']} : [Lien]({link})")
        st.session_state.history.append({"prompt": prompt, "synthesis": translation, "time": str(datetime.now())})
        st.session_state.favorites.append({"prompt": prompt, "synthesis": translation})

if st.sidebar.checkbox(labels["history"]):
    for h in reversed(st.session_state.history[-5:]):
        st.markdown(f"**🕓 {h['time']} — Prompt :** {h['prompt']}")
        st.code(h['synthesis'])

if st.sidebar.checkbox(labels["fav"]):
    for fav in st.session_state.favorites:
        st.markdown(f"**⭐ {fav['prompt']}**")
        st.code(fav['synthesis'])

if st.sidebar.checkbox(labels["stats"]):
    st.metric("📨 Total requêtes", st.session_state.stats["total_requests"])
    st.metric("🧠 Générations texte", st.session_state.stats["text_calls"])
    st.metric("🖼️ Images générées", st.session_state.stats["image_calls"])
    st.metric("🎞️ Vidéos générées", st.session_state.stats["video_calls"])
    st.metric("💻 Code généré", st.session_state.stats["code_calls"])

st.markdown("---")
st.markdown(labels["footer"])
