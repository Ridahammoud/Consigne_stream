import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Visualisation des heures", layout="wide")

st.title("⏱️ Visualisation des heures travaillées")
st.markdown("Chargez un fichier Excel contenant les colonnes : **Nom et prénom**, Heures jour, Heures nuit, Heures dimanche, Heures supp, Heures Férié, Total (h), etc.")

# Upload du fichier Excel
uploaded_file = st.file_uploader("📂 Charger le fichier Excel", type=["xlsx", "xls"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)

        st.subheader("📋 Aperçu du tableau")
        st.dataframe(df.style.background_gradient(cmap='Blues', subset=["Total (h)"]))

        # Liste des colonnes d'heures
        hour_cols = ["Heures jour", "Heures nuit", "Heures dimanche", "Heures supp", "Heures Férié"]

        # Graphique en barres empilées
        st.subheader("📊 Répartition des heures par type")
        fig1 = px.bar(
            df,
            x="Nom et prénom",
            y=hour_cols,
            title="Répartition des heures travaillées par type",
            labels={"value": "Heures", "variable": "Type d'heure"},
            barmode="stack"
        )
        st.plotly_chart(fig1, use_container_width=True)

        # Graphique total par personne
        st.subheader("🏁 Total des heures par personne")
        fig2 = px.bar(
            df,
            x="Total (h)",
            y="Nom et prénom",
            orientation="h",
            color="Total (h)",
            color_continuous_scale="blues",
            title="Total des heures par personne"
        )
        st.plotly_chart(fig2, use_container_width=True)

        # Choix de la colonne pour le camembert
        st.subheader("🥧 Camembert par type d’heure")
        selected_col = st.selectbox("Choisissez une colonne à visualiser", hour_cols)

        fig3 = px.pie(
            df,
            values=selected_col,
            names="Nom et prénom",
            title=f"Répartition des {selected_col} entre les personnes",
            hole=0.3
        )
        st.plotly_chart(fig3, use_container_width=True)

    except Exception as e:
        st.error(f"Erreur lors de la lecture du fichier : {e}")
else:
    st.info("Veuillez charger un fichier Excel pour commencer.")
