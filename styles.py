import streamlit as st

def apply_custom_css():
    """
    Applies a premium enterprise-grade AI SaaS theme (Inter font, Navy & Gold accents, Slate backgrounds).
    Hides all default Streamlit branding, sidebar, and headers.
    """
    st.markdown("""
        <style>
        /* Import Inter Font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        
        /* Disable default Streamlit headers, sidebars, and footers */
        [data-testid="stSidebar"] {
            display: none !important;
        }
        [data-testid="stHeader"] {
            display: none !important;
        }
        footer {
            visibility: hidden !important;
            height: 0px !important;
            padding: 0px !important;
        }
        .stDeployButton {
            display: none !important;
        }
        #MainMenu {
            visibility: hidden !important;
        }
        
        /* Base styles */
        html {
            scroll-behavior: smooth;
        }
        body, [class*="css"], .stApp {
            font-family: 'Inter', sans-serif;
            background-color: #F8FAFC !important;
            color: #1E293B !important;
        }
        
        /* Universal Streamlit Button styling */
        div.stButton > button {
            background-color: #0F172A !important;
            color: #ffffff !important;
            border: 1px solid #0F172A !important;
            border-radius: 8px !important;
            padding: 10px 24px !important;
            font-weight: 600 !important;
            font-family: 'Inter', sans-serif !important;
            font-size: 0.92rem !important;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05) !important;
        }
        
        div.stButton > button:hover {
            background-color: #C9A227 !important;
            border-color: #C9A227 !important;
            color: #0F172A !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 12px rgba(201, 162, 39, 0.2) !important;
        }
        
        div.stButton > button[kind="primary"] {
            background-color: #C9A227 !important;
            border-color: #C9A227 !important;
            color: #0F172A !important;
        }
        
        div.stButton > button[kind="primary"]:hover {
            background-color: #aa8412 !important;
            border-color: #aa8412 !important;
            color: #ffffff !important;
        }
        
        /* Form inputs & selections styling */
        div[data-testid="stTextInput"] input, div[data-testid="stTextArea"] textarea, div[data-testid="stSelectbox"] select {
            border-radius: 8px !important;
            border: 1px solid #E2E8F0 !important;
            font-family: 'Inter', sans-serif !important;
            font-size: 0.95rem !important;
            transition: all 0.2s ease !important;
            background-color: #ffffff !important;
            color: #1E293B !important;
        }
        
        div[data-testid="stTextInput"] input:focus, div[data-testid="stTextArea"] textarea:focus {
            border-color: #C9A227 !important;
            box-shadow: 0 0 0 2px rgba(201, 162, 39, 0.15) !important;
            outline: none !important;
        }

        /* Custom Fixed Top Navigation Bar */
        .fixed-navbar {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 70px;
            background-color: #ffffff;
            border-bottom: 1px solid #E2E8F0;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 5%;
            z-index: 999999;
        }
        
        .navbar-brand {
            display: flex;
            align-items: center;
            text-decoration: none;
        }
        
        .navbar-brand h2 {
            margin: 0;
            font-weight: 800;
            font-size: 1.3rem;
            color: #0F172A;
            letter-spacing: 1px;
        }
        
        .navbar-brand span {
            color: #C9A227;
        }
        
        .navbar-menu {
            display: flex;
            gap: 30px;
            align-items: center;
        }
        
        .navbar-link {
            text-decoration: none;
            color: #64748B;
            font-weight: 500;
            font-size: 0.95rem;
            transition: color 0.2s ease;
        }
        
        .navbar-link:hover {
            color: #0F172A;
        }
        
        .navbar-btn {
            text-decoration: none;
            color: #C9A227;
            border: 1px solid #C9A227;
            padding: 8px 18px;
            border-radius: 8px;
            font-weight: 600;
            font-size: 0.95rem;
            transition: all 0.2s ease;
            background-color: #ffffff;
        }
        
        .navbar-btn:hover {
            background-color: rgba(201, 162, 39, 0.05);
            color: #C9A227;
        }
        
        /* Offset content below navbar */
        .page-content-offset {
            margin-top: 70px !important;
        }
        
        /* Premium Luxury Hero Section */
        .saas-hero-section {
            background-image: linear-gradient(rgba(15, 23, 42, 0.82), rgba(15, 23, 42, 0.88)), url('https://images.unsplash.com/photo-1512453979798-5ea266f8880c?auto=format&fit=crop&w=1600&q=80');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            min-height: 85vh;
            display: flex;
            align-items: center;
            padding: 120px 5% 120px 5%;
            color: #ffffff;
            border-bottom: 2px solid #C9A227;
            animation: fadeIn 1.2s ease-in-out;
            position: relative;
        }
        
        .hero-logo-large {
            font-size: 1.6rem;
            font-weight: 800;
            color: #ffffff;
            letter-spacing: 2px;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .hero-logo-large span {
            color: #C9A227;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .saas-hero-title {
            font-size: 3.2rem;
            font-weight: 800;
            line-height: 1.15;
            margin-bottom: 20px;
            letter-spacing: -1px;
            color: #ffffff;
        }
        
        .saas-hero-title span {
            color: #C9A227;
        }
        
        .saas-hero-subtitle {
            font-size: 1.2rem;
            color: #E2E8F0;
            margin-bottom: 40px;
            line-height: 1.6;
            max-width: 600px;
            font-weight: 400;
        }
        
        /* Glassmorphic floating card */
        .glass-info-card {
            background: rgba(255, 255, 255, 0.06);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 24px;
            padding: 35px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
            color: #ffffff;
            max-width: 440px;
            width: 100%;
        }
        
        .glass-row {
            display: flex;
            align-items: center;
            gap: 10px;
            font-weight: 600;
            font-size: 0.95rem;
            margin-bottom: 12px;
            color: #E2E8F0;
        }
        
        .glass-row span {
            color: #C9A227;
        }
        
        /* Trust Badges Bar */
        .trust-badges-bar {
            display: flex;
            justify-content: space-around;
            align-items: center;
            padding: 25px 5%;
            background-color: #FFFFFF;
            border-bottom: 1px solid #E2E8F0;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02);
            flex-wrap: wrap;
            gap: 20px;
        }
        
        .trust-badge-item {
            font-weight: 600;
            color: #0F172A;
            font-size: 0.95rem;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .trust-badge-item span {
            color: #C9A227;
            font-size: 1.1rem;
        }
        
        /* About Section Showcase */
        .about-split-container {
            display: flex;
            gap: 5%;
            margin: 60px 5%;
            align-items: center;
            flex-wrap: wrap;
        }

        .about-img-frame {
            flex: 1;
            min-width: 300px;
            height: 480px;
            border-radius: 24px;
            background-image: url('https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?auto=format&fit=crop&w=800&q=80');
            background-size: cover;
            background-position: center;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.08);
            border: 1px solid #E2E8F0;
        }

        .about-text-content {
            flex: 1.2;
            min-width: 300px;
        }

        .about-features-mini {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-top: 30px;
        }

        .about-mini-card {
            background-color: #FFFFFF;
            border: 1px solid #E2E8F0;
            padding: 20px;
            border-radius: 16px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02);
            transition: all 0.2s ease;
        }

        .about-mini-card:hover {
            border-color: #C9A227;
            transform: translateY(-2px);
        }

        .about-mini-card h4 {
            margin: 0 0 8px 0;
            color: #0F172A;
            font-size: 1rem;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .about-mini-card p {
            margin: 0;
            font-size: 0.85rem;
            color: #64748B;
            line-height: 1.5;
        }

        .about-stats-row {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            margin: 40px 5%;
            text-align: center;
        }

        .stat-box {
            background-color: #FFFFFF;
            border: 1px solid #E2E8F0;
            padding: 30px 20px;
            border-radius: 16px;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02);
        }

        .stat-number {
            font-size: 2.2rem;
            font-weight: 800;
            color: #C9A227;
        }

        .stat-label {
            font-size: 0.9rem;
            color: #64748B;
            margin-top: 5px;
            font-weight: 500;
        }

        .timeline-flow {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin: 60px 5% 40px 5%;
            flex-wrap: wrap;
            gap: 20px;
        }

        .timeline-step {
            flex: 1;
            min-width: 150px;
            background-color: #FFFFFF;
            border: 1px solid #E2E8F0;
            padding: 25px 15px;
            border-radius: 16px;
            text-align: center;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02);
            position: relative;
        }

        .timeline-step-badge {
            position: absolute;
            top: -12px;
            left: 50%;
            transform: translateX(-50%);
            background-color: #0F172A;
            color: #C9A227;
            font-size: 0.7rem;
            font-weight: 700;
            padding: 3px 10px;
            border-radius: 50px;
            border: 1px solid #C9A227;
            text-transform: uppercase;
        }

        .timeline-arrow {
            color: #C9A227;
            font-size: 1.5rem;
            font-weight: 800;
        }
        
        /* Premium Service Showcases Grid */
        .saas-services-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 30px;
            padding: 20px 5%;
        }

        .saas-service-card {
            background-color: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .saas-service-card:hover {
            transform: translateY(-6px);
            border-color: #C9A227;
            box-shadow: 0 20px 25px -5px rgba(0,0,0,0.05);
        }

        .saas-service-img {
            height: 180px;
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            position: relative;
        }

        .saas-service-body {
            padding: 25px;
        }

        .saas-service-icon {
            position: absolute;
            bottom: -20px;
            left: 20px;
            width: 44px;
            height: 44px;
            background-color: #0F172A;
            color: #C9A227;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.25rem;
            box-shadow: 0 4px 10px rgba(0,0,0,0.15);
            border: 1px solid rgba(201, 162, 39, 0.2);
        }

        .saas-service-title {
            font-size: 1.15rem;
            font-weight: 700;
            color: #0F172A;
            margin: 10px 0 10px 0;
        }

        .saas-service-desc {
            font-size: 0.88rem;
            color: #64748B;
            line-height: 1.5;
            margin-bottom: 20px;
            height: 65px;
            overflow: hidden;
        }

        .saas-service-btn {
            display: inline-block;
            padding: 8px 16px;
            background-color: #F8FAFC;
            border: 1px solid #E2E8F0;
            border-radius: 8px;
            color: #0F172A;
            text-decoration: none;
            font-weight: 600;
            font-size: 0.85rem;
            transition: all 0.2s ease;
        }

        .saas-service-btn:hover {
            background-color: #0F172A;
            color: #C9A227;
            border-color: #0F172A;
        }

        .why-choose-banner {
            background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
            border-radius: 20px;
            padding: 40px;
            color: #ffffff;
            margin: 60px 5% 40px 5%;
            border: 1px solid rgba(201, 162, 39, 0.2);
            box-shadow: 0 10px 25px rgba(15, 23, 42, 0.15);
        }

        .why-choose-highlights {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            margin-top: 25px;
        }

        .why-choose-item {
            background-color: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.08);
            padding: 20px 15px;
            border-radius: 12px;
            text-align: center;
            font-weight: 600;
            color: #ffffff;
            font-size: 0.9rem;
        }

        .why-choose-item span {
            color: #C9A227;
            margin-right: 6px;
        }
        
        /* Why Invest Section Split */
        .why-invest-split {
            display: flex;
            gap: 5%;
            margin: 60px 5%;
            align-items: center;
            flex-wrap: wrap;
        }

        .why-invest-img {
            flex: 1;
            min-width: 300px;
            height: 480px;
            border-radius: 24px;
            background-image: url('https://images.unsplash.com/photo-1580674684081-7617fbf3d745?auto=format&fit=crop&w=800&q=80');
            background-size: cover;
            background-position: center;
            box-shadow: 0 20px 40px rgba(0,0,0,0.08);
            transition: transform 0.5s ease;
            border: 1px solid #E2E8F0;
        }

        .why-invest-img:hover {
            transform: scale(1.02);
        }

        .why-invest-content {
            flex: 1.2;
            min-width: 300px;
        }

        .why-invest-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-top: 25px;
        }

        .why-invest-card {
            background-color: #FFFFFF;
            border: 1px solid #E2E8F0;
            padding: 20px;
            border-radius: 16px;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02);
            transition: all 0.3s ease;
        }

        .why-invest-card:hover {
            border-color: #C9A227;
            transform: translateY(-2px);
        }

        .why-invest-card h4 {
            margin: 0 0 8px 0;
            color: #0F172A;
            font-size: 1rem;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .why-invest-card p {
            margin: 0;
            font-size: 0.85rem;
            color: #64748B;
            line-height: 1.5;
        }

        .investment-highlights-row {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            margin: 40px 5%;
            text-align: center;
        }

        .highlight-box {
            background-color: #FFFFFF;
            border: 1px solid #E2E8F0;
            padding: 25px 15px;
            border-radius: 16px;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02);
            transition: all 0.2s ease;
        }

        .highlight-box:hover {
            transform: translateY(-3px);
            border-color: #C9A227;
        }

        .highlight-icon {
            font-size: 1.8rem;
            margin-bottom: 10px;
        }

        .highlight-title {
            font-size: 0.95rem;
            font-weight: 700;
            color: #0F172A;
        }

        .luxury-cta-banner {
            background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
            border-radius: 20px;
            padding: 50px 30px;
            text-align: center;
            color: #ffffff;
            margin: 60px 5% 40px 5%;
            border: 1px solid rgba(201, 162, 39, 0.25);
            box-shadow: 0 15px 30px rgba(15, 23, 42, 0.2);
        }

        .luxury-cta-btn {
            display: inline-block;
            padding: 12px 35px;
            background-color: #C9A227;
            color: #0F172A;
            font-weight: 700;
            font-size: 1rem;
            border-radius: 8px;
            text-decoration: none;
            transition: all 0.2s ease;
            margin-top: 25px;
            border: 1px solid #C9A227;
        }

        .luxury-cta-btn:hover {
            background-color: #aa8412;
            border-color: #aa8412;
            transform: translateY(-2px);
            color: #0F172A !important;
        }
        
        /* Testimonial Section Grid */
        .trust-split-container {
            display: flex;
            gap: 5%;
            margin: 60px 5%;
            align-items: center;
            flex-wrap: wrap;
        }

        .trust-testimonials-column {
            flex: 1.2;
            min-width: 300px;
            display: flex;
            flex-direction: column;
            gap: 20px;
        }

        .testimonial-card {
            background-color: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 16px;
            padding: 25px;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02);
            transition: all 0.2s ease;
        }

        .testimonial-card:hover {
            transform: translateY(-2px);
            border-color: #C9A227;
        }

        .testimonial-user {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 12px;
        }

        .testimonial-avatar {
            width: 44px;
            height: 44px;
            border-radius: 50%;
            background-color: #0F172A;
            color: #C9A227;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 1rem;
            border: 1px solid rgba(201, 162, 39, 0.2);
        }

        .testimonial-stars {
            color: #C9A227;
            font-size: 0.9rem;
            margin-bottom: 8px;
        }

        .trust-img-column {
            flex: 1;
            min-width: 300px;
            height: 480px;
            border-radius: 24px;
            background-image: url('https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=800&q=80');
            background-size: cover;
            background-position: center;
            position: relative;
            box-shadow: 0 20px 40px rgba(0,0,0,0.08);
            border: 1px solid #E2E8F0;
        }

        .trust-img-floating-card {
            position: absolute;
            bottom: 30px;
            left: 30px;
            right: 30px;
            background: rgba(15, 23, 42, 0.85);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 25px;
            color: #ffffff;
            box-shadow: 0 15px 30px rgba(0,0,0,0.25);
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
        }

        .trust-badge-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 15px;
            margin: 40px 5%;
        }

        .trust-badge-card {
            background-color: #FFFFFF;
            border: 1px solid #E2E8F0;
            padding: 15px;
            border-radius: 12px;
            text-align: center;
            font-weight: 600;
            color: #0F172A;
            font-size: 0.88rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.01);
        }

        .trust-badge-card span {
            color: #C9A227;
            margin-right: 4px;
        }
        
        /* Modern Chat Layout */
        .chat-header-bar {
            background-color: #ffffff;
            border-bottom: 1px solid #E2E8F0;
            padding: 15px 5%;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 1px 2px 0 rgba(0,0,0,0.02);
        }
        
        .chat-header-left {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        
        .status-dot {
            width: 8px;
            height: 8px;
            background-color: #16A34A;
            border-radius: 50%;
            box-shadow: 0 0 8px #16A34A;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0% { transform: scale(0.9); opacity: 0.8; }
            50% { transform: scale(1.1); opacity: 1; }
            100% { transform: scale(0.9); opacity: 0.8; }
        }
        
        /* Chat bubble styles */
        .chat-bubble-container {
            display: flex;
            flex-direction: column;
            gap: 20px;
            padding: 20px 5%;
            max-height: 550px;
            overflow-y: auto;
        }
        
        .saas-chat-row {
            display: flex;
            align-items: flex-start;
            gap: 14px;
            margin-bottom: 5px;
        }
        
        .saas-chat-row.user {
            justify-content: flex-end;
        }
        
        .saas-avatar {
            width: 36px;
            height: 36px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 600;
            font-size: 1rem;
            flex-shrink: 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        
        .saas-avatar.assistant {
            background-color: #0F172A;
            color: #C9A227;
            border: 1px solid rgba(201, 162, 39, 0.2);
        }
        
        .saas-avatar.user {
            background-color: #E2E8F0;
            color: #0F172A;
        }
        
        .saas-chat-bubble {
            max-width: 65%;
            padding: 14px 20px;
            border-radius: 12px;
            font-size: 0.95rem;
            line-height: 1.55;
            box-shadow: 0 2px 5px 0 rgba(0, 0, 0, 0.02);
            position: relative;
        }
        
        .saas-chat-bubble.assistant {
            background-color: #ffffff;
            color: #1E293B;
            border: 1px solid #E2E8F0;
            border-top-left-radius: 2px;
        }
        
        .saas-chat-bubble.user {
            background-color: #0F172A;
            color: #ffffff;
            border-top-right-radius: 2px;
        }
        
        .timestamp-label {
            font-size: 0.75rem;
            color: #94A3B8;
            margin-top: 5px;
            margin-left: 50px;
        }
        
        .saas-chat-row.user + .timestamp-label {
            align-self: flex-end;
            margin-right: 50px;
            margin-left: 0;
        }

        /* Progress Bar wrapper */
        .progress-wrapper {
            background-color: #ffffff;
            border: 1px solid #E2E8F0;
            border-radius: 12px;
            padding: 15px 20px;
            margin: 20px 5%;
            box-shadow: 0 1px 3px rgba(0,0,0,0.02);
        }
        
        .progress-label-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
            font-size: 0.85rem;
            font-weight: 600;
            color: #64748B;
        }

        /* Chat input container */
        .chat-input-wrap {
            padding: 20px 5%;
            background-color: #ffffff;
            border-top: 1px solid #E2E8F0;
            display: flex;
            align-items: center;
            gap: 12px;
        }
        
        /* Premium Lead summary / breakdowns */
        .saas-lead-summary-card {
            background: #ffffff;
            border: 1px solid #E2E8F0;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 10px 15px -3px rgba(0,0,0,0.03);
            margin: 30px 5%;
        }

        .saas-payment-breakdown {
            background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
            border: 1px solid rgba(201, 162, 39, 0.25);
            border-radius: 20px;
            padding: 30px;
            color: #ffffff;
            box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.3);
            margin: 30px 5%;
        }

        /* Redesigned Premium Communities Section */
        .comm-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 25px;
            padding: 20px 5%;
        }

        @media (max-width: 992px) {
            .comm-grid {
                grid-template-columns: repeat(2, 1fr);
            }
        }

        @media (max-width: 600px) {
            .comm-grid {
                grid-template-columns: 1fr;
            }
        }

        .comm-card {
            background-color: #ffffff;
            border: 1px solid #E2E8F0;
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .comm-card:hover {
            transform: translateY(-6px);
            border-color: #C9A227;
            box-shadow: 0 15px 30px -5px rgba(0,0,0,0.05);
        }

        .comm-img {
            height: 220px;
            background-size: cover;
            background-position: center;
            transition: transform 0.5s ease;
        }

        .comm-card:hover .comm-img {
            transform: scale(1.05);
        }

        .comm-body {
            padding: 25px;
        }

        .comm-title {
            font-size: 1.25rem;
            font-weight: 700;
            color: #0F172A;
            margin: 0 0 10px 0;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .comm-title span {
            color: #C9A227;
            font-size: 0.85rem;
            background: rgba(201, 162, 39, 0.1);
            padding: 4px 10px;
            border-radius: 50px;
        }

        .comm-desc {
            font-size: 0.88rem;
            color: #64748B;
            line-height: 1.5;
            margin: 0;
        }

        /* FAQ Accordion Styling */
        .faq-container {
            max-width: 800px;
            margin: 40px auto;
            padding: 0 20px;
        }

        .faq-item {
            background-color: #ffffff;
            border: 1px solid #E2E8F0;
            border-radius: 12px;
            margin-bottom: 15px;
            overflow: hidden;
            box-shadow: 0 2px 4px rgba(0,0,0,0.01);
            transition: all 0.2s ease;
        }

        .faq-item:hover {
            border-color: #C9A227;
        }

        .faq-question {
            padding: 20px;
            font-weight: 700;
            color: #0F172A;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
            user-select: none;
        }

        .faq-answer {
            padding: 0 20px 20px 20px;
            color: #64748B;
            font-size: 0.9rem;
            line-height: 1.6;
        }

        /* Premium Footer Styling */
        .premium-footer {
            background-color: #0F172A;
            color: #ffffff;
            padding: 80px 5% 40px 5%;
            border-top: 3px solid #C9A227;
            margin-top: 80px;
        }

        .footer-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 40px;
            margin-bottom: 50px;
        }

        @media (max-width: 768px) {
            .footer-grid {
                grid-template-columns: repeat(2, 1fr);
            }
        }

        @media (max-width: 480px) {
            .footer-grid {
                grid-template-columns: 1fr;
            }
        }

        .footer-col h4 {
            color: #ffffff;
            font-size: 1.1rem;
            font-weight: 700;
            margin-top: 0;
            margin-bottom: 25px;
            position: relative;
        }

        .footer-col h4::after {
            content: '';
            position: absolute;
            bottom: -8px;
            left: 0;
            width: 30px;
            height: 2px;
            background-color: #C9A227;
        }

        .footer-logo {
            font-weight: 800;
            font-size: 1.4rem;
            letter-spacing: 1px;
            color: #ffffff;
            margin-bottom: 20px;
        }

        .footer-logo span {
            color: #C9A227;
        }

        .footer-text {
            color: #94A3B8;
            font-size: 0.88rem;
            line-height: 1.6;
            margin-bottom: 20px;
        }

        .footer-links {
            list-style: none;
            padding: 0;
            margin: 0;
        }

        .footer-links li {
            margin-bottom: 12px;
        }

        .footer-links a {
            color: #94A3B8;
            text-decoration: none;
            font-size: 0.88rem;
            transition: color 0.2s ease;
        }

        .footer-links a:hover {
            color: #C9A227;
        }

        .footer-contact-item {
            display: flex;
            align-items: flex-start;
            gap: 12px;
            color: #94A3B8;
            font-size: 0.88rem;
            margin-bottom: 15px;
            line-height: 1.5;
        }

        .footer-contact-item span {
            color: #C9A227;
            font-size: 1.1rem;
        }

        .footer-socials {
            display: flex;
            gap: 15px;
            margin-top: 20px;
        }

        .footer-social-icon {
            width: 36px;
            height: 36px;
            background-color: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.1);
            color: #ffffff;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            text-decoration: none;
            transition: all 0.2s ease;
            font-size: 1rem;
        }

        .footer-social-icon:hover {
            background-color: #C9A227;
            color: #0F172A;
            border-color: #C9A227;
            transform: translateY(-2px);
        }

        .footer-bottom {
            border-top: 1px solid rgba(255,255,255,0.1);
            padding-top: 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 20px;
        }

        .footer-copy {
            color: #64748B;
            font-size: 0.82rem;
            margin: 0;
        }

        /* Gallery Styles */
        .gallery-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 25px;
            margin-top: 30px;
        }
        .gallery-card {
            background-color: #ffffff;
            border: 1px solid #E2E8F0;
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            display: flex;
            flex-direction: column;
            height: 100%;
        }
        .gallery-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 20px -3px rgba(0,0,0,0.08);
            border-color: #C9A227;
        }
        .gallery-img {
            height: 200px;
            background-size: cover;
            background-position: center;
            transition: transform 0.3s ease;
        }
        .gallery-card:hover .gallery-img {
            transform: scale(1.05);
        }
        .gallery-body {
            padding: 20px;
            display: flex;
            flex-direction: column;
            flex-grow: 1;
        }
        .gallery-title {
            font-size: 1.1rem;
            font-weight: 800;
            color: #0F172A;
            margin: 0 0 5px 0;
        }
        .gallery-community {
            font-size: 0.8rem;
            color: #C9A227;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 12px;
        }
        .gallery-meta {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
            padding-bottom: 12px;
            border-bottom: 1px solid #F1F5F9;
        }
        .gallery-price {
            font-weight: 800;
            color: #0F172A;
            font-size: 1rem;
        }
        .gallery-roi {
            background-color: #F1F5F9;
            color: #0F172A;
            padding: 4px 8px;
            border-radius: 6px;
            font-size: 0.75rem;
            font-weight: 700;
        }
        .gallery-desc {
            font-size: 0.85rem;
            color: #64748B;
            line-height: 1.5;
            margin: 0 0 20px 0;
            flex-grow: 1;
        }
        </style>
    """, unsafe_allow_html=True)
