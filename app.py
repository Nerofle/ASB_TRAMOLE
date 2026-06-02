import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# Configuration de la page pour un affichage optimal sur Smartphone
st.set_page_config(
    page_title="Inscriptions ASBT 2026",
    page_icon="🔮",
    layout="wide"
)

# Design aux couleurs du logo (Bleu #003399 et Rouge #990000) et responsive mobile
st.markdown("""
    <style>
    :root {
        --bleu-asbt: #003399;
        --rouge-asbt: #990000;
    }
    .main-title { color: var(--bleu-asbt); font-weight: bold; text-align: center; margin-bottom: 5px; }
    
    /* Bannière défilante pour téléphones */
    .marquee-container {
        background-color: var(--rouge-asbt);
        color: white;
        padding: 10px;
        font-weight: bold;
        font-size: 15px;
        border-radius: 6px;
        margin-bottom: 20px;
        overflow: hidden;
        white-space: nowrap;
    }
    .marquee-text {
        display: inline-block;
        padding-left: 100%;
        animation: marquee 22s linear infinite;
    }
    @keyframes marquee {
        0%   { transform: translate(0, 0); }
        100% { transform: translate(-100%, 0); }
    }

    /* Cartes Concours adaptées aux écrans tactiles */
    .concours-card {
        border: 2px solid #eaeaea;
        border-radius: 12px;
        padding: 15px;
        background-color: #fdfdfd;
        margin-bottom: 12px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.03);
    }
    .complet-txt { color: var(--rouge-asbt); font-weight: bold; }
    .dispo-txt { color: #28a745; font-weight: bold; }
    
    /* Ajustements CSS pour petits écrans (Smartphones) */
    @media (max-width: 768px) {
        .main-title { font-size: 22px !important; }
        .concours-card h4 { font-size: 16px !important; }
        .stButton>button { width: 100% !important; margin-top: 5px; }
    }
    </style>
""", unsafe_allow_index=True)

# --- CONNEXION LIVE AU GOOGLE SHEETS ---
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df_joueurs = conn.read(worksheet="base de données")
except Exception as e:
    st.error("Liaison Google Sheets en cours de configuration...")
    df_joueurs = pd.DataFrame(columns=['ID_JOUEUR', 'NOM ET PRÉNOM', 'SOCIÉTÉ', 'MOBILE'])

# Correspondance exacte avec les onglets de votre lien Google Sheets
ONGLETS_CONCOURS = {
    "Challenge DOYEUX (Samedi 30 Mai)": {"sheet": "DOYEUX", "max": 32},
    "Challenge SOUVENIRS - 1er Tour (08h00)": {"sheet": "SOUVENIRS 1ER TOUR", "max": 32},
    "Challenge SOUVENIRS - 2ème Tour (09h00)": {"sheet": "SOUVENIRS 2ÈME TOUR", "max": 32},
    "Challenge SOUVENIRS - COMBINÉS (14h30)": {"sheet": "SOUVENIRS COMBINÉS", "max": 16},
    "CHALLENGE DE LA MUNICIPALITÉ (Samedi 15 Août)": {"sheet": "CHALLENGE DE LA MUNICIPALITÉ", "max": 32},
    "Challenge ASBT - 1er Tour (08h00)": {"sheet": "ASBT 1ER TOUR", "max": 32},
    "Challenge ASBT - 2ème Tour (09h00)": {"sheet": "ASBT 2ÈME TOUR", "max": 32}
}

if "user_asbt" not in st.session_state:
    st.session_state.user_asbt = None

# --- MENU NAVIGATION ADAPTÉ MOBILE ---
with st.sidebar:
    st.image("LOGO_ASBT_SANS_FOND_BLANC.png", use_container_width=True)
    st.markdown("---")
    menu = st.radio("Aller à :", ["🏠 Accueil & Places", "📝 Formulaire d'Inscription", "👥 Liste des Inscrits", "🔐 Annuler une inscription"])
    st.markdown("---")
    if st.session_state.user_asbt:
        st.success(f"👤 Connecté : {st.session_state.user_asbt['nom']}")
        if st.button("Déconnexion"):
            st.session_state.user_asbt = None
            st.rerun()

# ==========================================
# 🏠 ÉCRAN D'ACCUEIL
# ==========================================
if menu == "🏠 Accueil & Places":
    st.markdown('<div class="marquee-container"><div class="marquee-text">📞 INSCRIPTION SUR SMARTPHONE OU PAR TÉLÉPHONE AU 06 36 37 18 93 — PAS DE PAIEMENT EN LIGNE — RÈGLEMENT SUR PLACE LE JOUR DU CONCOURS</div></div>', unsafe_allow_index=True)
    st.markdown('<h1 class="main-title">A.S.B. TRAMOLÉ - Saison 2026</h1>', unsafe_allow_index=True)
    st.info("ℹ️ Règlement des concours : Les règlements se feront sur place le jour même du concours lors de la présentation des licences.")
    st.write("### 📅 Disponibilités en Temps Réel :")

    for label, info in ONGLETS_CONCOURS.items():
        try:
            df_c = conn.read(worksheet=info["sheet"])
            occupes = df_c['NOM'].dropna().count()
        except:
            occupes = 0
        restantes = info["max"] - occupes
        with st.container():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"""
                <div class="concours-card">
                    <h5 style="margin:0 0 5px 0; color:#003399;">{label}</h5>
                    <p style="margin:0; font-size:14px;"><b>Statut :</b> {"<span class='complet-txt'>❌ COMPLET</span>" if restantes<=0 else f"<span class='dispo-txt'>✅ {restantes} places libres sur {info['max']}</span>"}</p>
                </div>
                """, unsafe_allow_index=True)
            with col2:
                if restantes <= 0:
                    if st.button("Complet 🚫", key=f"home_comp_{info['sheet']}"):
                        st.error("Ce concours est complet ! Pour vous inscrire sur liste d'attente, contactez le 06 36 37 18 93.")
                else:
                    if st.button("S'inscrire 🎯", key=f"home_go_{info['sheet']}"):
                        st.session_state["selected_sheet_label"] = label
                        st.info("👉 Ouvrez l'onglet 'Formulaire d'Inscription' dans le menu pour vous inscrire.")
    st.markdown("---")
    st.caption("📍 Adresse : Clos Bouliste de l'A.S.B. Tramolé, 38300 Tramolé.")

# ==========================================
# 📝 FORMULAIRE D'INSCRIPTION
# ==========================================
elif menu == "📝 Formulaire d'Inscription":
    st.markdown('<h2 class="main-title">Saisie de l\'Inscription</h2>', unsafe_allow_index=True)
    label_defaut = st.session_state.get("selected_sheet_label", list(ONGLETS_CONCOURS.keys())[0])
    choix = st.selectbox("Sélectionnez le concours :", list(ONGLETS_CONCOURS.keys()), index=list(ONGLETS_CONCOURS.keys()).index(label_defaut))
    info_target = ONGLETS_CONCOURS[choix]
    df_target = conn.read(worksheet=info_target["sheet"])
    occupes = df_target['NOM'].dropna().count()
    restantes = info_target["max"] - occupes
    st.metric("Places restantes", int(restantes))

    if restantes <= 0:
        st.error("Désolé, ce concours est complet.")
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
                        st.success("🎉 Inscription validée en temps réel !")
                        st.balloons()
                    else:
                        st.error("Erreur : Plus de places disponibles.")

# ==========================================
# 👥 LISTE DES INSCRITS (Verrouillée)
# ==========================================
elif menu == "👥 Liste des Inscrits":
    st.markdown('<h2 class="main-title">Liste des Joueurs Engagés</h2>', unsafe_allow_index=True)
    choix = st.selectbox("Sélectionnez le concours :", list(ONGLETS_CONCOURS.keys()))
    df_visu = conn.read(worksheet=ONGLETS_CONCOURS[choix]["sheet"])
    df_presents = df_visu.dropna(subset=['NOM'])
    st.write(f"📊 **Inscrits actuels : {len(df_presents)}**")
    if df_presents.empty:
        st.info("Aucune inscription enregistrée pour le moment.")
    else:
        st.dataframe(df_presents[['RANG', 'NOM', 'PRÉNOM', 'SOCIÉTÉ', 'DATE INSCRIPTION']], use_container_width=True, hide_index=True)
        st.caption("🔒 Liste officielle horodatée et non modifiable.")

# ==========================================
# 🔐 ANNULATION ET COMPTE SÉCURISÉ
# ==========================================
elif menu == "🔐 Annulation & Compte":
    st.markdown('<h2 class="main-title">Espace Désinscription Autonome</h2>', unsafe_allow_index=True)
    t_co, t_creer, t_action = st.tabs(["Connexion", "Créer un compte", "Mes Annulations"])

    with t_creer:
        st.write("Créez votre compte pour gérer votre inscription de manière autonome.")
        c_nom = st.text_input("Votre NOM de famille").upper().strip()
        c_tel = st.text_input("Votre numéro de portable").strip()
        if st.button("Enregistrer mon accès smartphone"):
            st.success("Compte mémorisé ! Connectez-vous sur l'onglet de gauche.")

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
            st.warning("Veuillez vous connecter pour annuler votre inscription.")
        else:
            u = st.session_state.user_asbt
            st.write(f"Recherche d'inscriptions pour **{u['nom']}** :")
            trouve = False
            for label, info in ONGLETS_CONCOURS.items():
                df_c = conn.read(worksheet=info["sheet"])
                mes_lignes = df_c[(df_c['NOM'] == u['nom']) & (df_c['MOBILE'].astype(str).str.contains(u['tel']))]
                for idx, row in mes_lignes.iterrows():
                    trouve = True
                    st.warning(f"📍 {label} — Rang {row['RANG']}")
                    if st.button(f"Annuler ma place (Rang {row['RANG']}) ❌", key=f"del_{info['sheet']}_{idx}"):
                        df_c.at[idx, 'NOM'] = None
                        df_c.at[idx, 'PRÉNOM'] = None
                        df_c.at[idx, 'SOCIÉTÉ'] = None
                        df_c.at[idx, 'MOBILE'] = None
                        df_c.at[idx, 'DATE INSCRIPTION'] = None
                        conn.update(worksheet=info["sheet"], data=df_c)
                        st.error("Votre inscription a été annulée avec succès.")
                        st.rerun()
            if not trouve:
                st.info("Aucune inscription trouvée à ce nom. En cas d'erreur, contactez le 06 36 37 18 93.")
