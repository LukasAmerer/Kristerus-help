import streamlit as st
from PIL import Image
import os
from streamlit_option_menu import option_menu

# --- Page Configuration ---
st.set_page_config(page_title="KMUmeetKI", layout="wide")

# CSS / global styles
st.markdown(
    """
    <style>
    .stApp {
        background-color: #ffffff;
    }
    /* Reduce margins so content appears full width */
    .block-container {
        padding-top: 0rem;
        padding-left: 0rem;
        padding-right: 0rem;
    }
    /* Hide default Streamlit header/footer */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    a { text-decoration: none; }
    </style>
    """,
    unsafe_allow_html=True,
)

GREEN = "#00802F"

# ----------------------------
# TOP-BEREICH: LOGO + MENÜ
# ----------------------------
with st.container():
    col_logo, col_menu, col_right = st.columns([1, 4, 1])

    # Logo
    with col_logo:
        logo_path = "CS_Projekt_P_selber_images/KMUmeetKI_Logo.png"
        if os.path.exists(logo_path):
            try:
                logo_img = Image.open(logo_path)
                st.image(logo_img, width=150)
            except Exception as e:
                st.warning(f"Fehler beim Laden des Logos: {e}")
        else:
            st.warning(f"Logo nicht gefunden: {logo_path}")

    # Menü in der Mitte
    with col_menu:
        selected = option_menu(
            menu_title=None,
            options=[
                "Wissen",
                "Anwendungen von KI",
                "Angebot und Team",
                "Partner & Anbieter",
                "Research Assistant",
            ],
            icons=[None] * 5,
            default_index=0,
            orientation="horizontal",
            styles={
                "container": {
                    "padding": "20px 0px 0px 0px",
                    "background-color": "#ffffff",
                },
                "nav-link": {
                    "font-size": "14px",
                    "font-weight": "600",
                    "color": GREEN,
                    "margin": "0 60px 0 0",
                    "padding": "0 0 8px 0",
                    "text-align": "left",
                    "text-decoration": "none",
                    "letter-spacing": "0.15em",
                    "--hover-color": "#ffffff",
                },
                "nav-link-selected": {
                    "color": GREEN,
                    "background-color": "#ffffff",
                    "border-bottom": f"3px solid {GREEN}",
                },
            },
        )

    # rechter Bereich leer, damit Menü zentriert ist
    with col_right:
        st.write("")


# ============================================================
# SEITE 1: WISSEN – komplette Landingpage
# ============================================================
def render_wissen():
    # ---------- HERO ----------
    st.markdown(
        f"""
        <div style="padding: 60px 80px 40px 80px;">
            <div style="font-size: 48px; font-weight: 700; color: {GREEN};
                        font-family: sans-serif; margin-bottom: 8px;">
                KMUmeetKI
            </div>
            <div style="font-size: 20px; font-weight: 500; color: {GREEN};
                        font-family: sans-serif; margin-bottom: 16px;">
                Die zentrale KI-Wissensplattform für KMU
            </div>
            <div style="height: 3px; width: 260px; background-color: {GREEN};"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # schmaler grüner Balken
    st.markdown(
        f"""<div style="height: 8px; background-color: {GREEN}; width: 100%;"></div>""",
        unsafe_allow_html=True,
    )

    # ---------- GRÜNER BLOCK "Alles rund um Künstliche Intelligenz" ----------
    st.markdown(
        f"""
        <div style="background-color: {GREEN}; width: 100%; padding: 40px 80px 80px 80px;">
            <div style="font-size: 36px; font-weight: 700; color: #ffffff; font-family: sans-serif; margin-bottom: 8px;">
                Alles rund um Künstliche Intelligenz
            </div>
            <div style="font-size: 16px; color: #ffffff; font-family: sans-serif; margin-bottom: 32px;">
                Für KMU und KI-Enthusiasten – praxisorientiert, verständlich, befähigend.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ---------- 4 KARTEN (2×2) ----------
    card_style = """
        margin-top: -60px;
        background-color: #ffffff;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
        font-family: sans-serif;
        min-height: 180px;
    """

    cards_row1 = [
        {
            "title": "Grundlagen & Verständnis zu KI",
            "text": "Alles rund um die wichtigsten Begrifflichkeiten im Zusammenhang mit KI: einfach erklärt und nachvollziehbar.",
            "button": "Mehr Infos",
        },
        {
            "title": "Das wichtigste im Umgang mit ChatGPT & Co.",
            "text": "Lernen Sie die Kunst des Prompting kennen. Erfahren Sie, wie Sie das volle Potenzial von KI-Systemen wie ChatGPT & Co. ausschöpfen.",
            "button": "Mehr Infos",
        },
    ]

    cards_row2 = [
        {
            "title": "KI-Tools für den Arbeitsalltag",
            "text": "Entdecken Sie eine Auswahl an KI-Tools, die Ihnen helfen, Ihre Produktivität und Kreativität im Berufsalltag zu steigern.",
            "button": "Mehr Infos",
        },
        {
            "title": "KI-gestützte Marketingstrategien",
            "text": "Erfahren Sie, wie KI-Technologien genutzt werden können, um Marketingkampagnen zu optimieren und personalisierte Kundenerlebnisse zu schaffen.",
            "button": "Mehr Infos",
        },
    ]

    # Erste Reihe
    with st.container():
        cols = st.columns(2, gap="large")
        for col, card in zip(cols, cards_row1):
            col.markdown(
                f"""
                <div style="{card_style} margin-left: 80px; margin-right: 20px;">
                    <div style="font-size: 18px; font-weight: 700; color: {GREEN}; 
                                margin-bottom: 8px; white-space: pre-line;">
                        {card['title']}
                    </div>
                    <div style="font-size: 14px; color: #333333; margin-bottom: 16px;">
                        {card['text']}
                    </div>
                    <a href="#"
                       style="display: inline-block; padding: 8px 18px; border-radius: 20px;
                              background-color: {GREEN}; color: #ffffff; font-size: 13px; font-weight: 600;">
                        {card['button']}
                    </a>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # Zweite Reihe
    with st.container():
        cols = st.columns(2, gap="large")
        for col, card in zip(cols, cards_row2):
            col.markdown(
                f"""
                <div style="{card_style} margin-left: 80px; margin-right: 20px; margin-top: 20px;">
                    <div style="font-size: 18px; font-weight: 700; color: {GREEN}; 
                                margin-bottom: 8px; white-space: pre-line;">
                        {card['title']}
                    </div>
                    <div style="font-size: 14px; color: #333333; margin-bottom: 16px;">
                        {card['text']}
                    </div>
                    <a href="#"
                       style="display: inline-block; padding: 8px 18px; border-radius: 20px;
                              background-color: {GREEN}; color: #ffffff; font-size: 13px; font-weight: 600;">
                        {card['button']}
                    </a>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # ---------- SEKTION: "Die wichtigsten Grundlagen rund um KI" ----------
    st.markdown("<div style='height: 60px;'></div>", unsafe_allow_html=True)

    st.markdown(
        f"""
        <div style="height: 8px; background-color: {GREEN}; width: 100%;"></div>
        """,
        unsafe_allow_html=True,
    )

    with st.container():
        col_text, col_img = st.columns(2)

        with col_text:
            st.markdown(
                f"""
                <div style="background-color: #ffffff; padding: 60px 80px; font-family: sans-serif;">
                    <div style="font-size: 32px; font-weight: 700; color: {GREEN}; margin-bottom: 16px;">
                        Die wichtigsten Grundlagen rund um KI
                    </div>
                    <div style="font-size: 15px; color: #333333; margin-bottom: 24px;">
                        Anwendungen &amp; Use Cases
                    </div>
                    <a href="#"
                       style="display: inline-block; padding: 10px 24px; border-radius: 24px;
                              background-color: {GREEN}; color: #ffffff; font-size: 14px; font-weight: 600;">
                        Mehr Infos
                    </a>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col_img:
            st.markdown(
                """
                <div style="
                    height:260px;
                    margin-right: 80px;
                    margin-top: 60px;
                    background-color: #e5e5e5;
                    border-radius: 8px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-family: sans-serif;
                    color: #777777;
                    font-size: 14px;
                ">
                    Bild / Illustration zu KI (Platzhalter)
                </div>
                """,
                unsafe_allow_html=True,
            )

    # ---------- 2×2 GRID MIT TEXT + BILDERN ----------
    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)

    with st.container():
        col_img1, col_text1 = st.columns(2)

        with col_img1:
            st.markdown(
                """
                <div style="
                    height:260px;
                    margin-left: 80px;
                    margin-right: 20px;
                    background-color: #f0f0f0;
                    border-radius: 8px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-family: sans-serif;
                    color: #777777;
                    font-size: 14px;
                ">
                    Bild: Roboter-Hand (Platzhalter)
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col_text1:
            st.markdown(
                f"""
                <div style="padding:60px 80px 0 20px; font-family:sans-serif;">
                    <div style="font-size:28px; font-weight:700; color:{GREEN}; margin-bottom:16px;">
                        Anwendungen &amp; Use Cases
                    </div>
                    <div style="font-size:15px; color:#333333; margin-bottom:24px;">
                        Beispiele, wie KI heute schon in Marketing, Kundenservice, Administration
                        oder Strategie eingesetzt wird.
                    </div>
                    <a href="#"
                       style="display:inline-block; padding:10px 24px; border-radius:24px;
                              background-color:{GREEN}; color:#ffffff; font-size:14px;
                              font-weight:600;">
                        Mehr Infos
                    </a>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with st.container():
        col_text2, col_img2 = st.columns(2)

        with col_text2:
            st.markdown(
                f"""
                <div style="padding:60px 20px 60px 80px; font-family:sans-serif;">
                    <div style="font-size:28px; font-weight:700; color:{GREEN}; margin-bottom:16px;">
                        KMUmeetKI unterstützen als Partner / Sponsor
                    </div>
                    <div style="font-size:15px; color:#333333; margin-bottom:24px;">
                        Positionieren Sie sich als Vorreiter im Bereich KI für KMU und unterstützen Sie den weiteren Ausbau der Plattform.
                    </div>
                    <a href="#"
                       style="display:inline-block; padding:10px 24px; border-radius:24px;
                              background-color:{GREEN}; color:#ffffff; font-size:14px;
                              font-weight:600;">
                        Jetzt Kontakt aufnehmen
                    </a>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col_img2:
            st.markdown(
                """
                <div style="
                    height:260px;
                    margin-left: 20px;
                    margin-right: 80px;
                    background-color: #f0f0f0;
                    border-radius: 8px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-family: sans-serif;
                    color: #777777;
                    font-size: 14px;
                ">
                    Bild: Handschlag / Partnerschaft (Platzhalter)
                </div>
                """,
                unsafe_allow_html=True,
            )

    # ---------- TOP 6 ANWENDUNGEN / USE CASES ----------
    st.markdown(
        f"""
        <div style ="background-color: {GREEN}; width: 100%; padding: 40px 80px 30px 80px; margin-top: 40px; font-family: sans-serif;">
            <div style="font-size: 32px; font-weight: 700; color: #ffffff; margin-bottom: 8px;">
                Top 6 Anwendungen / Use Cases
            </div>
            <div style="font-size: 15px; color: #ffffff;">
                Einfach umsetzbar, hoher Nutzen
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    use_cases = [
        {
            "category": "Kundenbetreuung / Costumer Success",
            "title": "Kundenrezensionen mit KI auswerten",
        },
        {
            "category": "Kundenbetreuung / Costumer Success",
            "title": "Einfachen Support Chatbot für die Website erstellen",
        },
        {
            "category": "Alltagsoptimierung, Strategie & Entwicklung",
            "title": "Diagramme & Grafiken aus Text automatisch erstellen",
        },
        {
            "category": "Alltagsoptimierung",
            "title": "Eigenen GPT für ein spezifisches Thema aufsetzen",
        },
        {
            "category": "Akquise & Vertrieb",
            "title": "Kaltakquise-Mails mit KI vorbereiten",
        },
        {
            "category": "Analytics & Insights",
            "title": "Trendanalyse aus Social-Media-Kommentaren",
        },
    ]

    card_style_uc = """
        background-color: #ffffff;
        border-radius: 12px;
        padding: 18px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
        font-family: sans-serif;
        min-height: 260px;
        margin-top: 30px;
    """

    index = 0
    for _ in range(2):
        cols = st.columns(3, gap="large")
        for col in cols:
            if index >= len(use_cases):
                break
            uc = use_cases[index]
            index += 1
            col.markdown(
                f"""
                <div style="{card_style_uc}">
                    <div style="font-size:12px; font-weight:600; color:{GREEN};
                                margin-bottom:6px;">
                        {uc['category']}
                    </div>
                    <div style="font-size:16px; font-weight:700; color:#111111;
                                margin-bottom:12px;">
                        {uc['title']}
                    </div>
                    <div style="font-size:13px; color:#555555; margin-bottom:16px;">
                        Kurzbeschreibung der Anwendung – warum sie nützlich ist und
                        in welchen Situationen sie sich anbietet.
                    </div>
                    <div style="
                        height:110px;
                        background-color:#f0f0f0;
                        border-radius:8px;
                        margin-bottom:16px;
                        display:flex;
                        align-items:center;
                        justify-content:center;
                        color:#777777;
                        font-size:12px;
                    ">
                        Bild / Screenshot (optional)
                    </div>
                    <a href="#"
                       style="display:inline-block; padding:8px 18px; border-radius:20px;
                              background-color:{GREEN}; color:#ffffff; font-size:13px;
                              font-weight:600;">
                        Mehr Infos
                    </a>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # Footer – nur auf Wissen-Seite
    st.markdown(
        f"""
        <div style="margin-top: 40px; padding: 20px 80px; border-top: 4px solid {GREEN};
                    font-family: sans-serif; font-size: 13px; text-align: center; color: {GREEN};">
            Kontakt | Feedbackformular | Eigene KI-Anwendung einreichen
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# SEITE 2–4: Platzhalter
# ============================================================
def render_anwendungen():
    st.markdown(
        f"""
        <div style="padding: 60px 80px; font-family: sans-serif;">
            <div style="font-size: 36px; font-weight: 700; color:{GREEN}; margin-bottom: 16px;">
                Anwendungen von KI
            </div>
            <div style="font-size: 15px; color:#333;">
                Platzhalter-Seite: Hier kannst du später deine konkreten Use Cases, Filter
                und Detailansichten einbauen.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_angebot_team():
    st.markdown(
        f"""
        <div style="padding: 60px 80px; font-family: sans-serif;">
            <div style="font-size: 36px; font-weight: 700; color:{GREEN}; margin-bottom: 16px;">
                Angebot &amp; Team
            </div>
            <div style="font-size: 15px; color:#333;">
                Platzhalter-Seite: Leistungen, Preise und Teamvorstellung.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_partner():
    st.markdown(
        f"""
        <div style="padding: 60px 80px; font-family: sans-serif;">
            <div style="font-size: 36px; font-weight: 700; color:{GREEN}; margin-bottom: 16px;">
                Partner &amp; Anbieter
            </div>
            <div style="font-size: 15px; color:#333;">
                Platzhalter-Seite: Logos, Kurzbeschreibungen und Links zu Partnern &amp; Tool-Anbietern.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# SEITE 5: RESEARCH ASSISTANT – ChatGPT-artig
# ============================================================
def render_research_assistant():
    # Sidebar wie ChatGPT: Projekte
    with st.sidebar:
        st.markdown(
            f"""
            <div style="font-size: 18px; font-weight: 700; color: {GREEN}; margin: 10px 0 4px 0;">
                Projekte
            </div>
            <div style="font-size: 12px; color: #555; margin-bottom: 12px;">
                Lege Projekte an und wechsle zwischen ihnen – ähnlich wie Chats in ChatGPT.
            </div>
            """,
            unsafe_allow_html=True,
        )

        if "ra_projects" not in st.session_state:
            st.session_state.ra_projects = ["Standard-Projekt"]

        selected_project = st.radio(
            "Aktives Projekt",
            st.session_state.ra_projects,
            index=0,
        )

        new_name = st.text_input("Neues Projekt anlegen", placeholder="z.B. KI für Kundenservice")
        if st.button("Projekt hinzufügen"):
            if new_name.strip():
                st.session_state.ra_projects.append(new_name.strip())
                st.success(f"Projekt '{new_name.strip()}' hinzugefügt.")

        st.markdown("---")
        st.markdown(
            f"""
            <div style="font-size: 12px; color: #555;">
                <b>Beispiel-Rollen im LLM-Council:</b><br/>
                • Strategische KI-Beratung<br/>
                • Daten- &amp; Use-Case-Analyst<br/>
                • Risiko &amp; Compliance<br/>
                • Umsetzungs-Coach
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Main-Bereich: Titel + Chat (wie ChatGPT-Mitte)
    st.markdown(
        f"""
        <div style="padding: 24px 80px 8px 80px; font-family: sans-serif;">
            <div style="font-size: 28px; font-weight: 700; color: {GREEN}; margin-bottom: 4px;">
                KMU Research Assistant
            </div>
            <div style="font-size: 13px; color: #555;">
                Projekt: <b>{selected_project}</b> – dein persönlicher Arbeitsbereich mit LLM-Council.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if "ra_messages" not in st.session_state:
        st.session_state.ra_messages = []

    for role, content in st.session_state.ra_messages:
        with st.chat_message(role):
            st.markdown(content)

    prompt = st.chat_input("Frag den Research Assistant oder beschreibe dein Vorhaben …")
    if prompt:
        st.session_state.ra_messages.append(("user", prompt))
        answer = (
            f"Du hast im Projekt **{selected_project}** gefragt:\n\n"
            f"> {prompt}\n\n"
            "Für die Abgabe kannst du hier später die echte Logik einbauen "
            "(LLM-Council, Analysen, Report-Generierung etc.)."
        )
        st.session_state.ra_messages.append(("assistant", answer))
        with st.chat_message("assistant"):
            st.markdown(answer)


# ============================================================
# ROUTING – es läuft IMMER nur genau eine Seite
# ============================================================
if selected == "Wissen":
    render_wissen()
elif selected == "Anwendungen von KI":
    render_anwendungen()
elif selected == "Angebot und Team":
    render_angebot_team()
elif selected == "Partner & Anbieter":
    render_partner()
elif selected == "Research Assistant":
    render_research_assistant()
