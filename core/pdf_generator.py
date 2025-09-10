from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from config.settings import PDF_OUTPUT_DIR, DEFAULT_SENDER
import os

def build_invoice_pdf(invoice_id, customer, items, date_str,  tax_rate=0.0, discount=0.0, notes=""):
    os.makedirs(PDF_OUTPUT_DIR, exist_ok=True)
    filename = PDF_OUTPUT_DIR / f"{invoice_id}.pdf"

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name='InfoBlock',
        parent=styles['Normal'],
        leading=14,
        fontSize=10,
        spaceAfter=4
    ))
    story = []

    # === Title ===
    story.append(Paragraph("<b>INVOICE</b>", styles['Title']))
    story.append(Spacer(1, 12))

    # === Sender & Customer Info ===
    sender_lines = [
        DEFAULT_SENDER.get("name"),
        DEFAULT_SENDER.get("email"),
        DEFAULT_SENDER.get("phone"),
        DEFAULT_SENDER.get("address")
    ]
    sender_lines = [line for line in sender_lines if line]

    customer_lines = [
        customer.get("name"),
        customer.get("email"),
        customer.get("phone"),
        customer.get("address")
    ]
    customer_lines = [line for line in customer_lines if line]

    meta_table = Table([
        [
            Paragraph("<b>From</b>", styles['Heading4']),
            Paragraph("<b>To</b>", styles['Heading4']),
            Paragraph("<b>Invoice Info</b>", styles['Heading4'])
        ],
        [
            Paragraph("<br/>".join(sender_lines), styles['InfoBlock']),
            Paragraph("<br/>".join(customer_lines), styles['InfoBlock']),
            Paragraph(
                f"<b>Date:</b> {date_str}<br/>"
                f"<b>No:</b> {invoice_id}<br/>",
                styles['InfoBlock']
            )
        ]
    ], colWidths=[200, 200, 140])
    meta_table.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.25, colors.grey),
        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.lightgrey),
        ('BACKGROUND', (0,0), (-1,0), colors.whitesmoke),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 12))

    # === Items Table ===
    data = [["Item", "Rate", "Tax %", "Tax Amt", "Qty", "Total"]]
    subtotal = 0.0
    total_tax = 0.0

    for item in items:
        rate = item["rate"]
        qty = item["quantity"]
        tax = item["tax"]

        base = rate * qty
        tax_amt = base * (tax / 100)
        total = base + tax_amt

        
        subtotal += base
        total_tax += tax_amt

        data.append([
            item["name"],
            f"{rate:.2f}",
            f"{tax:.2f}%",
            f"{tax_amt:.2f}",
            str(qty),
            f"{total:.2f}"
        ])

    item_table = Table(data, colWidths=[180, 70, 70, 70, 70, 80])
    item_table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.25, colors.lightgrey),
        ('BACKGROUND', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (1,1), (-1,-1), 'RIGHT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(item_table)
    story.append(Spacer(1, 12))

    # === Summary Table ===
    # tax_amt = round(subtotal * (tax_rate / 100.0), 2)
    # total = round(subtotal + tax_amt, 2)
    total = subtotal + total_tax

    summary_data = [
        ["Subtotal", f"{subtotal:.2f}"],
        ["Tax Amount", f"{total_tax:.2f}"],
        ["Total", f"{total:.2f}"]
    ]
    summary_table = Table(summary_data, colWidths=[460, 80])
    summary_table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.25, colors.lightgrey),
        ('BACKGROUND', (0,-1), (-1,-1), colors.beige),
        ('ALIGN', (1,0), (1,-1), 'RIGHT'),
    ]))
    story.append(summary_table)

    # === Notes ===
    if notes.strip():
        story.append(Spacer(1, 12))
        story.append(Paragraph(f"<b>Notes</b><br/>{notes}", styles['Normal']))

    # === Build PDF ===
    doc = SimpleDocTemplate(str(filename), pagesize=A4, rightMargin=24, leftMargin=24, topMargin=24, bottomMargin=24)
    doc.build(story)
