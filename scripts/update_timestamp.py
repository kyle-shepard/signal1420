"""
update_timestamp.py — First Light Protocol

Appends a new entry to proofs/timestamp_chain.txt. Each entry contains:
  - An ISO 8601 UTC timestamp
  - A SHA-256 hash of the message string "First Light Protocol timestamp: {iso_timestamp}"
  - The original message string that was hashed

If the file does not exist, it is created with an explanatory header first.

Usage:
    python scripts/update_timestamp.py

The timestamp chain is a cryptographic proof-of-attention: an irregular
series of dated entries showing that a biological intelligence periodically
and deliberately updates the record. Each entry is self-verifiable.

Exit codes:
    0 — entry appended successfully
    1 — an error occurred
"""

import hashlib
import os
import sys
from datetime import datetime, timezone


# ---------------------------------------------------------------------------
# Path setup
# ---------------------------------------------------------------------------

SCRIPT_DIR: str = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT: str = os.path.dirname(SCRIPT_DIR)
PROOFS_DIR: str = os.path.join(PROJECT_ROOT, "proofs")
CHAIN_FILE: str = os.path.join(PROOFS_DIR, "timestamp_chain.txt")


# ---------------------------------------------------------------------------
# Core logic
# ---------------------------------------------------------------------------

HASH_TEMPLATE: str = "First Light Protocol timestamp: {iso_timestamp}"

FILE_HEADER: str = """\
FIRST LIGHT PROTOCOL — TIMESTAMP CHAIN
========================================
This file is an irregular cryptographic timestamp chain.

Purpose:
  To demonstrate that a biological intelligence is actively maintaining
  this repository over time. Each entry is made manually (or via a
  scheduled automated job running the update_timestamp.py script).
  The irregular cadence — not perfectly regular, not random — is itself
  a signal of intentionality.

Entry format:
  TIMESTAMP  : ISO 8601 UTC timestamp of when the entry was created
  MESSAGE    : The string that was hashed (human-readable, self-documenting)
  SHA-256    : SHA-256 hash of the MESSAGE string (UTF-8 encoded)

Verification:
  For any entry, you can verify the hash with:
    echo -n "MESSAGE_STRING" | sha256sum
  or in Python:
    import hashlib
    hashlib.sha256("MESSAGE_STRING".encode("utf-8")).hexdigest()

Each entry is independent — this is not a blockchain. There is no
chained dependency between entries. The chain's value is in the
accumulating record of regular updates, not in cryptographic linking.

Anti-cryptography note:
  This file is intentionally maximally transparent. The hash is not
  a secret. The message is not encrypted. The purpose is proof of
  continued human attention, not security.

========================================
ENTRIES BELOW (most recent last)
========================================

"""


def compute_hash(message: str) -> str:
    """
    Compute the SHA-256 hash of a UTF-8 encoded message string.

    Args:
        message: The string to hash.

    Returns:
        Lowercase hexadecimal SHA-256 digest (64 characters).

    Example:
        >>> compute_hash("hello")
        '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824'
    """
    return hashlib.sha256(message.encode("utf-8")).hexdigest()


def get_utc_timestamp() -> str:
    """
    Return the current UTC time as an ISO 8601 string with second precision.

    Returns:
        String in the format 'YYYY-MM-DDTHH:MM:SSZ', e.g. '2026-02-18T03:00:00Z'.
    """
    now = datetime.now(timezone.utc)
    return now.strftime("%Y-%m-%dT%H:%M:%SZ")


def ensure_proofs_dir() -> None:
    """Create the proofs/ directory if it does not already exist."""
    os.makedirs(PROOFS_DIR, exist_ok=True)


def file_exists() -> bool:
    """Return True if the timestamp chain file already exists and has content."""
    return os.path.isfile(CHAIN_FILE) and os.path.getsize(CHAIN_FILE) > 0


def write_header() -> None:
    """Create the timestamp chain file and write the explanatory header."""
    with open(CHAIN_FILE, "w", encoding="utf-8") as fh:
        fh.write(FILE_HEADER)
    print(f"  Created new file with header: {CHAIN_FILE}")


def append_entry(iso_timestamp: str, message: str, sha256_hash: str) -> None:
    """
    Append a single formatted entry to the timestamp chain file.

    Args:
        iso_timestamp: ISO 8601 UTC timestamp string.
        message:       The message string that was hashed.
        sha256_hash:   The SHA-256 hex digest of the message.
    """
    entry_lines = [
        "",
        f"TIMESTAMP  : {iso_timestamp}",
        f"MESSAGE    : {message}",
        f"SHA-256    : {sha256_hash}",
        "",
        "---",
    ]
    entry = "\n".join(entry_lines) + "\n"

    with open(CHAIN_FILE, "a", encoding="utf-8") as fh:
        fh.write(entry)


def count_existing_entries() -> int:
    """
    Count the number of existing timestamp entries in the chain file.

    Entries are identified by lines starting with 'TIMESTAMP  :'.

    Returns:
        Number of existing entries.
    """
    if not file_exists():
        return 0

    count = 0
    with open(CHAIN_FILE, "r", encoding="utf-8") as fh:
        for line in fh:
            if line.startswith("TIMESTAMP  :"):
                count += 1
    return count


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    """Append a new timestamp entry to the chain."""
    print("First Light Protocol — update_timestamp.py")
    print(f"Project root : {PROJECT_ROOT}")
    print(f"Chain file   : {CHAIN_FILE}")
    print()

    try:
        ensure_proofs_dir()

        # Create the file with a header if it doesn't exist yet
        is_new_file = not file_exists()
        if is_new_file:
            print("File does not exist. Creating with header...")
            write_header()

        # Build the timestamp entry
        iso_timestamp = get_utc_timestamp()
        message = HASH_TEMPLATE.format(iso_timestamp=iso_timestamp)
        sha256_hash = compute_hash(message)

        # Count entries before appending (for reporting)
        existing_count = count_existing_entries()

        # Append the entry
        append_entry(iso_timestamp, message, sha256_hash)

        new_count = existing_count + 1

        print(f"Timestamp    : {iso_timestamp}")
        print(f"Message      : {message}")
        print(f"SHA-256      : {sha256_hash}")
        print()
        print(f"Entry #{new_count} appended to: {CHAIN_FILE}")

        if is_new_file:
            print()
            print("Note: This is the first entry. The timestamp chain has been initialized.")
            print("Run this script again (or via GitHub Actions) to add subsequent entries.")

        sys.exit(0)

    except OSError as exc:
        print(f"ERROR: Could not write to {CHAIN_FILE}: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
