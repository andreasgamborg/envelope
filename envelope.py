#!/usr/bin/env python3
import argparse

from pathlib import Path
from math import sqrt

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib import colors

from utils.drawing import *
from utils.recipient import Recipient, read_addresses_from_txt, str_to_recipient
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
    bl = envelope_width / 8.0  # base length

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
        "FOLD-IT-YOURSELF ENVELOPE TEMPLATE",
    )

    pdf.setFont("Helvetica", 10)
    pdf.drawCentredString(
        square_side / 2.0,
        excess_height - 17 * mm,
        "Print at 100% / actual size",
    )

    draw_cut_line(pdf, 0, excess_height, square_side, excess_height)

    draw_fold_line(pdf, *square_ml, *square_tm)
    draw_fold_line(pdf, *square_mr, *square_bm)

    pdf.saveState()
    pdf.translate(*square_mm)
    pdf.rotate(-45)

    pdf.setFont("Helvetica", 12)
    pdf.drawCentredString(0, 7 * bl, "Top")
    pdf.drawCentredString(0, -7 * bl, "Bottom")

    # Horizontal fold line
    draw_fold_line(pdf, -4 * bl, -2 * bl, 4 * bl, -2 * bl)
    draw_fold_line(pdf, -3 * bl, -5 * bl, 3 * bl, -5 * bl)

    # Sides of tounge
    draw_fold_line(pdf, 4 * bl, -2 * bl, bl, -5 * bl)
    draw_fold_line(pdf, -4 * bl, -2 * bl, -1 * bl, -5 * bl)

    # step 1 and step 2
    draw_test_bubble(pdf, -1 * bl, 0, "1")
    draw_test_bubble(pdf, 1 * bl, 0, "2")
    draw_guide_line(pdf, -bl, -bl, bl, bl)
    draw_guide_line(pdf, bl, -bl, -bl, bl)
    # step 3
    draw_test_bubble(pdf, 0, 3 * bl, "3")
    draw_guide_line(pdf, 0, -2 * bl, -bl, -3 * bl)
    draw_guide_line(pdf, 0, -2 * bl, bl, -3 * bl)
    # step 4
    draw_test_bubble(pdf, 0, -3 * bl, "4")
    draw_guide_line(pdf, 0, 4 * bl, bl, 3 * bl)
    draw_guide_line(pdf, 0, 4 * bl, -bl, 3 * bl)
    # step 5 and step 6
    draw_test_bubble(pdf, -3 * bl, -4 * bl, "5")
    draw_test_bubble(pdf, 3 * bl, -4 * bl, "6")
    draw_guide_line(pdf, bl, -3 * bl, 2 * bl, -2 * bl)
    draw_guide_line(pdf, -bl, -3 * bl, -2 * bl, -2 * bl)

    pdf.drawImage(
        QR_IMG,
        -3 * bl / 4.0,
        3 * bl / 4.0,
        width=1.5 * bl,
        height=1.5 * bl,
        preserveAspectRatio=True,
        mask="auto",
    )
    pdf.setFont("Helvetica", 10)
    pdf.drawCentredString(
        0,
        9 / 4.0 * bl,
        "github.com/andreasgamborg/envelope",
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
    draw_cut_line(pdf, line_x, row1_y, line_x + check_width, row1_y)
    pdf.drawString(name_x, row2_y, "Fold line")
    draw_fold_line(pdf, line_x, row2_y, line_x + check_width, row2_y)
    pdf.drawString(name_x, row3_y, "Guide line")
    draw_guide_line(pdf, line_x, row3_y, line_x + check_width, row3_y)

    qr_x = 135 * mm
    pdf.drawImage(
        QR_IMG,
        qr_x,
        low_line + 4 * mm,
        width=50 * mm,
        height=50 * mm,
        preserveAspectRatio=True,
        mask="auto",
    )
    pdf.setFont("Helvetica", 10)
    pdf.drawString(
        qr_x,
        low_line,
        "github.com/andreasgamborg/envelope",
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
        -4 * bl,
        4 * bl - 10 * mm,
        4 * bl,
        4 * bl - 10 * mm,
    )
    draw_fold_line(
        pdf,
        -6 * bl,
        -2 * bl,
        6 * bl,
        -2 * bl,
    )
    draw_fold_line(
        pdf,
        -3 * bl,
        -5 * bl,
        3 * bl,
        -5 * bl,
    )

    # Wrap fold lines
    draw_fold_line(pdf, -4 * bl, -2 * bl, -5 * bl, -3 * bl)
    draw_fold_line(pdf, 4 * bl, -2 * bl, 5 * bl, -3 * bl)
    draw_fold_line(pdf, -1 * bl, -5 * bl, -2 * bl, -6 * bl)
    draw_fold_line(pdf, 1 * bl, -5 * bl, 2 * bl, -6 * bl)

    # Wrap guide lines
    draw_guide_line(pdf, -bl, -5 * bl, -bl, -7 * bl)
    draw_guide_line(pdf, bl, -5 * bl, bl, -7 * bl)

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
        please_do_not_bend_stamp(pdf, 0, 0)

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

    return_address = None
    if args.return_address:
        return_file = Path(args.return_address)
        if return_file.exists():
            with open(return_file, "r", encoding="utf-8") as file:
                return_address = file.read()
            print(
                f"{"Using return address from:":30s}\033[36m{return_file.resolve()}\033[0m"
            )
        else:
            print(
                f"{"Using return address from:":30s}\033[31m{return_file.resolve()} NOT FOUND!\033[0m"
            )
    else:
        print(f"{"Using return address from:":30s}\033[33mNo return address\033[0m")

    if args.do_not_bend:
        print(f"{"\"Please, do not bend\" stamp:":30s}\033[32mYes\033[0m")
    else:
        print(f"{"\"Please, do not bend\" stamp:":30s}\033[31mNo\033[0m")

    print("")

    recipients: list[Recipient]

    if input_file.exists():
        recipients = read_addresses_from_txt(input_file)
    else:
        printc("No input file detected", "yellow")
        recipients = read_address_from_shell()

    for recipient in recipients:
        make_envelope(
            output_path=output_path,
            recipient=recipient,
            do_not_bend_stamp=args.do_not_bend,
            return_address=return_address,
        )


def read_address_from_shell() -> list[Recipient]:
    print("Paste address here, then send an empty line")
    lines = []
    while True:
        line = input()
        if line.strip() == "":
            break
        lines.append(line)
    text = "\n".join(lines)

    print("Got input:")
    printc(text, "cyan")

    return [str_to_recipient(text)]


if __name__ == "__main__":
    main()
