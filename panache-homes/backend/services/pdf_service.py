import os
import json
from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether

def clean_budget_numeric(budget_str):
    # Parse numbers out of the budget string
    import re
    cleaned = re.sub(r'[^\d\.]', '', str(budget_str))
    if not cleaned:
        return 0
    try:
        val = float(cleaned)
        # If it's a small decimal/int, check if it meant Millions (e.g. 1.2 or 1.5)
        if val < 100:
            val = val * 1000000
        return int(val)
    except Exception:
        return 0

def generate_lead_pdf(lead_data):
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=54,
        leftMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    # Custom Palette
    c_primary = colors.HexColor("#0F172A") # Slate 900
    c_secondary = colors.HexColor("#334155") # Slate 700
    c_accent = colors.HexColor("#B45309") # Amber 700
    c_light_bg = colors.HexColor("#F8FAFC") # Slate 50
    c_border = colors.HexColor("#E2E8F0") # Slate 200
    
    # Custom Paragraph Styles
    style_h1 = ParagraphStyle(
        'HeaderTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=c_primary,
        spaceAfter=6
    )
    style_h2 = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=c_accent,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )
    style_body = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=c_secondary
    )
    style_body_bold = ParagraphStyle(
        'BodyTextBoldCustom',
        parent=style_body,
        fontName='Helvetica-Bold'
    )
    style_transcript_role = ParagraphStyle(
        'TranscriptRole',
        parent=style_body,
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=c_primary
    )
    style_transcript_text = ParagraphStyle(
        'TranscriptText',
        parent=style_body,
        fontSize=9,
        leading=13,
        textColor=c_secondary
    )

    story = []
    
    # --- Header ---
    story.append(Paragraph("PANACHE HOMES", ParagraphStyle('PH', parent=style_h1, fontSize=28, leading=32, textColor=c_accent)))
    story.append(Paragraph("Dubai Property Consultation Report", ParagraphStyle('Sub', parent=style_body, fontName='Helvetica-Bold', fontSize=12, leading=16, textColor=c_secondary)))
    story.append(Spacer(1, 15))
    
    # --- Lead Metadata Table ---
    created_at = lead_data.get("created_at")
    if not created_at:
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
    meta_data = [
        [Paragraph("<b>Date & Time:</b>", style_body), Paragraph(str(created_at), style_body),
         Paragraph("<b>Lead Grade:</b>", style_body), Paragraph(f"Grade {lead_data.get('grade', 'C')}", style_body_bold)],
        [Paragraph("<b>Lead Name:</b>", style_body), Paragraph(f"{lead_data.get('first_name', '')} {lead_data.get('last_name', '')}".strip(), style_body),
         Paragraph("<b>Budget:</b>", style_body), Paragraph(f"{lead_data.get('budget')} AED", style_body)],
        [Paragraph("<b>Email:</b>", style_body), Paragraph(str(lead_data.get('email', 'Unconfirmed')), style_body),
         Paragraph("<b>Payment Method:</b>", style_body), Paragraph(str(lead_data.get('payment_method')), style_body)],
        [Paragraph("<b>Country:</b>", style_body), Paragraph(str(lead_data.get('country')), style_body),
         Paragraph("<b>Purchase Timeline:</b>", style_body), Paragraph(str(lead_data.get('timeline')), style_body)],
        [Paragraph("<b>Purpose:</b>", style_body), Paragraph(str(lead_data.get('purpose')), style_body),
         Paragraph("", style_body), Paragraph("", style_body)]
    ]
    
    t_meta = Table(meta_data, colWidths=[1.2*inch, 2.2*inch, 1.2*inch, 2.2*inch])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_light_bg),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 15))
    
    # --- AI Summary ---
    summary_text = lead_data.get("ai_summary") or lead_data.get("notes") or "No consultation summary available."
    story.append(Paragraph("Conversation Summary", style_h2))
    story.append(Paragraph(summary_text, style_body))
    story.append(Spacer(1, 15))
    
    # --- Investment Recommendation ---
    story.append(Paragraph("Investment Recommendation", style_h2))
    
    # Parse budget numeric for recommendation logic
    raw_budget = lead_data.get("budget", "")
    budget_val = clean_budget_numeric(raw_budget)
    
    recomms = []
    # 1. Golden Visa eligibility
    if budget_val >= 2000000:
        recomms.append("<b>Golden Visa Eligibility:</b> Qualified. Your budget meets the AED 2 Million threshold for the 10-Year UAE Golden Visa.")
    else:
        recomms.append("<b>Golden Visa Eligibility:</b> Not Qualified. Golden Visa requires a minimum property value of AED 2 Million. If you increase your budget, we can unlock this for you.")
        
    # 2. Budget analysis
    if budget_val >= 5000000:
        recomms.append("<b>Budget Analysis:</b> Luxury tier. High flexibility for premium villas and prime penthouse selections in beachside locations.")
    elif budget_val >= 2000000:
        recomms.append("<b>Budget Analysis:</b> Premium tier. Suitable for 2-3 bedroom sea-view apartments or custom townhouse options.")
    else:
        recomms.append("<b>Budget Analysis:</b> Entry investor tier. Well-suited for high-yielding studios, 1-bed apartments, and strategic co-living projects.")
        
    # 3. Suggested payment plan
    payment_method = str(lead_data.get("payment_method", "")).lower()
    if "mortgage" in payment_method:
        recomms.append("<b>Suggested Payment Plan:</b> Mortgage. Local banks require a minimum 20% down payment for international buyers. Remaining 80% can be financed up to 25 years.")
    else:
        recomms.append("<b>Suggested Payment Plan:</b> Standard developer milestone plan (typically 10%–20% booking down payment, instalments during construction, and final payment on handover).")
        
    # 4. Recommended communities
    if budget_val >= 5000000:
        recomms.append("<b>Recommended Communities:</b> Palm Jumeirah Signature Villas, Downtown Dubai Penthouses, or Dubai Hills Gated Estates.")
    elif budget_val >= 2000000:
        recomms.append("<b>Recommended Communities:</b> Dubai Marina Waterfront Residences, Downtown Dubai Luxury Suites, or Dubai Hills Estate townhouses.")
    else:
        recomms.append("<b>Recommended Communities:</b> Jumeirah Village Circle (JVC) apartments, Business Bay canal-view studios, or Arjan high-yield investments.")
        
    # 5. Rental yield guidance
    recomms.append("<b>Rental Yield Guidance:</b> Target standard yields of 6%–8% net annual ROI. We recommend choosing properties close to metro stations or beaches for maximum capital growth and occupancy rates.")
    
    for r in recomms:
        story.append(Paragraph(f"• {r}", ParagraphStyle('RecText', parent=style_body, spaceAfter=4, leftIndent=12)))
        
    story.append(Spacer(1, 15))
    
    # --- Grade Breakdown (Grade A special payment schedule) ---
    if str(lead_data.get("grade", "")).strip().upper() == "A":
        story.append(Paragraph("Grade A Exclusive 20/80 Payment Schedule", style_h2))
        usd_budget = budget_val / 3.6725
        dp_aed = budget_val * 0.20
        dp_usd = usd_budget * 0.20
        inst_aed = budget_val * 0.80
        inst_usd = usd_budget * 0.80
        
        breakdown_data = [
            [Paragraph("<b>Milestone</b>", style_body_bold), Paragraph("<b>AED Value</b>", style_body_bold), Paragraph("<b>USD Equivalent (Peg: 3.6725)</b>", style_body_bold)],
            [Paragraph("Total Budget", style_body), Paragraph(f"{budget_val:,.2f} AED", style_body), Paragraph(f"${usd_budget:,.2f} USD", style_body)],
            [Paragraph("20% Down Payment", style_body), Paragraph(f"{dp_aed:,.2f} AED", style_body), Paragraph(f"${dp_usd:,.2f} USD", style_body)],
            [Paragraph("80% Construction & Handover", style_body), Paragraph(f"{inst_aed:,.2f} AED", style_body), Paragraph(f"${inst_usd:,.2f} USD", style_body)]
        ]
        t_breakdown = Table(breakdown_data, colWidths=[2.2*inch, 2.2*inch, 2.4*inch])
        t_breakdown.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), c_light_bg),
            ('BOX', (0,0), (-1,-1), 1, c_border),
            ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('ALIGN', (1,0), (-1,-1), 'RIGHT'),
        ]))
        story.append(t_breakdown)
        story.append(Spacer(1, 15))
        
    story.append(PageBreak())
    
    # --- Conversation Transcript ---
    story.append(Paragraph("Conversation Transcript", style_h2))
    
    transcript = []
    chat_transcript_str = lead_data.get("chat_transcript")
    if chat_transcript_str:
        try:
            if isinstance(chat_transcript_str, str):
                transcript = json.loads(chat_transcript_str)
            elif isinstance(chat_transcript_str, list):
                transcript = chat_transcript_str
        except Exception:
            pass
            
    if transcript:
        for idx, msg in enumerate(transcript):
            role = "Client" if msg.get("role") == "user" else "Panache AI Assistant"
            content = msg.get("content", "")
            timestamp = msg.get("timestamp", "")
            role_label = f"<b>{role}</b>"
            if timestamp:
                role_label += f" <font color='#64748B'>• {timestamp}</font>"
            
            p_role = Paragraph(role_label, style_transcript_role)
            p_text = Paragraph(content, style_transcript_text)
            
            t_msg = Table([[p_role], [p_text]], colWidths=[6.8*inch])
            bg_color = c_light_bg if role == "Client" else colors.white
            t_msg.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), bg_color),
                ('TOPPADDING', (0,0), (-1,-1), 4),
                ('BOTTOMPADDING', (0,0), (-1,-1), 4),
                ('LEFTPADDING', (0,0), (-1,-1), 8),
                ('RIGHTPADDING', (0,0), (-1,-1), 8),
                ('LINEBELOW', (0,-1), (-1,-1), 0.5, c_border),
            ]))
            story.append(KeepTogether([t_msg, Spacer(1, 4)]))
    else:
        story.append(Paragraph("No conversation history found.", style_body))
        
    # Build Page Layout Callbacks for footers
    def add_page_decorations(canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(c_border)
        canvas.setLineWidth(0.5)
        # Header line
        canvas.line(54, 750, 558, 750)
        # Footer line
        canvas.line(54, 60, 558, 60)
        # Footer text
        canvas.setFont('Helvetica', 8)
        canvas.setFillColor(c_secondary)
        canvas.drawString(54, 45, "Panache Homes | AI Property Advisor")
        canvas.drawRightString(558, 45, f"Page {doc.page} | Generated automatically")
        canvas.restoreState()
        
    doc.build(story, onFirstPage=add_page_decorations, onLaterPages=add_page_decorations)
    buffer.seek(0)
    return buffer
