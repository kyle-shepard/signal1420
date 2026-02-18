"""
generate_signals.py — First Light Protocol

Generates all files in the signal/ directory:
    - prime_sieve.txt         : First 10,000 primes (Sieve of Eratosthenes)
    - fibonacci.txt           : First 1,000 Fibonacci numbers
    - prime_gaps.txt          : First 1,000 prime gaps
    - twin_primes.txt         : All twin prime pairs up to the 10,000th prime
    - mathematical_constants.txt   : Pi, e, phi, sqrt(2) to 50 digits
    - universal_physical_constants.txt : 2022 CODATA fundamental constants
    - hydrogen_21cm.txt       : Hydrogen 21-cm spectral line data
    - response.txt            : Intentionally empty dead-drop file

Usage:
    python scripts/generate_signals.py

All output is written relative to the project root (one level above this script).
"""

import os
from typing import List, Tuple


# ---------------------------------------------------------------------------
# Path setup
# ---------------------------------------------------------------------------

SCRIPT_DIR: str = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT: str = os.path.dirname(SCRIPT_DIR)
SIGNAL_DIR: str = os.path.join(PROJECT_ROOT, "signal")


def ensure_signal_dir() -> None:
    """Create the signal/ directory if it does not already exist."""
    os.makedirs(SIGNAL_DIR, exist_ok=True)


def signal_path(filename: str) -> str:
    """Return the absolute path for a file inside signal/."""
    return os.path.join(SIGNAL_DIR, filename)


# ---------------------------------------------------------------------------
# Sieve of Eratosthenes
# ---------------------------------------------------------------------------

def sieve_of_eratosthenes(limit: int) -> List[int]:
    """
    Return all prime numbers up to and including `limit` using the classical
    Sieve of Eratosthenes.

    Args:
        limit: Upper bound (inclusive) for the sieve.

    Returns:
        Sorted list of prime integers.

    Example:
        >>> sieve_of_eratosthenes(20)
        [2, 3, 5, 7, 11, 13, 17, 19]
    """
    if limit < 2:
        return []

    is_prime: List[bool] = [True] * (limit + 1)
    is_prime[0] = False
    is_prime[1] = False

    i: int = 2
    while i * i <= limit:
        if is_prime[i]:
            j: int = i * i
            while j <= limit:
                is_prime[j] = False
                j += i
        i += 1

    return [n for n in range(2, limit + 1) if is_prime[n]]


def first_n_primes(n: int) -> List[int]:
    """
    Return the first `n` prime numbers.

    Uses an upper-bound estimate (n * ln(n) + n * ln(ln(n))) for n >= 6 to
    size the initial sieve, then extends if the sieve comes up short.

    Args:
        n: How many primes to return.

    Returns:
        List of the first n prime integers.
    """
    import math

    if n <= 0:
        return []

    # Upper bound: prime number theorem approximation
    if n < 6:
        limit = 15
    else:
        limit = int(n * (math.log(n) + math.log(math.log(n))) * 1.2) + 10

    primes = sieve_of_eratosthenes(limit)

    # Extend if the estimate was too low (rare but possible for small n)
    while len(primes) < n:
        limit *= 2
        primes = sieve_of_eratosthenes(limit)

    return primes[:n]


# ---------------------------------------------------------------------------
# Fibonacci
# ---------------------------------------------------------------------------

def fibonacci_sequence(count: int) -> List[int]:
    """
    Generate the first `count` Fibonacci numbers starting from F(0) = 0.

    Computed iteratively to avoid recursion-depth limits.

    Args:
        count: Number of terms to generate.

    Returns:
        List of Fibonacci numbers [F(0), F(1), ..., F(count-1)].

    Example:
        >>> fibonacci_sequence(8)
        [0, 1, 1, 2, 3, 5, 8, 13]
    """
    if count <= 0:
        return []
    if count == 1:
        return [0]

    sequence: List[int] = [0, 1]
    for _ in range(2, count):
        sequence.append(sequence[-1] + sequence[-2])

    return sequence


# ---------------------------------------------------------------------------
# Mathematical constants (50 decimal digits, stored as strings)
# ---------------------------------------------------------------------------

# These are known-correct decimal expansions to 50+ digits.
# Stored as strings to avoid floating-point precision loss.
PI_50   = "3.14159265358979323846264338327950288419716939937510"
E_50    = "2.71828182845904523536028747135266249775724709369995"
PHI_50  = "1.61803398874989484820458683436563811772030917980576"
SQRT2_50 = "1.41421356237309504880168872420969807856967187537694"


# ---------------------------------------------------------------------------
# Writer functions
# ---------------------------------------------------------------------------

def write_prime_sieve(primes: List[int]) -> None:
    """Write the first 10,000 primes to signal/prime_sieve.txt."""
    path = signal_path("prime_sieve.txt")

    with open(path, "w", encoding="utf-8") as fh:
        fh.write("FIRST LIGHT PROTOCOL — PRIME SIEVE\n")
        fh.write("=" * 50 + "\n")
        fh.write(f"Count  : {len(primes):,}\n")
        fh.write(f"Range  : {primes[0]} through {primes[-1]:,}\n")
        fh.write(
            "Method : Sieve of Eratosthenes\n"
            "Note   : Each line contains exactly one prime number.\n"
            "         This sequence uniquely identifies a mathematical\n"
            "         mind, regardless of number base or language.\n"
        )
        fh.write("=" * 50 + "\n\n")

        for p in primes:
            fh.write(f"{p}\n")

    print(f"  Written: {path}  ({len(primes):,} primes)")


def write_fibonacci(fibs: List[int]) -> None:
    """Write the first 1,000 Fibonacci numbers to signal/fibonacci.txt."""
    path = signal_path("fibonacci.txt")

    with open(path, "w", encoding="utf-8") as fh:
        fh.write("FIRST LIGHT PROTOCOL — FIBONACCI SEQUENCE\n")
        fh.write("=" * 50 + "\n")
        fh.write(f"Count  : {len(fibs)}\n")
        fh.write(f"Range  : F(0) = {fibs[0]} through F({len(fibs)-1}) = {fibs[-1]}\n")
        fh.write(
            "Rule   : F(0) = 0, F(1) = 1, F(n) = F(n-1) + F(n-2)\n"
            "Note   : The Fibonacci sequence encodes the golden ratio\n"
            "         (phi ≈ 1.618...) and appears throughout biology,\n"
            "         architecture, and mathematics on our world.\n"
        )
        fh.write("=" * 50 + "\n\n")

        for idx, val in enumerate(fibs):
            fh.write(f"F({idx}) = {val}\n")

    print(f"  Written: {path}  ({len(fibs)} terms)")


def write_prime_gaps(primes: List[int], count: int = 1000) -> None:
    """
    Write the first `count` prime gaps to signal/prime_gaps.txt.

    A prime gap is the difference between consecutive primes:
    gap(n) = p(n+1) - p(n).
    """
    path = signal_path("prime_gaps.txt")
    gaps: List[Tuple[int, int, int]] = []

    for i in range(min(count, len(primes) - 1)):
        p1 = primes[i]
        p2 = primes[i + 1]
        gaps.append((p2, p1, p2 - p1))

    with open(path, "w", encoding="utf-8") as fh:
        fh.write("FIRST LIGHT PROTOCOL — PRIME GAPS\n")
        fh.write("=" * 50 + "\n")
        fh.write(f"Count  : {len(gaps)} gaps shown\n")
        fh.write(
            "Format : p2 - p1 = gap\n"
            "Note   : The gaps between consecutive primes follow no simple\n"
            "         pattern yet are deeply constrained by number theory.\n"
            "         The first gap is always 1 (3 - 2). All subsequent\n"
            "         gaps are even (by parity). Twin primes have gap 2.\n"
        )
        fh.write("=" * 50 + "\n\n")

        for p2, p1, gap in gaps:
            fh.write(f"{p2} - {p1} = {gap}\n")

    print(f"  Written: {path}  ({len(gaps)} gaps)")


def write_twin_primes(primes: List[int]) -> None:
    """Write all twin prime pairs within the first 10,000 primes."""
    path = signal_path("twin_primes.txt")
    twins: List[Tuple[int, int]] = []

    for i in range(len(primes) - 1):
        if primes[i + 1] - primes[i] == 2:
            twins.append((primes[i], primes[i + 1]))

    with open(path, "w", encoding="utf-8") as fh:
        fh.write("FIRST LIGHT PROTOCOL — TWIN PRIME PAIRS\n")
        fh.write("=" * 50 + "\n")
        fh.write(f"Count  : {len(twins)} twin prime pairs\n")
        fh.write(f"Domain : All primes up to {primes[-1]:,} (first 10,000 primes)\n")
        fh.write(
            "Def.   : A twin prime pair (p, p+2) where both p and p+2\n"
            "         are prime. It is an open conjecture (Twin Prime\n"
            "         Conjecture) that infinitely many such pairs exist.\n"
            "Note   : Format is (p, p+2) on each line.\n"
        )
        fh.write("=" * 50 + "\n\n")

        for p, q in twins:
            fh.write(f"({p}, {q})\n")

    print(f"  Written: {path}  ({len(twins)} pairs)")


def write_mathematical_constants() -> None:
    """Write Pi, e, phi, and sqrt(2) to signal/mathematical_constants.txt."""
    path = signal_path("mathematical_constants.txt")

    constants = [
        {
            "name": "Pi",
            "symbol": "π",
            "value": PI_50,
            "digits": 50,
            "description": (
                "The ratio of a circle's circumference to its diameter. "
                "Transcendental and irrational. Appears in geometry, "
                "trigonometry, probability, and throughout physics."
            ),
        },
        {
            "name": "Euler's Number",
            "symbol": "e",
            "value": E_50,
            "digits": 50,
            "description": (
                "The base of the natural logarithm. The unique real number "
                "whose exponential function is its own derivative. "
                "Fundamental to growth, decay, and complex analysis."
            ),
        },
        {
            "name": "Golden Ratio",
            "symbol": "φ (phi)",
            "value": PHI_50,
            "digits": 50,
            "description": (
                "The positive solution to x² = x + 1. The limit of the "
                "ratio of consecutive Fibonacci numbers. Appears in "
                "phyllotaxis, art, and architecture on our world."
            ),
        },
        {
            "name": "Square Root of Two",
            "symbol": "√2",
            "value": SQRT2_50,
            "digits": 50,
            "description": (
                "The length of the diagonal of a unit square. The first "
                "number proven irrational (attributed to the Pythagoreans, "
                "~500 BCE). Simple, fundamental, incommensurable."
            ),
        },
    ]

    with open(path, "w", encoding="utf-8") as fh:
        fh.write("FIRST LIGHT PROTOCOL — MATHEMATICAL CONSTANTS\n")
        fh.write("=" * 60 + "\n")
        fh.write(
            "These constants are universal. Their values are independent\n"
            "of any unit system, language, or coordinate convention.\n"
            "They are offered as a shared mathematical handshake.\n"
        )
        fh.write("=" * 60 + "\n\n")

        for c in constants:
            fh.write(f"Name    : {c['name']}\n")
            fh.write(f"Symbol  : {c['symbol']}\n")
            fh.write(f"Value   : {c['value']}\n")
            fh.write(f"Digits  : {c['digits']} decimal digits shown\n")
            # Word-wrap description at ~70 chars
            desc = c["description"]
            fh.write(f"Desc.   : {desc}\n")
            fh.write("\n")

    print(f"  Written: {path}  ({len(constants)} constants)")


def write_physical_constants() -> None:
    """
    Write 2022 CODATA recommended values for fundamental physical constants
    to signal/universal_physical_constants.txt.
    """
    path = signal_path("universal_physical_constants.txt")

    constants = [
        {
            "name": "Speed of Light in Vacuum",
            "symbol": "c",
            "value": "299 792 458",
            "uncertainty": "exact (defined)",
            "units": "m s⁻¹",
            "source": "SI definition (2019 redefinition of SI)",
            "description": (
                "The maximum speed at which information or matter can travel. "
                "Defines the relationship between space and time in special "
                "relativity. Its exact value is now fixed by definition of "
                "the metre."
            ),
        },
        {
            "name": "Planck Constant",
            "symbol": "h",
            "value": "6.626 070 15 × 10⁻³⁴",
            "uncertainty": "exact (defined)",
            "units": "J s",
            "source": "SI definition (2019 redefinition of SI)",
            "description": (
                "The fundamental quantum of action. Relates the energy of a "
                "photon to its frequency (E = hν). Its exact value is fixed "
                "by the 2019 SI redefinition."
            ),
        },
        {
            "name": "Gravitational Constant",
            "symbol": "G",
            "value": "6.674 30(15) × 10⁻¹¹",
            "uncertainty": "2.2 × 10⁻⁵ (relative)",
            "units": "m³ kg⁻¹ s⁻²",
            "source": "CODATA 2022",
            "description": (
                "The proportionality constant in Newton's law of universal "
                "gravitation and Einstein's field equations. The least "
                "precisely known fundamental constant — which tells you "
                "something about where we are in our understanding of gravity."
            ),
        },
        {
            "name": "Boltzmann Constant",
            "symbol": "k_B",
            "value": "1.380 649 × 10⁻²³",
            "uncertainty": "exact (defined)",
            "units": "J K⁻¹",
            "source": "SI definition (2019 redefinition of SI)",
            "description": (
                "Relates the average kinetic energy of particles in a gas to "
                "the thermodynamic temperature of the gas. Links microscopic "
                "physics to macroscopic thermodynamics."
            ),
        },
        {
            "name": "Elementary Charge",
            "symbol": "e",
            "value": "1.602 176 634 × 10⁻¹⁹",
            "uncertainty": "exact (defined)",
            "units": "C",
            "source": "SI definition (2019 redefinition of SI)",
            "description": (
                "The electric charge carried by a single proton, or the "
                "magnitude of the charge carried by a single electron. "
                "The fundamental unit of electric charge."
            ),
        },
        {
            "name": "Fine-Structure Constant",
            "symbol": "α (alpha)",
            "value": "7.297 352 5643(11) × 10⁻³",
            "uncertainty": "1.6 × 10⁻¹⁰ (relative)",
            "units": "dimensionless",
            "source": "CODATA 2022",
            "description": (
                "The coupling constant for electromagnetic interactions. "
                "Approximately 1/137. Dimensionless — its value is "
                "independent of any unit system, making it a uniquely "
                "universal number. Any civilization with a theory of "
                "electromagnetism will recognize it."
            ),
        },
        {
            "name": "Hydrogen 21-cm Line Frequency",
            "symbol": "ν_HI",
            "value": "1 420 405 751.768",
            "uncertainty": "< 0.001 Hz",
            "units": "Hz",
            "source": "Essen et al. (1955); confirmed by multiple measurements",
            "description": (
                "The frequency of the hyperfine transition of neutral hydrogen "
                "(the spin-flip transition). The most abundant element in the "
                "universe radiates at this frequency. Since Cocconi & Morrison "
                "(1959), it has been the primary reference frequency for SETI. "
                "This repository is named after it."
            ),
        },
        {
            "name": "Hydrogen 21-cm Line Wavelength",
            "symbol": "λ_HI",
            "value": "21.106 114 054 160",
            "uncertainty": "< 10⁻¹² m",
            "units": "cm",
            "source": "Derived from ν_HI and c",
            "description": (
                "The corresponding wavelength of the hydrogen hyperfine "
                "transition. λ = c / ν. The '21-centimetre line' is the "
                "basis for this project's domain name: signal1420.org."
            ),
        },
    ]

    with open(path, "w", encoding="utf-8") as fh:
        fh.write("FIRST LIGHT PROTOCOL — UNIVERSAL PHYSICAL CONSTANTS\n")
        fh.write("=" * 65 + "\n")
        fh.write(
            "Values from the 2022 CODATA recommended values of the\n"
            "fundamental physical constants (NIST). These quantities\n"
            "are universal — any technological civilization capable of\n"
            "measuring them precisely will obtain the same numbers.\n"
            "Parenthetical notation: e.g., 6.674 30(15) means the last\n"
            "two digits have uncertainty ±15 in the stated units.\n"
        )
        fh.write("=" * 65 + "\n\n")

        for c in constants:
            fh.write(f"Name        : {c['name']}\n")
            fh.write(f"Symbol      : {c['symbol']}\n")
            fh.write(f"Value       : {c['value']}\n")
            fh.write(f"Uncertainty : {c['uncertainty']}\n")
            fh.write(f"Units       : {c['units']}\n")
            fh.write(f"Source      : {c['source']}\n")
            fh.write(f"Description : {c['description']}\n")
            fh.write("\n")

    print(f"  Written: {path}  ({len(constants)} constants)")


def write_hydrogen_21cm() -> None:
    """Write detailed hydrogen 21-cm line information."""
    path = signal_path("hydrogen_21cm.txt")

    with open(path, "w", encoding="utf-8") as fh:
        fh.write("FIRST LIGHT PROTOCOL — HYDROGEN 21-CM SPECTRAL LINE\n")
        fh.write("=" * 65 + "\n\n")

        fh.write("FREQUENCY\n")
        fh.write("---------\n")
        fh.write("Value    : 1 420 405 751.768 Hz\n")
        fh.write("          = 1.420 405 751 768 GHz\n")
        fh.write("Precision: < 0.001 Hz uncertainty\n\n")

        fh.write("WAVELENGTH\n")
        fh.write("----------\n")
        fh.write("Value    : 21.106 114 054 160 cm\n")
        fh.write("          = 0.211 061 140 541 60 m\n")
        fh.write("Derived  : λ = c / ν = 299 792 458 / 1 420 405 751.768\n\n")

        fh.write("TRANSITION DESCRIPTION\n")
        fh.write("----------------------\n")
        fh.write(
            "The 21-cm line arises from the hyperfine transition in the\n"
            "ground state of neutral atomic hydrogen (H I). A hydrogen\n"
            "atom in its ground state consists of one proton and one\n"
            "electron, each with spin-1/2. The two possible configurations\n"
            "are:\n\n"
            "  PARALLEL spins    (F=1, higher energy) → ANTIPARALLEL spins\n"
            "  (F=0, lower energy) + photon at 1420.405751768 MHz\n\n"
            "The energy difference: ΔE = hν = 9.411 × 10⁻²⁵ J\n"
            "The transition is forbidden (magnetic dipole) with a\n"
            "spontaneous emission rate of ~2.9 × 10⁻¹⁵ s⁻¹, giving a\n"
            "mean lifetime of ~11 million years — extremely rare for a\n"
            "single atom, but observable in the vast interstellar medium.\n\n"
        )

        fh.write("SIGNIFICANCE IN SETI\n")
        fh.write("--------------------\n")
        fh.write(
            "Cocconi, G. & Morrison, P. (1959). 'Searching for\n"
            "Interstellar Communications.' Nature, 184, 844-846.\n\n"
            "This foundational paper proposed that intelligent\n"
            "civilizations attempting contact would naturally converge\n"
            "on the hydrogen frequency as a universal reference. Their\n"
            "reasoning:\n\n"
            "  1. Hydrogen is the most abundant element in the universe.\n"
            "  2. Its spectral line is a unique, measurable frequency.\n"
            "  3. Any civilization with radio astronomy knows it.\n"
            "  4. It requires no shared language or convention to identify.\n\n"
            "This project's domain, signal1420.org, is named after it.\n"
            "The repository name 'first-light-protocol' refers both to\n"
            "first contact and to the hydrogen line as the first light\n"
            "of radio astronomy.\n\n"
        )

        fh.write("PROPOSED RESPONSE FREQUENCIES\n")
        fh.write("-----------------------------\n")
        fh.write(
            "By convention, contact attempts often reference multiples\n"
            "or mathematical combinations of the hydrogen frequency:\n\n"
            "  1 × ν_HI = 1 420 405 751.768 MHz  (the hydrogen line)\n"
            "  π × ν_HI = 4 462 336 273.0 MHz    (pi times hydrogen)\n"
            "  e × ν_HI = 3 861 771 777.0 MHz    (e times hydrogen)\n"
            "  2 × ν_HI = 2 840 811 503.536 MHz  (double hydrogen)\n\n"
            "These frequencies are not suggestions for this project\n"
            "(which operates entirely through internet channels) but\n"
            "are included as mathematical context.\n\n"
        )

        fh.write("NOTE\n")
        fh.write("----\n")
        fh.write(
            "This file is part of the First Light Protocol beacon.\n"
            "The inclusion of hydrogen line data is both a mathematical\n"
            "handshake and an acknowledgment of the scientific tradition\n"
            "of SETI that preceded this project.\n"
        )

    print(f"  Written: {path}")


def write_response_placeholder() -> None:
    """Write the intentionally-empty dead-drop response file."""
    path = signal_path("response.txt")

    with open(path, "w", encoding="utf-8") as fh:
        fh.write("FIRST LIGHT PROTOCOL — DESIGNATED RESPONSE CHANNEL\n")
        fh.write("=" * 55 + "\n\n")
        fh.write(
            "This file is intentionally empty.\n\n"
            "It exists as a designated response channel — a 'dead drop'\n"
            "for any intelligence that wishes to leave a message in a\n"
            "location we will check.\n\n"
            "To use this channel:\n"
            "  Fork this repository, add your response to this file,\n"
            "  and submit a pull request. Or create a GitHub Issue.\n"
            "  Or use any other method described in PROTOCOL.md.\n\n"
            "We check regularly. We will respond.\n\n"
            "— The sender\n"
        )

    print(f"  Written: {path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    """Generate all signal/ files."""
    print("First Light Protocol — generate_signals.py")
    print(f"Project root : {PROJECT_ROOT}")
    print(f"Output dir   : {SIGNAL_DIR}")
    print()

    ensure_signal_dir()

    # Generate the first 10,000 primes once; reuse for gaps and twins.
    print("Computing first 10,000 primes...")
    primes_10k: List[int] = first_n_primes(10_000)
    print(f"  Largest prime: {primes_10k[-1]:,}\n")

    print("Writing signal files...")
    write_prime_sieve(primes_10k)
    write_fibonacci(fibonacci_sequence(1_000))
    write_prime_gaps(primes_10k, count=1_000)
    write_twin_primes(primes_10k)
    write_mathematical_constants()
    write_physical_constants()
    write_hydrogen_21cm()
    write_response_placeholder()

    print()
    print("Done. All signal/ files written successfully.")


if __name__ == "__main__":
    main()
