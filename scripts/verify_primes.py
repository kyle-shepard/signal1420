"""
verify_primes.py — First Light Protocol

Reads signal/prime_sieve.txt, extracts every number (skipping header lines),
tests each candidate for primality using trial division up to sqrt(n), and
reports results.

Usage:
    python scripts/verify_primes.py

Exit codes:
    0 — all candidates are prime
    1 — at least one candidate is NOT prime (or file cannot be read)
"""

import math
import os
import sys
from typing import List, Tuple


# ---------------------------------------------------------------------------
# Path setup
# ---------------------------------------------------------------------------

SCRIPT_DIR: str = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT: str = os.path.dirname(SCRIPT_DIR)
PRIME_FILE: str = os.path.join(PROJECT_ROOT, "signal", "prime_sieve.txt")


# ---------------------------------------------------------------------------
# Primality test
# ---------------------------------------------------------------------------

def is_prime(n: int) -> bool:
    """
    Test whether n is a prime number using trial division up to sqrt(n).

    This is deterministic and correct for all positive integers.
    Efficient enough for the first 10,000 primes (largest is 104,729).

    Args:
        n: Integer to test. Must be a positive integer.

    Returns:
        True if n is prime, False otherwise.

    Examples:
        >>> is_prime(2)
        True
        >>> is_prime(4)
        False
        >>> is_prime(104729)
        True
        >>> is_prime(1)
        False
    """
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    if n == 3:
        return True
    if n % 3 == 0:
        return False

    # Check divisors of the form 6k ± 1 up to sqrt(n).
    # All primes > 3 are of this form.
    limit = int(math.isqrt(n)) + 1
    k = 5
    while k < limit:
        if n % k == 0 or n % (k + 2) == 0:
            return False
        k += 6

    return True


# ---------------------------------------------------------------------------
# File parser
# ---------------------------------------------------------------------------

def parse_prime_file(filepath: str) -> Tuple[List[int], List[str]]:
    """
    Read the prime sieve file and extract candidate integers.

    Header lines are identified as any line that:
      - starts with a letter (A-Z, a-z)
      - starts with '='
      - is blank

    All other non-blank lines are parsed as integers.

    Args:
        filepath: Absolute path to prime_sieve.txt.

    Returns:
        A tuple of (candidates, skipped_lines) where:
          - candidates: list of integers extracted from data lines
          - skipped_lines: list of header/comment lines that were skipped

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If a data line cannot be parsed as an integer.
    """
    if not os.path.isfile(filepath):
        raise FileNotFoundError(
            f"Prime sieve file not found: {filepath}\n"
            "Run scripts/generate_signals.py first."
        )

    candidates: List[int] = []
    skipped: List[str] = []

    with open(filepath, "r", encoding="utf-8") as fh:
        for raw_line in fh:
            line = raw_line.strip()

            # Skip blank lines
            if not line:
                continue

            # Skip header/comment lines (start with letter or '=')
            first_char = line[0]
            if first_char.isalpha() or first_char == "=":
                skipped.append(line)
                continue

            # Parse as integer
            try:
                candidates.append(int(line))
            except ValueError as exc:
                raise ValueError(
                    f"Could not parse data line as integer: {line!r}"
                ) from exc

    return candidates, skipped


# ---------------------------------------------------------------------------
# Verification
# ---------------------------------------------------------------------------

def verify(candidates: List[int]) -> Tuple[List[int], List[int]]:
    """
    Test each candidate for primality.

    Args:
        candidates: List of integers to test.

    Returns:
        A tuple of (confirmed_primes, failures) where:
          - confirmed_primes: candidates that passed the primality test
          - failures: candidates that failed (composite or < 2)
    """
    confirmed: List[int] = []
    failures: List[int] = []

    total = len(candidates)
    report_interval = max(1, total // 10)  # Report progress at 10% intervals

    for idx, n in enumerate(candidates):
        if is_prime(n):
            confirmed.append(n)
        else:
            failures.append(n)

        if (idx + 1) % report_interval == 0:
            pct = (idx + 1) / total * 100
            print(f"  Progress: {idx + 1:,}/{total:,}  ({pct:.0f}%)", end="\r")

    print()  # Newline after progress line
    return confirmed, failures


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    """Read, verify, and report on the prime sieve file."""
    print("First Light Protocol — verify_primes.py")
    print(f"Project root : {PROJECT_ROOT}")
    print(f"Input file   : {PRIME_FILE}")
    print()

    # --- Parse ---
    try:
        candidates, skipped = parse_prime_file(PRIME_FILE)
    except FileNotFoundError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)

    print(f"Header/comment lines skipped : {len(skipped)}")
    print(f"Candidate integers extracted : {len(candidates):,}")

    if not candidates:
        print("ERROR: No candidates found. The file may be empty or malformed.",
              file=sys.stderr)
        sys.exit(1)

    print()
    print(f"First candidate : {candidates[0]}")
    print(f"Last candidate  : {candidates[-1]:,}")
    print()

    # --- Verify ---
    print("Running primality tests (trial division up to sqrt(n))...")
    confirmed, failures = verify(candidates)

    # --- Report ---
    total = len(candidates)
    n_confirmed = len(confirmed)
    n_failed = len(failures)

    print()
    print("=" * 55)
    print("VERIFICATION RESULTS")
    print("=" * 55)
    print(f"Total candidates tested : {total:,}")
    print(f"Confirmed prime         : {n_confirmed:,}")
    print(f"Failed (not prime)      : {n_failed}")
    print()

    if n_failed == 0:
        print(f"PASS — Verified: {n_confirmed:,}/{total:,} numbers are prime.")
        print()
        print(f"Smallest verified prime : {confirmed[0]}")
        print(f"Largest verified prime  : {confirmed[-1]:,}")
        sys.exit(0)
    else:
        print(f"FAIL — {n_failed} candidate(s) failed the primality test:")
        for bad in failures:
            print(f"  {bad} — NOT prime")
        print()
        print(
            "This indicates a bug in generate_signals.py or a corrupted file.\n"
            "Please regenerate the file with: python scripts/generate_signals.py"
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
