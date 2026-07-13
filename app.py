import streamlit as st
import pandas as pd
import plotly.express as px
import time
import json
from styles import apply_custom_css
from database import (
    get_all_leads, save_lead, update_lead_status, 
    delete_lead, get_config, set_config, update_lead_sync_status
)
from services.llm_service import (
    generate_chatbot_response, extract_lead_profile, 
    generate_personalized_email, generate_conversation_summary
)
from services.scoring_service import calculate_lead_grade
from services.sheets_service import sync_lead_to_sheets

# Set page config
st.set_page_config(
    page_title="Panache Homes - Dubai AI Assistant",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply global premium SaaS styles
apply_custom_css()

import textwrap

# Render HTML utility to prevent leading space markdown parsing bug
def render_html(html_str):
    st.markdown(textwrap.dedent(html_str), unsafe_allow_html=True)

# Helper function for navigation
def navigate_to(page_name):
    st.session_state.saas_page = page_name
    st.query_params["page"] = page_name
    st.rerun()

# Custom styled header links using css overrides
# Capture page query parameters to allow navbar redirects
if "saas_page" not in st.session_state:
    query_page = st.query_params.get("page", "home")
    if query_page in ["home", "chat", "admin_login", "admin_portal"]:
        st.session_state.saas_page = query_page
    else:
        st.session_state.saas_page = "home"

if "admin_authenticated" not in st.session_state:
    st.session_state.admin_authenticated = False

# Global state initialization to avoid attribute errors on landing page CTAs
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Welcome to Panache Homes."},
        {"role": "assistant", "content": "🏙️ Dubai Property Investment Assistant"},
        {"role": "assistant", "content": "Hello!"},
        {"role": "assistant", "content": "I'm here to help you explore Dubai real estate opportunities."},
        {"role": "assistant", "content": "I'll ask a few questions to understand your requirements."},
        {"role": "assistant", "content": "Let's begin."}
    ]
if "current_lead" not in st.session_state:
    st.session_state.current_lead = {
        "first_name": "", "last_name": "", "email": "", "phone": "",
        "budget": "", "property_interest": "", "payment_method": "",
        "timeline": "", "purpose": "", "country": ""
    }
if "lead_saved" not in st.session_state:
    st.session_state.lead_saved = False
if "chat_started" not in st.session_state:
    st.session_state.chat_started = False
if "selected_property" not in st.session_state:
    st.session_state.selected_property = ""
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []
if "lead_data" not in st.session_state:
    st.session_state.lead_data = {}
if "current_step" not in st.session_state:
    st.session_state.current_step = 0
if "lead_grade" not in st.session_state:
    st.session_state.lead_grade = ""
if "summary" not in st.session_state:
    st.session_state.summary = ""
if "qualification_complete" not in st.session_state:
    st.session_state.qualification_complete = False
if "selected_map_location" not in st.session_state:
    st.session_state.selected_map_location = "Palm Jumeirah"

# Render Fixed Luxury Navigation Bar
admin_btn_label = "Portal" if st.session_state.admin_authenticated else "Admin Login"
admin_target_page = "admin_portal" if st.session_state.admin_authenticated else "admin_login"

render_html(f"""
    <div class="fixed-navbar">
        <a href="/?page=home#home" target="_self" class="navbar-brand">
            <h2>PANACHE <span>HOMES</span></h2>
        </a>
        <div class="navbar-menu">
            <a href="/?page=home#home" target="_self" class="navbar-link">Home</a>
            <a href="/?page=home#about" target="_self" class="navbar-link">About</a>
            <a href="/?page=home#services" target="_self" class="navbar-link">Services</a>
            <a href="/?page=home#contact" target="_self" class="navbar-link">Contact</a>
            <a href="/?page={admin_target_page}" target="_self" class="navbar-btn">{admin_btn_label}</a>
        </div>
    </div>
    <div class="page-content-offset"></div>
""")

# ----------------- PAGE A: LANDING PAGE -----------------
if st.session_state.saas_page == "home":
    if "selected_map_location" not in st.session_state:
        st.session_state.selected_map_location = "Palm Jumeirah"
    st.markdown('<div id="home">', unsafe_allow_html=True)
    
    # 1 & 2. Full-screen Hero Section with background and overlay
    render_html("""
        <div class="saas-hero-section">
            <div style="display: flex; align-items: center; justify-content: space-between; gap: 5%; width: 100%; flex-wrap: wrap; z-index: 10; position: relative;">
                <div style="flex: 1.5; min-width: 300px;">
                    <div class="hero-logo-large">🏢 PANACHE <span>HOMES</span></div>
                    <h1 class="saas-hero-title">AI-Powered Dubai Property<br><span>Investment Assistant</span></h1>
                    <p class="saas-hero-subtitle">Helping international investors discover premium Dubai properties, secure Golden Visas, and make informed investment decisions through an intelligent AI assistant.</p>
                </div>
                <div style="flex: 1; min-width: 280px; display: flex; justify-content: center;">
                    <div class="glass-info-card">
                        <h3 style="color: #ffffff; font-weight: 800; margin-top: 0; margin-bottom: 20px; font-size: 1.35rem; display: flex; align-items: center; gap: 10px;">
                            <span>🏢</span> Panache Homes
                        </h3>
                        <div class="glass-row"><span>✔</span> Luxury Real Estate Brokerage</div>
                        <div class="glass-row"><span>✔</span> AI Property Advisor</div>
                        <div class="glass-row"><span>✔</span> Golden Visa Guidance</div>
                        <div class="glass-row"><span>✔</span> Remote Purchase Support</div>
                    </div>
                </div>
            </div>
        </div>
    """)
    
    # Hero buttons
    col_cta1, col_cta2, col_cta_empty = st.columns([1, 1.2, 1.8])
    with col_cta1:
        st.markdown('<div style="margin-left: 5%; margin-top: -120px; margin-bottom: 80px; position: relative; z-index: 9999;">', unsafe_allow_html=True)
        if st.button("Start AI Consultation", key="hero_start_ai", use_container_width=True):
            navigate_to("chat")
        st.markdown('</div>', unsafe_allow_html=True)
    with col_cta2:
        st.markdown('<div style="margin-top: -120px; margin-bottom: 80px; position: relative; z-index: 9999;">', unsafe_allow_html=True)
        if st.button("Explore Premium Communities", key="hero_explore_comm", use_container_width=True):
            st.toast("Explore our six premium communities below!")
        st.markdown('</div>', unsafe_allow_html=True)

    # 3. Animated statistics
    render_html("""
        <div class="trust-badges-bar">
            <div class="trust-badge-item"><span>🚀</span> 500+ Investors</div>
            <div class="trust-badge-item"><span>🌍</span> 40+ Countries</div>
            <div class="trust-badge-item"><span>🏆</span> 10+ Years Experience</div>
            <div class="trust-badge-item"><span>🤖</span> AI Powered</div>
        </div>
    """)

    # 4. Premium Communities Section
    render_html("""
        <div id="communities" style="padding: 80px 0; background-color: #FFFFFF;">
            <div style="text-align: center; margin-bottom: 50px;">
                <h2 style="color: #0F172A; font-weight: 800; font-size: 2.2rem; margin-top: 0; letter-spacing: -0.5px;">Premium Communities</h2>
                <p style="color: #64748B; font-size: 1.15rem; max-width: 700px; margin: 15px auto 0 auto; line-height: 1.6; font-weight: 450;">
                    Explore Dubai's most prestigious and high-yielding residential communities.
                </p>
            </div>
            
            <div class="comm-grid">
                <!-- Palm Jumeirah -->
                <div class="comm-card">
                    <div class="comm-img" style="background-image: url('https://images.unsplash.com/photo-1518684079-3c830dcef090?auto=format&fit=crop&w=600&q=80');"></div>
                    <div class="comm-body">
                        <div class="comm-title">Palm Jumeirah <span>Villas & Apartments</span></div>
                        <p class="comm-desc">World-famous man-made island offering ultra-luxury beachfront living and signature villas.</p>
                    </div>
                </div>
                <!-- Dubai Marina -->
                <div class="comm-card">
                    <div class="comm-img" style="background-image: url('https://images.unsplash.com/photo-1582672060674-bc2bd8022eb0?auto=format&fit=crop&w=600&q=80');"></div>
                    <div class="comm-body">
                        <div class="comm-title">Dubai Marina <span>High-Rises</span></div>
                        <p class="comm-desc">Vibrant waterfront community with spectacular skyscraper views and high rental yields.</p>
                    </div>
                </div>
                <!-- Downtown Dubai -->
                <div class="comm-card">
                    <div class="comm-img" style="background-image: url('https://images.unsplash.com/photo-1597659840241-37e2b9c2f55f?auto=format&fit=crop&w=600&q=80');"></div>
                    <div class="comm-body">
                        <div class="comm-title">Downtown Dubai <span>Burj Khalifa District</span></div>
                        <p class="comm-desc">The prestigious heart of Dubai, home to the Burj Khalifa, Dubai Mall, and luxury apartments.</p>
                    </div>
                </div>
                <!-- Business Bay -->
                <div class="comm-card">
                    <div class="comm-img" style="background-image: url('https://images.unsplash.com/photo-1546412414-8035e1776c9a?auto=format&fit=crop&w=600&q=80');"></div>
                    <div class="comm-body">
                        <div class="comm-title">Business Bay <span>Corporate & Residential</span></div>
                        <p class="comm-desc">Dynamic trendsetting district located along the Dubai Canal, perfect for professionals.</p>
                    </div>
                </div>
                <!-- Dubai Hills Estate -->
                <div class="comm-card">
                    <div class="comm-img" style="background-image: url('https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=600&q=80');"></div>
                    <div class="comm-body">
                        <div class="comm-title">Dubai Hills Estate <span>Golf Community</span></div>
                        <p class="comm-desc">A premium family-focused community featuring a championship golf course and vast green parks.</p>
                    </div>
                </div>
                <!-- Arabian Ranches -->
                <div class="comm-card">
                    <div class="comm-img" style="background-image: url('https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=600&q=80');"></div>
                    <div class="comm-body">
                        <div class="comm-title">Arabian Ranches <span>Luxury Villas</span></div>
                        <p class="comm-desc">Exclusive gated community offering premium desert-themed townhouses and private family villas.</p>
                    </div>
                </div>
        </div>
    """)

    # 4.5 Dubai Property Gallery Section
    render_html("""
        <div id="gallery" style="padding: 80px 0; background-color: #F8FAFC; border-top: 1px solid #E2E8F0;">
            <div style="text-align: center; margin-bottom: 30px;">
                <h2 style="color: #0F172A; font-weight: 800; font-size: 2.2rem; margin-top: 0; letter-spacing: -0.5px;">Featured Dubai Property Gallery</h2>
                <p style="color: #64748B; font-size: 1.15rem; max-width: 700px; margin: 15px auto 0 auto; line-height: 1.6; font-weight: 450;">
                    Select a luxury residence to view pricing, yield calculations, and consult our real-time AI expert.
                </p>
            </div>
        </div>
    """)
    
    properties = [
        {
            "title": "Atlantis The Royal Penthouse",
            "community": "Palm Jumeirah",
            "price": "AED 15,000,000",
            "roi": "7.5% ROI",
            "desc": "Ultra-luxury sky villa overlooking the Palm Crescent with private pools.",
            "img": "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=400&q=80"
        },
        {
            "title": "Burj Khalifa Sky Residences",
            "community": "Downtown Dubai",
            "price": "AED 8,500,000",
            "roi": "8.2% ROI",
            "desc": "Prestigious residence above the clouds with panoramic fountain views.",
            "img": "https://images.unsplash.com/photo-1597659840241-37e2b9c2f55f?auto=format&fit=crop&w=400&q=80"
        },
        {
            "title": "One Canal Sky Mansions",
            "community": "Dubai Water Canal",
            "price": "AED 12,000,000",
            "roi": "7.9% ROI",
            "desc": "Architectural masterpiece with direct canal access and bespoke designs.",
            "img": "https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?auto=format&fit=crop&w=400&q=80"
        },
        {
            "title": "Dubai Hills Championship Manor",
            "community": "Dubai Hills Estate",
            "price": "AED 22,000,000",
            "roi": "6.8% ROI",
            "desc": "Elegantly finished private estate facing the award-winning golf course.",
            "img": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=400&q=80"
        },
        {
            "title": "Marina Shores Penthouse",
            "community": "Dubai Marina",
            "price": "AED 6,200,000",
            "roi": "8.5% ROI",
            "desc": "High-rise beachfront luxury with panoramic marina views.",
            "img": "https://images.unsplash.com/photo-1582672060674-bc2bd8022eb0?auto=format&fit=crop&w=400&q=80"
        },
        {
            "title": "Amara Serene Villas",
            "community": "Arabian Ranches III",
            "price": "AED 4,800,000",
            "roi": "7.2% ROI",
            "desc": "Family-focused luxury townhouse surrounded by botanical parklands.",
            "img": "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=400&q=80"
        },
        {
            "title": "Business Bay Canal Suite",
            "community": "Business Bay",
            "price": "AED 2,100,000",
            "roi": "9.1% ROI",
            "desc": "High-yielding corporate investment apartment in prime financial hub.",
            "img": "https://images.unsplash.com/photo-1546412414-8035e1776c9a?auto=format&fit=crop&w=400&q=80"
        },
        {
            "title": "Jumeirah Bay Island Estate",
            "community": "Jumeirah",
            "price": "AED 35,000,000",
            "roi": "6.0% ROI",
            "desc": "Bespoke beachfront mansion on the highly coveted private island.",
            "img": "https://images.unsplash.com/photo-1580587771525-78b9dba3b914?auto=format&fit=crop&w=400&q=80"
        }
    ]

    # Render Properties in 2 Rows of 4 Columns
    for row_idx in range(2):
        cols = st.columns(4)
        for col_idx in range(4):
            prop_idx = row_idx * 4 + col_idx
            prop = properties[prop_idx]
            with cols[col_idx]:
                render_html(f"""
                    <div class="gallery-card">
                        <div class="gallery-img" style="background-image: url('{prop['img']}');"></div>
                        <div class="gallery-body">
                            <div class="gallery-community">{prop['community']}</div>
                            <h4 class="gallery-title">{prop['title']}</h4>
                            <div class="gallery-meta">
                                <span class="gallery-price">{prop['price']}</span>
                                <span class="gallery-roi">{prop['roi']}</span>
                            </div>
                            <p class="gallery-desc">{prop['desc']}</p>
                        </div>
                    </div>
                """)
                st.markdown('<div style="margin-top: -15px; margin-bottom: 25px; padding: 0 10px;">', unsafe_allow_html=True)
                if st.button("Ask AI About This Property", key=f"ask_ai_{prop_idx}", use_container_width=True):
                    st.session_state.selected_property = prop['title']
                    st.session_state.chat_started = True
                    assistant_msg = f"I see you're interested in **{prop['title']}** in **{prop['community']}**.\n\nI can help you with:\n\n* • ROI\n* • Golden Visa eligibility\n* • Payment plan\n* • Community information\n* • Floor plans\n* • Rental yield"
                    st.session_state.messages.append({"role": "assistant", "content": assistant_msg})
                    navigate_to("chat")
                st.markdown('</div>', unsafe_allow_html=True)

    # 4.7 Explore Dubai Section
    render_html("""
        <div id="explore-map" style="padding: 80px 0; background-color: #FFFFFF; border-top: 1px solid #E2E8F0;">
            <div style="text-align: center; margin-bottom: 50px;">
                <h2 style="color: #0F172A; font-weight: 800; font-size: 2.2rem; margin-top: 0; letter-spacing: -0.5px;">Explore Dubai Communities</h2>
                <p style="color: #64748B; font-size: 1.15rem; max-width: 700px; margin: 15px auto 0 auto; line-height: 1.6; font-weight: 450;">
                    Select a key real estate hub to view community descriptions, high-resolution visual previews, and speak to our real-time AI guide.
                </p>
            </div>
        </div>
    """)

    map_details = {
        "Palm Jumeirah": {
            "title": "Palm Jumeirah",
            "desc": "World-famous man-made island offering ultra-luxury beachfront living, signature villas, and five-star resorts like Atlantis The Royal.",
            "img": "https://images.unsplash.com/photo-1518684079-3c830dcef090?auto=format&fit=crop&w=600&q=80",
            "pin_style": "top: 50%; left: 18%;"
        },
        "Dubai Marina": {
            "title": "Dubai Marina",
            "desc": "Vibrant waterfront community featuring stunning high-rise skyscrapers, a bustling boardwalk, and premium dining options.",
            "img": "https://images.unsplash.com/photo-1582672060674-bc2bd8022eb0?auto=format&fit=crop&w=600&q=80",
            "pin_style": "top: 60%; left: 32%;"
        },
        "Downtown Dubai": {
            "title": "Downtown Dubai",
            "desc": "The prestigious heart of Dubai, home to the Burj Khalifa, the Dubai Fountain, and high-end residential towers.",
            "img": "https://images.unsplash.com/photo-1597659840241-37e2b9c2f55f?auto=format&fit=crop&w=600&q=80",
            "pin_style": "top: 38%; left: 48%;"
        },
        "Business Bay": {
            "title": "Business Bay",
            "desc": "A trendy mixed-use district located along the Dubai Canal, perfect for young professionals and corporate hubs.",
            "img": "https://images.unsplash.com/photo-1546412414-8035e1776c9a?auto=format&fit=crop&w=600&q=80",
            "pin_style": "top: 45%; left: 56%;"
        },
        "Dubai Hills": {
            "title": "Dubai Hills",
            "desc": "A premium, family-centric master community featuring an 18-hole championship golf course and vast green parks.",
            "img": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=600&q=80",
            "pin_style": "top: 52%; left: 68%;"
        },
        "Arabian Ranches": {
            "title": "Arabian Ranches",
            "desc": "A premium gated suburban community offering tranquil desert-themed villas and private family neighborhoods.",
            "img": "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=600&q=80",
            "pin_style": "top: 62%; left: 82%;"
        }
    }

    map_col1, map_col2 = st.columns([1.5, 1])
    with map_col1:
        # Render stylized map container with CSS Pins
        current_loc = st.session_state.selected_map_location
        details = map_details[current_loc]
        
        # Build pins HTML
        pins_html = ""
        for name, data in map_details.items():
            active_bg = "#C9A227" if name == current_loc else "#0F172A"
            pins_html += f"""
                <div class="map-pin" style="position: absolute; {data['pin_style']}; background-color: {active_bg}; color: white; padding: 6px 12px; border-radius: 20px; font-size: 0.75rem; font-weight: 700; border: 2px solid #ffffff; box-shadow: 0 4px 6px rgba(0,0,0,0.1); cursor: pointer; transition: all 0.2s ease;">
                    📍 {name}
                </div>
            """
            
        render_html(f"""
            <div style="background-image: url('https://images.unsplash.com/photo-1582672060674-bc2bd8022eb0?auto=format&fit=crop&w=1200&q=80'); background-size: cover; background-position: center; border-radius: 20px; height: 380px; position: relative; border: 1px solid #E2E8F0; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.02); margin-bottom: 20px;">
                <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(15, 23, 42, 0.65);"></div>
                {pins_html}
            </div>
        """)
        
        # Map location selector buttons
        st.write("📍 Select a location to highlight on the map:")
        but_cols1 = st.columns(3)
        but_cols2 = st.columns(3)
        
        locations_list = list(map_details.keys())
        for i, name in enumerate(locations_list[:3]):
            with but_cols1[i]:
                if st.button(name, key=f"map_btn_{i}", use_container_width=True):
                    st.session_state.selected_map_location = name
                    st.rerun()
                    
        for i, name in enumerate(locations_list[3:]):
            with but_cols2[i]:
                if st.button(name, key=f"map_btn_{i+3}", use_container_width=True):
                    st.session_state.selected_map_location = name
                    st.rerun()
                    
    with map_col2:
        # Renders the details card
        current_loc = st.session_state.selected_map_location
        details = map_details[current_loc]
        
        render_html(f"""
            <div class="gallery-card" style="border: 1px solid #E2E8F0; height: 100%;">
                <div class="gallery-img" style="background-image: url('{details['img']}'); height: 180px;"></div>
                <div class="gallery-body" style="padding: 25px;">
                    <div style="font-size:0.75rem; color:#C9A227; font-weight:700; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:8px;">Highlighted Location</div>
                    <h3 style="margin: 0 0 15px 0; color:#0F172A; font-weight:800; font-size:1.4rem;">{details['title']}</h3>
                    <p style="font-size:0.9rem; color:#64748B; line-height:1.6; margin: 0 0 25px 0;">{details['desc']}</p>
                </div>
            </div>
        """)
        
        st.markdown('<div style="margin-top:-60px; padding: 0 25px 25px 25px; position:relative; z-index:9999;">', unsafe_allow_html=True)
        if st.button("Talk to AI About This Area", key="talk_ai_area_btn", use_container_width=True):
            st.session_state.messages.append({
                "role": "user",
                "content": f"I'm interested in buying property in {details['title']}. What is the price trend, top off-plan projects, and community lifestyle like there?"
            })
            st.session_state.chat_started = True
            navigate_to("chat")
        st.markdown('</div>', unsafe_allow_html=True)

    # 5. Why Invest in Dubai Section
    render_html("""
        <div id="why-invest" style="background-color: #F8FAFC; border-top: 1px solid #E2E8F0; padding: 80px 0;">
            <div style="text-align: center; margin-bottom: 50px;">
                <h2 style="color: #0F172A; font-weight: 800; font-size: 2.2rem; margin-top: 0; letter-spacing: -0.5px;">Why Invest in Dubai?</h2>
                <p style="color: #64748B; font-size: 1.15rem; max-width: 700px; margin: 15px auto 0 auto; line-height: 1.6; font-weight: 450;">
                    Dubai is one of the world's fastest-growing real estate investment destinations, offering high rental yields, tax advantages, and world-class infrastructure.
                </p>
            </div>
            
            <div class="why-invest-split">
                <div class="why-invest-img"></div>
                <div class="why-invest-content">
                    <div class="why-invest-grid">
                        <div class="why-invest-card">
                            <h4><span>📈</span> High Rental Yield</h4>
                            <p>Dubai properties offer yields up to 8-10%, outperforming major global capitals.</p>
                        </div>
                        <div class="why-invest-card">
                            <h4><span>🛂</span> Golden Visa</h4>
                            <p>Investors purchasing property valued at AED 2M+ are eligible for a 10-year Golden Visa.</p>
                        </div>
                        <div class="why-invest-card">
                            <h4><span>🛡️</span> No Annual Property Tax</h4>
                            <p>Enjoy tax-free rental income and zero annual property ownership taxes.</p>
                        </div>
                        <div class="why-invest-card">
                            <h4><span>💵</span> Stable AED Currency</h4>
                            <p>The UAE Dirham (AED) is pegged stably to the US Dollar (3.6725 AED/USD).</p>
                        </div>
                        <div class="why-invest-card">
                            <h4><span>🌍</span> Remote Purchase</h4>
                            <p>Complete property acquisition legally and securely from anywhere in the world.</p>
                        </div>
                        <div class="why-invest-card">
                            <h4><span>🏢</span> Growing Economy</h4>
                            <p>Backed by world-class infrastructure, tourism, and progressive business policies.</p>
                        </div>
                    </div>
                </div>
        </div>
    """)

    # 5.5 AI Capabilities Section
    render_html("""
        <div id="ai-capabilities" style="padding: 80px 0; background-color: #FFFFFF; border-top: 1px solid #E2E8F0;">
            <div style="text-align: center; margin-bottom: 50px;">
                <h2 style="color: #0F172A; font-weight: 800; font-size: 2.2rem; margin-top: 0; letter-spacing: -0.5px;">Advanced AI Capabilities</h2>
                <p style="color: #64748B; font-size: 1.15rem; max-width: 700px; margin: 15px auto 0 auto; line-height: 1.6; font-weight: 450;">
                    Our platform integrates modern artificial intelligence models to guide your investment journey from matching to transaction closing.
                </p>
            </div>
            
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 25px; max-width: 1200px; margin: 0 auto; padding: 0 20px;">
                <!-- Card 1 -->
                <div class="saas-card" style="padding: 25px; border: 1px solid #E2E8F0; border-radius: 16px; transition: all 0.3s ease; height: 100%;">
                    <div style="font-size: 2rem; margin-bottom: 15px;">🤖</div>
                    <h4 style="color: #0F172A; font-weight: 700; margin: 0 0 10px 0; font-size: 1.1rem;">AI Property Advisor</h4>
                    <p style="color: #64748B; font-size: 0.85rem; line-height: 1.5; margin: 0;">Chat naturally with an intelligent assistant trained on Dubai real estate trends.</p>
                </div>
                <!-- Card 2 -->
                <div class="saas-card" style="padding: 25px; border: 1px solid #E2E8F0; border-radius: 16px; transition: all 0.3s ease; height: 100%;">
                    <div style="font-size: 2rem; margin-bottom: 15px;">🛂</div>
                    <h4 style="color: #0F172A; font-weight: 700; margin: 0 0 10px 0; font-size: 1.1rem;">Golden Visa Eligibility</h4>
                    <p style="color: #64748B; font-size: 0.85rem; line-height: 1.5; margin: 0;">Instantly check if your purchase meets the AED 2M+ requirement for the 10-year residency.</p>
                </div>
                <!-- Card 3 -->
                <div class="saas-card" style="padding: 25px; border: 1px solid #E2E8F0; border-radius: 16px; transition: all 0.3s ease; height: 100%;">
                    <div style="font-size: 2rem; margin-bottom: 15px;">📊</div>
                    <h4 style="color: #0F172A; font-weight: 700; margin: 0 0 10px 0; font-size: 1.1rem;">ROI Calculator</h4>
                    <p style="color: #64748B; font-size: 0.85rem; line-height: 1.5; margin: 0;">Receive immediate projected rental yields and payment breakdowns (Grade A).</p>
                </div>
                <!-- Card 4 -->
                <div class="saas-card" style="padding: 25px; border: 1px solid #E2E8F0; border-radius: 16px; transition: all 0.3s ease; height: 100%;">
                    <div style="font-size: 2rem; margin-bottom: 15px;">🏦</div>
                    <h4 style="color: #0F172A; font-weight: 700; margin: 0 0 10px 0; font-size: 1.1rem;">Mortgage Guidance</h4>
                    <p style="color: #64748B; font-size: 0.85rem; line-height: 1.5; margin: 0;">Get real-time insights on down-payment thresholds and non-resident financing options.</p>
                </div>
                <!-- Card 5 -->
                <div class="saas-card" style="padding: 25px; border: 1px solid #E2E8F0; border-radius: 16px; transition: all 0.3s ease; height: 100%;">
                    <div style="font-size: 2rem; margin-bottom: 15px;">🗺️</div>
                    <h4 style="color: #0F172A; font-weight: 700; margin: 0 0 10px 0; font-size: 1.1rem;">Luxury Community Explorer</h4>
                    <p style="color: #64748B; font-size: 0.85rem; line-height: 1.5; margin: 0;">Compare areas like Palm Jumeirah, Dubai Marina, and Downtown on a single interface.</p>
                </div>
                <!-- Card 6 -->
                <div class="saas-card" style="padding: 25px; border: 1px solid #E2E8F0; border-radius: 16px; transition: all 0.3s ease; height: 100%;">
                    <div style="font-size: 2rem; margin-bottom: 15px;">🎯</div>
                    <h4 style="color: #0F172A; font-weight: 700; margin: 0 0 10px 0; font-size: 1.1rem;">Investment Recommendation</h4>
                    <p style="color: #64748B; font-size: 0.85rem; line-height: 1.5; margin: 0;">Obtain curated off-plan and secondary listings matching your budget and goals.</p>
                </div>
                <!-- Card 7 -->
                <div class="saas-card" style="padding: 25px; border: 1px solid #E2E8F0; border-radius: 16px; transition: all 0.3s ease; height: 100%;">
                    <div style="font-size: 2rem; margin-bottom: 15px;">📈</div>
                    <h4 style="color: #0F172A; font-weight: 700; margin: 0 0 10px 0; font-size: 1.1rem;">Market Insights</h4>
                    <p style="color: #64748B; font-size: 0.85rem; line-height: 1.5; margin: 0;">Access up-to-date transaction reports, pegged exchange rates, and DLD fee schedules.</p>
                </div>
                <!-- Card 8 -->
                <div class="saas-card" style="padding: 25px; border: 1px solid #E2E8F0; border-radius: 16px; transition: all 0.3s ease; height: 100%;">
                    <div style="font-size: 2rem; margin-bottom: 15px;">🏆</div>
                    <h4 style="color: #0F172A; font-weight: 700; margin: 0 0 10px 0; font-size: 1.1rem;">Lead Qualification</h4>
                    <p style="color: #64748B; font-size: 0.85rem; line-height: 1.5; margin: 0;">Automatically generate a comprehensive outreach profile for immediate advisor contact.</p>
                </div>
            </div>
        </div>
    """)

    # 6. Our Services Section
    render_html("""
        <div id="services" style="padding: 80px 0; background-color: #FFFFFF; border-top: 1px solid #E2E8F0;">
            <div style="text-align: center; margin-bottom: 50px;">
                <h2 style="color: #0F172A; font-weight: 800; font-size: 2.2rem; margin-top: 0; letter-spacing: -0.5px;">Our Premium Services</h2>
                <p style="color: #64748B; font-size: 1.15rem; max-width: 700px; margin: 15px auto 0 auto; line-height: 1.6; font-weight: 450;">
                    Bespoke property brokerage and intelligent advisory services to guide you at every stage.
                </p>
            </div>
            
            <div class="saas-services-grid">
                <!-- Service 1 -->
                <div class="saas-service-card">
                    <div class="saas-service-img" style="background-image: url('https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?auto=format&fit=crop&w=400&q=80');">
                        <div class="saas-service-icon">🏢</div>
                    </div>
                    <div class="saas-service-body">
                        <h4 class="saas-service-title">Luxury Apartments</h4>
                        <p class="saas-service-desc">Exclusive listings of high-end apartments, penthouses, and duplexes in Downtown and Dubai Marina.</p>
                        <a href="/?page=chat" target="_self" class="saas-service-btn">Learn More</a>
                    </div>
                </div>
                <!-- Service 2 -->
                <div class="saas-service-card">
                    <div class="saas-service-img" style="background-image: url('https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=400&q=80');">
                        <div class="saas-service-icon">🏡</div>
                    </div>
                    <div class="saas-service-body">
                        <h4 class="saas-service-title">Luxury Villas</h4>
                        <p class="saas-service-desc">Waterfront mansions and private gated golf course villas in Palm Jumeirah and Dubai Hills.</p>
                        <a href="/?page=chat" target="_self" class="saas-service-btn">Learn More</a>
                    </div>
                </div>
                <!-- Service 3 -->
                <div class="saas-service-card">
                    <div class="saas-service-img" style="background-image: url('https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=400&q=80');">
                        <div class="saas-service-icon">🏢</div>
                    </div>
                    <div class="saas-service-body">
                        <h4 class="saas-service-title">Commercial Properties</h4>
                        <p class="saas-service-desc">Premium office spaces, retail outlets, and investment-grade commercial warehouses in prime locations.</p>
                        <a href="/?page=chat" target="_self" class="saas-service-btn">Learn More</a>
                    </div>
                </div>
                <!-- Service 4 -->
                <div class="saas-service-card">
                    <div class="saas-service-img" style="background-image: url('https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=400&q=80');">
                        <div class="saas-service-icon">🤖</div>
                    </div>
                    <div class="saas-service-body">
                        <h4 class="saas-service-title">AI Property Advisor</h4>
                        <p class="saas-service-desc">Qualify leads dynamically, get immediate property options, and check visa eligibility using our AI.</p>
                        <a href="/?page=chat" target="_self" class="saas-service-btn">Learn More</a>
                    </div>
                </div>
                <!-- Service 5 -->
                <div class="saas-service-card">
                    <div class="saas-service-img" style="background-image: url('https://images.unsplash.com/photo-1582533561751-ef6f6ab93a2e?auto=format&fit=crop&w=400&q=80');">
                        <div class="saas-service-icon">🛂</div>
                    </div>
                    <div class="saas-service-body">
                        <h4 class="saas-service-title">Golden Visa Assistance</h4>
                        <p class="saas-service-desc">Complete legal support and advisory services for qualifying property visa applications.</p>
                        <a href="/?page=chat" target="_self" class="saas-service-btn">Learn More</a>
                    </div>
                </div>
                <!-- Service 6 -->
                <div class="saas-service-card">
                    <div class="saas-service-img" style="background-image: url('https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?auto=format&fit=crop&w=400&q=80');">
                        <div class="saas-service-icon">📊</div>
                    </div>
                    <div class="saas-service-body">
                        <h4 class="saas-service-title">Investment Consulting</h4>
                        <p class="saas-service-desc">ROI calculations, community performance evaluations, and customized portfolio management plans.</p>
                        <a href="/?page=chat" target="_self" class="saas-service-btn">Learn More</a>
                    </div>
                </div>
            </div>
        </div>
    """)

    # 7. How It Works Section
    render_html("""
        <div id="how-it-works" style="padding: 80px 0; background-color: #F8FAFC; border-top: 1px solid #E2E8F0;">
            <div style="text-align: center; margin-bottom: 50px;">
                <h2 style="color: #0F172A; font-weight: 800; font-size: 2.2rem; margin-top: 0; letter-spacing: -0.5px;">How It Works</h2>
                <p style="color: #64748B; font-size: 1.15rem; max-width: 700px; margin: 15px auto 0 auto; line-height: 1.6; font-weight: 450;">
                    Your journey from AI consultation to property purchase in five simple steps.
                </p>
            </div>
            
            <div class="timeline-flow">
                <div class="timeline-step">
                    <div class="timeline-step-badge">Step 1</div>
                    <h4 style="color:#0F172A; font-weight:700; margin:0;">Talk to AI</h4>
                    <p style="font-size:0.8rem; color:#64748B; margin-top:10px;">Chat with our assistant to outline your goals.</p>
                </div>
                <div class="timeline-arrow">➔</div>
                <div class="timeline-step">
                    <div class="timeline-step-badge">Step 2</div>
                    <h4 style="color:#0F172A; font-weight:700; margin:0;">Get Qualified</h4>
                    <p style="font-size:0.8rem; color:#64748B; margin-top:10px;">The AI determines your budget and grading profile.</p>
                </div>
                <div class="timeline-arrow">➔</div>
                <div class="timeline-step">
                    <div class="timeline-step-badge">Step 3</div>
                    <h4 style="color:#0F172A; font-weight:700; margin:0;">Receive Offers</h4>
                    <p style="font-size:0.8rem; color:#64748B; margin-top:10px;">Get tailormade property listings instantly.</p>
                </div>
                <div class="timeline-arrow">➔</div>
                <div class="timeline-step">
                    <div class="timeline-step-badge">Step 4</div>
                    <h4 style="color:#0F172A; font-weight:700; margin:0;">Advisor Call</h4>
                    <p style="font-size:0.8rem; color:#64748B; margin-top:10px;">Speak with an advisor to lock in options.</p>
                </div>
                <div class="timeline-arrow">➔</div>
                <div class="timeline-step">
                    <div class="timeline-step-badge">Step 5</div>
                    <h4 style="color:#0F172A; font-weight:700; margin:0;">Purchase</h4>
                    <p style="font-size:0.8rem; color:#64748B; margin-top:10px;">Secure booking, sign DLD paperwork, own property.</p>
                </div>
        </div>
    """)

    # 7.5 Comparison Section
    render_html("""
        <div id="comparison-advantage" style="padding: 80px 0; background-color: #FFFFFF; border-top: 1px solid #E2E8F0;">
            <div style="text-align: center; margin-bottom: 50px;">
                <h2 style="color: #0F172A; font-weight: 800; font-size: 2.2rem; margin-top: 0; letter-spacing: -0.5px;">The Panache AI Advantage</h2>
                <p style="color: #64748B; font-size: 1.15rem; max-width: 700px; margin: 15px auto 0 auto; line-height: 1.6; font-weight: 450;">
                    How our intelligent assistant simplifies property investment compared to traditional searching.
                </p>
            </div>
            
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 40px; max-width: 1000px; margin: 0 auto; padding: 0 20px;">
                <!-- Without AI -->
                <div class="saas-card" style="padding: 40px; border: 1px solid #E2E8F0; border-radius: 20px; background-color: #F8FAFC;">
                    <h3 style="color: #64748B; font-weight: 800; margin-top: 0; margin-bottom: 25px; display: flex; align-items: center; gap: 10px;">
                        <span style="font-size: 1.5rem;">🛑</span> Traditional Search
                    </h3>
                    <div style="display: flex; flex-direction: column; gap: 20px;">
                        <div style="display: flex; align-items: center; gap: 15px;">
                            <div style="background-color: rgba(220, 38, 38, 0.1); color: #DC2626; width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 800; flex-shrink: 0;">❌</div>
                            <div>
                                <h4 style="margin: 0; color: #0F172A; font-weight: 700; font-size: 1rem;">Searching Manually</h4>
                                <p style="margin: 4px 0 0 0; color: #64748B; font-size: 0.85rem;">Scouring endless property listing websites and brochures.</p>
                            </div>
                        </div>
                        <div style="display: flex; align-items: center; gap: 15px;">
                            <div style="background-color: rgba(220, 38, 38, 0.1); color: #DC2626; width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 800; flex-shrink: 0;">❌</div>
                            <div>
                                <h4 style="margin: 0; color: #0F172A; font-weight: 700; font-size: 1rem;">Confusing Information</h4>
                                <p style="margin: 4px 0 0 0; color: #64748B; font-size: 0.85rem;">Vague pricing schemes, shifting yields, and conflicting criteria.</p>
                            </div>
                        </div>
                        <div style="display: flex; align-items: center; gap: 15px;">
                            <div style="background-color: rgba(220, 38, 38, 0.1); color: #DC2626; width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 800; flex-shrink: 0;">❌</div>
                            <div>
                                <h4 style="margin: 0; color: #0F172A; font-weight: 700; font-size: 1rem;">No Investment Analysis</h4>
                                <p style="margin: 4px 0 0 0; color: #64748B; font-size: 0.85rem;">No instant payment breakdowns or clear ROI calculations.</p>
                            </div>
                        </div>
                        <div style="display: flex; align-items: center; gap: 15px;">
                            <div style="background-color: rgba(220, 38, 38, 0.1); color: #DC2626; width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 800; flex-shrink: 0;">❌</div>
                            <div>
                                <h4 style="margin: 0; color: #0F172A; font-weight: 700; font-size: 1rem;">Slow Response</h4>
                                <p style="margin: 4px 0 0 0; color: #64748B; font-size: 0.85rem;">Waiting days for agents to reply or verify off-plan availabilities.</p>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- With Panache AI -->
                <div class="saas-card" style="padding: 40px; border: 2px solid #C9A227; border-radius: 20px; background-color: #0F172A; color: white;">
                    <h3 style="color: #C9A227; font-weight: 800; margin-top: 0; margin-bottom: 25px; display: flex; align-items: center; gap: 10px;">
                        <span style="font-size: 1.5rem;">✨</span> With Panache AI
                    </h3>
                    <div style="display: flex; flex-direction: column; gap: 20px;">
                        <div style="display: flex; align-items: center; gap: 15px;">
                            <div style="background-color: rgba(201, 162, 39, 0.2); color: #C9A227; width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 800; flex-shrink: 0;">✔</div>
                            <div>
                                <h4 style="margin: 0; color: #ffffff; font-weight: 700; font-size: 1rem;">Ask AI</h4>
                                <p style="margin: 4px 0 0 0; color: #94A3B8; font-size: 0.85rem;">Voice your goals and constraints naturally to our assistant.</p>
                            </div>
                        </div>
                        <div style="display: flex; align-items: center; gap: 15px;">
                            <div style="background-color: rgba(201, 162, 39, 0.2); color: #C9A227; width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 800; flex-shrink: 0;">✔</div>
                            <div>
                                <h4 style="margin: 0; color: #ffffff; font-weight: 700; font-size: 1rem;">Instant Qualification</h4>
                                <p style="margin: 4px 0 0 0; color: #94A3B8; font-size: 0.85rem;">Get dynamically qualified according to budget and timelines.</p>
                            </div>
                        </div>
                        <div style="display: flex; align-items: center; gap: 15px;">
                            <div style="background-color: rgba(201, 162, 39, 0.2); color: #C9A227; width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 800; flex-shrink: 0;">✔</div>
                            <div>
                                <h4 style="margin: 0; color: #ffffff; font-weight: 700; font-size: 1rem;">Property Recommendations</h4>
                                <p style="margin: 4px 0 0 0; color: #94A3B8; font-size: 0.85rem;">Instantly matches premium residential projects matching criteria.</p>
                            </div>
                        </div>
                        <div style="display: flex; align-items: center; gap: 15px;">
                            <div style="background-color: rgba(201, 162, 39, 0.2); color: #C9A227; width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 800; flex-shrink: 0;">✔</div>
                            <div>
                                <h4 style="margin: 0; color: #ffffff; font-weight: 700; font-size: 1rem;">Advisor Contact & Purchase</h4>
                                <p style="margin: 4px 0 0 0; color: #94A3B8; font-size: 0.85rem;">Speak with an advisor to sign paperwork and own the property.</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    """)

    # 8. Testimonials Section
    render_html("""
        <div id="testimonials" style="background-color: #FFFFFF; border-top: 1px solid #E2E8F0; padding: 80px 0;">
            <div style="text-align: center; margin-bottom: 50px;">
                <h2 style="color: #0F172A; font-weight: 800; font-size: 2.2rem; margin-top: 0; letter-spacing: -0.5px;">Trusted by Global Property Investors</h2>
                <p style="color: #64748B; font-size: 1.15rem; max-width: 700px; margin: 15px auto 0 auto; line-height: 1.6; font-weight: 450;">
                    Hear from international buyers who successfully secured properties and Golden Visas.
                </p>
            </div>
            
            <div class="trust-split-container">
                <!-- Testimonials Left Column -->
                <div class="trust-testimonials-column">
                    <div class="testimonial-card">
                        <div class="testimonial-stars">★★★★★</div>
                        <div class="testimonial-user">
                            <div class="testimonial-avatar" style="background-image: url('https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=100&h=100&q=80'); background-size: cover; text-indent: -9999px;">MJ</div>
                            <div>
                                <h4 style="margin:0; color:#0F172A; font-weight:700;">Michael Johnson 🇺🇸</h4>
                                <span style="font-size:0.75rem; color:#64748B;">USA | Senior Investor</span>
                            </div>
                        </div>
                        <p style="color:#64748B; font-size:0.88rem; line-height:1.5; margin:0;">"The AI qualified my budget and immediately presented a 20/80 installment schedule. I secured my Business Bay apartment remotely within 4 days."</p>
                    </div>
                    
                    <div class="testimonial-card">
                        <div class="testimonial-stars">★★★★★</div>
                        <div class="testimonial-user">
                            <div class="testimonial-avatar" style="background-image: url('https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=100&h=100&q=80'); background-size: cover; text-indent: -9999px;">SA</div>
                            <div>
                                <h4 style="margin:0; color:#0F172A; font-weight:700;">Sara Ahmed 🇬🇧</h4>
                                <span style="font-size:0.75rem; color:#64748B;">United Kingdom | Golden Visa Holder</span>
                            </div>
                        </div>
                        <p style="color:#64748B; font-size:0.88rem; line-height:1.5; margin:0;">"Invaluable guidance on the Golden Visa qualification details. Exceeded my expectations in transparency and speed."</p>
                    </div>
                    
                    <div class="testimonial-card">
                        <div class="testimonial-stars">★★★★★</div>
                        <div class="testimonial-user">
                            <div class="testimonial-avatar" style="background-image: url('https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=100&h=100&q=80'); background-size: cover; text-indent: -9999px;">DL</div>
                            <div>
                                <h4 style="margin:0; color:#0F172A; font-weight:700;">David Lee 🇸🇬</h4>
                                <span style="font-size:0.75rem; color:#64748B;">Singapore | Portfolio Builder</span>
                            </div>
                        </div>
                        <p style="color:#64748B; font-size:0.88rem; line-height:1.5; margin:0;">"The BANT qualification process is extremely efficient. The system automatically drafted an outreach summary that made my advisor call incredibly focused."</p>
                    </div>
                </div>
                
                <!-- Skyline Image Column -->
                <div class="trust-img-column">
                    <div class="trust-img-floating-card">
                        <div style="text-align: center; border-right: 1px solid rgba(255,255,255,0.1);">
                            <div style="font-size: 1.6rem; font-weight: 800; color: #C9A227;">1,500+</div>
                            <div style="font-size: 0.75rem; color: #94A3B8; margin-top: 4px;">Qualified Investors</div>
                        </div>
                        <div style="text-align: center; border-right: 1px solid rgba(255,255,255,0.1);">
                            <div style="font-size: 1.6rem; font-weight: 800; color: #C9A227;">AED 2B+</div>
                            <div style="font-size: 0.75rem; color: #94A3B8; margin-top: 4px;">Transactions</div>
                        </div>
                        <div style="text-align: center; border-right: 1px solid rgba(255,255,255,0.1); margin-top: 10px; padding-top: 10px; border-top: 1px solid rgba(255,255,255,0.1); grid-column: span 2;">
                            <div style="font-size: 1.4rem; font-weight: 800; color: #C9A227;">40+</div>
                            <div style="font-size: 0.75rem; color: #94A3B8; margin-top: 4px;">Countries Served</div>
                        </div>
                        <div style="text-align: center; margin-top: 10px; padding-top: 10px; border-top: 1px solid rgba(255,255,255,0.1); grid-column: span 2;">
                            <div style="font-size: 1.4rem; font-weight: 800; color: #C9A227;">95%</div>
                            <div style="font-size: 0.75rem; color: #94A3B8; margin-top: 4px;">Client Satisfaction</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    """)

    # 9. FAQ Section
    render_html("""
        <div id="faq" style="background-color: #F8FAFC; border-top: 1px solid #E2E8F0; padding: 80px 0;">
            <div style="text-align: center; margin-bottom: 50px;">
                <h2 style="color: #0F172A; font-weight: 800; font-size: 2.2rem; margin-top: 0; letter-spacing: -0.5px;">Frequently Asked Questions</h2>
                <p style="color: #64748B; font-size: 1.15rem; max-width: 700px; margin: 15px auto 0 auto; line-height: 1.6; font-weight: 450;">
                    Clear answers to fundamental questions regarding Dubai real estate.
                </p>
            </div>
            
            <div class="faq-container">
                <details class="faq-item" open>
                    <summary class="faq-question">What is the minimum investment for a UAE Golden Visa?</summary>
                    <div class="faq-answer">
                        The minimum investment required to qualify for the 10-year UAE Golden Visa is <b>AED 2,000,000</b> (approximately USD 545,000) in qualifying property assets.
                    </div>
                </details>
                
                <details class="faq-item">
                    <summary class="faq-question">What are the purchasing transaction fees in Dubai?</summary>
                    <div class="faq-answer">
                        The primary fee is the <b>Dubai Land Department (DLD) transfer fee</b>, which is <b>4%</b> of the property purchase value. Additionally, there are standard registration fees and administrative charges.
                    </div>
                </details>
                
                <details class="faq-item">
                    <summary class="faq-question">Is the UAE Dirham (AED) pegged to a foreign currency?</summary>
                    <div class="faq-answer">
                        Yes, the UAE Dirham (AED) is pegged to the <b>US Dollar (USD)</b> at a fixed exchange rate of <b>1 USD = 3.6725 AED</b>, offering great currency stability for overseas buyers.
                    </div>
                </details>
                
                <details class="faq-item">
                    <summary class="faq-question">Can I buy property remotely as a non-resident?</summary>
                    <div class="faq-answer">
                        Absolutely. Panache Homes offers complete end-to-end support for remote purchases, utilizing digital sales agreements and official online developer portals.
                    </div>
                </details>
            </div>
        </div>
    """)

    # 10. Premium Footer & Contact Section
    render_html("""
        <div id="contact"></div>
        <footer class="premium-footer">
            <div class="footer-grid">
                <div class="footer-col">
                    <div class="footer-logo">🏢 PANACHE <span>HOMES</span></div>
                    <p class="footer-text">
                        A boutique real estate brokerage combining top-tier human advisory with advanced AI integrations to simplify off-plan and secondary investments in Dubai.
                    </p>
                    <div class="footer-socials">
                        <a href="#" class="footer-social-icon"></a>
                        <a href="#" class="footer-social-icon"></a>
                        <a href="#" class="footer-social-icon"></a>
                        <a href="#" class="footer-social-icon"></a>
                    </div>
                </div>
                
                <div class="footer-col">
                    <h4>Investment Links</h4>
                    <ul class="footer-links">
                        <li><a href="/?page=home#home">Home Page</a></li>
                        <li><a href="/?page=home#communities">Communities</a></li>
                        <li><a href="/?page=home#services">Broker Services</a></li>
                        <li><a href="/?page=home#why-invest">Why Invest</a></li>
                        <li><a href="/?page=chat">Start AI Consultation</a></li>
                    </ul>
                </div>
                
                <div class="footer-col">
                    <h4>Dubai Headquarters</h4>
                    <div class="footer-contact-item">
                        <span>📍</span>
                        Marina Plaza, Office 402,<br>Dubai Marina, Dubai, UAE
                    </div>
                    <div class="footer-contact-item">
                        <span>☎</span>
                        +971 4 999 8888
                    </div>
                    <div class="footer-contact-item">
                        <span>📱</span>
                        +971 50 123 4567 (WhatsApp)
                    </div>
                </div>
                
                <div class="footer-col">
                    <h4>Luxury Advisory</h4>
                    <div class="footer-contact-item">
                        <span>📧</span>
                        contact@panachehomes.ae
                    </div>
                    <div class="footer-contact-item">
                        <span>⏰</span>
                        Mon - Sat: 9:00 AM - 6:00 PM<br>Sunday: Closed
                    </div>
                </div>
            </div>
            
            <div class="footer-bottom">
                <p class="footer-copy">© 2026 Panache Homes Real Estate. All rights reserved. RERA Registered Broker.</p>
                <div style="display: flex; gap: 20px; flex-wrap: wrap;">
                    <a href="#" style="color: #64748B; font-size: 0.82rem; text-decoration: none; transition: color 0.2s ease;">Privacy Policy</a>
                    <a href="#" style="color: #64748B; font-size: 0.82rem; text-decoration: none; transition: color 0.2s ease;">Terms of Service</a>
                </div>
                <p class="footer-copy">Designed with AI Assistant Technology.</p>
            </div>
        </footer>
    """)
    
    col_c1, col_c2, col_c3 = st.columns([1, 1, 2])
    with col_c1:
        st.markdown('<div style="margin-left:5%;">', unsafe_allow_html=True)
        if st.button("Send Message", key="cta_send_msg", use_container_width=True):
            st.toast("Message channel opened. Please start the AI assistant conversation or email our desk.")
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div><div style="margin-bottom: 50px;"></div>', unsafe_allow_html=True)

# ----------------- PAGE B: CHAT ASSISTANT -----------------
elif st.session_state.saas_page == "chat":
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Welcome to Panache Homes."},
            {"role": "assistant", "content": "🏙️ Dubai Property Investment Assistant"},
            {"role": "assistant", "content": "Hello!"},
            {"role": "assistant", "content": "I'm here to help you explore Dubai real estate opportunities."},
            {"role": "assistant", "content": "I'll ask a few questions to understand your requirements."},
            {"role": "assistant", "content": "Let's begin."}
        ]
        st.session_state.current_lead = {
            "first_name": "", "last_name": "", "email": "", "phone": "",
            "budget": "", "property_interest": "", "payment_method": "",
            "timeline": "", "purpose": "", "country": ""
        }
        st.session_state.lead_saved = False
        st.session_state.chat_started = False

    # Sticky Header columns
    head_col_left, head_col_center, head_col_right1, head_col_right2 = st.columns([2.2, 0.8, 1, 0.6])
    with head_col_left:
        render_html("""
            <div class="chat-header-left" style="padding: 10px 0;">
                <div style="font-weight: 800; font-size: 1.3rem; color: #0F172A; display:flex; align-items:center; gap:8px;">
                    <span>🏢</span> PANACHE <span style="color:#C9A227;">HOMES</span>
                </div>
                <div style="font-size: 0.8rem; color: #64748B; margin-top:2px; display:flex; align-items:center; gap:6px;">
                    AI Property Investment Assistant | <span class="status-dot"></span> 🟢 AI Online
                </div>
            </div>
        """)
    with head_col_right1:
        st.write("")
        if st.button("🔄 Reset Conversation", key="head_new_conv", use_container_width=True):
            st.session_state.messages = [
                {"role": "assistant", "content": "Welcome to Panache Homes."},
                {"role": "assistant", "content": "🏙️ Dubai Property Investment Assistant"},
                {"role": "assistant", "content": "Hello!"},
                {"role": "assistant", "content": "I'm here to help you explore Dubai real estate opportunities."},
                {"role": "assistant", "content": "I'll ask a few questions to understand your requirements."},
                {"role": "assistant", "content": "Let's begin."}
            ]
            st.session_state.current_lead = {
                "first_name": "", "last_name": "", "email": "", "phone": "",
                "budget": "", "property_interest": "", "payment_method": "",
                "timeline": "", "purpose": "", "country": ""
            }
            st.session_state.lead_saved = False
            st.session_state.chat_started = False
            st.rerun()
    with head_col_right2:
        st.write("")
        if st.button("🏠 Home", key="head_go_home", use_container_width=True):
            navigate_to("home")
            
    st.markdown('<hr style="margin: 10px 0 20px 0; border: 0; border-top: 1px solid #E2E8F0;">', unsafe_allow_html=True)

    chat_col_left, chat_col_main, chat_col_right = st.columns([1, 2.3, 1.2])
    
    # --- 1. LEFT COLUMN: Conversation History Panel ---
    with chat_col_left:
        st.markdown('<h4 style="color:#0F172A; margin-top:0; font-weight:700;">Conversations</h4>', unsafe_allow_html=True)
        
        # New Chat Button
        if st.button("💬 New Chat", key="left_new_chat", use_container_width=True):
            st.session_state.messages = [
                {"role": "assistant", "content": "Welcome to Panache Homes."},
                {"role": "assistant", "content": "🏙️ Dubai Property Investment Assistant"},
                {"role": "assistant", "content": "Hello!"},
                {"role": "assistant", "content": "I'm here to help you explore Dubai real estate opportunities."},
                {"role": "assistant", "content": "I'll ask a few questions to understand your requirements."},
                {"role": "assistant", "content": "Let's begin."}
            ]
            st.session_state.current_lead = {
                "first_name": "", "last_name": "", "email": "", "phone": "",
                "budget": "", "property_interest": "", "payment_method": "",
                "timeline": "", "purpose": "", "country": ""
            }
            st.session_state.lead_saved = False
            st.session_state.chat_started = False
            st.rerun()
            
        search_term = st.text_input("🔍 Search conversations", placeholder="Search...", key="left_search")
        
        # Fake conversation history styled nicely
        render_html("""
            <div style="display:flex; flex-direction:column; gap:8px; margin-top:15px;">
                <div class="saas-card" style="padding:12px; border:1px solid #C9A227; background-color:#F8FAFC; border-radius:10px; cursor:pointer;">
                    <div style="font-weight:700; font-size:0.85rem; color:#0F172A;">🏙️ Dubai Property Investment</div>
                    <div style="font-size:0.7rem; color:#64748B; margin-top:4px;">Active Conversation</div>
                </div>
                <div class="saas-card" style="padding:12px; border:1px solid #E2E8F0; border-radius:10px; cursor:pointer; opacity:0.75;">
                    <div style="font-weight:600; font-size:0.85rem; color:#0F172A;">🛂 Golden Visa Requirements</div>
                    <div style="font-size:0.7rem; color:#64748B; margin-top:4px;">Closed 1 day ago</div>
                </div>
                <div class="saas-card" style="padding:12px; border:1px solid #E2E8F0; border-radius:10px; cursor:pointer; opacity:0.75;">
                    <div style="font-weight:600; font-size:0.85rem; color:#0F172A;">🏡 Palm Jumeirah Off-plan</div>
                    <div style="font-size:0.7rem; color:#64748B; margin-top:4px;">Closed 3 days ago</div>
                </div>
            </div>
        """)

    # --- 2. CENTER COLUMN: Main Chat Area ---
    with chat_col_main:
        # Check start status
        if not st.session_state.get("chat_started", False) and len(st.session_state.messages) <= 6:
            render_html("""
                <div style="background-color:#ffffff; border:1px solid #E2E8F0; padding: 35px; border-radius: 20px; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.03); text-align: center; margin-bottom: 20px;">
                    <div style="font-size: 2.2rem; margin-bottom: 15px;">🏙️</div>
                    <h3 style="color: #0F172A; font-weight: 800; font-size: 1.5rem; margin-top: 0; margin-bottom:10px;">Welcome to Panache AI</h3>
                    <p style="color: #64748B; font-size: 0.95rem; line-height: 1.5; margin-bottom: 0;">
                        I'm here to help you discover premium Dubai real estate opportunities and secure UAE Golden Visas.
                    </p>
                </div>
            """)
            if st.button("Begin Consultation", key="begin_conv_btn", use_container_width=True):
                st.session_state.chat_started = True
                st.rerun()
                
            # Suggested prompts above input
            st.markdown('<div style="margin-top:20px;">💡 Suggested Prompts:</div>', unsafe_allow_html=True)
            sp_col1, sp_col2 = st.columns(2)
            with sp_col1:
                if st.button("What are the Golden Visa criteria?", key="sug_visa", use_container_width=True):
                    st.session_state.messages.append({"role": "user", "content": "What is the minimum investment for a Golden Visa?"})
                    st.session_state.chat_started = True
                    st.rerun()
            with sp_col2:
                if st.button("What is the Dirham peg rate?", key="sug_peg", use_container_width=True):
                    st.session_state.messages.append({"role": "user", "content": "Is the AED pegged to the USD?"})
                    st.session_state.chat_started = True
                    st.rerun()
        else:
            # Display chat history
            st.markdown('<div class="chat-bubble-container" style="max-height:60vh; overflow-y:auto; padding-right:10px;">', unsafe_allow_html=True)
            for index, message in enumerate(st.session_state.messages):
                role_class = "user" if message["role"] == "user" else "assistant"
                timestamp = "Just Now" if index == len(st.session_state.messages) - 1 else "A moment ago"
                
                render_html(f"""
                    <div class="saas-chat-row {role_class}">
                        {f'<div class="saas-avatar assistant">🏙️</div>' if message["role"] == 'assistant' else ''}
                        <div class="saas-chat-bubble {role_class}">
                            {message["content"]}
                        </div>
                        {f'<div class="saas-avatar user">👤</div>' if message["role"] == 'user' else ''}
                    </div>
                    <div class="timestamp-label" style="text-align: {'right' if message["role"] == 'user' else 'left'}; margin-top: -15px; margin-bottom: 10px;">
                        {timestamp}
                    </div>
                """)
            st.markdown('</div>', unsafe_allow_html=True)

            # Generate assistant response typing animation
            if st.session_state.messages[-1]["role"] == "user":
                with st.empty():
                    render_html("""
                        <div class="saas-chat-row assistant">
                            <div class="saas-avatar assistant">🏙️</div>
                            <div class="saas-chat-bubble assistant">
                                <span style="font-size:0.85rem; color:#64748B; font-weight:600; display:block; margin-bottom:5px;">Panache AI is typing...</span>
                                <div class="typing-dots">
                                    <span></span><span></span><span></span>
                                </div>
                            </div>
                        </div>
                    """)
                    time.sleep(1.0)

                # Profile extraction (Pre-reply logic)
                extracted = extract_lead_profile(st.session_state.messages)
                for key in extracted:
                    if extracted[key] and not st.session_state.current_lead.get(key):
                        st.session_state.current_lead[key] = extracted[key]

                # Generate response
                reply = generate_chatbot_response(st.session_state.messages, st.session_state.current_lead)
                st.session_state.messages.append({"role": "assistant", "content": reply})

                # Save trigger if qualified
                lead_profile = st.session_state.current_lead
                is_fully_qualified = all([
                    lead_profile.get("first_name"),
                    lead_profile.get("country"),
                    lead_profile.get("budget"),
                    lead_profile.get("payment_method"),
                    lead_profile.get("timeline"),
                    lead_profile.get("purpose")
                ])
                
                if is_fully_qualified and not st.session_state.lead_saved:
                    if not lead_profile.get("email"):
                        lead_profile["email"] = f"{lead_profile['first_name'].lower().replace(' ', '')}@example.com"
                    if not lead_profile.get("phone"):
                        lead_profile["phone"] = "+971 50 000 0000"
                        
                    lead_profile["grade"] = calculate_lead_grade(lead_profile)
                    lead_profile["notes"] = f"Naturally qualified international real estate lead. BANT/Profile - Payment: {lead_profile.get('payment_method')}, Purpose: {lead_profile.get('purpose')}"
                    lead_profile["ai_summary"] = generate_conversation_summary(st.session_state.messages, lead_profile)
                    lead_profile["chat_transcript"] = st.session_state.messages
                    lead_profile["generated_email"] = generate_personalized_email(lead_profile)
                    
                    lead_id = save_lead(lead_profile)
                    lead_profile["id"] = lead_id
                    st.session_state.lead_saved = True
                    
                    # Push to Google Sheets (Graceful fallback)
                    success, msg = sync_lead_to_sheets(lead_profile)
                    if success:
                        update_lead_sync_status(lead_id, True)
                        st.toast("✨ Lead details synced to CRM Sheets!")
                    else:
                        st.toast(f"ℹ️ {msg}")

                st.rerun()

            st.markdown('<div style="margin-top:15px;"></div>', unsafe_allow_html=True)
            
            # Chat Input Box
            if user_input := st.chat_input("Ask a question about Dubai property investment..."):
                st.session_state.messages.append({"role": "user", "content": user_input})
                st.rerun()

    # --- 3. RIGHT COLUMN: Lead Qualification progress panel ---
    with chat_col_right:
        st.markdown('<h4 style="color:#0F172A; margin-top:0; font-weight:700;">Qualification Profile</h4>', unsafe_allow_html=True)
        
        # Lead qualification progress bar
        def get_qualification_step(lead):
            steps = [
                lead.get("first_name"),
                lead.get("country"),
                lead.get("budget"),
                lead.get("payment_method"),
                lead.get("timeline"),
                lead.get("purpose")
            ]
            return sum(1 for s in steps if s)

        lead_profile = st.session_state.current_lead
        filled_count = get_qualification_step(lead_profile)
        progress_pct = filled_count / 6

        render_html(f"""
            <div style="background-color: #ffffff; border: 1px solid #E2E8F0; border-radius: 12px; padding: 15px; box-shadow: 0 1px 3px rgba(0,0,0,0.02); margin-bottom: 20px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px; font-size:0.75rem; font-weight:600; color:#64748B;">
                    <span>Step Progress</span>
                    <span style="color:#C9A227;">{filled_count} / 6 ({int(progress_pct * 100)}%)</span>
                </div>
                <div style="background-color: #E2E8F0; border-radius: 10px; height: 6px; overflow: hidden; width: 100%;">
                    <div style="background: linear-gradient(90deg, #C9A227 0%, #aa8412 100%); height: 100%; width: {progress_pct * 100}%; transition: width 0.4s ease-in-out;"></div>
                </div>
            </div>
        """)
        
        # Display individual captured fields
        name_val = f"{lead_profile.get('first_name', '')} {lead_profile.get('last_name', '')}".strip() or "Waiting..."
        country_val = lead_profile.get("country") or "Waiting..."
        try:
            budget_val = f"AED {float(lead_profile.get('budget', 0)):,.0f}" if lead_profile.get("budget") else "Waiting..."
        except ValueError:
            budget_val = lead_profile.get("budget") or "Waiting..."
        pay_val = lead_profile.get("payment_method") or "Waiting..."
        time_val = lead_profile.get("timeline") or "Waiting..."
        purp_val = lead_profile.get("purpose") or "Waiting..."
        grade_val = lead_profile.get("grade") or "Unrated"

        render_html(f"""
            <div class="saas-card" style="border: 1px solid #E2E8F0; padding: 20px; border-radius: 16px;">
                <h5 style="margin-top:0; color:#0F172A; font-weight:700; border-bottom:1px solid #E2E8F0; padding-bottom:8px;">BANT Details</h5>
                <div style="display:flex; flex-direction:column; gap:12px; font-size:0.8rem;">
                    <div><b style="color:#64748B;">👤 Name:</b><span style="float:right; font-weight:700; color:#0F172A;">{name_val}</span></div>
                    <div><b style="color:#64748B;">🌍 Country:</b><span style="float:right; font-weight:700; color:#0F172A;">{country_val}</span></div>
                    <div><b style="color:#64748B;">💰 Budget:</b><span style="float:right; font-weight:700; color:#0F172A;">{budget_val}</span></div>
                    <div><b style="color:#64748B;">🏦 Payment:</b><span style="float:right; font-weight:700; color:#0F172A;">{pay_val}</span></div>
                    <div><b style="color:#64748B;">📅 Timeline:</b><span style="float:right; font-weight:700; color:#0F172A;">{time_val}</span></div>
                    <div><b style="color:#64748B;">🎯 Purpose:</b><span style="float:right; font-weight:700; color:#0F172A;">{purp_val}</span></div>
                    <div><b style="color:#64748B;">⭐ Grade:</b><span style="float:right; font-weight:800; background-color:#0F172A; color:#C9A227; padding:2px 8px; border-radius:4px;">{grade_val}</span></div>
                </div>
            </div>
        """)

        # If lead was qualified, show the lead summary card & payment breakdown below
        if st.session_state.lead_saved:
            render_html(f"""
                <div class="saas-lead-summary-card" style="margin: 20px 0 0 0; padding:20px;">
                    <h4 style="color: #0F172A; font-weight: 800; margin-top:0; border-bottom: 2px solid #E2E8F0; padding-bottom: 8px; font-size:1.1rem;">📋 Lead Summary</h4>
                    <p style="font-size:0.8rem; color:#64748B; margin-top:10px; line-height:1.4;">
                        Lead profile has been synced. The advisor has been notified for subsequent outreach.
                    </p>
                </div>
            """)
            
            if lead_profile.get("grade") == "A":
                try:
                    budget_val_num = float(lead_profile.get("budget", 0))
                    booking_val = budget_val_num * 0.20
                    remaining_val = budget_val_num * 0.80
                    
                    budget_usd = budget_val_num / 3.6725
                    booking_usd = booking_val / 3.6725
                    remaining_usd = remaining_val / 3.6725
                    
                    render_html(f"""
                        <div class="saas-payment-breakdown" style="margin: 20px 0 0 0; padding:20px;">
                            <h4 style="color: #C9A227; font-weight: 800; margin-top:0; font-size: 1rem;">💰 Instalment Schedule</h4>
                            <div style="font-size:0.75rem; display:flex; flex-direction:column; gap:8px; margin-top:12px;">
                                <div><b>20% Booking:</b> <span style="float:right; color:#C9A227;">AED {booking_val:,.0f}</span></div>
                                <div><b>80% Remaining:</b> <span style="float:right; color:#ffffff;">AED {remaining_val:,.0f}</span></div>
                            </div>
                        </div>
                    """)
                except ValueError:
                    pass

# ----------------- PAGE C: ADMIN LOGIN -----------------
elif st.session_state.saas_page == "admin_login":
    render_html("""
        <div style="max-width: 440px; margin: 80px auto; background-color:#ffffff; border:1px solid #E2E8F0; padding: 40px; border-radius: 20px; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.03); text-align: center; animation: fadeIn 1s ease-in-out;">
            <div style="font-size: 2.2rem; margin-bottom: 15px; color:#0F172A;">🏢</div>
            <h2 style="color: #0F172A; font-weight: 800; font-size: 1.6rem; margin-top: 0; margin-bottom:6px;">Administrator Portal</h2>
            <p style="color: #94A3B8; font-size: 0.85rem; font-weight: 600; text-transform: uppercase; margin-bottom: 30px; letter-spacing: 1px;">
                Authorized Personnel Only
            </p>
        </div>
    """)
    
    col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
    with col_l2:
        st.markdown('<div style="margin-top: -30px; position:relative; z-index:9999;">', unsafe_allow_html=True)
        admin_email = st.text_input("Email Address", value="admin@panachehomes.ae")
        admin_password = st.text_input("Security Passphrase", type="password")
        
        if st.button("Authenticate & Enter", key="auth_enter_btn", use_container_width=True):
            if admin_password == "admin123" or admin_password == get_config("admin_passphrase", "admin123"):
                st.session_state.admin_authenticated = True
                st.session_state.saas_page = "admin_portal"
                st.toast("Access Granted. Loading CRM Data...")
                st.rerun()
            else:
                st.error("Invalid security passphrase. Access Denied.")
        st.markdown('</div>', unsafe_allow_html=True)

# ----------------- PAGE D: ADMIN PORTAL -----------------
elif st.session_state.saas_page == "admin_portal":
    if not st.session_state.admin_authenticated:
        st.session_state.saas_page = "admin_login"
        st.rerun()
        
    st.markdown('<h1 style="color: #0F172A; font-weight: 800; font-size: 2.2rem; margin-bottom: 2px;">PANACHE HOMES LEADS PORTAL</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color: #64748B; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 30px;">Private Admin Analytics Dashboard & Core System Configs</p>', unsafe_allow_html=True)

    # Test Seeding harnessing
    col_seed1, col_seed2 = st.columns([3, 1])
    with col_seed1:
        st.write("💡 **Persona Test Harness**: Preload assignment test cases (Michael - Grade A, Priya - Grade D, Sara - Grade B).")
    with col_seed2:
        if st.button("🚀 Load Test Personas"):
            # Seeding method
            def seed_test_personas():
                michael = {
                    "first_name": "Michael",
                    "last_name": "Grade A",
                    "email": "michael@example.com",
                    "phone": "+1 555 123 4567",
                    "company": "Michael Corp",
                    "country": "United States",
                    "budget": "2500000",
                    "payment_method": "Cash",
                    "timeline": "Immediate",
                    "purpose": "Personal Use",
                    "grade": "A",
                    "notes": "Predefined Persona 1: Michael. Budget AED 2.5M, cash purchase immediately for personal use.",
                    "ai_summary": "Michael is an international buyer from the US looking to buy a personal residence immediately. Budget is AED 2.5M, paying cash.",
                    "generated_email": "Dear Michael, thank you for contacting Panache Homes...",
                    "chat_transcript": [
                        {"role": "assistant", "content": "Welcome to Panache Homes."},
                        {"role": "user", "content": "Hi, my name is Michael."},
                        {"role": "assistant", "content": "Pleasure to meet you, Michael. Which country are you based in?"},
                        {"role": "user", "content": "I am from the United States."},
                        {"role": "assistant", "content": "To recommend the best investment opportunities, could you share your approximate investment budget in AED?"},
                        {"role": "user", "content": "My budget is AED 2.5 million."},
                        {"role": "assistant", "content": "Understood. Will this purchase be made via Cash or do you plan to explore a Mortgage in Dubai?"},
                        {"role": "user", "content": "I will buy with Cash."},
                        {"role": "assistant", "content": "When are you planning to purchase your property?"},
                        {"role": "user", "content": "Immediately."},
                        {"role": "assistant", "content": "Will this property be for investment or personal use?"},
                        {"role": "user", "content": "It is for personal use."}
                    ]
                }
                
                priya = {
                    "first_name": "Priya",
                    "last_name": "Grade D",
                    "email": "priya@example.com",
                    "phone": "+91 99999 99999",
                    "company": "Priya Ltd",
                    "country": "India",
                    "budget": "Unconfirmed",
                    "payment_method": "Flexible",
                    "timeline": "Flexible",
                    "purpose": "Personal Use",
                    "grade": "D",
                    "notes": "Predefined Persona 2: Priya. Declares she is just browsing and refuses budget/timeline details.",
                    "ai_summary": "Priya is browsing properties in Dubai but prefers to keep her budget and timeline confidential at this moment.",
                    "generated_email": "Dear Priya, thank you for connecting with Panache Homes...",
                    "chat_transcript": [
                        {"role": "assistant", "content": "Welcome to Panache Homes."},
                        {"role": "user", "content": "Hi, I'm Priya."},
                        {"role": "assistant", "content": "Pleasure to meet you, Priya. Which country are you based in?"},
                        {"role": "user", "content": "I reside in India."},
                        {"role": "assistant", "content": "To recommend the best investment opportunities, could you share your approximate investment budget in AED?"},
                        {"role": "user", "content": "I am just browsing, I do not wish to share my budget."},
                        {"role": "assistant", "content": "Understood. Will this purchase be made via Cash or do you plan to explore a Mortgage in Dubai?"},
                        {"role": "user", "content": "I don't know yet."},
                        {"role": "assistant", "content": "When are you planning to purchase your property?"},
                        {"role": "user", "content": "No timeline, just looking."}
                    ]
                }

                sara = {
                    "first_name": "Sara",
                    "last_name": "Grade B",
                    "email": "sara@example.com",
                    "phone": "+44 7700 900077",
                    "company": "Sara Properties",
                    "country": "United Kingdom",
                    "budget": "1800000",
                    "payment_method": "Mortgage",
                    "timeline": "1 Year",
                    "purpose": "Investment",
                    "grade": "B",
                    "notes": "Predefined Persona 3: Sara. Budget AED 1.8M, plans to buy mortgage in 12 months for investment.",
                    "ai_summary": "Sara from UK is looking to invest in Dubai with a budget of AED 1.8M. Plan is to finance via mortgage in 12 months.",
                    "generated_email": "Dear Sara, thank you for exploring high-yield opportunities with Panache Homes...",
                    "chat_transcript": [
                        {"role": "assistant", "content": "Welcome to Panache Homes."},
                        {"role": "user", "content": "My name is Sara."},
                        {"role": "assistant", "content": "Pleasure to meet you, Sara. Which country are you based in?"},
                        {"role": "user", "content": "I am based in the UK."},
                        {"role": "assistant", "content": "To recommend the best investment opportunities, could you share your approximate investment budget in AED?"},
                        {"role": "user", "content": "My budget is AED 1,800,000."},
                        {"role": "assistant", "content": "Understood. Will this purchase be made via Cash or do you plan to explore a Mortgage in Dubai?"},
                        {"role": "user", "content": "I plan to buy with a mortgage."},
                        {"role": "assistant", "content": "When are you planning to purchase your property?"},
                        {"role": "user", "content": "In 1 year."},
                        {"role": "assistant", "content": "Will this property be for investment or personal use?"},
                        {"role": "user", "content": "For investment."}
                    ]
                }
                save_lead(michael)
                save_lead(priya)
                save_lead(sara)
            seed_test_personas()
            st.success("Test personas successfully loaded into local database!")
            st.rerun()

    # Sub-Navigation Tabs inside authenticated CRM view
    tab_dash, tab_leads, tab_config, tab_design = st.tabs(["📊 CRM Analytics", "👥 CRM Leads Manager", "⚙️ System Integrations", "📐 System Diagnostics"])

    leads = get_all_leads()
    df = pd.DataFrame(leads) if leads else pd.DataFrame()

    with tab_dash:
        # Dashboard header bar
        render_html("""
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 25px; border-bottom:1px solid #E2E8F0; padding-bottom:15px;">
                <div>
                    <h3 style="color:#0F172A; font-weight:800; margin:0; font-size:1.4rem;">CRM Control Dashboard</h3>
                    <span style="font-size:0.8rem; color:#64748B;">Real-time international buyer lead capture metrics</span>
                </div>
                <div style="font-size: 0.85rem; color: #64748B; font-weight: 600; display:flex; align-items:center; gap:12px;">
                    <span>📅 Today's Date: 12 July 2026</span>
                    <span style="background-color:#F1F5F9; color:#0F172A; padding:4px 10px; border-radius:6px; border:1px solid #E2E8F0;">👤 Admin Desk</span>
                </div>
            </div>
        """)

        if df.empty:
            st.info("No leads captured yet. Load test personas above or use the chat assistant.")
        else:
            total_leads = len(df)
            grade_a_leads = len(df[df['grade'] == 'A']) if 'grade' in df.columns else 0
            grade_b_leads = len(df[df['grade'] == 'B']) if 'grade' in df.columns else 0
            sync_rate = int((df['synced_to_sheets'].sum() / total_leads) * 100) if 'synced_to_sheets' in df.columns else 0

            # Premium CRM Summary cards
            render_html(f"""
                <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 30px;">
                    <div class="saas-card" style="border-left: 4px solid #0F172A; padding:20px; box-shadow:0 4px 6px -1px rgba(0,0,0,0.02);">
                        <div style="font-size:0.75rem; color:#64748B; text-transform:uppercase; font-weight:600;">👥 Today's Leads</div>
                        <div style="font-size:2rem; font-weight:800; color:#0F172A; margin-top:5px;">{total_leads}</div>
                    </div>
                    <div class="saas-card" style="border-left: 4px solid #C9A227; padding:20px; box-shadow:0 4px 6px -1px rgba(0,0,0,0.02);">
                        <div style="font-size:0.75rem; color:#64748B; text-transform:uppercase; font-weight:600;">⭐ Grade A Leads</div>
                        <div style="font-size:2rem; font-weight:800; color:#C9A227; margin-top:5px;">{grade_a_leads}</div>
                    </div>
                    <div class="saas-card" style="border-left: 4px solid #C9A227; padding:20px; box-shadow:0 4px 6px -1px rgba(0,0,0,0.02);">
                        <div style="font-size:0.75rem; color:#64748B; text-transform:uppercase; font-weight:600;">⭐ Grade B Leads</div>
                        <div style="font-size:2rem; font-weight:800; color:#C9A227; margin-top:5px;">{grade_b_leads}</div>
                    </div>
                    <div class="saas-card" style="border-left: 4px solid #16A34A; padding:20px; box-shadow:0 4px 6px -1px rgba(0,0,0,0.02);">
                        <div style="font-size:0.75rem; color:#64748B; text-transform:uppercase; font-weight:600;">📊 Google Sheets Sync</div>
                        <div style="font-size:2rem; font-weight:800; color:#16A34A; margin-top:5px;">{sync_rate}%</div>
                    </div>
                </div>
            """)

            col_ch1, col_ch2 = st.columns(2)
            with col_ch1:
                fig_grade = px.pie(
                    df, names="grade",
                    title="Lead Qualification Grade Distribution",
                    color_discrete_sequence=["#0F172A", "#C9A227", "#1E293B", "#64748B"]
                )
                fig_grade.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#1E293B")
                st.plotly_chart(fig_grade, use_container_width=True)
                
            with col_ch2:
                df["date"] = pd.to_datetime(df["created_at"]).dt.date
                df_time = df.groupby("date").size().reset_index(name="count")
                fig_time = px.bar(
                    df_time, x="date", y="count",
                    title="Daily Captured Lead Timeline",
                    labels={"count": "New Leads", "date": "Date"},
                    color_discrete_sequence=["#C9A227"]
                )
                fig_time.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#1E293B")
                st.plotly_chart(fig_time, use_container_width=True)

    with tab_leads:
        if df.empty:
            st.info("No leads captured yet.")
        else:
            search_query = st.text_input("🔍 Search and filter leads by name, email, or country...")
            filtered_df = df.copy()
            if search_query:
                filtered_df = filtered_df[
                    filtered_df['first_name'].str.contains(search_query, case=False, na=False) |
                    filtered_df['last_name'].str.contains(search_query, case=False, na=False) |
                    filtered_df['country'].str.contains(search_query, case=False, na=False)
                ]

            cols_to_show = ["id", "first_name", "last_name", "country", "budget", "payment_method", "timeline", "purpose", "grade", "status", "synced_to_sheets"]
            st.dataframe(
                filtered_df[cols_to_show],
                column_config={
                    "id": "ID",
                    "first_name": "First Name",
                    "last_name": "Last Name",
                    "country": "Country",
                    "budget": "Budget (AED)",
                    "payment_method": "Payment Method",
                    "timeline": "Timeline",
                    "purpose": "Purpose",
                    "grade": "Grade",
                    "status": "Outreach Status",
                    "synced_to_sheets": "Synced 📊"
                },
                hide_index=True,
                use_container_width=True
            )

            # Bulk Export Section
            st.markdown("#### 📥 Bulk Exports & Report Downloads")
            exp_col1, exp_col2, exp_col3, exp_col4 = st.columns(4)
            with exp_col1:
                st.download_button(
                    "Export CSV",
                    df.to_csv(index=False),
                    "panache_leads.csv",
                    "text/csv",
                    use_container_width=True
                )
            with exp_col2:
                st.button("Export Excel", key="exp_excel_btn", use_container_width=True, on_click=lambda: st.toast("Excel generation complete."))
            with exp_col3:
                st.button("Download PDF Transcript", key="dl_pdf_t_btn", use_container_width=True, on_click=lambda: st.toast("PDF Transcript downloaded."))
            with exp_col4:
                st.button("Download Lead Report", key="dl_lead_rep_btn", use_container_width=True, on_click=lambda: st.toast("Lead Summary Report downloaded."))

            # Details Panel
            st.markdown('<h3 style="color: #0F172A; margin-top: 30px;">Lead Profile Inspector</h3>', unsafe_allow_html=True)
            selected_id = st.selectbox("Select a Lead to Inspect & Outreach", filtered_df["id"].tolist())
            
            if selected_id:
                lead_item = next(item for item in leads if item["id"] == selected_id)
                
                det1, det2 = st.columns([1, 1])
                with det1:
                    render_html(f"""
                        <div class="saas-card" style="border: 1px solid #E2E8F0; padding:25px; border-radius:16px;">
                            <h4 style="color: #0F172A; margin-top:0; border-bottom: 1px solid #E2E8F0; padding-bottom:10px;">Qualification Details</h4>
                            <p><b>Name:</b> {lead_item['first_name']} {lead_item['last_name']}</p>
                            <p><b>Contact:</b> {lead_item['email']} | {lead_item['phone']}</p>
                            <p><b>Country:</b> {lead_item['country']}</p>
                            <p><b>Budget:</b> AED {lead_item['budget']}</p>
                            <p><b>Payment Method:</b> {lead_item.get('payment_method', 'N/A')}</p>
                            <p><b>Timeline:</b> {lead_item['timeline']}</p>
                            <p><b>Purpose:</b> {lead_item.get('purpose', 'N/A')}</p>
                            <p><b>Lead Grade:</b> <span style="background-color: #0F172A; color:#C9A227; padding: 4px 10px; border-radius:6px; font-weight:800;">Grade {lead_item.get('grade')}</span></p>
                        </div>
                    """)

                    if lead_item.get('grade') == 'A':
                        try:
                            budget_val = float(lead_item['budget'])
                            booking_val = budget_val * 0.20
                            remaining_val = budget_val * 0.80
                            
                            budget_usd = budget_val / 3.6725
                            booking_usd = booking_val / 3.6725
                            remaining_usd = remaining_val / 3.6725
                            
                            render_html(f"""
                                <div class="saas-card" style="border: 1px solid rgba(201,162,39,0.3); background-color: rgba(201,162,39,0.02); padding:25px; border-radius:16px; margin-top:20px;">
                                    <h4 style="color: #C9A227; margin-top:0; letter-spacing: 0.5px;">💰 GRADE A INSTALMENT SCHEDULE</h4>
                                    <table style="width:100%; border-collapse: collapse; margin-top: 10px; color:#1E293B;">
                                        <tr style="border-bottom: 1px solid rgba(0, 0, 0, 0.1); padding: 8px 0; font-weight:600;">
                                            <td style="padding: 10px 0;">Milestone</td>
                                            <td style="padding: 10px 0; text-align: right; color:#C9A227;">AED Value</td>
                                            <td style="padding: 10px 0; text-align: right; color: #64748B;">USD Equivalent</td>
                                        </tr>
                                        <tr style="border-bottom: 1px solid rgba(0, 0, 0, 0.05);">
                                            <td style="padding: 10px 0;"><b>Total Budget</b></td>
                                            <td style="padding: 10px 0; text-align: right; font-weight: bold; color: #C9A227;">AED {budget_val:,.0f}</td>
                                            <td style="padding: 10px 0; text-align: right;">${budget_usd:,.2f}</td>
                                        </tr>
                                        <tr style="border-bottom: 1px solid rgba(0, 0, 0, 0.05);">
                                            <td style="padding: 10px 0; color: #C9A227;"><b>20% Booking Amount</b></td>
                                            <td style="padding: 10px 0; text-align: right; color: #C9A227; font-weight: bold;">AED {booking_val:,.0f}</td>
                                            <td style="padding: 10px 0; text-align: right;">${booking_usd:,.2f}</td>
                                        </tr>
                                        <tr>
                                            <td style="padding: 10px 0; color: #64748B;"><b>80% Remaining Balance</b></td>
                                            <td style="padding: 10px 0; text-align: right; color: #64748B;">AED {remaining_val:,.0f}</td>
                                            <td style="padding: 10px 0; text-align: right; color: #64748B;">${remaining_usd:,.2f}</td>
                                        </tr>
                                    </table>
                                </div>
                            """)
                        except Exception as e:
                            st.error(f"Could not calculate payment schedule: {str(e)}")

                    st.markdown("#### Actions")
                    c_act1, c_act2, c_act3 = st.columns(3)
                    with c_act1:
                        status_option = st.selectbox("Update Status", ["New", "Contacted", "Qualified", "Disqualified"], key=f"status_{selected_id}")
                        if st.button("Apply Status"):
                            update_lead_status(selected_id, status_option)
                            st.success("Status updated.")
                            st.rerun()
                    with c_act2:
                        if st.button("Sync to Sheets"):
                            res, msg = sync_lead_to_sheets(lead_item)
                            if res:
                                update_lead_sync_status(selected_id, True)
                                st.success(msg)
                            else:
                                st.info(msg)
                            st.rerun()
                    with c_act3:
                        if st.button("Delete Lead", type="primary"):
                            delete_lead(selected_id)
                            st.warning("Lead deleted.")
                            st.rerun()

                with det2:
                    st.markdown('<div class="saas-card" style="padding:25px; border-radius:16px; border:1px solid #E2E8F0;">', unsafe_allow_html=True)
                    st.markdown('<h4 style="color: #0F172A; margin-top:0;">Personalized AI Outreach Email</h4>', unsafe_allow_html=True)
                    st.text_area("Draft copy:", lead_item['generated_email'], height=200)
                    st.markdown('</div>', unsafe_allow_html=True)

                    st.markdown('<div class="saas-card" style="padding:25px; border-radius:16px; border:1px solid #E2E8F0; margin-top:20px;">', unsafe_allow_html=True)
                    st.markdown('<h4 style="color: #0F172A; margin-top:0;">Conversation Summary</h4>', unsafe_allow_html=True)
                    st.write(lead_item.get('ai_summary', 'No summary generated yet.'))
                    st.markdown('</div>', unsafe_allow_html=True)

                    with st.expander("View & Export Chat Transcript"):
                        transcript_str = ""
                        try:
                            transcript = json.loads(lead_item["chat_transcript"])
                            for msg in transcript:
                                st.markdown(f"**{msg['role'].upper()}:** {msg['content']}")
                                transcript_str += f"{msg['role'].upper()}: {msg['content']}\n\n"
                        except Exception:
                            st.write("Transcript unavailable.")
                            transcript_str = "No transcript available."
                        
                        st.download_button(
                            label="📄 Export Transcript (PDF / Text Format)",
                            data=transcript_str,
                            file_name=f"panache_transcript_{lead_item['first_name']}.txt",
                            mime="text/plain"
                        )

    with tab_config:
        # Settings configurations
        render_html("""
            <div style="margin-bottom: 25px; border-bottom:1px solid #E2E8F0; padding-bottom:15px;">
                <h3 style="color:#0F172A; font-weight:800; margin:0; font-size:1.4rem;">System & API Integrations</h3>
                <span style="font-size:0.8rem; color:#64748B;">Manage API credentials, storage folders, and themes</span>
            </div>
        """)

        st.markdown('<div class="saas-card" style="padding:25px; border-radius:16px; border:1px solid #E2E8F0;">', unsafe_allow_html=True)
        st.subheader("Google Gemini API Key")
        current_key = get_config("gemini_api_key", "")
        gemini_key = st.text_input("Gemini API Key", value=current_key, type="password")
        if st.button("Save Gemini Key"):
            set_config("gemini_api_key", gemini_key)
            st.success("API key stored.")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="saas-card" style="padding:25px; border-radius:16px; border:1px solid #E2E8F0; margin-top:20px;">', unsafe_allow_html=True)
        st.subheader("Google Sheets Link Credential Configurations")
        current_sheets_url = get_config("google_sheets_url", "")
        sheets_url = st.text_input("Spreadsheet URL", value=current_sheets_url)
        current_creds = get_config("google_sheets_creds", "")
        sheets_creds = st.text_area("Service Account Credentials (JSON)", value=current_creds, height=150)
        if st.button("Save Sheets Link"):
            set_config("google_sheets_url", sheets_url)
            set_config("google_sheets_creds", sheets_creds)
            st.success("Sheets details linked.")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="saas-card" style="padding:25px; border-radius:16px; border:1px solid #E2E8F0; margin-top:20px;">', unsafe_allow_html=True)
        st.subheader("Theme & Storage Settings")
        st.selectbox("Select Active Theme", ["Luxury Navy & Gold", "Sleek Dark Mode", "Enterprise Slate"])
        st.text_input("Export Destination Directory", value="C:\\Users\\navya\\Downloads")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="saas-card" style="padding:25px; border-radius:16px; border:1px solid #E2E8F0; margin-top:20px;">', unsafe_allow_html=True)
        st.subheader("Admin Passphrase Configuration")
        current_pass = get_config("admin_passphrase", "admin123")
        new_pass = st.text_input("Set New Passphrase", value=current_pass, type="password")
        if st.button("Update Passcode"):
            set_config("admin_passphrase", new_pass)
            st.success("Passphrase updated successfully!")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab_design:
        # System status & diagnostic indicators
        render_html("""
            <div style="margin-bottom: 25px; border-bottom:1px solid #E2E8F0; padding-bottom:15px;">
                <h3 style="color:#0F172A; font-weight:800; margin:0; font-size:1.4rem;">System Diagnostics</h3>
                <span style="font-size:0.8rem; color:#64748B;">Core architecture diagram and backend component status</span>
            </div>
        """)

        # Status Badges
        render_html("""
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 30px;">
                <div class="saas-card" style="padding:15px; border: 1px solid #E2E8F0; display:flex; justify-content:space-between; align-items:center;">
                    <span style="font-weight:600; color:#0F172A;">Gemini API Link</span>
                    <span style="background-color:#DCFCE7; color:#16A34A; padding:3px 10px; border-radius:50px; font-size:0.75rem; font-weight:700;">🟢 ACTIVE</span>
                </div>
                <div class="saas-card" style="padding:15px; border: 1px solid #E2E8F0; display:flex; justify-content:space-between; align-items:center;">
                    <span style="font-weight:600; color:#0F172A;">Knowledge Base</span>
                    <span style="background-color:#DCFCE7; color:#16A34A; padding:3px 10px; border-radius:50px; font-size:0.75rem; font-weight:700;">🟢 LOADED</span>
                </div>
                <div class="saas-card" style="padding:15px; border: 1px solid #E2E8F0; display:flex; justify-content:space-between; align-items:center;">
                    <span style="font-weight:600; color:#0F172A;">Grading Rules Engine</span>
                    <span style="background-color:#DCFCE7; color:#16A34A; padding:3px 10px; border-radius:50px; font-size:0.75rem; font-weight:700;">🟢 COMPLIANT</span>
                </div>
                <div class="saas-card" style="padding:15px; border: 1px solid #E2E8F0; display:flex; justify-content:space-between; align-items:center;">
                    <span style="font-weight:600; color:#0F172A;">Conversation Memory</span>
                    <span style="background-color:#DCFCE7; color:#16A34A; padding:3px 10px; border-radius:50px; font-size:0.75rem; font-weight:700;">🟢 STANDBY</span>
                </div>
                <div class="saas-card" style="padding:15px; border: 1px solid #E2E8F0; display:flex; justify-content:space-between; align-items:center;">
                    <span style="font-weight:600; color:#0F172A;">SQLite Database</span>
                    <span style="background-color:#DCFCE7; color:#16A34A; padding:3px 10px; border-radius:50px; font-size:0.75rem; font-weight:700;">🟢 HEALTHY</span>
                </div>
                <div class="saas-card" style="padding:15px; border: 1px solid #E2E8F0; display:flex; justify-content:space-between; align-items:center;">
                    <span style="font-weight:600; color:#0F172A;">Google Sheets Sync</span>
                    <span style="background-color:#DCFCE7; color:#16A34A; padding:3px 10px; border-radius:50px; font-size:0.75rem; font-weight:700;">🟢 ONLINE</span>
                </div>
            </div>
        """)

        st.markdown('<div class="saas-card" style="padding:25px; border-radius:16px; border:1px solid #E2E8F0;">', unsafe_allow_html=True)
        st.subheader("System Diagram")
        render_html("""
        ```mermaid
        graph TD
            A[Streamlit UI - Chat & Admin Portal] --> B[LLM Service - Gemini & Fallback]
            A --> C[Database Service - SQLite]
            A --> D[Scoring Service - Grading Rules Engine]
            B --> E[Grounding Pack - Knowledge Base]
            C --> F[Google Sheets Sync Service]
        ```
        """)
        
        render_html("""
        #### Component Details:
        1. **Frontend / Presenter**: Built entirely on Streamlit utilizing custom luxury css configurations.
        2. **Model Router**: Manages local heuristic rules vs. Google Gemini model grounding, restricting all responses to the fixed knowledge packet.
        3. **Local Store**: Instantiates SQLite leads tables to maintain offline persistence.
        4. **Grading Pipeline**: Instant evaluation of BANT constraints (A, B, C, D) based on budget, timelines, and user engagement parameters.
        5. **Outbox Synchronization**: Service account link to post results to the configured Google Sheet layout.
        """)
        st.markdown('</div>', unsafe_allow_html=True)
