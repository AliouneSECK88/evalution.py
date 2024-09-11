import streamlit as st
import pandas as pd
import hashlib
import os
from fpdf import FPDF
from io import BytesIO

# Dictionnaire simple pour stocker les noms d'utilisateurs et mots de passe
users = {
    "Alioune SECK": "password123",
    "Mouhamed Naby GUEYE": "password124",
    "Sokhna Adama MBACKE": "password125",
    "AMI SYLLA": "password1236",
    "EL HADJI FALLOU DIOP": "password1237",
    "evaluator6": "securepass7",
    "evaluator7": "mypassword7",
}


# Fonction pour hasher les mots de passe
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# Fonction pour vérifier les identifiants de l'utilisateur
def check_credentials(username, password):
    if username in users and hash_password(password) == hash_password(users[username]):
        return True
    return False


# Fonction pour enregistrer les évaluations dans un fichier CSV
def save_evaluation(data):
    if os.path.exists("evaluations.csv"):
        data.to_csv("evaluations.csv", mode="a", header=False, index=False)
    else:
        data.to_csv("evaluations.csv", index=False)


# Fonction pour charger les évaluations existantes à partir d'un fichier CSV
def load_evaluations():
    if os.path.exists("evaluations.csv"):
        return pd.read_csv("evaluations.csv")
    else:
        return pd.DataFrame(
            columns=[
                "Utilisateur",
                "Société",
                "Missions Audit SI",
                "Missions SMSI",
                "Missions Intégration",
                "Approche Technique",
                "Plan de Travail",
                "Organisation Personnel",
                "Qualif Directeur",
                "Expérience Directeur",
                "Expérience Pertinente Directeur",
                "Langue et Région Directeur",
                "Qualif Expert Audit",
                "Expérience Expert Audit",
                "Expérience Pertinente Expert Audit",
                "Langue et Région Expert Audit",
                "Qualif Expert Sécurité",
                "Expérience Expert Sécurité",
                "Expérience Pertinente Expert Sécurité",
                "Langue et Région Expert Sécurité",
                "Commentaires Expérience",
                "Commentaires Conformité",
                "Commentaires Qualifications",
            ]
        )


# Fonction pour enregistrer l'état de progression dans un fichier spécifique à l'utilisateur
def save_progress(username, progress_data):
    filepath = f"{username}_progress.csv"
    progress_data.to_csv(filepath, index=False)


# Fonction pour charger l'état de progression de l'utilisateur
def load_progress(username):
    filepath = f"{username}_progress.csv"
    if os.path.exists(filepath):
        return pd.read_csv(filepath)
    else:
        return pd.DataFrame(
            columns=[
                "Société",
                "Missions Audit SI",
                "Missions SMSI",
                "Missions Intégration",
                "Approche Technique",
                "Plan de Travail",
                "Organisation Personnel",
                "Qualif Directeur",
                "Expérience Directeur",
                "Expérience Pertinente Directeur",
                "Langue et Région Directeur",
                "Qualif Expert Audit",
                "Expérience Expert Audit",
                "Expérience Pertinente Expert Audit",
                "Langue et Région Expert Audit",
                "Qualif Expert Sécurité",
                "Expérience Expert Sécurité",
                "Expérience Pertinente Expert Sécurité",
                "Langue et Région Expert Sécurité",
                "Commentaires Expérience",
                "Commentaires Conformité",
                "Commentaires Qualifications",
            ]
        )


# Fonction pour générer un fichier PDF avec les évaluations
def generate_pdf(evaluation_data):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", size=12)
    pdf.cell(
        200, 10, txt="Evaluation des sociétés soumissionnaires", ln=True, align="C"
    )

    # Adding evaluation data to the PDF
    for index, row in evaluation_data.iterrows():
        pdf.cell(200, 10, txt=f"Société: {row['Société']}", ln=True, align="L")
        pdf.cell(
            200,
            10,
            txt=f"Score Expérience: {row['Missions Audit SI']} / 10",
            ln=True,
            align="L",
        )
        pdf.cell(
            200,
            10,
            txt=f"Score Conformité: {row['Approche Technique']} / 30",
            ln=True,
            align="L",
        )
        pdf.cell(
            200,
            10,
            txt=f"Score Qualifications: {row['Qualif Directeur']} / 60",
            ln=True,
            align="L",
        )
        pdf.cell(
            200,
            10,
            txt=f"Commentaires Expérience: {row['Commentaires Expérience']}",
            ln=True,
            align="L",
        )
        pdf.cell(
            200,
            10,
            txt=f"Commentaires Conformité: {row['Commentaires Conformité']}",
            ln=True,
            align="L",
        )
        pdf.cell(
            200,
            10,
            txt=f"Commentaires Qualifications: {row['Commentaires Qualifications']}",
            ln=True,
            align="L",
        )
        pdf.cell(
            200,
            10,
            txt="--------------------------------------------------------",
            ln=True,
            align="L",
        )

    # Saving to BytesIO buffer instead of a file
    pdf_buffer = BytesIO()
    pdf.output(pdf_buffer)  # save PDF to buffer
    pdf_buffer.seek(0)

    return pdf_buffer


# Titre de l'application Streamlit
st.title("Évaluation des sociétés soumissionnaires")

# Initialiser l'état de session pour la connexion
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False  # Utilisateur non authentifié par défaut
if "username" not in st.session_state:
    st.session_state["username"] = ""  # Nom d'utilisateur vide par défaut

# Formulaire de connexion
if not st.session_state["authenticated"]:
    st.sidebar.header("Connexion")
    username = st.sidebar.text_input("Nom d'utilisateur")
    password = st.sidebar.text_input("Mot de passe", type="password")
    login_button = st.sidebar.button("Connexion")

    if login_button:
        if check_credentials(username, password):
            st.sidebar.success("Connexion réussie!")
            st.session_state["authenticated"] = True
            st.session_state["username"] = username
        else:
            st.sidebar.error("Nom d'utilisateur ou mot de passe incorrect.")

# Vérifier si l'utilisateur est authentifié
if st.session_state["authenticated"]:
    # Définir les sociétés à évaluer
    societes = ["Deloitte", "GT Technologies", "Forvis Mazars", "SYNAPSYS"]

    # Charger les évaluations existantes
    evaluations = load_evaluations()

    # Charger la progression de l'utilisateur
    progress_data = load_progress(st.session_state["username"])

    # Afficher les évaluations existantes sous forme de tableau
    st.subheader("Évaluations existantes")
    st.dataframe(evaluations)

    # Initialiser un dataframe pour les nouvelles évaluations
    df = pd.DataFrame(
        columns=[
            "Société",
            "Missions Audit SI",
            "Missions SMSI",
            "Missions Intégration",
            "Approche Technique",
            "Plan de Travail",
            "Organisation Personnel",
            "Qualif Directeur",
            "Expérience Directeur",
            "Expérience Pertinente Directeur",
            "Langue et Région Directeur",
            "Qualif Expert Audit",
            "Expérience Expert Audit",
            "Expérience Pertinente Expert Audit",
            "Langue et Région Expert Audit",
            "Qualif Expert Sécurité",
            "Expérience Expert Sécurité",
            "Expérience Pertinente Expert Sécurité",
            "Langue et Région Expert Sécurité",
            "Commentaires Expérience",
            "Commentaires Conformité",
            "Commentaires Qualifications",
        ]
    )

    # Section pour chaque société
    for societe in societes:
        st.header(f"Évaluation pour {societe}")

        # Charger les choix précédents si disponibles
        previous_data = progress_data[progress_data["Société"] == societe]

        prev_missions_audit_si = (
            int(previous_data["Missions Audit SI"].values[0])
            if not previous_data["Missions Audit SI"].isna().all()
            else 0
        )
        prev_missions_smsi = (
            int(previous_data["Missions SMSI"].values[0])
            if not previous_data["Missions SMSI"].isna().all()
            else 0
        )
        prev_missions_integration = (
            int(previous_data["Missions Intégration"].values[0])
            if not previous_data["Missions Intégration"].isna().all()
            else 0
        )
        prev_approche_technique = (
            int(previous_data["Approche Technique"].values[0])
            if not previous_data["Approche Technique"].isna().all()
            else 0
        )
        prev_plan_travail = (
            int(previous_data["Plan de Travail"].values[0])
            if not previous_data["Plan de Travail"].isna().all()
            else 0
        )
        prev_organisation_personnel = (
            int(previous_data["Organisation Personnel"].values[0])
            if not previous_data["Organisation Personnel"].isna().all()
            else 0
        )

        # Charger les commentaires précédents si disponibles
        prev_comment_exp = (
            previous_data["Commentaires Expérience"].values[0]
            if not previous_data["Commentaires Expérience"].isna().all()
            else ""
        )
        prev_comment_conf = (
            previous_data["Commentaires Conformité"].values[0]
            if not previous_data["Commentaires Conformité"].isna().all()
            else ""
        )
        prev_comment_qualif = (
            previous_data["Commentaires Qualifications"].values[0]
            if not previous_data["Commentaires Qualifications"].isna().all()
            else ""
        )

        # Section 1: Expérience des Candidats pertinente pour la mission
        st.subheader("Expérience des Candidats pertinente pour la mission (10 points)")

        # Grille d'évaluation pour les missions avec les valeurs maximales correctes
        missions_audit_si = st.radio(
            "Missions d’audit SI (au cours des 5 dernières années, max 2.5)",
            [0, 1],
            key=f"missions_audit_si_{societe}",
        )
        missions_smsi = st.radio(
            "Missions d’accompagnement SMSI (au cours des 3 dernières années, max 5)",
            [0, 1, 2],
            key=f"missions_smsi_{societe}",
        )
        missions_integration = st.radio(
            "Missions d’intégration de solutions de sécurité (au cours des 2 dernières années, max 2.5)",
            [0, 1],
            key=f"missions_integration_{societe}",
        )

        # Calculer le score pour l'expérience
        score_experience = (
            missions_audit_si * 2.5 + missions_smsi * 2.5 + missions_integration * 2.5
        )

        st.write(f"**Score total pour l'expérience: {score_experience} / 10**")

        # Commentaire pour la rubrique Expérience des Candidats
        commentaire_experience = st.text_area(
            "Commentaires pour Expérience des Candidats",
            value=prev_comment_exp,
            key=f"comment_exp_{societe}",
        )

        # Section 2: Conformité du plan de travail et de la méthode proposés
        st.subheader(
            "Conformité du plan de travail et de la méthode proposés (30 points)"
        )

        approche_technique = st.selectbox(
            "Approche technique et méthodologie (max 15)",
            list(range(0, 16)),
            index=prev_approche_technique,
            key=f"approche_technique_{societe}",
        )
        plan_de_travail = st.selectbox(
            "Plan de travail (max 7)",
            list(range(0, 8)),
            index=prev_plan_travail,
            key=f"plan_de_travail_{societe}",
        )
        organisation_personnel = st.selectbox(
            "Organisation et personnel (max 8)",
            list(range(0, 9)),
            index=prev_organisation_personnel,
            key=f"organisation_personnel_{societe}",
        )

        # Commentaire pour la rubrique Conformité
        commentaire_conformite = st.text_area(
            "Commentaires pour Conformité du plan de travail",
            value=prev_comment_conf,
            key=f"comment_conf_{societe}",
        )

        # Section 3: Qualifications et compétence du personnel pour la mission (60 points)
        st.subheader(
            "Qualifications et compétence du personnel pour la mission (60 points)"
        )

        qualif_directeur = st.selectbox(
            "Qualif. Directeur (max 7)",
            list(range(0, 8)),
            key=f"qualif_directeur_{societe}",
        )
        experience_pertinente_directeur = st.selectbox(
            "Expérience pertinente Directeur (max 15)",
            [0, 5, 10, 15],
            key=f"experience_pertinente_directeur_{societe}",
        )
        langue_region_directeur = st.selectbox(
            "Langue et Région Directeur (max 3)",
            [0, 1.5, 3],
            key=f"langue_region_directeur_{societe}",
        )

        qualif_expert_audit = st.selectbox(
            "Qualif. Expert Audit (max 6)",
            list(range(0, 7)),
            key=f"qualif_expert_audit_{societe}",
        )
        experience_pertinente_expert_audit = st.selectbox(
            "Expérience pertinente Expert Audit (max 12)",
            [0, 4, 8, 12],
            key=f"experience_pertinente_expert_audit_{societe}",
        )
        langue_region_expert_audit = st.selectbox(
            "Langue et Région Expert Audit (max 2)",
            [0, 1, 2],
            key=f"langue_region_expert_audit_{societe}",
        )

        qualif_expert_securite = st.selectbox(
            "Qualif. Expert Sécurité (max 4)",
            list(range(0, 5)),
            key=f"qualif_expert_securite_{societe}",
        )
        experience_pertinente_expert_securite = st.selectbox(
            "Expérience pertinente Expert Sécurité (max 9)",
            [0, 3, 6, 9],
            key=f"experience_pertinente_expert_securite_{societe}",
        )
        langue_region_expert_securite = st.selectbox(
            "Langue et Région Expert Sécurité (max 2)",
            [0, 1, 2],
            key=f"langue_region_expert_securite_{societe}",
        )

        # Commentaire pour la rubrique Qualifications
        commentaire_qualifications = st.text_area(
            "Commentaires pour Qualifications et compétence du personnel",
            value=prev_comment_qualif,
            key=f"comment_qualif_{societe}",
        )

        # Calcul des scores
        score_experience = (
            missions_audit_si * 2.5 + missions_smsi * 2.5 + missions_integration * 2.5
        )
        score_conformite = approche_technique + plan_de_travail + organisation_personnel
        score_qualifications = (
            + qualif_directeur
            + experience_pertinente_directeur
            + langue_region_directeur
            + qualif_expert_audit
            + experience_pertinente_expert_audit
            + langue_region_expert_audit
            + qualif_expert_securite
            + experience_pertinente_expert_securite
            + langue_region_expert_securite
        )

        st.write(f"Score total pour l'expérience: {score_experience} / 10")
        st.write(f"Score total pour la conformité: {score_conformite} / 30")
        st.write(f"Score total pour les qualifications: {score_qualifications} / 60")

        # Sauvegarder la progression
        new_row = pd.DataFrame(
            {
                "Société": [societe],
                "Missions Audit SI": [missions_audit_si],
                "Missions SMSI": [missions_smsi],
                "Missions Intégration": [missions_integration],
                "Approche Technique": [approche_technique],
                "Plan de Travail": [plan_de_travail],
                "Organisation Personnel": [organisation_personnel],
                "Qualif Directeur": [qualif_directeur],
                "Expérience Pertinente Directeur": [experience_pertinente_directeur],
                "Langue et Région Directeur": [langue_region_directeur],
                "Qualif Expert Audit": [qualif_expert_audit],
                "Expérience Pertinente Expert Audit": [
                    experience_pertinente_expert_audit
                ],
                "Langue et Région Expert Audit": [langue_region_expert_audit],
                "Qualif Expert Sécurité": [qualif_expert_securite],
                "Expérience Pertinente Expert Sécurité": [
                    experience_pertinente_expert_securite
                ],
                "Langue et Région Expert Sécurité": [langue_region_expert_securite],
                "Commentaires Expérience": [commentaire_experience],
                "Commentaires Conformité": [commentaire_conformite],
                "Commentaires Qualifications": [commentaire_qualifications],
            }
        )
        df = pd.concat([df, new_row], ignore_index=True)

    # Enregistrer la progression de l'utilisateur
    save_progress(st.session_state["username"], df)

    # Ajouter un bouton pour générer et télécharger un fichier PDF
    if st.button("Télécharger en PDF"):
        pdf_data = generate_pdf(df)
        st.download_button(
            label="Cliquez ici pour télécharger le PDF",
            data=pdf_data,
            file_name="evaluation.pdf",
            mime="application/pdf",
        )

# Déconnexion
if st.sidebar.button("Déconnexion"):
    st.session_state["authenticated"] = False
    st.session_state["username"] = ""
    st.query_params.to_dict()
