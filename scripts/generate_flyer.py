from io import BytesIO
from pathlib import Path

from PIL import Image, ImageEnhance
from reportlab.graphics import renderPDF
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A5
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "pdf" / "nexia-flyer-prospection-a5-recto-verso.pdf"
IMAGES = ROOT / "public" / "images"

INK = HexColor("#18221d")
FOREST = HexColor("#334138")
MOSS = HexColor("#687363")
CREAM = HexColor("#f4eee2")
PAPER = HexColor("#fbf8f1")
EMBER = HexColor("#d68a4a")
GOLD = HexColor("#d9b07b")
MUTED = HexColor("#5f675f")
WHITE = HexColor("#ffffff")


def register_fonts():
    pdfmetrics.registerFont(TTFont("Georgia", "/System/Library/Fonts/Supplemental/Georgia.ttf"))
    pdfmetrics.registerFont(TTFont("Georgia-Bold", "/System/Library/Fonts/Supplemental/Georgia Bold.ttf"))
    pdfmetrics.registerFont(TTFont("Georgia-Italic", "/System/Library/Fonts/Supplemental/Georgia Italic.ttf"))


def prepared_image(path, brightness=1.0, saturation=1.0):
    source = Image.open(path).convert("RGB")
    if brightness != 1.0:
        source = ImageEnhance.Brightness(source).enhance(brightness)
    if saturation != 1.0:
        source = ImageEnhance.Color(source).enhance(saturation)
    source.thumbnail((1800, 1800), Image.Resampling.LANCZOS)
    buffer = BytesIO()
    source.save(buffer, format="JPEG", quality=90, optimize=True)
    buffer.seek(0)
    return ImageReader(buffer)


def cover_geometry(image, width, height, focus_x=0.5, focus_y=0.5):
    image_width, image_height = image.getSize()
    scale = max(width / image_width, height / image_height)
    drawn_width = image_width * scale
    drawn_height = image_height * scale
    image_x = -(drawn_width - width) * focus_x
    image_y = -(drawn_height - height) * focus_y
    return image_x, image_y, drawn_width, drawn_height


def draw_cover(c, path, x, y, width, height, focus_x=0.5, focus_y=0.5, radius=0, brightness=1.0, saturation=1.0):
    image = prepared_image(path, brightness, saturation)
    image_x, image_y, drawn_width, drawn_height = cover_geometry(image, width, height, focus_x, focus_y)
    c.saveState()
    clip = c.beginPath()
    if radius:
        clip.roundRect(x, y, width, height, radius)
    else:
        clip.rect(x, y, width, height)
    c.clipPath(clip, stroke=0, fill=0)
    c.drawImage(image, x + image_x, y + image_y, drawn_width, drawn_height, mask="auto")
    c.restoreState()


def draw_circle_image(c, path, x, y, diameter, focus_x=0.5, focus_y=0.5, brightness=1.0):
    image = prepared_image(path, brightness)
    image_x, image_y, drawn_width, drawn_height = cover_geometry(image, diameter, diameter, focus_x, focus_y)
    c.saveState()
    clip = c.beginPath()
    clip.circle(x + diameter / 2, y + diameter / 2, diameter / 2)
    c.clipPath(clip, stroke=0, fill=0)
    c.drawImage(image, x + image_x, y + image_y, drawn_width, drawn_height, mask="auto")
    c.restoreState()
    c.setStrokeColor(WHITE)
    c.setLineWidth(3)
    c.circle(x + diameter / 2, y + diameter / 2, diameter / 2, fill=0, stroke=1)


def brush_banner(c, x, y, width, height, color):
    c.setFillColor(color)
    path = c.beginPath()
    path.moveTo(x + 2, y + 5)
    path.lineTo(x + 10, y + 1)
    path.lineTo(x + width - 8, y + 3)
    path.lineTo(x + width, y + 9)
    path.lineTo(x + width - 5, y + height - 3)
    path.lineTo(x + width - 18, y + height)
    path.lineTo(x + 7, y + height - 2)
    path.lineTo(x, y + height - 8)
    path.close()
    c.drawPath(path, fill=1, stroke=0)
    c.setStrokeColor(color)
    c.setLineWidth(2.2)
    c.line(x + 6, y - 2, x + width - 16, y)
    c.line(x + 14, y + height + 2, x + width - 7, y + height + 1)


def logo(c, x, y, size=13, dark=False):
    first = INK if dark else WHITE
    c.setFont("Helvetica-Bold", size)
    c.setFillColor(first)
    c.drawString(x, y, "NE")
    offset = c.stringWidth("NE", "Helvetica-Bold", size)
    c.setFillColor(EMBER)
    c.drawString(x + offset + 1, y, "X")
    offset += c.stringWidth("X", "Helvetica-Bold", size) + 2
    c.setFillColor(first)
    c.drawString(x + offset, y, "IA")


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


def footer(c, page_width):
    c.setFillColor(INK)
    c.rect(0, 0, page_width, 18, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 5.7)
    c.drawString(22, 6.5, "NEXIA-EXPERIENCE.NETLIFY.APP")
    c.setFillColor(WHITE)
    c.drawRightString(page_width - 22, 6.5, "NORMAN HUBERT + PATRICK MARTINEZ")


def draw_front(c, page_width, page_height):
    c.setFillColor(PAPER)
    c.rect(0, 0, page_width, page_height, fill=1, stroke=0)

    hero_height = 274
    hero_y = page_height - hero_height
    draw_cover(c, IMAGES / "hero-stone-courtyard.jpg", 0, hero_y, page_width, hero_height, focus_y=0.48, brightness=0.64, saturation=1.05)
    c.setFillColor(INK)
    c.rect(0, page_height - 54, page_width, 54, fill=1, stroke=0)
    logo(c, 24, page_height - 35, 15)
    c.setFillColor(CREAM)
    c.setFont("Helvetica-Bold", 6.3)
    c.drawRightString(page_width - 24, page_height - 34, "DIRIGEANTS - CODIR - ÉQUIPES")

    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 25)
    c.drawString(24, page_height - 96, "FAIRE VIVRE")
    brush_banner(c, 20, page_height - 149, 292, 42, FOREST)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 26)
    c.drawString(31, page_height - 139, "L’IA. VRAIMENT.")
    brush_banner(c, 27, page_height - 177, 173, 21, EMBER)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(39, page_height - 171, "COMPRENDRE. TESTER. DÉCIDER.")

    draw_circle_image(c, IMAGES / "live-norman-patrick.jpg", page_width - 139, hero_y - 35, 112, focus_x=0.5, focus_y=0.42, brightness=0.94)

    intro_style = ParagraphStyle("front-intro", fontName="Helvetica", fontSize=8.7, leading=12.6, textColor=INK)
    paragraph(c, "Quelques heures, une journée ou deux jours pour comprendre ce qui change, expérimenter sur vos cas réels et construire une réponse qui vous appartient.", 24, hero_y - 16, 238, intro_style)

    brush_banner(c, 22, 215, 236, 24, INK)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 8.2)
    c.drawString(34, 223, "CE QUE VOUS VIVEZ AVEC NEXIA")

    experiences = [
        (FOREST, "01", "COMPRENDRE", "Des repères communs sur les possibilités et les limites de l’IA."),
        (EMBER, "02", "EXPÉRIMENTER", "Des outils confrontés à vos métiers, vos pratiques et vos contraintes."),
        (GOLD, "03", "CONSTRUIRE", "Un cas d’usage, une méthode ou une première réalisation adaptée."),
        (MOSS, "04", "DÉCIDER", "Des priorités claires pour lancer, approfondir ou écarter."),
    ]
    bullet_style = ParagraphStyle("bullet", fontName="Helvetica", fontSize=6.6, leading=9.1, textColor=MUTED)
    y = 187
    for color, number, title, text in experiences:
        c.setFillColor(color)
        c.circle(37, y + 6, 13, fill=1, stroke=0)
        c.setFillColor(WHITE if color != GOLD else INK)
        c.setFont("Helvetica-Bold", 6.8)
        c.drawCentredString(37, y + 4, number)
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 7.4)
        c.drawString(58, y + 11, title)
        paragraph(c, text, 58, y + 6, 212, bullet_style)
        y -= 37

    brush_banner(c, 284, 77, 113, 118, FOREST)
    c.setFillColor(WHITE)
    c.setFont("Georgia-Italic", 10.5)
    c.drawCentredString(340.5, 175, "Scannez pour")
    c.drawCentredString(340.5, 162, "découvrir NEXIA")
    c.setFillColor(PAPER)
    c.roundRect(308, 88, 68, 64, 3, fill=1, stroke=0)
    draw_qr(c, "https://nexia-experience.netlify.app", 313, 93, 58)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 6.2)
    c.drawCentredString(342, 82, "LE SITE ET LES FORMATS")

    c.setFillColor(INK)
    c.setFont("Georgia-Bold", 15)
    c.drawString(24, 48, "Une expérience professionnelle")
    c.drawString(24, 31, "et humaine de l’intelligence artificielle.")
    footer(c, page_width)


def draw_back(c, page_width, page_height):
    c.setFillColor(PAPER)
    c.rect(0, 0, page_width, page_height, fill=1, stroke=0)

    logo(c, 24, page_height - 34, 14, dark=True)
    c.setFillColor(MUTED)
    c.setFont("Helvetica-Bold", 5.8)
    c.drawRightString(page_width - 24, page_height - 33, "EXPÉRIENCES D’INTELLIGENCE ARTIFICIELLE")

    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(23, page_height - 76, "QUATRE FAÇONS")
    brush_banner(c, 20, page_height - 126, 333, 39, FOREST)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(32, page_height - 117, "DE VIVRE NEXIA")
    brush_banner(c, 233, page_height - 151, 160, 19, EMBER)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 8.2)
    c.drawCentredString(313, page_height - 145, "À VOTRE RYTHME, SUR VOS SUJETS")

    back_intro = ParagraphStyle("back-intro", fontName="Helvetica-Bold", fontSize=7.8, leading=11.2, textColor=INK)
    paragraph(c, "Le bon format est celui qui permet à votre groupe de comprendre, d’essayer et de repartir avec une direction commune.", 24, 432, 355, back_intro)

    c.setFillColor(WHITE)
    c.roundRect(20, 282, 240, 126, 8, fill=1, stroke=0)
    draw_cover(c, IMAGES / "live-norman-patrick.jpg", 24, 286, 232, 118, focus_x=0.5, focus_y=0.47, radius=6, brightness=0.98)
    draw_circle_image(c, IMAGES / "immersion-pond-premium.jpg", 276, 288, 116, focus_x=0.54, focus_y=0.66, brightness=1.02)
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 5.8)
    c.drawString(24, 272, "EXPERTISE, PÉDAGOGIE, MISE EN SITUATION ET TEMPS DE RECUL")

    brush_banner(c, 20, 241, 179, 23, INK)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(31, 249, "CHOISISSEZ VOTRE FORMAT")

    formats = [
        ("01", "UNE DEMI-JOURNÉE", "Ouvrir le sujet et mettre une équipe en mouvement."),
        ("02", "UNE JOURNÉE", "Prendre du recul, tester et construire sur des cas réels."),
        ("03", "DEUX JOURS - IMMERSION", "Un petit groupe, un lieu à part et le temps d’aller plus loin."),
        ("04", "SUR SCÈNE - LIVE", "Une conférence à deux voix, claire, vivante et mémorable."),
    ]
    small_style = ParagraphStyle("format-copy", fontName="Helvetica", fontSize=5.9, leading=7.5, textColor=MUTED)
    y = 210
    for index, (number, title, text) in enumerate(formats):
        color = [FOREST, EMBER, GOLD, MOSS][index]
        c.setFillColor(color)
        c.roundRect(24, y - 1, 27, 27, 4, fill=1, stroke=0)
        c.setFillColor(WHITE if index != 2 else INK)
        c.setFont("Helvetica-Bold", 6.5)
        c.drawCentredString(37.5, y + 8, number)
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 7.2)
        c.drawString(62, y + 14, title)
        paragraph(c, text, 62, y + 8, 330, small_style)
        y -= 38

    brush_banner(c, 20, 61, 164, 24, FOREST)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 7.8)
    c.drawString(31, 69, "CE QUI RESTE APRÈS")
    c.setFillColor(INK)
    c.setFont("Georgia-Bold", 11)
    c.drawString(24, 43, "Des repères. Des usages testés. Des choix.")
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 6.2)
    c.drawString(24, 30, "Selon le format : une suite praticable et une projection à 30, 60 et 90 jours.")

    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 6.6)
    c.drawRightString(page_width - 24, 70, "PARLONS DE VOTRE PROJET")
    c.setFillColor(EMBER)
    c.setFont("Georgia-Italic", 10.5)
    c.drawRightString(page_width - 24, 52, "normanhubert@gmail.com")
    c.setFillColor(MUTED)
    c.setFont("Helvetica-Bold", 6)
    c.drawRightString(page_width - 24, 36, "NEXIA-EXPERIENCE.NETLIFY.APP")
    footer(c, page_width)


def build():
    register_fonts()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    page_width, page_height = A5
    c = canvas.Canvas(str(OUTPUT), pagesize=A5, pageCompression=1)
    c.setTitle("NEXIA - Flyer prospection recto-verso")
    c.setAuthor("NEXIA - Norman Hubert et Patrick Martinez")
    c.setSubject("Expériences immersives en intelligence artificielle")
    draw_front(c, page_width, page_height)
    c.showPage()
    draw_back(c, page_width, page_height)
    c.showPage()
    c.save()
    print(OUTPUT)


if __name__ == "__main__":
    build()
