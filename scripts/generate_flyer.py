from pathlib import Path

from PIL import Image, ImageEnhance
from reportlab.graphics import renderPDF
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing
from reportlab.lib.colors import Color, HexColor
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "pdf" / "nexia-flyer-prospection-a4.pdf"
HERO = ROOT / "public" / "images" / "hero-stone-courtyard.jpg"

INK = HexColor("#18221d")
INK_SOFT = HexColor("#334138")
CREAM = HexColor("#f4eee2")
PAPER = HexColor("#fbf8f1")
EMBER = HexColor("#d68a4a")
MUTED = HexColor("#6f746f")


def register_fonts():
    pdfmetrics.registerFont(TTFont("Georgia", "/System/Library/Fonts/Supplemental/Georgia.ttf"))
    pdfmetrics.registerFont(TTFont("Georgia-Bold", "/System/Library/Fonts/Supplemental/Georgia Bold.ttf"))
    pdfmetrics.registerFont(TTFont("Georgia-Italic", "/System/Library/Fonts/Supplemental/Georgia Italic.ttf"))


def draw_cover(c, image_path, x, y, width, height, focus_x=0.5, focus_y=0.5, brightness=1.0):
    source = Image.open(image_path).convert("RGB")
    if brightness != 1.0:
        source = ImageEnhance.Brightness(source).enhance(brightness)
    image = ImageReader(source)
    image_width, image_height = image.getSize()
    scale = max(width / image_width, height / image_height)
    drawn_width = image_width * scale
    drawn_height = image_height * scale
    image_x = x - (drawn_width - width) * focus_x
    image_y = y - (drawn_height - height) * focus_y

    c.saveState()
    clip = c.beginPath()
    clip.rect(x, y, width, height)
    c.clipPath(clip, stroke=0, fill=0)
    c.drawImage(image, image_x, image_y, drawn_width, drawn_height, mask="auto")
    c.restoreState()


def paragraph(c, text, x, y_top, width, style):
    item = Paragraph(text, style)
    _, height = item.wrap(width, 1000)
    item.drawOn(c, x, y_top - height)
    return height


def draw_qr(c, value, x, y, size):
    widget = QrCodeWidget(value)
    bounds = widget.getBounds()
    width = bounds[2] - bounds[0]
    height = bounds[3] - bounds[1]
    drawing = Drawing(size, size, transform=[size / width, 0, 0, size / height, 0, 0])
    drawing.add(widget)
    renderPDF.draw(drawing, c, x, y)


def build():
    register_fonts()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    page_width, page_height = A4
    c = canvas.Canvas(str(OUTPUT), pagesize=A4, pageCompression=1)
    c.setTitle("NEXIA - Flyer prospection")
    c.setAuthor("NEXIA - Norman Hubert et Patrick Martinez")
    c.setSubject("Expériences immersives en intelligence artificielle")

    # Background and photographic opening.
    c.setFillColor(CREAM)
    c.rect(0, 0, page_width, page_height, fill=1, stroke=0)
    hero_height = 350
    hero_y = page_height - hero_height
    draw_cover(c, HERO, 0, hero_y, page_width, hero_height, focus_x=0.5, focus_y=0.52, brightness=0.55)

    margin = 42
    c.setFillColor(PAPER)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(margin, page_height - 42, "NE")
    ne_width = c.stringWidth("NE", "Helvetica-Bold", 13)
    c.setFillColor(EMBER)
    c.drawString(margin + ne_width + 2.1, page_height - 42, "X")
    x_width = c.stringWidth("X", "Helvetica-Bold", 13)
    c.setFillColor(PAPER)
    c.drawString(margin + ne_width + x_width + 4.2, page_height - 42, "IA")

    c.setFont("Helvetica-Bold", 6.5)
    c.drawRightString(page_width - margin, page_height - 42, "DIRIGEANTS  -  CODIR  -  ÉQUIPES")

    c.setFillColor(PAPER)
    c.setFont("Helvetica-Bold", 7.2)
    c.drawString(margin, page_height - 96, "EXPÉRIENCES D’INTELLIGENCE ARTIFICIELLE")

    c.setFont("Georgia", 40)
    c.drawString(margin, page_height - 146, "Faire vivre l’IA.")
    c.setFillColor(HexColor("#edb77f"))
    c.setFont("Georgia-Italic", 45)
    c.drawString(margin, page_height - 193, "Vraiment.")

    hero_body = ParagraphStyle(
        "hero-body",
        fontName="Helvetica",
        fontSize=10.8,
        leading=16,
        textColor=PAPER,
        alignment=TA_LEFT,
    )
    paragraph(
        c,
        "Quelques heures, une journée ou deux jours hors du quotidien pour "
        "<b>comprendre, expérimenter et construire</b> votre propre manière de travailler avec l’intelligence artificielle.",
        margin,
        page_height - 226,
        430,
        hero_body,
    )

    # Formats section.
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 7)
    c.drawString(margin, 458, "QUATRE FORMATS, UN MÊME OBJECTIF : VOUS FAIRE AVANCER")

    cards = [
        ("01", "Une demi-journée", "Ouvrir le sujet et mettre une équipe en mouvement."),
        ("02", "Une journée", "Tester, prendre du recul et construire sur vos cas réels."),
        ("03", "Deux jours", "Vivre une immersion intensive dans un lieu à part."),
        ("04", "Sur scène", "Faire de l’IA une conférence vivante et mémorable."),
    ]
    card_gap = 12
    card_width = (page_width - 2 * margin - card_gap) / 2
    card_height = 68
    card_style = ParagraphStyle("card", fontName="Helvetica", fontSize=7.7, leading=11.2, textColor=MUTED)

    for index, (number, title, body) in enumerate(cards):
        column = index % 2
        row = index // 2
        x = margin + column * (card_width + card_gap)
        y = 374 - row * (card_height + 11)
        c.setFillColor(PAPER if index != 2 else HexColor("#d9b07b"))
        c.roundRect(x, y, card_width, card_height, 3, fill=1, stroke=0)
        c.setFillColor(EMBER if index != 2 else INK)
        c.setFont("Helvetica-Bold", 6.4)
        c.drawString(x + 14, y + card_height - 17, number)
        c.setFillColor(INK)
        c.setFont("Georgia-Bold", 13)
        c.drawString(x + 38, y + card_height - 19, title)
        paragraph(c, body, x + 38, y + card_height - 30, card_width - 52, card_style)

    # Concrete outcomes band.
    band_y = 136
    band_height = 105
    c.setFillColor(INK_SOFT)
    c.rect(0, band_y, page_width, band_height, fill=1, stroke=0)
    c.setFillColor(HexColor("#edb77f"))
    c.setFont("Helvetica-Bold", 6.6)
    c.drawString(margin, band_y + 78, "CE QUI RESTE APRÈS L’EXPÉRIENCE")
    c.setFillColor(PAPER)
    c.setFont("Georgia", 22)
    c.drawString(margin, band_y + 44, "Comprendre. Tester. Décider.")
    outcome_style = ParagraphStyle("outcome", fontName="Helvetica", fontSize=8.2, leading=12.5, textColor=Color(1, 1, 1, alpha=0.72))
    paragraph(
        c,
        "Des repères partagés, des usages éprouvés et des prochaines étapes claires - sans céder à l’effet de mode.",
        332,
        band_y + 74,
        220,
        outcome_style,
    )

    # Contact area and QR code.
    c.setFillColor(INK)
    c.setFont("Georgia", 18)
    c.drawString(margin, 104, "Parlons de ce que vous voulez faire bouger.")
    c.setFont("Helvetica", 7.5)
    c.setFillColor(MUTED)
    c.drawString(margin, 82, "Norman Hubert + Patrick Martinez  -  Une proposition construite pour votre contexte")
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 8.2)
    c.drawString(margin, 55, "NEXIA-EXPERIENCE.NETLIFY.APP")
    c.setFillColor(EMBER)
    c.circle(margin + 218, 57, 2.2, fill=1, stroke=0)
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 6.8)
    c.drawString(margin + 229, 55, "Échangeons sur votre prochain format")

    qr_size = 72
    qr_x = page_width - margin - qr_size
    qr_y = 39
    c.setFillColor(PAPER)
    c.roundRect(qr_x - 6, qr_y - 6, qr_size + 12, qr_size + 12, 4, fill=1, stroke=0)
    draw_qr(c, "https://nexia-experience.netlify.app", qr_x, qr_y, qr_size)

    c.showPage()
    c.save()
    print(OUTPUT)


if __name__ == "__main__":
    build()
