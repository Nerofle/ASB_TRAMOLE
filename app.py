import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# Configuration de la page
st.set_page_config(
    page_title="Inscriptions ASBT 2026",
    page_icon="🔮",
    layout="wide"
)

# --- DESIGN MODERNE (STYLE Capture.39.PNG) ---
st.markdown("""
    <style>
    :root {
        --bleu-asbt: #003399;
        --rouge-asbt: #b30000;
    }
    .main-title { color: var(--bleu-asbt); font-weight: bold; text-align: center; margin-bottom: 25px; font-size: 28px; }
    
    /* Style de la bannière défilante */
    .marquee-container {
        background-color: var(--rouge-asbt);
        color: white;
        padding: 10px;
        font-weight: bold;
        font-size: 14px;
        border-radius: 6px;
        margin-bottom: 25px;
        overflow: hidden;
        white-space: nowrap;
    }
    .marquee-text {
        display: inline-block;
        padding-left: 100%;
        animation: marquee 25s linear infinite;
    }
    @keyframes marquee {
        0%   { transform: translate(0, 0); }
        100% { transform: translate(-100%, 0); }
    }

    /* Style exact des cartes blanches de Capture.39.PNG */
    .card-style {
        background: white;
        padding: 24px;
        border-radius: 16px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        border: 1px solid #eaeaea;
        margin-bottom: 20px;
        min-height: 380px;
        display: flex;
        flex-direction: column;
    }
    .card-title {
        color: #003399;
        font-size: 22px;
        font-weight: bold;
        margin-bottom: 15px;
    }
    .card-info {
        font-size: 16px;
        margin-bottom: 10px;
        color: #333333;
    }
    .status-complet {
        color: #b30000;
        font-weight: bold;
    }
    
    /* Bouton rouge personnalisé et centré */
    .stButton>button {
        background-color: var(--rouge-asbt) !important;
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 10px 20px !important;
        font-size: 16px !important;
        font-weight: bold !important;
        width: 100% !important;
        margin-top: auto !important;
        transition: background 0.3s;
    }
    .stButton>button:hover {
        background-color: #8a0000 !important;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .main-title { font-size: 24px !important; }
        .card-style { min-height: auto !important; }
    }
    </style>
""", unsafe_allow_html=True)

# --- CONNEXION LIVE AU GOOGLE SHEETS ---
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df_joueurs = conn.read(worksheet="base de données")
except Exception as e:
    st.error("Liaison Google Sheets en cours de configuration...")
    df_joueurs = pd.DataFrame(columns=['ID_JOUEUR', 'NOM ET PRÉNOM', 'SOCIÉTÉ', 'MOBILE'])

# Structure des données calquée sur l'affichage demandé
EVENEMENTS = [
    {
        "titre": "Challenge DOYEUX",
        "date": "samedi 30 mai",
        "format": "Triplettes",
        "tours": [
            {"nom": "08h00", "sheet": "DOYEUX", "max": 32}
        ]
    },
    {
        "titre": "Challenge Souvenirs (Simples)",
        "date": "dimanche 28 juin",
        "format": "Simples",
        "tours": [
            {"nom": "08h00", "sheet": "SOUVENIRS 1ER TOUR", "max": 32},
            {"nom": "09h00", "sheet": "SOUVENIRS 2ÈME TOUR", "max": 32}
        ]
    },
    {
        "titre": "Challenge Souvenirs (Combinés)",
        "date": "dimanche 28 juin",
        "format": "Combinés",
        "tours": [
            {"nom": "14h30", "sheet": "SOUVENIRS COMBINÉS", "max": 16}
        ]
    },
    {
        "titre": "Challenge Municipalité",
        "date": "samedi 15 août",
        "format": "Quadrettes",
        "tours": [
            {"nom": "08h00", "sheet": "CHALLENGE DE LA MUNICIPALITÉ", "max": 32}
        ]
    },
    {
        "titre": "Challenge A.S.B. Tramolé",
        "date": "dimanche 16 août",
        "format": "Simples",
        "tours": [
            {"nom": "08h00", "sheet": "ASBT 1ER TOUR", "max": 32},
            {"nom": "09h00", "sheet": "ASBT 2ÈME TOUR", "max": 32}
        ]
    }
]

# Liste à plat pour le formulaire de sélection
LISTE_CHOIX_FORMULAIRE = {}
for ev in EVENEMENTS:
    for t in ev["tours"]:
        label_complet = f"{ev['titre']} ({ev['date']}) - {t['nom']}"
        LISTE_CHOIX_FORMULAIRE[label_complet] = {"sheet": t["sheet"], "max": t["max"]}

if "selected_event_form" not in st.session_state:
    st.session_state["selected_event_form"] = list(LISTE_CHOIX_FORMULAIRE.keys())[0]

if "user_asbt" not in st.session_state:
    st.session_state.user_asbt = None

# --- MENU NAVIGATION ---
with st.sidebar:
    st.markdown("### 🔮 A.S.B. TRAMOLÉ")
    st.markdown("---")
    menu = st.radio("Aller à :", ["🏠 Accueil & Places", "📝 Formulaire d'Inscription", "👥 Liste des Inscrits", "🔐 Annuler une inscription"])
    st.markdown("---")
    if st.session_state.user_asbt:
        st.success(f"👤 Connecté : {st.session_state.user_asbt['nom']}")
        if st.button("Déconnexion"):
            st.session_state.user_asbt = None
            st.rerun()

# ==========================================
# 🏠 ÉCRAN D'ACCUEIL (STYLE GRILLE DE CARTES)
# ==========================================
if menu == "🏠 Accueil & Places":
    st.markdown('<div class="marquee-container"><div class="marquee-text">📞 INSCRIPTION SUR SMARTPHONE — PAS DE PAIEMENT EN LIGNE — RÈGLEMENT SUR PLACE LE JOUR DU CONCOURS (PRÉSENTATION DES LICENCES)</div></div>', unsafe_allow_html=True)
    st.markdown('<h1 class="main-title">A.S.B. TRAMOLÉ - Saison 2026</h1>', unsafe_allow_html=True)
    
    # Grille de 3 colonnes comme sur l'image
    cols = st.columns(3)
    
    for i, ev in enumerate(EVENEMENTS):
        # On distribue les cartes sur les 3 colonnes
        with cols[i % 3]:
            # Construction des lignes de texte pour les horaires
            tours_html = ""
            evenement_complet = True
            bouton_labels = []
            
            for t in ev["tours"]:
                try:
                    df_c = conn.read(worksheet=t["sheet"])
                    occupes = df_c['NOM'].dropna().count()
                except:
                    occupes = 0
                restantes = t["max"] - occupes
                
                if restantes <= 0:
                    tours_html += f"<div class='card-info'>🕒 {t['nom']} : <span class='status-complet'>COMPLET</span></div>"
                else:
                    tours_html += f"<div class='card-info'>🕒 {t['nom']} : {restantes} places restantes</div>"
                    evenement_complet = False
                    bouton_labels.append((f"{ev['titre']} ({ev['date']}) - {t['nom']}", t['nom']))

            # Affichage de la carte HTML
            st.markdown(f"""
            <div class="card-style">
                <div class="card-title">{ev['titre']}</div>
                <div class="card-info">📅 {ev['date']}</div>
                <div class="card-info">🏆 {ev['format']}</div>
                {tours_html}
            </div>
            """, unsafe_allow_html=True)
            
            # Affichage du vrai bouton Streamlit juste en dessous (qui prend le style CSS du gros bouton rouge)
            if evenement_complet:
                if st.button("Complet 🚫", key=f"btn_comp_{i}"):
                    st.error("Ce concours est complet ! Pour la liste d'attente, contactez le 06 36 37 18 93.")
            else:
                # Si un seul tour dispo, on redirige direct, si plusieurs on propose le premier disponible
                label_cible = bouton_labels[0][0]
                if st.button("S'inscrire", key=f"btn_go_{i}"):
                    st.session_state["selected_event_form"] = label_cible
                    st.info("👉 Rendez-vous maintenant dans l'onglet 'Formulaire d'Inscription' dans le menu de gauche.")

# ==========================================
# 📝 FORMULAIRE D'INSCRIPTION
# ==========================================
elif menu == "📝 Formulaire d'Inscription":
    st.markdown('<h2 class="main-title">Saisie de l\'Inscription</h2>', unsafe_allow_html=True)
    
    choix = st.selectbox("Sélectionnez le concours et l'horaire :", list(LISTE_CHOIX_FORMULAIRE.keys()), index=list(LISTE_CHOIX_FORMULAIRE.keys()).index(st.session_state["selected_event_form"]))
    info_target = LISTE_CHOIX_FORMULAIRE[choix]
    
    df_target = conn.read(worksheet=info_target["sheet"])
    occupes = df_target['NOM'].dropna().count()
    restantes = info_target["max"] - occupes
    st.metric("Places restantes pour ce créneau", int(restantes))

    if restantes <= 0:
        st.error("Désolé, ce créneau est complet.")
    else:
        st.markdown("### 🔍 Auto-complétion Intelligente")
        list_options = ["-- Saisir manuellement (Nouveau joueur) --"] + df_joueurs['NOM ET PRÉNOM'].dropna().tolist()
        recherche = st.selectbox("Rechercher un joueur existant dans la base :", list_options)
        v_nom, v_prenom, v_soc, v_tel = "", "", "", ""
        if recherche != "-- Saisir manuellement (Nouveau joueur) --":
            row_j = df_joueurs[df_joueurs['NOM ET PRÉNOM'] == recherche].iloc[0]
            nom_complet = str(row_j['NOM ET PRÉNOM']).strip().split(" ")
            v_nom = nom_complet[0].upper()
            v_prenom = " ".join(nom_complet[1:]) if len(nom_complet) > 1 else ""
            v_soc = str(row_j['SOCIÉTÉ'])
            v_tel = "0" + str(int(row_j['MOBILE'])) if pd.notna(row_j['MOBILE']) else ""

        with st.form("form_mobile"):
            nom = st.text_input("Nom du participant *", value=v_nom).upper().strip()
            prenom = st.text_input("Prénom du participant *", value=v_prenom).strip()
            societe = st.text_input("Société / Club *", value=v_soc).strip()
            telephone = st.text_input("Téléphone portable *", value=v_tel).strip()
            submit = st.form_submit_button("Valider l'Inscription")

            if submit:
                if not nom or not prenom or not societe or not telephone:
                    st.error("Veuillez remplir tous les champs obligatoires (*).")
                else:
                    idx_vides = df_target[df_target['NOM'].isna() | (df_target['NOM'] == '')].index
                    if len(idx_vides) > 0:
                        cible = idx_vides[0]
                        df_target.at[cible, 'NOM'] = nom
                        df_target.at[cible, 'PRÉNOM'] = prenom
                        df_target.at[cible, 'SOCIÉTÉ'] = societe
                        df_target.at[cible, 'MOBILE'] = telephone
                        df_target.at[cible, 'DATE INSCRIPTION'] = datetime.now().strftime("%d/%m/%Y %H:%M")
                        conn.update(worksheet=info_target["sheet"], data=df_target)

                        if recherche == "-- Saisir manuellement (Nouveau joueur) --":
                            nouveau_j = pd.DataFrame([{"ID_JOUEUR": len(df_joueurs)+1, "NOM ET PRÉNOM": f"{nom} {prenom}", "SOCIÉTÉ": societe, "MOBILE": telephone}])
                            df_joueurs = pd.concat([df_joueurs, nouveau_j], ignore_index=True)
                            conn.update(worksheet="base de données", data=df_joueurs)
                        st.success("🎉 Inscription validée avec succès !")
                        st.balloons()
                    else:
                        st.error("Erreur : Plus de places disponibles.")

# ==========================================
# 👥 LISTE DES INSCRITS
# ==========================================
elif menu == "👥 Liste des Inscrits":
    st.markdown('<h2 class="main-title">Liste des Joueurs Engagés</h2>', unsafe_allow_html=True)
    choix = st.selectbox("Sélectionnez le concours :", list(LISTE_CHOIX_FORMULAIRE.keys()))
    df_visu = conn.read(worksheet=LISTE_CHOIX_FORMULAIRE[choix]["sheet"])
    df_presents = df_visu.dropna(subset=['NOM'])
    st.write(f"📊 **Inscrits actuels : {len(df_presents)}**")
    if df_presents.empty:
        st.info("Aucune inscription enregistrée pour ce créneau.")
    else:
        st.dataframe(df_presents[['RANG', 'NOM', 'PRÉNOM', 'SOCIÉTÉ', 'DATE INSCRIPTION']], use_container_width=True, hide_index=True)

# ==========================================
# 🔐 ANNULATION DE PLACES
# ==========================================
elif menu == "🔐 Annuler une inscription":
    st.markdown('<h2 class="main-title">Espace Désinscription Autonome</h2>', unsafe_allow_html=True)
    t_co, t_creer, t_action = st.tabs(["Connexion", "Créer un compte", "Mes Annulations"])

    with t_creer:
        st.write("Créez votre compte pour gérer votre inscription.")
        c_nom = st.text_input("Votre NOM de famille").upper().strip()
        c_tel = st.text_input("Votre numéro de portable").strip()
        if st.button("Enregistrer mon accès smartphone"):
            st.success("Compte enregistré ! Connectez-vous sur l'onglet Connexion.")

    with t_co:
        l_nom = st.text_input("NOM :").upper().strip()
        l_tel = st.text_input("Téléphone :").strip()
        if st.button("Me connecter"):
            if l_nom and l_tel:
                st.session_state.user_asbt = {"nom": l_nom, "tel": l_tel}
                st.success("Connexion réussie !")
                st.rerun()

    with t_action:
        if not st.session_state.user_asbt:
            st.warning("Veuillez vous connecter pour annuler une place.")
        else:
            u = st.session_state.user_asbt
            st.write(f"Recherche pour **{u['nom']}** :")
            trouve = False
            for label, info in LISTE_CHOIX_FORMULAIRE.items():
                df_c = conn.read(worksheet=info["sheet"])
                mes_lignes = df_c[(df_c['NOM'] == u['nom']) & (df_c['MOBILE'].astype(str).str.contains(u['tel']))]
                for idx, row in mes_lignes.iterrows():
                    trouve = True
                    st.warning(f"📍 {label} — Rang {row['RANG']}")
                    if st.button(f"Annuler ce dossard (Rang {row['RANG']}) ❌", key=f"del_{info['sheet']}_{idx}"):
                        df_c.at[idx, 'NOM'] = None
                        df_c.at[idx, 'PRÉNOM'] = None
                        df_c.at[idx, 'SOCIÉTÉ'] = None
                        df_c.at[idx, 'MOBILE'] = None
                        df_c.at[idx, 'DATE INSCRIPTION'] = None
                        conn.update(worksheet=info["sheet"], data=df_c)
                        st.error("Inscription annulée.")
                        st.rerun()
            if not trouve:
                st.info("Aucune place trouvée à ce nom.")
