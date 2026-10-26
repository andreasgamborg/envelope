from dataclasses import dataclass
from .misc import printc


@dataclass
class Recipient:
    name: str
    co: str
    street: str
    city: str
    country: str


def str_to_recipient(s) -> Recipient:
    b = s.strip().split("\n")
    if len(b) == 4:
        name = b[0].strip()
        co = ""
        street = b[1].strip()
        city = b[2].strip()
        country = b[3].strip()
    elif len(b) == 5:
        name = b[0].strip()
        co = b[1].strip()
        street = b[2].strip()
        city = b[3].strip()
        country = b[4].strip()
    else:
        printc(
            f"Could not parse the following {len(b)} line address into a Recipient object\n{b}",
            "red",
        )
        raise ValueError(
            "Use 4-5 lines per recipient (name, [co], street, city, country)"
        )
    return Recipient(name, co, street, city, country)


def read_addresses_from_txt(filename) -> list[Recipient]:
    """
    Read multiple addresses from a text file.

    Format:

        [ADDRESS BLOCK]
        ---
        [ADDRESS BLOCK]
        ---
    """

    with open(filename, "r", encoding="utf-8") as file:
        contents = file.read()

    # Split records at lines containing only "---"
    blocks = contents.split("---")

    recipients: list[Recipient] = []

    for block in blocks:
        r = str_to_recipient(block)
        recipients.append(r)

    return recipients


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
