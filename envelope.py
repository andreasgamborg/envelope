#!/usr/bin/env python3
import argparse

from pathlib import Path
from math import sqrt

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib import colors

from utils.drawing import *
from utils.recipient import Recipient, read_addresses_from_txt 
from utils.misc import make_filename, printc

SCRIPT_DIR = Path(__file__).resolve().parent
ENVELOPE_IMG = SCRIPT_DIR / "resources" / "envelope.png"
QR_IMG = SCRIPT_DIR / "resources" / "qr-code.png"

def make_envelope(
    output_path: Path,
    recipient: Recipient,
    return_address: str,
    do_not_bend_stamp: bool,
):
    """
    Make a two sided A4 pdf which can be folded into an envelope
    """
    print(f"Making envelope for {recipient.name:<20s}")
    output_file = output_path / make_filename(recipient.name, ".pdf")
    if output_file.exists():
        printc(f"Overwriting file {output_file}", "yellow")
    pdf = canvas.Canvas(str(output_file), pagesize=A4)
    pdf.setTitle(f"Envelope for {recipient.name}")

    # ------------------------------------------------------------
    # Envelope dimensions in millimetres
    # ------------------------------------------------------------
    page_width, page_height = A4
    square_side = page_width
    excess_height = page_height - square_side
    half_side = square_side / 2.0

    square_tl = (0, excess_height + square_side)
    square_tm = (half_side, excess_height + square_side)
    square_tr = (square_side, excess_height + square_side)

    square_ml = (0, excess_height + half_side)
    square_mm = (half_side, excess_height + half_side)
    square_mr = (square_side, excess_height + half_side)

    square_bl = (0, excess_height)
    square_bm = (half_side, excess_height)
    square_br = (square_side, excess_height)

    envelope_width = sqrt(2 * half_side**2)

    # ------------------------------------------------------------
    # Envelope Back
    # ------------------------------------------------------------

    pdf.drawImage(
        ENVELOPE_IMG,
        x=30 * mm,
        y=excess_height - 20 * mm,
        width=15 * mm,
        height=15 * mm,
        preserveAspectRatio=True,
        mask="auto",
    )

    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawCentredString(
        square_side / 2.0,
        excess_height - 12 * mm,
        "SELF-FOLD ENVELOPE TEMPLATE",
    )

    pdf.setFont("Helvetica", 8)
    pdf.drawCentredString(
        square_side / 2.0,
        excess_height - 17 * mm,
        "Print at 100% / actual size",
    )

    draw_cut_line(pdf, 0, excess_height, square_side, excess_height)

    draw_guide_line(pdf, *square_tm, *square_bm)
    draw_guide_line(pdf, *square_ml, *square_mr)
    draw_guide_line(pdf, *square_bl, *square_tr)

    draw_fold_line(pdf, *square_ml, *square_tm)
    draw_fold_line(pdf, *square_mr, *square_bm)

    pdf.saveState()
    pdf.setFont("Helvetica", 8)
    pdf.translate(*square_mm)
    pdf.rotate(-45)

    pdf.drawString(2 * mm, 80 * mm, "Top")
    draw_guide_line(pdf, -20 * mm, envelope_width / 2.0, 20 * mm, envelope_width / 2.0)
    pdf.drawString(2 * mm, -80 * mm, "Bottom")
    draw_fold_line(
        pdf,
        -envelope_width / 2.0,
        -envelope_width / 4.0,
        envelope_width / 2,
        -envelope_width / 4.0,
    )

    draw_fold_line(
        pdf,
        -40 * mm,
        -5 * envelope_width / 8.0,
        40 * mm,
        -5 * envelope_width / 8.0,
    )

    x =  5*mm
    y =  -5*mm
    pdf.drawImage(
        QR_IMG,
        x,
        y,
        width=30 * mm,
        height=30 * mm,
        preserveAspectRatio=True,
        mask="auto",
    )
    pdf.drawString(
        x,
        y-2*mm,
        "https://github.com/andreasgamborg/envelope",
    )


    pdf.restoreState()

    name_x = 15 * mm
    line_x = 40 * mm
    row1_y = 26 * mm
    row2_y = 20 * mm
    row3_y = 14 * mm
    check_width = 70 * mm
    low_line = 10 * mm

    pdf.setFont("Helvetica", 12)
    pdf.drawString(name_x, row1_y, "Cut line")
    draw_cut_line(pdf,line_x, row1_y, line_x + check_width, row1_y)
    pdf.drawString(name_x, row2_y, "Fold line")
    draw_fold_line(pdf,line_x, row2_y, line_x + check_width, row2_y)
    pdf.drawString(name_x,row3_y, "Guide line")
    draw_guide_line(pdf,line_x, row3_y, line_x + check_width, row3_y)


    # pdf.setFont("Helvetica", 8)
    # pdf.drawCentredString(
    #     check_x + check_width / 2.0,
    #     low_line,
    #     "50 mm scale check",
    # )

    qr_x = 140 * mm
    pdf.drawImage(
        QR_IMG,
        qr_x,
        low_line + 2*mm,
        width=50 * mm,
        height=50 * mm,
        preserveAspectRatio=True,
        mask="auto",
    )
    pdf.setFont("Helvetica", 8)
    pdf.drawString(
        qr_x,
        low_line,
        "https://github.com/andreasgamborg/envelope",
    )

    pdf.showPage()

    # ------------------------------------------------------------
    # Envelope Front
    # ------------------------------------------------------------

    draw_cut_line(pdf, 0, excess_height, square_side, excess_height)
    draw_fold_line(pdf, *square_tm, *square_mr)
    draw_fold_line(pdf, *square_bm, *square_ml)

    pdf.translate(*square_mm)
    pdf.rotate(45)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.saveState()

    draw_fold_line(
        pdf,
        -envelope_width / 2.0,
        envelope_width / 2.0 - 10 * mm,
        envelope_width / 2.0,
        envelope_width / 2.0 - 10 * mm,
    )
    draw_fold_line(
        pdf,
        -envelope_width / 2.0,
        -envelope_width / 4.0,
        envelope_width / 2.0,
        -envelope_width / 4.0,
    )

    reci = [recipient.name]
    if recipient.co:
        reci.append(recipient.co)
    reci.append(recipient.street)
    reci.append(recipient.city)
    reci.append(recipient.country.upper())

    draw_multiline_text(
        pdf,
        reci,
        -130,
        40,
        font_size=14,
        leading=20,
    )

    pdf.translate(80, -80)
    pdf.rotate(10)

    red = colors.HexColor("#B22222")
    pdf.setStrokeColor(red)
    pdf.setFillColor(red)
    pdf.setLineWidth(1.5)

    # Outer border and inset border
    if do_not_bend_stamp:
        please_do_not_bend_stamp(pdf,0,0)

    pdf.restoreState()

    if return_address:
        pdf.rotate(180)
        pdf.translate(0, -70 * mm)
        pdf.setFont("Helvetica", 8)
        y = 0
        lines = return_address.split("\n")
        for line in lines:
            pdf.drawCentredString(0, y, line)
            y = y - 10

    # ------------------------------------------------------------

    pdf.showPage()
    pdf.save()
    printc("DONE!", "green")

def main():

    parser = argparse.ArgumentParser(description="Describe what your script does.")
    parser.add_argument(
        "-i",
        "--input_file",
        help="Input .txt file containing recipients",
        default="input.txt",
    )
    parser.add_argument("-o", "--output_dir", help="Output folder", default="output")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Show extra details"
    )
    parser.add_argument(
        "-r", "--return-address", help="File containing the return address"
    )
    parser.add_argument(
        "-b",
        "--do-not-bend",
        action="store_true",
        help='Show "Please Do Not Bend" stamp on envelope',
    )
    args = parser.parse_args()

    input_file = Path(args.input_file)
    output_path = Path(args.output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    print("Starting envelope generation")
    print(f"{"Using input file:":30s}\033[36m{input_file.resolve()}\033[0m")
    print(f"{"Writing to output folder:":30s}\033[36m{output_path.resolve()}\033[0m")

    recipients: list[Recipient] = []

    return_address = None
    return_file = Path(args.return_address)
    if return_file:
        with open(return_file, "r", encoding="utf-8") as file:
            return_address = file.read()
        print(f"{"Using return address from:":30s}\033[36m{return_file.resolve()}\033[0m")

    print("")

    if args.input_file:
        recipients = read_addresses_from_txt(args.input_file)
    else:
        import tkinter as tk

        input("Copy the address to your clipboard, then press <ENTER>")
        root = tk.Tk()
        root.withdraw()  # Keep the window hidden
        text = root.clipboard_get()
        root.destroy()
        print(text)

        r = str_to_recipient(text)
        recipients.append(r)

    for recipient in recipients:
        make_envelope(
            output_path=output_path,
            recipient=recipient,
            do_not_bend_stamp=args.do_not_bend,
            return_address=return_address,
        )

if __name__ == "__main__":
    main()
