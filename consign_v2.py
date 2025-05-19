import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Visualisation des heures", layout="wide")

st.title("⏱️ Visualisation des heures travaillées")
st.markdown("Chargez un fichier Excel avec les colonnes suivantes : **Nom et prénom**, Heures jour, Heures nuit, Heures dimanche, Heures supp, Heures Férié, Total (h).")

uploaded_file = st.file_uploader("📂 Charger le fichier Excel", type=["xlsx", "xls"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)

        # Nettoyage : s'assurer que les colonnes numériques sont bien au bon format
        heure_cols = ["Heures jour", "Heures nuit", "Heures dimanche", "Heures supp", "Heures Férié", "Total (h)"]
        for col in heure_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            df[col] = df[col].round(2)

        st.subheader("📋 Aperçu du tableau")
        st.dataframe(df.style.background_gradient(cmap='Blues', subset=["Total (h)"]))

        hour_cols = ["Heures jour", "Heures nuit", "Heures dimanche", "Heures supp", "Heures Férié"]

        # Répartition des heures par type
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

        # Tabs : Tous / Top 10 / Top 20
        st.subheader("🏁 Total des heures par personne")
        tabs = st.tabs(["🔍 Tous", "⭐ Top 10", "🔥 Top 20"])

        # Slider de filtrage
        with tabs[0]:
            min_hours = st.slider("Filtrer les personnes avec plus de :", 0, int(df["Total (h)"].max()), 0)
            df_filtered = df[df["Total (h)"] >= min_hours].sort_values("Total (h)", ascending=True)

            fig_height = max(500, len(df_filtered) * 40)

            fig2 = px.bar(
                df_filtered,
                x="Total (h)",
                y="Nom et prénom",
                orientation="h",
                color="Total (h)",
                color_continuous_scale="Blues",
                title="Total des heures par personne"
            )
            fig2.update_layout(
                height=fig_height,
                margin=dict(l=150, r=20, t=50, b=20),
                yaxis_title=None
            )
            st.plotly_chart(fig2, use_container_width=True)

        # Top 10
        with tabs[1]:
            top10 = df.sort_values("Total (h)", ascending=False).head(10)
            fig_top10 = px.bar(
                top10.sort_values("Total (h)", ascending=True),
                x="Total (h)",
                y="Nom et prénom",
                orientation="h",
                color="Total (h)",
                color_continuous_scale="Blues",
                title="Top 10 - Total des heures"
            )
            st.plotly_chart(fig_top10, use_container_width=True)

        # Top 20
        with tabs[2]:
            top20 = df.sort_values("Total (h)", ascending=False).head(20)
            fig_top20 = px.bar(
                top20.sort_values("Total (h)", ascending=True),
                x="Total (h)",
                y="Nom et prénom",
                orientation="h",
                color="Total (h)",
                color_continuous_scale="Blues",
                title="Top 20 - Total des heures"
            )
            st.plotly_chart(fig_top20, use_container_width=True)

        # Camembert dynamique
        st.subheader("🥧 Camembert par type d’heure")
        selected_col = st.selectbox("Choisissez une colonne à visualiser :", hour_cols)

        fig_pie = px.pie(
            df,
            values=selected_col,
            names="Nom et prénom",
            title=f"Répartition des {selected_col}",
            hole=0.3
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    except Exception as e:
        st.error(f"Erreur lors de la lecture ou du traitement du fichier : {e}")
else:
    st.info("Veuillez charger un fichier Excel pour commencer.")
