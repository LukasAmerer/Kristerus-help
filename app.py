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
                        
                        # Cache MISS - generate with LLM and cache the result
                        with st.spinner("🤔 LLM Council analysiert Ihre Frage..."):
                            # Create context for the query
                            context_query = f"{question} - Fokus: {dept_name}"
                            
                            # Try LLM analysis first
                            from analysis import analyze_content_llm, validate_with_apertus
                            
                            # For direct questions, we'll use the LLM without scraping
                            # Create a mock result structure for the question
                            mock_results = [{
                                'title': f'{dept_name} KI-Tools',
                                'url': 'internal',
                                'content': f'Frage zum Bereich {dept_name}: {question}'
                            }]
                            
                            llm_result = analyze_content_llm(mock_results, context_query)
                            
                            if "error" not in llm_result:
                                council_answer = llm_result["analysis"]
                                
                                # Silently validate with Apertus in background (not shown to user)
                                # This is for quality control only
                                apertus_result = validate_with_apertus(council_answer, question)
                                
                                # Cache the answer for future use
                                cache.store_answer(question, dept_name, council_answer)
                                
                                # Always show just the Council answer, validation happens silently
                                st.session_state[chat_key].append(("assistant", council_answer))
                            else:
                                # Fallback to simple response if LLM fails
                                if llm_result["error"] == "No API key found":
                                    answer = f"ℹ️ Für eine KI-gestützte Antwort zu '{question}' im Bereich {dept_name}, fügen Sie bitte einen OpenAI API Key in die .env Datei ein.\n\nPlatzhalter-Antwort: Diese Funktionalität wird mit dem LLM Council verbunden."
                                else:
                                    answer = f"❌ Fehler bei der Analyse: {llm_result['error']}"
                                st.session_state[chat_key].append(("assistant", answer))
                        
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
            
            # Custom question input with more spacing
            st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)
            st.markdown(
                """
                <div style="text-align: center; margin-bottom: 15px;">
                    <p style="color: #000; font-weight: 600; font-size: 15px;">Eigene Frage stellen:</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            custom_question = st.chat_input(f"Fragen Sie nach KI-Tools für {dept_name}...", key=f"{dept_name}_custom_input")
            if custom_question:
                # Add spacing before processing
                st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
                
                st.session_state[chat_key].append(("user", custom_question))
                
                # Check cache first
                from db_cache import cache
                cached_result = cache.get_cached_answer(custom_question, dept_name)
                
                if cached_result:
                    # Cache HIT - instant response!
                    st.session_state[chat_key].append(("assistant", cached_result['answer']))
                    st.rerun()
                
                # Cache MISS - generate with LLM and cache
                with st.spinner("🤔 LLM Council analysiert Ihre Frage..."):
                    context_query = f"{custom_question} - Fokus:  {dept_name}"
                    
                    from analysis import analyze_content_llm, validate_with_apertus
                    
                    mock_results = [{
                        'title': f'{dept_name} KI-Tools',
                        'url': 'internal',
                        'content': f'Frage zum Bereich {dept_name}: {custom_question}'
                    }]
                    
                    llm_result = analyze_content_llm(mock_results, context_query)
                    
                    if "error" not in llm_result:
                        council_answer = llm_result["analysis"]
                        
                        # Silently validate with Apertus in background (not shown to user)
                        apertus_result = validate_with_apertus(council_answer, custom_question)
                        
                        # Cache the answer
                        cache.store_answer(custom_question, dept_name, council_answer)
                        
                        # Always show just the Council answer
                        st.session_state[chat_key].append(("assistant", council_answer))
                    else:
                        if llm_result["error"] == "No API key found":
                            answer = f"ℹ️ Für eine KI-gestützte Antwort, fügen Sie bitte einen OpenAI API Key in die .env Datei ein."
                        else:
                            answer = f"❌ Fehler: {llm_result['error']}"
                        st.session_state[chat_key].append(("assistant", answer))
                
                st.rerun()


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
            key="active_project_radio"
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

    # Main-Bereich: Titel
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

    # Tabs for Chat and Scraper
    tab1, tab2 = st.tabs(["Chat Assistant", "Web Scraper"])

    with tab1:
        # Initialize the dictionary for all project chats if it doesn't exist
        if "project_chats" not in st.session_state:
            st.session_state.project_chats = {}

        # Ensure the current project has an entry
        if selected_project not in st.session_state.project_chats:
            st.session_state.project_chats[selected_project] = []

        # Display messages for the selected project
        for role, content in st.session_state.project_chats[selected_project]:
            with st.chat_message(role):
                st.markdown(content)

        prompt = st.chat_input("Frag den Research Assistant oder beschreibe dein Vorhaben …")
        if prompt:
            # Add user message to the specific project's history
            st.session_state.project_chats[selected_project].append(("user", prompt))
            
            # Display user message immediately
            with st.chat_message("user"):
                st.markdown(prompt)

            # Generate and add assistant response
            answer = (
                f"Du hast im Projekt **{selected_project}** gefragt:\n\n"
                f"> {prompt}\n\n"
                "Für die Abgabe kannst du hier später die echte Logik einbauen "
                "(LLM-Council, Analysen, Report-Generierung etc.)."
            )
            st.session_state.project_chats[selected_project].append(("assistant", answer))
            
            with st.chat_message("assistant"):
                st.markdown(answer)

    with tab2:
        st.markdown(
            """
            <div style="padding: 20px 0; font-family: sans-serif;">
                <h3 style="color: #333;">Research & Web Scraper</h3>
                <p style="color: #555; font-size: 14px;">
                    Suche nach Themen (z.B. "Beste KI Tools für Marketing") oder gib eine spezifische URL ein.
                    Das System sucht, scrapt und analysiert die Inhalte.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        search_mode = st.radio("Modus", ["URL Scrapen", "Web Suche"], horizontal=True)
        
        if search_mode == "URL Scrapen":
            url_input = st.text_input("URL eingeben:", placeholder="https://example.com")
            if st.button("Inhalt scrapen"):
                if url_input:
                    with st.spinner("Webseite wird analysiert..."):
                        result = scrape_website(url_input)
                        if result["status"] == "success":
                            st.success("Erfolgreich gescrapt!")
                            st.markdown(f"**Titel:** {result['title']}")
                            with st.expander("Vollständigen Text anzeigen"):
                                st.text_area("Inhalt", result["text"], height=400)
                        else:
                            st.error(f"Fehler beim Scrapen: {result['message']}")
                else:
                    st.warning("Bitte gib eine gültige URL ein.")
                    
        else: # Web Suche
            query = st.text_input("Suchanfrage:", placeholder="Beste KI Tools für Buchhaltung")
            if st.button("Suchen & Analysieren"):
                if query:
                    with st.spinner("Suche und analysiere Webseiten..."):
                        results = search_and_scrape(query, max_results=3)
                        
                        if results and "error" not in results[0]:
                            st.success(f"{len(results)} relevante Seiten gefunden und analysiert.")
                            
                            # --- LLM Council Analysis ---
                            st.markdown("### 🧠 LLM Council Analyse")
                            
                            # Try LLM analysis first
                            llm_result = analyze_content_llm(results, query)
                            
                            if "error" not in llm_result:
                                st.markdown(llm_result["analysis"])
                                
                                # --- Apertus Validation ---
                                st.markdown("---")
                                st.subheader("🇨🇭 Apertus Validation (Swiss AI)")
                                with st.spinner("Apertus validiert die Antwort..."):
                                    apertus_result = validate_with_apertus(llm_result["analysis"], query)
                                    
                                    if "error" not in apertus_result:
                                        st.success("Validierung abgeschlossen")
                                        st.markdown(apertus_result["validation"])
                                    else:
                                        st.error(f"Apertus konnte nicht validieren: {apertus_result['error']}")
                                        st.info("Möglicherweise ist das Modell gerade überlastet oder benötigt einen HF_TOKEN in der .env Datei.")

                            else:
                                # Fallback or Error Message
                                if llm_result["error"] == "No API key found":
                                    st.warning("Kein OpenAI API Key gefunden. Fallback auf Keyword-Analyse.")
                                    st.info("Füge einen API Key in die .env Datei ein, um die volle 'Council' Power zu nutzen.")
                                    
                                    # Fallback Heuristics
                                    ranked_tools = analyze_content_heuristics(results)
                                    if ranked_tools:
                                        top_tool = ranked_tools[0][0]
                                        st.markdown(f"**Top-Empfehlung (basierend auf Nennungen):** :trophy: **{top_tool}**")
                                        for tool, count in ranked_tools:
                                            st.write(f"- **{tool}**: {count} Nennungen")
                                    else:
                                        st.warning("Keine bekannten KI-Tools in den Suchergebnissen gefunden.")
                                else:
                                    st.error(f"Fehler bei der KI-Analyse: {llm_result['error']}")

                            st.markdown("---")
                            st.markdown("**Detaillierte Quellen:**")
                            for i, res in enumerate(results):
                                with st.expander(f"Quelle {i+1}: {res.get('title', 'Ohne Titel')}"):
                                    st.markdown(f"**URL:** {res.get('url')}")
                                    st.markdown(f"**Snippet:** {res.get('snippet')}")
                                    st.text_area("Gescrapter Inhalt", res.get('content')[:1000] + "...", height=200)
                        else:
                            st.error(f"Fehler bei der Suche: {results[0].get('error') if results else 'Keine Ergebnisse'}")
                else:
                    st.warning("Bitte gib eine Suchanfrage ein.")



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
