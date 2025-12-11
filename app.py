import streamlit as st
from PIL import Image
import os
from streamlit_option_menu import option_menu
from scraper import scrape_website, search_and_scrape
from analysis import analyze_content_heuristics, analyze_content_llm, validate_with_apertus
from duckduckgo_search import DDGS



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

    /* Force black text in chat messages with light background for contrast */
    [data-testid="stChatMessage"] {
        background-color: #f0f0f0 !important;
        color: #000000 !important;
        border-radius: 10px;
        padding: 10px;
    }
    [data-testid="stChatMessage"] p, [data-testid="stChatMessage"] div {
        color: #000000 !important;
    }

    /* Tab styling for AI Applications page */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0px;
        width: 100%;
        border-bottom: 2px solid #e0e0e0;
    }
    
    .stTabs [data-baseweb="tab"] {
        flex: 1;
        color: #000000 !important;
        font-size: 18px !important;
        font-weight: 600 !important;
        padding: 15px 0px !important;
        text-align: center;
        border-bottom: 3px solid transparent !important;
        border-left: 1px solid #e0e0e0;
        border-right: 1px solid #e0e0e0;
        border-top: 1px solid #e0e0e0;
        background-color: #f8f8f8;
    }
    
    .stTabs [data-baseweb="tab"]:first-child {
        border-left: 2px solid #e0e0e0;
    }
    
    .stTabs [data-baseweb="tab"]:last-child {
        border-right: 2px solid #e0e0e0;
    }
    
    .stTabs [aria-selected="true"] {
        color: #00802F !important;
        border-bottom: 3px solid #00802F !important;
        background-color: #ffffff !important;
        box-shadow: none !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        color: #00802F !important;
        background-color: #ffffff;
    }
    
    .stTabs [data-baseweb="tab-highlight"] {
        display: none !important;
    }
    
    /* Remove default Streamlit tab panel border that might be red */
    .stTabs [data-baseweb="tab-panel"] {
        padding-top: 20px;
    }
    
    /* Compact chat input */
    .stChatInput {
        max-width: 800px;
        margin: 0 auto;
    }
    
    /* Responsive design for AI Applications */
    @media (max-width: 768px) {
        .stTabs [data-baseweb="tab"] {
            font-size: 14px !important;
            padding: 12px 5px !important;
        }
    }

    /* --- RESPONSIVE TYPOGRAPHY & LAYOUT --- */
    
    /* Hero Section */
    .hero-container {
        padding: 60px 80px 40px 80px;
    }
    .hero-title {
        font-size: 48px; 
        font-weight: 700; 
        color: #00802F;
        font-family: sans-serif; 
        margin-bottom: 8px;
    }
    .hero-subtitle {
        font-size: 20px; 
        font-weight: 500; 
        color: #00802F;
        font-family: sans-serif; 
        margin-bottom: 16px;
    }
    .hero-line {
        height: 3px; 
        width: 260px; 
        background-color: #00802F;
    }

    /* Green Block */
    .green-block {
        background-color: #00802F; 
        width: 100%; 
        padding: 40px 80px 80px 80px;
    }
    .green-block-title {
        font-size: 36px; 
        font-weight: 700; 
        color: #ffffff; 
        font-family: sans-serif; 
        margin-bottom: 8px;
    }
    .green-block-text {
        font-size: 16px; 
        color: #ffffff; 
        font-family: sans-serif; 
        margin-bottom: 32px;
    }

    /* Cards (Row 1 & 2) */
    .card-box {
        background-color: #ffffff;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
        font-family: sans-serif;
        min-height: 180px;
        /* Desktop default margins */
        margin-top: -60px; 
        margin-left: 40px; 
        margin-right: 40px;
    }
    .card-title {
        font-size: 18px; 
        font-weight: 700; 
        color: #00802F; 
        margin-bottom: 8px; 
        white-space: pre-line;
    }
    .card-text {
        font-size: 14px; 
        color: #333333; 
        margin-bottom: 16px;
    }
    .card-btn {
        display: inline-block; 
        padding: 8px 18px; 
        border-radius: 20px;
        background-color: #00802F; 
        color: #ffffff; 
        font-size: 13px; 
        font-weight: 600;
    }

    /* Content Sections (Text + Image) */
    .content-section {
        background-color: #ffffff; 
        padding: 60px 80px; 
        font-family: sans-serif;
    }
    .content-title {
        font-size: 32px; 
        font-weight: 700; 
        color: #00802F; 
        margin-bottom: 16px;
    }
    .content-desc {
        font-size: 15px; 
        color: #333333; 
        margin-bottom: 24px;
    }
    .img-placeholder {
        height: 260px;
        background-color: #e5e5e5;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-family: sans-serif;
        color: #777777;
        font-size: 14px;
        margin: 20px;
    }

    /* Use Cases */
    .use-case-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 18px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
        font-family: sans-serif;
        min-height: 260px;
        margin-top: 30px;
    }

    /* --- MEDIA QUERIES --- */
    @media (max-width: 900px) {
        .hero-container { padding: 40px 30px; }
        .hero-title { font-size: 36px; }
        .green-block { padding: 30px 30px 60px 30px; }
        .green-block-title { font-size: 28px; }
        
        .card-box {
            margin-top: 20px; /* Remove negative margin overlap */
            margin-left: 0;
            margin-right: 0;
            margin-bottom: 20px;
        }
        
        .content-section { padding: 30px 20px; }
        .content-title { font-size: 24px; }
        
        .img-placeholder { margin: 0 0 20px 0; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

GREEN = "#00802F"

# ----------------------------
# TOP-BEREICH: LOGO + MENÜ
# ----------------------------
# ----------------------------
# TOP-BEREICH: LOGO + MENÜ
# ----------------------------
with st.container():
    col_logo, col_menu, col_right = st.columns([1, 4, 1])

    # Logo
    with col_logo:
        logo_path = "KMUmeetKI_Logo.png"
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
        # Initialize login state
        if "logged_in" not in st.session_state:
            st.session_state.logged_in = False
        
        # Build menu options based on login state
        menu_options = [
            "Wissen",
            "Anwendungen von KI",
            "Angebot und Team",
            "Partner & Anbieter",
        ]
        
        if st.session_state.logged_in:
            menu_options.append("Research Assistant")
        
        menu_options.append("Login" if not st.session_state.logged_in else "Logout")
        
        selected = option_menu(
            menu_title=None,
            options=menu_options,
            icons=[None] * len(menu_options),
            default_index=0,
            orientation="horizontal",
            key="main_nav_menu",
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

    # rechter Bereich: Leer (Logout entfernt)
    with col_right:
        st.write("")


# ============================================================
# SEITE 1: WISSEN – komplette Landingpage
# ============================================================
def render_wissen():
    # ---------- HERO ----------
    st.markdown(
        f"""
        <div class="hero-container">
            <div class="hero-title">
                KMUmeetKI
            </div>
            <div class="hero-subtitle">
                Die zentrale KI-Wissensplattform für KMU
            </div>
            <div class="hero-line"></div>
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
        """
        <div class="green-block">
            <div class="green-block-title">
                Alles rund um Künstliche Intelligenz
            </div>
            <div class="green-block-text">
                Für KMU und KI-Enthusiasten – praxisorientiert, verständlich, befähigend.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ---------- 4 KARTEN (2×2) ----------
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
                <div class="card-box">
                    <div class="card-title">
                        {card['title']}
                    </div>
                    <div class="card-text">
                        {card['text']}
                    </div>
                    <a href="#" class="card-btn">
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
                <div class="card-box">
                    <div class="card-title">
                        {card['title']}
                    </div>
                    <div class="card-text">
                        {card['text']}
                    </div>
                    <a href="#" class="card-btn">
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
                <div class="content-section">
                    <div class="content-title">
                        Die wichtigsten Grundlagen rund um KI
                    </div>
                    <div class="content-desc">
                        Anwendungen &amp; Use Cases
                    </div>
                    <a href="#" class="card-btn">
                        Mehr Infos
                    </a>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col_img:
            st.markdown(
                """
                <div class="img-placeholder">
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
                <div class="img-placeholder">
                    Bild: Roboter-Hand (Platzhalter)
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col_text1:
            st.markdown(
                f"""
                <div class="content-section">
                    <div class="content-title">
                        Anwendungen &amp; Use Cases
                    </div>
                    <div class="content-desc">
                        Beispiele, wie KI heute schon in Marketing, Kundenservice, Administration
                        oder Strategie eingesetzt wird.
                    </div>
                    <a href="#" class="card-btn">
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
                <div class="content-section">
                    <div class="content-title">
                        KMUmeetKI unterstützen als Partner / Sponsor
                    </div>
                    <div class="content-desc">
                        Positionieren Sie sich als Vorreiter im Bereich KI für KMU und unterstützen Sie den weiteren Ausbau der Plattform.
                    </div>
                    <a href="#" class="card-btn">
                        Jetzt Kontakt aufnehmen
                    </a>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col_img2:
            st.markdown(
                """
                <div class="img-placeholder">
                    Bild: Handschlag / Partnerschaft (Platzhalter)
                </div>
                """,
                unsafe_allow_html=True,
            )

    # ---------- TOP 6 ANWENDUNGEN / USE CASES ----------
    st.markdown(
        f"""
        <div class="green-block" style="margin-top: 40px;">
            <div class="green-block-title">
                Top 6 Anwendungen / Use Cases
            </div>
            <div class="green-block-text">
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
                <div class="use-case-card">
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
                    <a href="#" class="card-btn">
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
        <div style="padding: 60px 80px 20px 80px; font-family: sans-serif;">
            <div style="font-size: 36px; font-weight: 700; color:{GREEN}; margin-bottom: 16px;">
                Anwendungen von KI
            </div>
            <div style="font-size: 15px; color:#333; margin-bottom: 20px;">
                Entdecken Sie spezifische KI-Anwendungen für verschiedene Unternehmensbereiche.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # Tabs for different departments
    tab_names = ["Marketing", "Customer Success", "HR", "Product", "General"]
    tabs = st.tabs(tab_names)
    
    # Pre-defined questions for each department
    questions_by_department = {
        "Marketing": [
            "Welche KI-Tools eignen sich am besten für Content-Erstellung?",
            "Wie kann KI bei SEO und Keyword-Recherche helfen?",
            "Welche Tools nutzen Sie für Social Media Automation?",
            "Wie verwenden Sie KI für Grafikdesign und Bildgenerierung?"
        ],
        "Customer Success": [
            "Welche Chatbot-Lösungen empfehlen Sie für KMUs?",
            "Wie kann KI bei der Analyse von Kundenfeedback helfen?",
            "Welche Tools automatisieren Support-Tickets am besten?",
            "Wie nutzen Sie KI für personalisierte Kundenansprache?"
        ],
        "HR": [
            "Welche KI-Tools unterstützen beim Recruiting?",
            "Wie kann KI im Onboarding-Prozess eingesetzt werden?",
            "Welche Tools helfen bei der Mitarbeiterentwicklung?",
            "Wie nutzen Sie KI für Leistungsbeurteilungen?"
        ],
        "Product": [
            "Welche KI-Coding-Assistenten empfehlen Sie?",
            "Wie kann KI bei der Produktplanung helfen?",
            "Welche Tools unterstützen beim UI/UX Design?",
            "Wie nutzen Sie KI für Feature-Priorisierung?"
        ],
        "General": [
            "Welche allgemeinen Produktivitätstools mit KI gibt es?",
            "Wie kann KI bei Meeting-Management helfen?",
            "Welche Tools empfehlen Sie für Wissensmanagement?",
            "Wie nutzen Sie KI für Dokumentenverarbeitung?"
        ]
    }
    
    # Content for each tab
    for idx, (tab, dept_name) in enumerate(zip(tabs, tab_names)):
        with tab:
            # Initialize session state for this department's chat
            chat_key = f"anwendungen_chat_{dept_name}"
            if chat_key not in st.session_state:
                st.session_state[chat_key] = []
            
            # Header section with centered text
            st.markdown(
                f"""
                <div style="text-align: center; padding: 30px 0 20px 0;">
                    <h2 style="color: #00802F; font-weight: 700; margin-bottom: 10px;">KI im {dept_name}</h2>
                    <p style="color: #555; font-size: 16px;">Stellen Sie Fragen zu KI-Tools in diesem Bereich</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Pre-defined question buttons with better styling
            st.markdown(
                """
                <div style="text-align: center; margin-bottom: 20px;">
                    <p style="color: #000; font-weight: 600; font-size: 15px;">Häufig gestellte Fragen:</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            cols = st.columns(2, gap="medium")
            for i, question in enumerate(questions_by_department[dept_name]):
                with cols[i % 2]:
                    if st.button(question, key=f"{dept_name}_q_{i}", use_container_width=True):
                        # Add spacing before spinner
                        st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
                        
                        st.session_state[chat_key].append(("user", question))
                        
                        # Check cache first for instant response
                        from db_cache import cache
                        cached_result = cache.get_cached_answer(question, dept_name)
                        
                        if cached_result:
                            # Cache HIT - instant response!
                            st.session_state[chat_key].append(("assistant", cached_result['answer']))
                            st.rerun()
                        
                        # Try SLM with curated knowledge first
                        with st.spinner("🤔 Suche in kuratiertem Wissen..."):
                            from slm_service import answer_with_curated_knowledge
                            
                            slm_result = answer_with_curated_knowledge(question, dept_name)
                            
                            if slm_result.get("curated") and slm_result.get("answer"):
                                # Successfully got answer from curated knowledge
                                answer_text = slm_result["answer"]
                                
                                # Add source attribution
                                sources = slm_result.get("sources", [])
                                if sources:
                                    answer_text += "\n\n---\n*Basierend auf kuratiertem Wissen*"
                                
                                # Cache for future use
                                cache.store_answer(question, dept_name, answer_text)
                                st.session_state[chat_key].append(("assistant", answer_text))
                                
                            elif slm_result.get("no_curated_data"):
                                # No curated data - fall back to direct LLM
                                from analysis import analyze_content_llm
                                
                                mock_results = [{
                                    'title': f'{dept_name} KI-Tools',
                                    'url': 'internal',
                                    'content': f'Frage zum Bereich {dept_name}: {question}'
                                }]
                                
                                llm_result = analyze_content_llm(mock_results, f"{question} - Fokus: {dept_name}")
                                
                                if "error" not in llm_result:
                                    answer = llm_result["analysis"]
                                    answer += "\n\n---\n*Hinweis: Diese Antwort wurde direkt generiert. Kuratiertes Wissen ist noch nicht verfügbar.*"
                                    cache.store_answer(question, dept_name, answer)
                                    st.session_state[chat_key].append(("assistant", answer))
                                else:
                                    st.session_state[chat_key].append(("assistant", f"❌ Fehler: {llm_result['error']}"))
                            else:
                                st.session_state[chat_key].append(("assistant", f"❌ Fehler: {slm_result.get('error', 'Unbekannt')}"))
                        
                        st.rerun()
            
            # Chat history display with more spacing
            if st.session_state[chat_key]:
                st.markdown("<div style='margin-top: 40px;'></div>", unsafe_allow_html=True)
                st.markdown(
                    """
                    <div style="text-align: center; margin-bottom: 20px;">
                        <p style="color: #000; font-weight: 600; font-size: 15px;">Chat-Verlauf:</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                for role, content in st.session_state[chat_key]:
                    with st.chat_message(role):
                        st.markdown(f"<div style='color: #000000;'>{content}</div>", unsafe_allow_html=True)
            
            # Chat input removed as per request - only predefined questions allowed



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
# SEITE 5: RESEARCH ASSISTANT – Admin Dashboard with Styled Tabs
# ============================================================

# Auto-search queries for each department - English queries for better results
AUTO_SEARCH_QUERIES = {
    "Marketing": "best AI marketing tools 2024 Jasper Copy.ai HubSpot",
    "Customer Success": "best AI customer service tools Intercom Zendesk Freshdesk",
    "HR": "best AI HR recruiting tools Workday HireVue Greenhouse",
    "Product": "best AI product development tools Notion Figma Miro",
    "General": "best AI business tools ChatGPT Claude Gemini productivity"
}

def run_auto_search_if_needed(force=False):
    """Check if daily auto-search is needed and run it."""
    from datetime import datetime, timedelta
    from db_cache import validated_results_manager
    import os
    
    # Check last search timestamp
    timestamp_file = os.path.join(os.path.dirname(__file__), '.last_auto_search')
    
    should_run = force  # Always run if forced
    if not force and os.path.exists(timestamp_file):
        with open(timestamp_file, 'r') as f:
            last_run = f.read().strip()
            try:
                last_datetime = datetime.fromisoformat(last_run)
                # Run if more than 24 hours have passed
                if datetime.now() - last_datetime > timedelta(hours=24):
                    should_run = True
            except:
                should_run = True
    elif not force:
        should_run = True
    
    if should_run:
        print("🔄 Running daily auto-search for new AI tools...")
        try:
            from scraper import search_and_scrape
            from analysis import analyze_content_llm, validate_with_apertus
            
            for dept, query in AUTO_SEARCH_QUERIES.items():
                print(f"  Searching for {dept}...")
                results = search_and_scrape(query, max_results=3)
                
                if results and "error" not in results[0]:
                    # Use LLM Council to extract actual tool names
                    from analysis import extract_tool_names
                    extracted_tools = extract_tool_names(results, dept)
                    
                    if extracted_tools:
                        # Store each extracted tool
                        for tool in extracted_tools:
                            # Find source URL from results
                            source_url = results[0].get('url', '') if results else ''
                            
                            validated_results_manager.add_pending_result(
                                query=query,
                                department=dept,
                                llm_analysis=tool.get('description', ''),
                                apertus_validation="LLM Council extracted",
                                tool_name=tool.get('tool_name'),
                                source_url=source_url
                            )
                    else:
                        # Fallback: store scraped page titles
                        for result in results[:2]:
                            validated_results_manager.add_pending_result(
                                query=query,
                                department=dept,
                                llm_analysis=result.get('snippet', ''),
                                apertus_validation="Direct scrape",
                                tool_name=result.get('title', 'Unknown')[:60],
                                source_url=result.get('url', '')
                            )
            
            # Update timestamp
            with open(timestamp_file, 'w') as f:
                f.write(datetime.now().isoformat())
            print("✅ Auto-search complete!")
        except Exception as e:
            print(f"⚠️ Auto-search failed: {e}")


def render_research_assistant():
    from db_cache import validated_results_manager
    
    # Auto-search disabled for now - runs in background separately
    # run_auto_search_if_needed()
    
    # Custom CSS for styled tabs
    st.markdown("""
    <style>
    /* Centered, rounded tabs */
    .stTabs [data-baseweb="tab-list"] {
        display: flex;
        justify-content: center;
        gap: 8px;
        max-width: 800px;
        margin: 0 auto;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 20px !important;
        padding: 8px 20px !important;
        background-color: #f0f0f0 !important;
        border: 2px solid #ccc !important;
        font-weight: 600 !important;
        color: #333 !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #00802F !important;
        color: #ffffff !important;
        border-color: #00802F !important;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #e0e0e0 !important;
        color: #000 !important;
    }
    /* Table styling */
    .tool-row {
        display: flex;
        align-items: center;
        padding: 12px 16px;
        background: #fafafa;
        border-radius: 8px;
        margin-bottom: 8px;
        border-left: 4px solid #00802F;
    }
    .tool-row.pending {
        border-left-color: #ffa500;
        background: #fffbf0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown(
        f"""
        <div style="text-align: center; padding: 30px 20px 20px 20px;">
            <div style="font-size: 32px; font-weight: 700; color: {GREEN}; margin-bottom: 8px;">
                🔬 Research Assistant
            </div>
            <div style="font-size: 14px; color: #666; max-width: 500px; margin: 0 auto;">
                Die KI sucht täglich automatisch nach neuen Tools. Aktivieren Sie relevante Einträge für die Nutzer.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # Manual sync button
    col_spacer1, col_btn, col_spacer2 = st.columns([3, 2, 3])
    with col_btn:
        if st.button("🔄 Neue Tools suchen", type="primary", use_container_width=True):
            with st.spinner("Suche nach neuen KI-Tools für alle Abteilungen..."):
                run_auto_search_if_needed(force=True)
            st.success("Fertig! Neue Tools wurden hinzugefügt.")
            st.rerun()
    
    # Department tabs
    dept_names = ["Marketing", "Customer Success", "HR", "Product", "General"]
    tabs = st.tabs(dept_names)
    
    for idx, dept_name in enumerate(dept_names):
        with tabs[idx]:
            # Get data for this department
            pending = validated_results_manager.get_pending_results()
            pending_dept = [r for r in pending if r.get('department') == dept_name]
            approved = validated_results_manager.get_approved_by_department(dept_name)
            
            # Combine all results with description
            all_results = []
            for r in approved:
                desc = r.get('llm_analysis', '')[:200]
                if len(r.get('llm_analysis', '')) > 200:
                    desc += "..."
                all_results.append({
                    'id': r.get('result_id'),
                    'tool_name': r.get('tool_name', r.get('query', 'Unbekannt'))[:40],
                    'source_url': r.get('source_url', ''),
                    'description': desc,
                    'is_active': True
                })
            for r in pending_dept:
                desc = r.get('llm_analysis', '')[:200]
                if len(r.get('llm_analysis', '')) > 200:
                    desc += "..."
                all_results.append({
                    'id': r.get('result_id'),
                    'tool_name': r.get('tool_name', r.get('query', 'Unbekannt'))[:40],
                    'source_url': r.get('source_url', ''),
                    'description': desc,
                    'is_active': False
                })
            
            if all_results:
                # Centered layout using columns
                _, main_col, _ = st.columns([1, 6, 1])
                
                with main_col:
                    st.markdown(f"<h3 style='text-align: center; color: #222; margin-bottom: 25px;'>{dept_name} - {len(all_results)} Tools</h3>", unsafe_allow_html=True)
                    
                    # Styles for the rows - BLACK TEXT always
                    st.markdown("""
                    <style>
                    .row-container {
                        padding: 10px 0;
                        border-bottom: 1px solid #eee;
                    }
                    .tool-link {
                        color: #0066cc !important;
                        text-decoration: none;
                        font-size: 14px;
                    }
                    .tool-link:hover { text-decoration: underline; }
                    div[data-testid="column"] { align-items: center; }
                    div[data-testid="column"] p, div[data-testid="column"] span { color: #000 !important; }
                    </style>
                    """, unsafe_allow_html=True)

                    # Header - BLACK TEXT - 4 columns now
                    h1, h2, h3, h4 = st.columns([2, 2, 4, 2])
                    h1.markdown("<span style='color: #000; font-weight: 700;'>Tool Name</span>", unsafe_allow_html=True)
                    h2.markdown("<span style='color: #000; font-weight: 700;'>Website</span>", unsafe_allow_html=True)
                    h3.markdown("<span style='color: #000; font-weight: 700;'>Beschreibung</span>", unsafe_allow_html=True)
                    h4.markdown("<span style='color: #000; font-weight: 700;'>Aktion</span>", unsafe_allow_html=True)
                    st.divider()

                    # Data Rows - 4 columns
                    for result in all_results:
                        c1, c2, c3, c4 = st.columns([2, 2, 4, 2])
                        
                        # Column 1: Name and Icon - BLACK TEXT
                        icon = "✅" if result['is_active'] else "⏳"
                        c1.markdown(f"<span style='color: #000; font-weight: 500; font-size:14px;'>{icon} {result['tool_name'][:20]}</span>", unsafe_allow_html=True)
                        
                        # Column 2: Link
                        url = result['source_url']
                        if url:
                            domain = url.replace('https://', '').replace('http://', '').replace('www.', '').split('/')[0]
                            c2.markdown(f"<a href='{url}' target='_blank' class='tool-link'>🔗 {domain[:15]}</a>", unsafe_allow_html=True)
                        else:
                            c2.markdown("<span style='color: #999;'>—</span>", unsafe_allow_html=True)
                        
                        # Column 3: Description - BLACK TEXT
                        desc = result.get('description', '')
                        if desc:
                            c3.markdown(f"<span style='color: #000; font-size: 13px;'>{desc}</span>", unsafe_allow_html=True)
                        else:
                            c3.markdown("<span style='color: #999; font-size: 13px;'>Keine Beschreibung</span>", unsafe_allow_html=True)
                        
                        # Column 4: Action Button
                        with c4:
                            if result['is_active']:
                                st.button(f"🔽", key=f"btn_hide_{result['id']}", 
                                         use_container_width=True,
                                         type="secondary",
                                         on_click=lambda rid=result['id']: validated_results_manager.revoke_approval(rid))
                            else:
                                st.button(f"✨", key=f"btn_show_{result['id']}", 
                                         use_container_width=True, 
                                         type="primary",
                                         on_click=lambda rid=result['id']: validated_results_manager.approve_result(rid, st.session_state.get('user_email', 'admin')))
                        
                        # Divider between rows
                        st.markdown("<div style='border-bottom: 1px solid #f0f0f0; margin: 4px 0;'></div>", unsafe_allow_html=True)

            else:
                st.info(f"Noch keine Tools für {dept_name}.")
            
            # Stats footer - centered
            st.markdown(f"""
            <div style="max-width: 600px; margin: 30px auto; background: linear-gradient(135deg, #e8f5e9, #c8e6c9); padding: 12px 24px; border-radius: 20px; text-align: center;">
                <span style="font-size: 13px; color: #333;">
                    ✅ <b>{len(approved)}</b> aktiv &nbsp;•&nbsp; 
                    ⏳ <b>{len(pending_dept)}</b> ausstehend
                </span>
            </div>
            """, unsafe_allow_html=True)



def render_login():
    """Azure AD Login page"""
    from azure_auth import login_with_azure
    login_with_azure()


def render_logout():
    """Azure AD Logout page"""
    from azure_auth import logout_azure
    logout_azure()


# ============================================================
# ROUTING – es läuft IMMER nur genau eine Seite
# ============================================================

# Special case: Handle OAuth callback (when Microsoft redirects back)
if "code" in st.query_params:
    # User is returning from Microsoft authentication
    render_login()
elif selected == "Wissen":
    render_wissen()
elif selected == "Anwendungen von KI":
    render_anwendungen()
elif selected == "Angebot und Team":
    render_angebot_team()
elif selected == "Partner & Anbieter":
    render_partner()
elif selected == "Research Assistant":
    if st.session_state.get("logged_in", False):
        render_research_assistant()
    else:
        st.error("Bitte melden Sie sich an, um auf den Research Assistant zuzugreifen.")
elif selected == "Login":
    render_login()
elif selected == "Logout":
    render_logout()
