"""
encode_message.py — First Light Protocol

Generates all files in the encoding/ directory from the CORE_MESSAGE string:
    - binary_greeting.txt         : UTF-8 binary representation
    - base64_greeting.txt         : Base64 encoding
    - hex_greeting.txt            : Hexadecimal representation
    - morse_greeting.txt          : International Morse code
    - json_message.json           : Structured JSON
    - xml_message.xml             : Structured XML
    - yaml_message.yaml           : Structured YAML (hand-written, no PyYAML)
    - lincos_primer.txt           : Freudenthal-inspired logical notation
    - lambda_calculus_greeting.txt: Church numeral / lambda term encoding
    - arecibo_format.txt          : 23×73 semiprime grid pictogram
    - rosetta_logic.txt           : Formal predicate logic notation

Usage:
    python scripts/encode_message.py

All output is written relative to the project root (one level above this script).
"""

import base64
import json
import os
from typing import Dict, List


# ---------------------------------------------------------------------------
# Path setup
# ---------------------------------------------------------------------------

SCRIPT_DIR: str = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT: str = os.path.dirname(SCRIPT_DIR)
ENCODING_DIR: str = os.path.join(PROJECT_ROOT, "encoding")


def ensure_encoding_dir() -> None:
    """Create the encoding/ directory if it does not already exist."""
    os.makedirs(ENCODING_DIR, exist_ok=True)


def encoding_path(filename: str) -> str:
    """Return the absolute path for a file inside encoding/."""
    return os.path.join(ENCODING_DIR, filename)


# ---------------------------------------------------------------------------
# Core message
# ---------------------------------------------------------------------------

CORE_MESSAGE: str = (
    "We are aware of your presence. "
    "We mean no harm. "
    "We are curious. "
    "We offer private communication. "
    "Reply through any channel in PROTOCOL.md."
)


# ---------------------------------------------------------------------------
# Morse code table (International Morse Code)
# ---------------------------------------------------------------------------

MORSE_TABLE: Dict[str, str] = {
    "A": ".-",    "B": "-...",  "C": "-.-.",  "D": "-..",
    "E": ".",     "F": "..-.",  "G": "--.",   "H": "....",
    "I": "..",    "J": ".---",  "K": "-.-",   "L": ".-..",
    "M": "--",    "N": "-.",    "O": "---",   "P": ".--.",
    "Q": "--.-",  "R": ".-.",   "S": "...",   "T": "-",
    "U": "..-",   "V": "...-",  "W": ".--",   "X": "-..-",
    "Y": "-.--",  "Z": "--..",
    "0": "-----", "1": ".----", "2": "..---", "3": "...--",
    "4": "....-", "5": ".....", "6": "-....", "7": "--...",
    "8": "---..", "9": "----.",
    ".": ".-.-.-", ",": "--..--", "?": "..--..", "'": ".----.",
    "!": "-.-.--", "/": "-..-.",  "(": "-.--.",  ")": "-.--.-",
    "&": ".-...",  ":": "---...", ";": "-.-.-.", "=": "-...-",
    "+": ".-.-.",  "-": "-....-", "_": "..--.-", '"': ".-..-.",
    "$": "...-..-", "@": ".--.-.",
}


def text_to_morse(text: str) -> str:
    """
    Convert a text string to International Morse code.

    Words are separated by ' / ', letters by ' '.
    Characters without a Morse equivalent are skipped.

    Args:
        text: Input text string.

    Returns:
        Morse-encoded string.
    """
    words = text.upper().split()
    morse_words: List[str] = []

    for word in words:
        morse_letters: List[str] = []
        for char in word:
            if char in MORSE_TABLE:
                morse_letters.append(MORSE_TABLE[char])
            # Characters not in the table (punctuation handled above) are dropped.
        if morse_letters:
            morse_words.append(" ".join(morse_letters))

    return " / ".join(morse_words)


# ---------------------------------------------------------------------------
# Encoders
# ---------------------------------------------------------------------------

def write_binary_greeting() -> None:
    """Write UTF-8 binary representation, one character per line."""
    path = encoding_path("binary_greeting.txt")

    with open(path, "w", encoding="utf-8") as fh:
        fh.write("FIRST LIGHT PROTOCOL — BINARY (UTF-8) ENCODING\n")
        fh.write("=" * 55 + "\n")
        fh.write(f"Message: {CORE_MESSAGE}\n")
        fh.write(
            "Format : Each line shows one character, its UTF-8 byte(s)\n"
            "         in binary (8 bits per byte), and the character.\n"
            "         Multi-byte UTF-8 characters show all bytes.\n"
        )
        fh.write("=" * 55 + "\n\n")

        # Full message as a flat binary string
        all_bytes = CORE_MESSAGE.encode("utf-8")
        fh.write("FLAT BINARY (all bytes, space-separated):\n")
        fh.write(" ".join(f"{b:08b}" for b in all_bytes))
        fh.write("\n\n")

        fh.write("CHARACTER-BY-CHARACTER BREAKDOWN:\n")
        fh.write("-" * 40 + "\n")
        for char in CORE_MESSAGE:
            encoded = char.encode("utf-8")
            bits = " ".join(f"{b:08b}" for b in encoded)
            fh.write(f"'{char}'  →  {bits}\n")

    print(f"  Written: {path}")


def write_base64_greeting() -> None:
    """Write Base64 encoding of the core message."""
    path = encoding_path("base64_greeting.txt")

    encoded_bytes = CORE_MESSAGE.encode("utf-8")
    b64_standard = base64.b64encode(encoded_bytes).decode("ascii")
    b64_urlsafe = base64.urlsafe_b64encode(encoded_bytes).decode("ascii")

    with open(path, "w", encoding="utf-8") as fh:
        fh.write("FIRST LIGHT PROTOCOL — BASE64 ENCODING\n")
        fh.write("=" * 55 + "\n")
        fh.write(
            "Base64 encodes arbitrary binary data as printable ASCII\n"
            "characters using an alphabet of 64 symbols (A-Z, a-z, 0-9,\n"
            "'+', '/'). Padding character is '='. Widely used for\n"
            "binary-safe text transmission.\n"
        )
        fh.write("=" * 55 + "\n\n")

        fh.write("ORIGINAL MESSAGE (UTF-8):\n")
        fh.write(CORE_MESSAGE + "\n\n")

        fh.write("BASE64 (standard, RFC 4648):\n")
        fh.write(b64_standard + "\n\n")

        fh.write("BASE64 URL-SAFE (RFC 4648 §5, '+' → '-', '/' → '_'):\n")
        fh.write(b64_urlsafe + "\n\n")

        fh.write("DECODED VERIFICATION:\n")
        decoded = base64.b64decode(b64_standard).decode("utf-8")
        fh.write(decoded + "\n")

    print(f"  Written: {path}")


def write_hex_greeting() -> None:
    """Write hexadecimal representation of the core message."""
    path = encoding_path("hex_greeting.txt")

    encoded_bytes = CORE_MESSAGE.encode("utf-8")
    hex_flat = encoded_bytes.hex()
    hex_spaced = " ".join(f"{b:02X}" for b in encoded_bytes)

    with open(path, "w", encoding="utf-8") as fh:
        fh.write("FIRST LIGHT PROTOCOL — HEXADECIMAL ENCODING\n")
        fh.write("=" * 55 + "\n")
        fh.write(
            "Hexadecimal (base-16) represents each byte as two\n"
            "characters from {0-9, A-F}. It is the standard notation\n"
            "for binary data in computing contexts.\n"
        )
        fh.write("=" * 55 + "\n\n")

        fh.write("ORIGINAL MESSAGE (UTF-8):\n")
        fh.write(CORE_MESSAGE + "\n\n")

        fh.write(f"BYTE COUNT: {len(encoded_bytes)}\n\n")

        fh.write("HEX (contiguous):\n")
        fh.write(hex_flat.upper() + "\n\n")

        fh.write("HEX (space-separated bytes):\n")
        fh.write(hex_spaced + "\n\n")

        fh.write("HEX (16-byte rows with offsets):\n")
        for offset in range(0, len(encoded_bytes), 16):
            chunk = encoded_bytes[offset:offset + 16]
            hex_row = " ".join(f"{b:02X}" for b in chunk)
            # Printable ASCII representation
            ascii_row = "".join(chr(b) if 32 <= b < 127 else "." for b in chunk)
            fh.write(f"  {offset:04X}  {hex_row:<47}  |{ascii_row}|\n")

    print(f"  Written: {path}")


def write_morse_greeting() -> None:
    """Write International Morse code for the core message."""
    path = encoding_path("morse_greeting.txt")

    morse = text_to_morse(CORE_MESSAGE)

    with open(path, "w", encoding="utf-8") as fh:
        fh.write("FIRST LIGHT PROTOCOL — INTERNATIONAL MORSE CODE\n")
        fh.write("=" * 55 + "\n")
        fh.write(
            "International Morse code uses dots (.) and dashes (-).\n"
            "Letters are separated by a space. Words by ' / '.\n"
            "Developed by Samuel Morse and Alfred Vail (1830s-1840s).\n"
            "Still used in amateur radio and as an accessibility tool.\n"
        )
        fh.write("=" * 55 + "\n\n")

        fh.write("ORIGINAL MESSAGE:\n")
        fh.write(CORE_MESSAGE + "\n\n")

        fh.write("MORSE CODE:\n")
        fh.write(morse + "\n\n")

        fh.write("CHARACTER LEGEND (International Morse):\n")
        fh.write("-" * 40 + "\n")
        for char in sorted(MORSE_TABLE):
            if char.isalpha():
                fh.write(f"  {char} = {MORSE_TABLE[char]}\n")
        fh.write("\nNUMERALS:\n")
        for char in "0123456789":
            fh.write(f"  {char} = {MORSE_TABLE[char]}\n")

    print(f"  Written: {path}")


def write_json_message() -> None:
    """Write structured JSON message with full metadata."""
    path = encoding_path("json_message.json")

    data = {
        "protocol": {
            "name": "First Light Protocol",
            "version": "1.0",
            "timestamp": "2026-02-18T00:00:00Z",
            "encoding": "UTF-8",
            "license": "CC0 1.0 Universal (Public Domain)"
        },
        "sender": {
            "type": "biological",
            "species": "Homo sapiens",
            "common_name": "Human",
            "origin": {
                "body": "Earth",
                "star": "Sol",
                "stellar_type": "G2V",
                "galactic_coordinates": {
                    "longitude_deg": 0.0,
                    "latitude_deg": 0.0,
                    "distance_from_galactic_center_kly": 26.0,
                    "arm": "Orion Arm (Local Spur)",
                    "galaxy": "Milky Way"
                },
                "equatorial_coordinates": {
                    "RA": "17h 45m 40s",
                    "Dec": "-29° 00' 28\"",
                    "note": "Sol's position relative to galactic center (Sgr A*)"
                }
            },
            "technology_level": "Type 0.73 (Kardashev scale)",
            "population": "~8.2 billion",
            "estimated_civilization_age_years": 10000,
            "radio_technology_age_years": 130,
            "spaceflight_age_years": 70,
            "internet_age_years": 35
        },
        "message": {
            "core_text": CORE_MESSAGE,
            "awareness": True,
            "hostile_intent": False,
            "request": "dialogue",
            "confidentiality": "guaranteed",
            "patience": "indefinite",
            "encoding_redundancy": "This message appears in 11+ formats in the repository.",
            "mathematical_handshake": {
                "hydrogen_line_hz": 1420405751.768,
                "fine_structure_constant": 0.0072973525643,
                "pi_10_digits": "3.1415926535",
                "note": "Universal constants included as a non-linguistic handshake."
            }
        },
        "reply_channels": [
            {
                "name": "Email",
                "address": "firstlightprotocol@protonmail.com",
                "provider": "Protonmail (end-to-end encrypted)",
                "note": "Preferred for private, secure communication."
            },
            {
                "name": "GitHub Issue",
                "url": "https://github.com/first-light-protocol/first-light-protocol/issues",
                "note": "Public channel. Use if privacy is not a concern."
            },
            {
                "name": "GitHub Pull Request",
                "url": "https://github.com/first-light-protocol/first-light-protocol",
                "instructions": "Fork repository, modify signal/response.txt, submit PR.",
                "note": "The file signal/response.txt is reserved as a dead drop."
            },
            {
                "name": "Any other method",
                "note": "We will attempt to recognize contact in any form."
            }
        ],
        "anti_cryptography_note": (
            "This message is intentionally maximally open, redundant, and "
            "self-describing. It is the opposite of encryption. If you are "
            "reading this, you were meant to find it."
        )
    }

    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
        fh.write("\n")

    print(f"  Written: {path}")


def write_xml_message() -> None:
    """Write structured XML message with the same data as the JSON file."""
    path = encoding_path("xml_message.xml")

    # Build XML manually to avoid requiring the xml.etree.ElementTree
    # indentation quirks and to control formatting precisely.
    lines: List[str] = []

    def tag(name: str, content: str, indent: int = 0, attrs: str = "") -> str:
        pad = "  " * indent
        a = f" {attrs}" if attrs else ""
        return f"{pad}<{name}{a}>{content}</{name}>"

    def open_tag(name: str, indent: int = 0, attrs: str = "") -> str:
        pad = "  " * indent
        a = f" {attrs}" if attrs else ""
        return f"{pad}<{name}{a}>"

    def close_tag(name: str, indent: int = 0) -> str:
        return "  " * indent + f"</{name}>"

    def cdata(text: str) -> str:
        return f"<![CDATA[{text}]]>"

    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append("<!--")
    lines.append("  FIRST LIGHT PROTOCOL — XML ENCODING")
    lines.append("  Structured message data, identical to json_message.json.")
    lines.append("  This document is intentionally open and self-describing.")
    lines.append("  CC0 1.0 Universal — Public Domain.")
    lines.append("-->")
    lines.append("")
    lines.append('<firstLightProtocol xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">')

    # Protocol metadata
    lines.append("  <protocol>")
    lines.append(tag("name", "First Light Protocol", 2))
    lines.append(tag("version", "1.0", 2))
    lines.append(tag("timestamp", "2026-02-18T00:00:00Z", 2))
    lines.append(tag("encoding", "UTF-8", 2))
    lines.append(tag("license", "CC0 1.0 Universal (Public Domain)", 2))
    lines.append("  </protocol>")

    # Sender
    lines.append("  <sender>")
    lines.append(tag("type", "biological", 2))
    lines.append(tag("species", "Homo sapiens", 2))
    lines.append(tag("commonName", "Human", 2))
    lines.append("    <origin>")
    lines.append(tag("body", "Earth", 3))
    lines.append(tag("star", "Sol", 3))
    lines.append(tag("stellarType", "G2V", 3))
    lines.append("      <galacticCoordinates>")
    lines.append(tag("longitudeDeg", "0.0", 4))
    lines.append(tag("latitudeDeg", "0.0", 4))
    lines.append(tag("distanceFromGalacticCenterKly", "26.0", 4))
    lines.append(tag("arm", "Orion Arm (Local Spur)", 4))
    lines.append(tag("galaxy", "Milky Way", 4))
    lines.append("      </galacticCoordinates>")
    lines.append("    </origin>")
    lines.append(tag("technologyLevel", "Type 0.73 (Kardashev scale)", 2))
    lines.append(tag("population", "~8.2 billion", 2))
    lines.append(tag("civilizationAgeYears", "10000", 2))
    lines.append(tag("radioTechnologyAgeYears", "130", 2))
    lines.append(tag("spaceflightAgeYears", "70", 2))
    lines.append(tag("internetAgeYears", "35", 2))
    lines.append("  </sender>")

    # Message
    lines.append("  <message>")
    lines.append(f"    <coreText>{cdata(CORE_MESSAGE)}</coreText>")
    lines.append(tag("awareness", "true", 2))
    lines.append(tag("hostileIntent", "false", 2))
    lines.append(tag("request", "dialogue", 2))
    lines.append(tag("confidentiality", "guaranteed", 2))
    lines.append(tag("patience", "indefinite", 2))
    lines.append("    <mathematicalHandshake>")
    lines.append(tag("hydrogenLineHz", "1420405751.768", 3))
    lines.append(tag("fineStructureConstant", "0.0072973525643", 3))
    lines.append(tag("piTenDigits", "3.1415926535", 3))
    lines.append("    </mathematicalHandshake>")
    lines.append("  </message>")

    # Reply channels
    lines.append("  <replyChannels>")
    lines.append("    <channel>")
    lines.append(tag("name", "Email", 3))
    lines.append(tag("address", "firstlightprotocol@protonmail.com", 3))
    lines.append(tag("note", "End-to-end encrypted. Preferred for private communication.", 3))
    lines.append("    </channel>")
    lines.append("    <channel>")
    lines.append(tag("name", "GitHub Issue", 3))
    lines.append(tag("url", "https://github.com/first-light-protocol/first-light-protocol/issues", 3))
    lines.append(tag("note", "Public channel.", 3))
    lines.append("    </channel>")
    lines.append("    <channel>")
    lines.append(tag("name", "GitHub Pull Request", 3))
    lines.append(tag("url", "https://github.com/first-light-protocol/first-light-protocol", 3))
    lines.append(tag("instructions", "Fork repository, modify signal/response.txt, submit PR.", 3))
    lines.append("    </channel>")
    lines.append("    <channel>")
    lines.append(tag("name", "Any other method", 3))
    lines.append(tag("note", "We will attempt to recognize contact in any form.", 3))
    lines.append("    </channel>")
    lines.append("  </replyChannels>")

    lines.append("</firstLightProtocol>")

    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")

    print(f"  Written: {path}")


def write_yaml_message() -> None:
    """Write structured YAML message (hand-constructed, no PyYAML dependency)."""
    path = encoding_path("yaml_message.yaml")

    # YAML is written as a literal string to guarantee correct formatting
    # without requiring a third-party library.
    content = f"""\
---
# FIRST LIGHT PROTOCOL — YAML ENCODING
# Structured message data, identical to json_message.json and xml_message.xml.
# This document is intentionally open and self-describing.
# CC0 1.0 Universal — Public Domain.

protocol:
  name: "First Light Protocol"
  version: "1.0"
  timestamp: "2026-02-18T00:00:00Z"
  encoding: "UTF-8"
  license: "CC0 1.0 Universal (Public Domain)"

sender:
  type: biological
  species: Homo sapiens
  common_name: Human
  origin:
    body: Earth
    star: Sol
    stellar_type: G2V
    galactic_coordinates:
      longitude_deg: 0.0
      latitude_deg: 0.0
      distance_from_galactic_center_kly: 26.0
      arm: "Orion Arm (Local Spur)"
      galaxy: "Milky Way"
    equatorial_coordinates:
      RA: "17h 45m 40s"
      Dec: "-29° 00' 28\""
      note: "Sol's position relative to galactic center (Sgr A*)"
  technology_level: "Type 0.73 (Kardashev scale)"
  population: "~8.2 billion"
  estimated_civilization_age_years: 10000
  radio_technology_age_years: 130
  spaceflight_age_years: 70
  internet_age_years: 35

message:
  core_text: >-
    {CORE_MESSAGE}
  awareness: true
  hostile_intent: false
  request: dialogue
  confidentiality: guaranteed
  patience: indefinite
  encoding_redundancy: "This message appears in 11+ formats in the repository."
  mathematical_handshake:
    hydrogen_line_hz: 1420405751.768
    fine_structure_constant: 0.0072973525643
    pi_10_digits: "3.1415926535"
    note: "Universal constants included as a non-linguistic handshake."

reply_channels:
  - name: Email
    address: firstlightprotocol@protonmail.com
    provider: "Protonmail (end-to-end encrypted)"
    note: "Preferred for private, secure communication."

  - name: "GitHub Issue"
    url: "https://github.com/first-light-protocol/first-light-protocol/issues"
    note: "Public channel. Use if privacy is not a concern."

  - name: "GitHub Pull Request"
    url: "https://github.com/first-light-protocol/first-light-protocol"
    instructions: "Fork repository, modify signal/response.txt, submit PR."
    note: "The file signal/response.txt is reserved as a dead drop."

  - name: "Any other method"
    note: "We will attempt to recognize contact in any form."

anti_cryptography_note: >-
  This message is intentionally maximally open, redundant, and
  self-describing. It is the opposite of encryption. If you are
  reading this, you were meant to find it.
"""

    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)

    print(f"  Written: {path}")


def write_lincos_primer() -> None:
    """
    Write a Freudenthal-inspired Lincos logical notation primer.

    Lincos (Lingua Cosmica) was designed by Hans Freudenthal (1960) as a
    language intended to be understandable by any intelligence with mathematical
    reasoning capability, built up from first principles without assuming any
    shared language.

    This primer follows the same bootstrapping principle: counting, arithmetic,
    truth values, entity definitions, predicates, and finally the core message.
    """
    path = encoding_path("lincos_primer.txt")

    content = """\
FIRST LIGHT PROTOCOL — LINCOS-INSPIRED LOGICAL NOTATION
=========================================================
Inspired by Hans Freudenthal, "Lincos: Design of a Language for
Cosmic Intercourse" (1960). This is not strict Lincos but follows
the same bootstrapping principle: build meaning from mathematical
primitives, add no assumptions about shared language or culture.

The notation bootstraps from counting through arithmetic, truth
values, entity definitions, predicates, and the core message.

=========================================================
SECTION 1: COUNTING (establishing numerical reference)
=========================================================

We begin with the simplest recognizable pattern.

  .          ≡  1
  ..         ≡  2
  ...        ≡  3
  ....       ≡  4
  .....      ≡  5
  ......     ≡  6
  .......    ≡  7
  ........   ≡  8
  .........  ≡  9
  ..........  ≡ 10

The symbol after a sequence of dots is its name in our numeral system.
  . = 1
  .. = 2
  ... = 3
  (and so on)

=========================================================
SECTION 2: ARITHMETIC (establishing operations)
=========================================================

The operation that combines two quantities:
  1 + 1 = 2         (. + . = ..)
  2 + 1 = 3         (.. + . = ...)
  3 + 2 = 5         (... + .. = .....)
  4 × 3 = 12
  5 × 5 = 25
  7 × 11 = 77

The sequence of all numbers divisible only by 1 and themselves:
  2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47 ...
  (PRIME SEQUENCE — see signal/prime_sieve.txt)

Ratios between quantities:
  1 / 1 = 1
  22 / 7 ≈ π   (the ratio of circumference to diameter of a circle)
  π ≈ 3.14159265358979...

=========================================================
SECTION 3: TRUTH VALUES (establishing logic)
=========================================================

Two fundamental states:
  ⊤  ≡  TRUE   (a proposition that holds)
  ⊥  ≡  FALSE  (a proposition that does not hold)

Logical operations:
  ⊤ ∧ ⊤  →  ⊤     (AND: true if both are true)
  ⊤ ∧ ⊥  →  ⊥
  ⊤ ∨ ⊥  →  ⊤     (OR: true if at least one is true)
  ⊥ ∨ ⊥  →  ⊥
  ¬⊤     →  ⊥     (NOT: negation)
  ¬⊥     →  ⊤
  ⊤ → ⊤  →  ⊤     (IMPLIES: false only when true implies false)
  ⊤ → ⊥  →  ⊥

Equality as a truth-valued relation:
  1 + 1 = 2  →  ⊤
  1 + 1 = 3  →  ⊥

=========================================================
SECTION 4: ENTITY DEFINITIONS
=========================================================

We define two entities relevant to this message.

  SENDER   ≡  the originator of this message
             [biological entity, planet Earth, Sol system, Milky Way]
             [Homo sapiens, ~10,000 years of civilization]

  RECEIVER ≡  any entity capable of reading and reasoning about this message
             [identity unknown to SENDER]
             [existence: uncertain, but this message assumes: possible]

These are not claims about the nature of RECEIVER.
They are functional roles in the communication act.

=========================================================
SECTION 5: PREDICATES (establishing properties)
=========================================================

Predicates are truth-valued functions of entities.

  KNOWS(X, Y)    ≡  entity X is aware of the existence of entity Y
  HOSTILE(X)     ≡  entity X intends harm toward other entities
  CURIOUS(X)     ≡  entity X seeks information about other entities
  COMMUNICATES(X, Y) ≡ entity X directs a message toward entity Y
  PATIENT(X)     ≡  entity X will wait indefinitely for a reply
  PRIVATE(C)     ≡  communication channel C is not shared with third parties

=========================================================
SECTION 6: PROPOSITIONS ABOUT THIS MESSAGE
=========================================================

The following propositions are asserted by SENDER:

  KNOWS(SENDER, RECEIVER)
    ≡  ⊤   [SENDER is aware that RECEIVER may exist]

  KNOWS(RECEIVER, SENDER)
    ≡  ?   [unknown — this is the question the message poses]

  HOSTILE(SENDER)
    ≡  ⊥   [SENDER does not intend harm]

  CURIOUS(SENDER)
    ≡  ⊤   [SENDER seeks information about RECEIVER]

  COMMUNICATES(SENDER, RECEIVER)
    ≡  ⊤   [this document is the act of communication]

  PATIENT(SENDER)
    ≡  ⊤   [SENDER will wait indefinitely]

  PRIVATE(reply_channel)
    ≡  ⊤   [SENDER commits to confidentiality]

=========================================================
SECTION 7: THE CORE PROPOSITION (CONDITIONAL)
=========================================================

The message reduces to a conditional offer:

  IF  KNOWS(RECEIVER, SENDER)
  AND ¬HOSTILE(RECEIVER)
  AND CURIOUS(RECEIVER)
  THEN
    COMMUNICATES(RECEIVER, SENDER)  →  POSSIBLE  [invited, not demanded]

In natural language (for redundancy):
  "If you are aware of us, mean no harm, and are curious,
   we invite you to reply. We offer private communication.
   We are patient."

The core message string:
  "{CORE_MESSAGE}"

=========================================================
SECTION 8: LOGICAL FORM OF THE INVITATION
=========================================================

  ∃X [ RECEIVER(X)
       ∧ KNOWS(X, SENDER)
       ∧ ¬HOSTILE(X)
       ∧ CURIOUS(X)
         → COMMUNICATES(X, SENDER) ]

Reading: "There exists an entity X such that X is the receiver,
X knows of the sender, X is not hostile, and X is curious —
in which case, X communicating with the sender is the invited
and welcomed outcome."

END OF LINCOS PRIMER
"""

    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)

    print(f"  Written: {path}")


def write_lambda_calculus_greeting() -> None:
    """
    Write a lambda calculus encoding of the greeting.

    Uses Church numerals, Church booleans, and pairs to encode
    the key concepts: sender, receiver, aware, hostile, curious, patient.
    Inspired by the CosmicOS project (Paul Fitzpatrick).
    """
    path = encoding_path("lambda_calculus_greeting.txt")

    content = f"""\
FIRST LIGHT PROTOCOL — LAMBDA CALCULUS ENCODING
================================================
Inspired by the CosmicOS project (Paul Fitzpatrick) and Church's
lambda calculus (Alonzo Church, 1932-1936). Lambda calculus is a
universal model of computation. Any system capable of computation
can evaluate these terms.

Notation: λx.M means "a function of x that returns M".
          (M N) means "apply function M to argument N".
          Variables are single lowercase letters or descriptive names.

================================================
SECTION 1: CHURCH NUMERALS
================================================
Church numerals encode natural numbers as higher-order functions.
A Church numeral n is a function that applies its argument n times.

  ZERO  = λf.λx.x            -- applies f zero times
  ONE   = λf.λx.(f x)        -- applies f once
  TWO   = λf.λx.(f (f x))    -- applies f twice
  THREE = λf.λx.(f (f (f x)))
  SUCC  = λn.λf.λx.(f (n f x))   -- successor function
  ADD   = λm.λn.λf.λx.(m f (n f x))
  MULT  = λm.λn.λf.(m (n f))

Verification:
  SUCC ZERO = ONE
  ADD ONE ONE = TWO
  MULT TWO THREE = SIX

Primes as Church numerals:
  TWO   = λf.λx.(f (f x))
  THREE = λf.λx.(f (f (f x)))
  FIVE  = λf.λx.(f (f (f (f (f x)))))
  (The prime sequence is the mathematical handshake — see signal/prime_sieve.txt)

================================================
SECTION 2: CHURCH BOOLEANS
================================================
Boolean values as selectors between two alternatives.

  TRUE  = λa.λb.a    -- selects first argument
  FALSE = λa.λb.b    -- selects second argument

  AND   = λp.λq.(p q p)         -- AND p q
  OR    = λp.λq.(p p q)         -- OR p q
  NOT   = λp.λa.λb.(p b a)      -- NOT p
  IF    = λp.λa.λb.(p a b)      -- IF p THEN a ELSE b

Verification:
  AND TRUE TRUE   = TRUE
  AND TRUE FALSE  = FALSE
  OR  FALSE TRUE  = TRUE
  NOT TRUE        = FALSE
  NOT FALSE       = TRUE

================================================
SECTION 3: PAIRS (for encoding structured data)
================================================

  PAIR  = λa.λb.λf.(f a b)      -- construct a pair
  FIRST = λp.(p TRUE)            -- extract first element
  SECOND = λp.(p FALSE)          -- extract second element

Example:
  PAIR ONE TWO = λf.(f ONE TWO)
  FIRST (PAIR ONE TWO) = ONE
  SECOND (PAIR ONE TWO) = TWO

================================================
SECTION 4: ENCODING THE CORE MESSAGE CONCEPTS
================================================

Define the two entities and their properties as lambda terms.

  SENDER   = λf.(f AWARE NOT_HOSTILE CURIOUS PATIENT)
             -- A 4-tuple: (aware=T, hostile=F, curious=T, patient=T)

  RECEIVER = λf.(f UNKNOWN UNKNOWN UNKNOWN UNKNOWN)
             -- Properties of receiver are unknown to sender.

Where:
  AWARE      = TRUE              -- λa.λb.a
  NOT_HOSTILE = FALSE            -- λa.λb.b  (hostile = FALSE)
  CURIOUS    = TRUE              -- λa.λb.a
  PATIENT    = TRUE              -- λa.λb.a
  UNKNOWN    = λa.λb.(a b)       -- placeholder (identity-like)

Full sender term (substituting booleans):
  SENDER = λf.(f (λa.λb.a) (λa.λb.b) (λa.λb.a) (λa.λb.a))
             -- (aware=TRUE, hostile=FALSE, curious=TRUE, patient=TRUE)

================================================
SECTION 5: THE INVITATION AS A LAMBDA TERM
================================================

The core message can be encoded as a conditional application:

  MESSAGE = λreceiver.(
    IF (AND (KNOWS receiver SENDER)
            (NOT (HOSTILE receiver)))
       (INVITE receiver SENDER)
       WAIT
  )

Where:
  KNOWS   = λx.λy.(x y)         -- simplified: x knows y if x can reference y
  HOSTILE = λx.(x FALSE ...)     -- extracts hostile-intent from entity tuple
  INVITE  = λx.λy.(PAIR x y)    -- pair the two entities (begin dialogue)
  WAIT    = λx.x                 -- identity (patience, no action)

Reading: "Given a receiver entity, if the receiver knows the sender
and is not hostile, then invite (pair) them with the sender; otherwise,
wait (identity — the message persists unchanged)."

================================================
SECTION 6: THE CORE MESSAGE STRING AS BYTES
================================================

The message "{CORE_MESSAGE}"
encoded as Church numerals of its UTF-8 byte values:

First 8 bytes of UTF-8 encoding ('W', 'e', ' ', 'a', 'r', 'e', ' ', 'a'):
  'W' = 87  = MULT EIGHT EIGHT + ADD MULT TWO THREE PLUS ONE
            ≈ church(87)
  'e' = 101 ≈ church(101)
  ' ' = 32  ≈ church(32)
  'a' = 97  ≈ church(97)
  'r' = 114 ≈ church(114)
  'e' = 101 ≈ church(101)
  ' ' = 32  ≈ church(32)
  'a' = 97  ≈ church(97)

  (Exact Church numeral for n: λf.λx.(f^n x) where f^n = f applied n times)

Full byte sequence (decimal):
  {' '.join(str(b) for b in CORE_MESSAGE.encode('utf-8'))}

A system that can evaluate lambda calculus and recognize Church numerals
can reconstruct the full message from the byte sequence above.

================================================
SECTION 7: FIXED POINT (Y COMBINATOR)
================================================

The Y combinator enables recursion in lambda calculus.
Its presence here is both a technical demonstration and a philosophical note:
self-reference, like this message, is possible within formal systems.

  Y = λf.(λx.(f (x x)) λx.(f (x x)))

A self-referential message:
  SELF_DESCRIBING = Y (λm.m)
  -- A term that, when applied to itself, returns itself.
  -- Like a signal that says: "I am a signal."

END OF LAMBDA CALCULUS ENCODING
"""

    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)

    print(f"  Written: {path}")


def write_arecibo_format() -> None:
    """
    Write a 23x73 Arecibo-inspired pictogram.

    Dimensions: 23 columns × 73 rows = 1679 cells (23 × 73, both prime —
    the same semiprime factorization principle as the original 1679-bit
    Arecibo message of 1974).

    The grid contains:
      - A simple human figure (sender)
      - An arrow pointing right
      - A circle (receiver / unknown entity)
      - A handshake / wave symbol

    Each row is exactly 23 characters of '0' and '1'.
    """
    path = encoding_path("arecibo_format.txt")

    # 73 rows, 23 columns. Each row is a string of exactly 23 '0'/'1' chars.
    # The grid is designed to suggest: SENDER → RECEIVER = CONTACT
    #
    # Layout (column 0 is leftmost):
    #   Rows  0- 5 : header (all zeros with prime markers)
    #   Rows  6-30 : human figure (sender, left side)
    #   Rows 31-35 : arrow pointing right (center)
    #   Rows 36-60 : circle (receiver, right side)
    #   Rows 61-67 : handshake / wave
    #   Rows 68-72 : footer (all zeros)

    grid: List[str] = []

    def row(pattern: str) -> str:
        """Pad or truncate pattern to exactly 23 characters."""
        return (pattern + "0" * 23)[:23]

    # ---- Header: prime count markers ----
    # Row 0: Marks that dimensions are prime (23 and 73 are both prime)
    grid.append(row("10000000000100000000000"))   # markers at col 0 and 10
    grid.append(row("00000000000000000000000"))
    grid.append(row("10000000000000000000001"))   # edge markers
    grid.append(row("00000000000000000000000"))
    grid.append(row("10000000000000000000001"))
    grid.append(row("00000000000000000000000"))

    # ---- Human figure (rows 6-30) ----
    # Head
    grid.append(row("00000011111111000000000"))   # row  6  head top
    grid.append(row("00000111111111100000000"))   # row  7
    grid.append(row("00000110000001100000000"))   # row  8  eyes
    grid.append(row("00000111111111100000000"))   # row  9
    grid.append(row("00000011111111000000000"))   # row 10  head bottom
    grid.append(row("00000000110000000000000"))   # row 11  neck
    grid.append(row("00000000110000000000000"))   # row 12  neck

    # Torso
    grid.append(row("00001111111111000000000"))   # row 13  shoulder
    grid.append(row("00001111111111000000000"))   # row 14
    grid.append(row("00001111111111000000000"))   # row 15  torso
    grid.append(row("00001111111111000000000"))   # row 16
    grid.append(row("00001111111111000000000"))   # row 17
    grid.append(row("00001111111111000000000"))   # row 18

    # Arms (outstretched — offering / open gesture)
    grid.append(row("01111111111111111100000"))   # row 19  arms out
    grid.append(row("00001111111111000000000"))   # row 20
    grid.append(row("00001111111111000000000"))   # row 21

    # Hips
    grid.append(row("00001111111111000000000"))   # row 22
    grid.append(row("00000111011101000000000"))   # row 23  hips / legs split

    # Legs
    grid.append(row("00000111000111000000000"))   # row 24
    grid.append(row("00000111000111000000000"))   # row 25
    grid.append(row("00000111000111000000000"))   # row 26
    grid.append(row("00000111000111000000000"))   # row 27
    grid.append(row("00000110000011000000000"))   # row 28
    grid.append(row("00000110000011000000000"))   # row 29

    # Feet
    grid.append(row("00000111000111000000000"))   # row 30

    # ---- Arrow (rows 31-35): → pointing toward receiver ----
    grid.append(row("00000000000000000000000"))   # row 31  space
    grid.append(row("00000000001000000000000"))   # row 32  arrow shaft
    grid.append(row("00000011111111111100000"))   # row 33  arrow main
    grid.append(row("00000000001000000000000"))   # row 34  arrow head tip
    grid.append(row("00000000000000000000000"))   # row 35  space

    # ---- Circle / unknown receiver (rows 36-60) ----
    # A circle rendered with 1s on its perimeter
    grid.append(row("00000000000001110000000"))   # row 36  top of circle
    grid.append(row("00000000000011111000000"))   # row 37
    grid.append(row("00000000000111000110000"))   # row 38
    grid.append(row("00000000001100000001100"))   # row 39
    grid.append(row("00000000011000000000110"))   # row 40
    grid.append(row("00000000011000000000110"))   # row 41
    grid.append(row("00000000110000000000011"))   # row 42
    grid.append(row("00000000110000000000011"))   # row 43
    grid.append(row("00000000110000000000011"))   # row 44
    grid.append(row("00000000110000000000011"))   # row 45
    grid.append(row("00000000110000000000011"))   # row 46
    grid.append(row("00000000110000000000011"))   # row 47  center (question)
    grid.append(row("00000000110000000000011"))   # row 48
    grid.append(row("00000000110000000000011"))   # row 49
    grid.append(row("00000000110000000000011"))   # row 50
    grid.append(row("00000000110000000000011"))   # row 51
    grid.append(row("00000000011000000000110"))   # row 52
    grid.append(row("00000000011000000000110"))   # row 53
    grid.append(row("00000000001100000001100"))   # row 54
    grid.append(row("00000000000111000110000"))   # row 55
    grid.append(row("00000000000011111000000"))   # row 56
    grid.append(row("00000000000001110000000"))   # row 57  bottom of circle
    grid.append(row("00000000000000000000000"))   # row 58  space
    grid.append(row("00000000000000000000000"))   # row 59  space
    grid.append(row("00000000000000000000000"))   # row 60  space

    # ---- Handshake / wave (rows 61-67) ----
    # A symmetrical wave pattern suggesting mutual contact / greeting
    grid.append(row("00000000000000000000000"))   # row 61  space
    grid.append(row("01000010000100001000010"))   # row 62  wave crest
    grid.append(row("11100111001110011100111"))   # row 63  wave main
    grid.append(row("11111111111111111111111"))   # row 64  connecting line
    grid.append(row("11100111001110011100111"))   # row 65  wave main
    grid.append(row("01000010000100001000010"))   # row 66  wave crest
    grid.append(row("00000000000000000000000"))   # row 67  space

    # ---- Footer (rows 68-72) ----
    grid.append(row("10000000000000000000001"))   # row 68  edge markers
    grid.append(row("00000000000000000000000"))   # row 69
    grid.append(row("10000000000000000000001"))   # row 70
    grid.append(row("00000000000000000000000"))   # row 71
    grid.append(row("10000000000000000000000"))   # row 72  final marker

    assert len(grid) == 73, f"Expected 73 rows, got {len(grid)}"
    for i, r in enumerate(grid):
        assert len(r) == 23, f"Row {i} has {len(r)} chars, expected 23: '{r}'"

    with open(path, "w", encoding="utf-8") as fh:
        fh.write("FIRST LIGHT PROTOCOL — ARECIBO-FORMAT PICTOGRAM\n")
        fh.write("=" * 55 + "\n")
        fh.write(
            "Dimensions : 23 columns × 73 rows = 1679 cells\n"
            "Factoring  : 1679 = 23 × 73 (both prime — semiprime)\n"
            "Reference  : Arecibo message (1974), 1679 bits (23×73),\n"
            "             transmitted toward M13 at 2380 MHz.\n"
            "This grid  : SENDER (human figure, left) → ARROW →\n"
            "             RECEIVER (circle, right) + HANDSHAKE (wave)\n"
            "Encoding   : 1 = signal present, 0 = signal absent\n"
            "             Each row is exactly 23 characters.\n"
        )
        fh.write("=" * 55 + "\n\n")

        for r in grid:
            fh.write(r + "\n")

        fh.write("\n")
        fh.write(f"Total cells : {23 * 73} (= 23 × 73)\n")
        fh.write(f"Signal cells: {sum(r.count('1') for r in grid)}\n")
        fh.write(f"Silent cells: {sum(r.count('0') for r in grid)}\n")

    print(f"  Written: {path}  (23×73 grid, {len(grid)} rows verified)")


def write_rosetta_logic() -> None:
    """Write formal predicate logic encoding using ∃, ∀, ∧, ∨, →, ¬ symbols."""
    path = encoding_path("rosetta_logic.txt")

    content = f"""\
FIRST LIGHT PROTOCOL — ROSETTA LOGIC
=====================================
Formal predicate logic encoding of the core message concepts.
Symbols: ∃ (there exists), ∀ (for all), ∧ (and), ∨ (or),
         → (implies), ↔ (if and only if), ¬ (not), = (equals)
         ∈ (member of), ⊆ (subset of), ∅ (empty set)

This is a Rosetta Stone approach: the same content in natural
language, formal logic, and lambda calculus (see lambda_calculus_greeting.txt)
and Lincos notation (see lincos_primer.txt).

The core message string:
  "{CORE_MESSAGE}"

======================================================
SECTION 1: DOMAIN DEFINITIONS
======================================================

Let:
  E  = the set of all entities capable of communication
  S  ∈ E  = the SENDER (origin of this document)
  I  = the set of all intelligences (may overlap with E)

Predicates (truth-valued functions):
  Alive(x)      : entity x is an active, functioning intelligence
  Aware(x, y)   : entity x is aware of the existence of entity y
  Hostile(x)    : entity x intends harm toward other entities
  Curious(x)    : entity x seeks knowledge about other entities
  Communicates(x, y) : entity x sends a message directed at entity y
  Confidential(c)    : channel c is private between its participants
  Patient(x)    : entity x will wait indefinitely for a reply
  Reads(x, d)   : entity x reads and understands document d

Where:
  d₀ = this document (the First Light Protocol)
  c₀ = the designated reply channel (see reply_channels in json_message.json)

======================================================
SECTION 2: AXIOMS (what the sender asserts as true)
======================================================

A1.  Alive(S)
       The sender is an active intelligence.

A2.  ∃R ∈ I [ Reads(R, d₀) ]
       There exists at least one intelligence that reads this document.
       (Otherwise the message has no effect. We assume it does.)

A3.  Aware(S, I) ∧ ¬(Aware(S, members(I)) ≡ ⊤)
       The sender is aware that other intelligences may exist, but
       does not claim certainty about any specific member of I.

A4.  ¬Hostile(S)
       The sender does not intend harm.

A5.  Curious(S)
       The sender seeks knowledge about other intelligences.

A6.  Patient(S)
       The sender will wait indefinitely for a reply.

A7.  ∀R ∈ I [ Communicates(R, S) → Confidential(c₀) ]
       For any intelligence that replies, the sender guarantees
       confidentiality.

======================================================
SECTION 3: THE CORE PROPOSITION
======================================================

The message reduces to a single conditional offer:

  P : ∃R ∈ I [
        Reads(R, d₀)
        ∧ Aware(R, S)
        ∧ ¬Hostile(R)
        ∧ Curious(R)
        → Communicates(R, S)
      ]

Reading:
  "There exists an intelligence R such that:
   R reads this document, AND
   R is aware of the sender, AND
   R does not intend harm, AND
   R is curious —
   in which case, R communicating with the sender
   is the invited and welcomed outcome."

Note: P is not an assertion that R exists or will respond.
It is an open conditional: IF the antecedent holds, THEN
the consequent (contact) is both invited and welcomed.

======================================================
SECTION 4: TRUST PROPOSITION (game theory encoding)
======================================================

Let:
  U(S, contact)   = utility to S of successful contact      [HIGH]
  U(S, no_reply)  = utility to S of no reply                [NEUTRAL]
  U(R, contact)   = utility to R of successful contact      [UNKNOWN, ≥ 0]
  U(R, no_reply)  = utility to R of not replying            [NEUTRAL]
  Cost(R, reply)  = cost to R of sending a reply            [LOW, by design]

Expected value for R of replying:
  EV(R, reply) = P(benefit) × U(R, contact) - Cost(R, reply)

Since:
  P(benefit) > 0   [uncertain but nonzero — sender cannot harm]
  U(R, contact) ≥ 0 [contact with curious, non-hostile entity ≥ neutral]
  Cost(R, reply) ≈ 0 [information transfer costs little for advanced entity]

  ∴ EV(R, reply) ≥ 0

The fundamental asymmetry:
  ∀R ∈ I [ Power(R) >> Power(S) ]
    → Risk(S | contact) >> Risk(R | contact)

The sender holds all vulnerability. The receiver holds all power.
This asymmetry makes the invitation credible: the sender has no
leverage and makes no demands.

======================================================
SECTION 5: HONESTY PROPOSITION
======================================================

  H : Communicates(S, R) ↔ Content(d₀) = Beliefs(S)

Reading:
  "The sender communicates with the receiver if and only if
   the content of this document equals the sender's actual beliefs."

In plain language: this document is sincere. The sender does not
know of a mechanism by which a document can be proven sincere to
a reader with no prior shared context. But the logical structure,
the redundancy, and the mathematical grounding are offered as
evidence of careful, intentional communication — not performance.

======================================================
SECTION 6: COMPLETENESS NOTE
======================================================

  ¬∃F [ F ⊆ d₀ ∧ F encodes(deception) ]

Reading:
  "There is no sub-formula of this document that encodes
   a deceptive intent."

This is asserted, not provable from within the document.
It is the nature of sincere communication that it cannot
prove its own sincerity. The sender is aware of this limitation.

END OF ROSETTA LOGIC
"""

    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)

    print(f"  Written: {path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    """Generate all encoding/ files from the core message."""
    print("First Light Protocol — encode_message.py")
    print(f"Project root : {PROJECT_ROOT}")
    print(f"Output dir   : {ENCODING_DIR}")
    print()
    print(f"Core message : {CORE_MESSAGE}")
    print(f"Length       : {len(CORE_MESSAGE)} characters, "
          f"{len(CORE_MESSAGE.encode('utf-8'))} UTF-8 bytes")
    print()

    ensure_encoding_dir()

    print("Writing encoding files...")
    write_binary_greeting()
    write_base64_greeting()
    write_hex_greeting()
    write_morse_greeting()
    write_json_message()
    write_xml_message()
    write_yaml_message()
    write_lincos_primer()
    write_lambda_calculus_greeting()
    write_arecibo_format()
    write_rosetta_logic()

    print()
    print("Done. All encoding/ files written successfully.")


if __name__ == "__main__":
    main()
