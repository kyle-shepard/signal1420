"""
Signal 1420 — Verification Script
===================================
Verifies all mathematical constraints in the Signal 1420 beacon.
Uses only Python standard library. No external dependencies.

Usage:
    python verify.py ../index.html
"""

import re
import sys
from html.parser import HTMLParser


# --- Primality testing (trial division, sufficient for our byte counts) ---

def is_prime(n):
    """Test primality via trial division. Sufficient for numbers < 10^12."""
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


# --- HTML nesting depth parser ---

VOID_ELEMENTS = frozenset([
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
])


class DepthParser(HTMLParser):
    """Finds the maximum nesting depth of DOM elements within a fragment."""

    def __init__(self):
        super().__init__()
        self.depth = 0
        self.max_depth = 0

    def handle_starttag(self, tag, attrs):
        if tag.lower() not in VOID_ELEMENTS:
            self.depth += 1
            if self.depth > self.max_depth:
                self.max_depth = self.depth

    def handle_endtag(self, tag):
        if tag.lower() not in VOID_ELEMENTS:
            self.depth -= 1


def get_max_depth(html_fragment):
    """Return the maximum nesting depth of elements in an HTML fragment.
    Depth 1 means a direct child element exists (e.g., <section><p>...</p></section>).
    """
    parser = DepthParser()
    parser.feed(html_fragment)
    return parser.max_depth


# --- Section extraction ---

def extract_sections(content):
    """Extract innerHTML of each <section> by ID.
    Returns list of (section_id, inner_html) tuples in document order.
    """
    section_ids = ["preamble", "greeting", "challenges", "verification", "timestamp", "references"]
    results = []
    for sid in section_ids:
        pattern = re.compile(
            r'<section\s[^>]*id="' + re.escape(sid) + r'"[^>]*>(.*?)</section>',
            re.DOTALL
        )
        match = pattern.search(content)
        if match:
            results.append((sid, match.group(1)))
        else:
            results.append((sid, None))
    return results


# --- Data attribute extraction ---

def extract_data_attributes(content):
    """Extract all data-* attributes and their values from the HTML."""
    pattern = re.compile(r'data-([\w-]+)="([^"]*)"')
    attrs = {}
    for match in pattern.finditer(content):
        name = match.group(1)
        value = match.group(2)
        if name not in attrs:
            attrs[name] = []
        attrs[name].append(value)
    return attrs


# --- Physical constants ---

PHYSICAL_CONSTANTS = {
    "hydrogen": "1420.405751768",
    "c": "299792458",
    "pi": "3.14159265358979323846",
    "euler": "2.71828182845904523536",
    "planck": "6.62607015e-34",
    "alpha": "0.0072973525693",
}

# --- Fibonacci sequence for nesting depths (1-indexed) ---

FIBONACCI_DEPTHS = {
    "preamble": 1,
    "greeting": 1,
    "challenges": 2,
    "verification": 3,
    "timestamp": 5,
    "references": 8,
}


# --- Main verification ---

def verify(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    print("=" * 50)
    print("Signal 1420 Verification Report")
    print("=" * 50)
    print()

    total_checks = 0
    passed_checks = 0
    failures = []

    # CHECK 1: Section byte counts are prime
    print("[CHECK 1] Section Byte Counts (prime)")
    print("-" * 40)
    sections = extract_sections(content)
    for sid, inner_html in sections:
        total_checks += 1
        if inner_html is None:
            print(f"  {sid}: FAIL (section not found)")
            failures.append(f"Section '{sid}' not found")
            continue
        byte_count = len(inner_html.encode("utf-8"))
        prime = is_prime(byte_count)
        status = "PASS" if prime else "FAIL"
        if prime:
            passed_checks += 1
        else:
            failures.append(f"Section '{sid}' byte count {byte_count} is not prime")
        print(f"  {sid}: {byte_count} bytes — {status}")
    print()

    # CHECK 2: Nesting depths match Fibonacci sequence
    print("[CHECK 2] Nesting Depths (Fibonacci: 1, 1, 2, 3, 5, 8)")
    print("-" * 40)
    for sid, inner_html in sections:
        total_checks += 1
        if inner_html is None:
            print(f"  {sid}: FAIL (section not found)")
            failures.append(f"Section '{sid}' not found for depth check")
            continue
        depth = get_max_depth(inner_html)
        expected = FIBONACCI_DEPTHS[sid]
        match = depth == expected
        status = "PASS" if match else "FAIL"
        if match:
            passed_checks += 1
        else:
            failures.append(f"Section '{sid}' depth {depth}, expected {expected}")
        print(f"  {sid}: depth {depth}, expected {expected} — {status}")
    print()

    # CHECK 3: Total character count divisible by 1420
    print("[CHECK 3] Total Character Count (divisible by 1420)")
    print("-" * 40)
    total_checks += 1
    char_count = len(content)
    remainder = char_count % 1420
    divisible = remainder == 0
    status = "PASS" if divisible else "FAIL"
    if divisible:
        passed_checks += 1
    else:
        failures.append(f"Total char count {char_count} % 1420 = {remainder}")
    print(f"  Total characters: {char_count}")
    print(f"  {char_count} % 1420 = {remainder} — {status}")
    print()

    # CHECK 4: Physical constants in data-* attributes
    print("[CHECK 4] Physical Constants in Data Attributes")
    print("-" * 40)
    data_attrs = extract_data_attributes(content)
    for const_name, const_value in PHYSICAL_CONSTANTS.items():
        total_checks += 1
        if const_name in data_attrs:
            occurrences = data_attrs[const_name]
            correct = [v for v in occurrences if v == const_value]
            if len(correct) >= 1:
                passed_checks += 1
                status = "PASS"
            else:
                status = "FAIL"
                failures.append(f"Constant '{const_name}' found but with wrong value(s): {occurrences}")
            print(f"  {const_name} = {const_value}: {len(correct)} occurrence(s) — {status}")
        else:
            status = "FAIL"
            failures.append(f"Constant '{const_name}' not found in data attributes")
            print(f"  {const_name}: not found — {status}")
    print()

    # SUMMARY
    print("=" * 50)
    print(f"SUMMARY: {passed_checks}/{total_checks} checks passed")
    print("=" * 50)

    if failures:
        print()
        print("Failures:")
        for f in failures:
            print(f"  - {f}")

    return 0 if passed_checks == total_checks else 1


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <path-to-index.html>")
        sys.exit(1)
    sys.exit(verify(sys.argv[1]))
