from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas


def draw_multiline_text(
    pdf,
    lines,
    x,
    y,
    font_name="Helvetica",
    font_size=10,
    leading=13,
):
    """Draw text from bottom to top, returning the final y position."""
    pdf.setFont(font_name, font_size)

    for line in lines:
        pdf.drawString(x, y, line)
        y -= leading

    return y


def draw_fold_line(pdf: canvas.Canvas, x1, y1, x2, y2):
    """Draw a dashed fold guide line."""
    pdf.saveState()
    pdf.setDash()
    pdf.setStrokeColor(colors.black)
    pdf.setLineWidth(0.8)
    pdf.line(x1, y1, x2, y2)
    pdf.restoreState()


def draw_guide_line(pdf: canvas.Canvas, x1, y1, x2, y2):
    """Draw a dashed fold guide line."""
    pdf.saveState()
    pdf.setDash(8, 4)
    pdf.setStrokeColor(colors.HexColor("#AAAAAA"))
    pdf.setLineWidth(0.4)
    pdf.line(x1, y1, x2, y2)
    pdf.restoreState()


def draw_cut_line(pdf: canvas.Canvas, x1, y1, x2, y2):
    """Draw a solid cutting line."""
    pdf.saveState()
    pdf.setDash(4, 3)
    pdf.setStrokeColor(colors.black)
    pdf.setLineWidth(1)
    pdf.line(x1, y1, x2, y2)
    pdf.restoreState()


def draw_test_bubble(pdf: canvas.Canvas, x, y, a: str):
    """Draw a solid cutting line."""
    pdf.saveState()
    pdf.setLineWidth(1)
    pdf.setStrokeColor(colors.black)
    pdf.setFont("Helvetica", 14)
    pdf.circle(x, y, 5 * mm)
    pdf.drawCentredString(x, y - 4, a)
    pdf.restoreState()


def please_do_not_bend_stamp(pdf: canvas.Canvas, x, y):
    width = 44 * mm
    height = 20 * mm
    pdf.roundRect(x, y, width, height, 2 * mm, stroke=1, fill=0)
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawCentredString(x + width / 2, y + 12 * mm, "PLEASE")
    pdf.drawCentredString(x + width / 2, y + 4 * mm, "DO NOT BEND")
