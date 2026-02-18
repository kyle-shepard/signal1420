"""
Signal 1420 — Challenge Generator
==================================
Generates cryptographic challenges for the First Light Protocol beacon.
Run once to produce public challenge data and private solutions.

Outputs:
  challenge_data.json   — public data for embedding in index.html (gitignored)
  PRIVATE_SOLUTIONS.txt — private keys, factors, preimages (gitignored, NEVER commit)
"""

import base64
import hashlib
import json
import secrets
import sys

try:
    from Crypto.Util.number import getPrime
except ImportError:
    print("ERROR: pycryptodome is required.")
    print("Install with: pip install pycryptodome")
    sys.exit(1)

try:
    from sympy import isprime as sympy_isprime
except ImportError:
    print("ERROR: sympy is required for cross-validation.")
    print("Install with: pip install sympy")
    sys.exit(1)


def generate_level_0():
    """Level 0: Base64 Decode — a warm handshake."""
    plaintext = (
        "If you have decoded this, you understand our encoding. "
        "This is a greeting across whatever distance separates us. "
        "We are here. We are listening. We invite conversation."
    )
    encoded = base64.b64encode(plaintext.encode("utf-8")).decode("ascii")
    return {
        "public": {
            "level": 0,
            "name": "Base64 Decode",
            "description": "A simple encoding — not encryption. Decode this message.",
            "data": encoded,
        },
        "private": {
            "level": 0,
            "name": "Base64 Decode",
            "plaintext": plaintext,
        },
    }


def generate_level_1():
    """Level 1: 512-bit Semiprime Factorization."""
    print("Generating Level 1: 512-bit semiprime (two 256-bit primes)...")
    p = getPrime(256)
    q = getPrime(256)

    if not sympy_isprime(p):
        raise ValueError(f"Cross-validation failed: p is not prime (sympy)")
    if not sympy_isprime(q):
        raise ValueError(f"Cross-validation failed: q is not prime (sympy)")

    n = p * q

    assert p.bit_length() == 256, f"p bit length: {p.bit_length()}, expected 256"
    assert q.bit_length() == 256, f"q bit length: {q.bit_length()}, expected 256"
    assert p * q == n, "p * q != N"

    n_hex = format(n, "x")
    n_dec = str(n)
    bit_length = n.bit_length()

    print(f"  N bit length: {bit_length}")
    print(f"  p bit length: {p.bit_length()}")
    print(f"  q bit length: {q.bit_length()}")
    print(f"  p * q == N: {p * q == n}")

    return {
        "public": {
            "level": 1,
            "name": "512-bit Semiprime Factorization",
            "description": (
                "Factor this semiprime into its two prime components. "
                "N = p * q where p and q are each 256-bit primes."
            ),
            "n_hex": n_hex,
            "n_decimal": n_dec,
            "bit_length": bit_length,
        },
        "private": {
            "level": 1,
            "name": "512-bit Semiprime Factorization",
            "p_hex": format(p, "x"),
            "q_hex": format(q, "x"),
            "p_decimal": str(p),
            "q_decimal": str(q),
            "p_bits": p.bit_length(),
            "q_bits": q.bit_length(),
        },
    }


def generate_level_2():
    """Level 2: 2048-bit RSA modulus."""
    print("Generating Level 2: 2048-bit RSA (two 1024-bit primes)...")
    p = getPrime(1024)
    q = getPrime(1024)

    if not sympy_isprime(p):
        raise ValueError(f"Cross-validation failed: p is not prime (sympy)")
    if not sympy_isprime(q):
        raise ValueError(f"Cross-validation failed: q is not prime (sympy)")

    n = p * q

    assert p.bit_length() == 1024, f"p bit length: {p.bit_length()}, expected 1024"
    assert q.bit_length() == 1024, f"q bit length: {q.bit_length()}, expected 1024"
    assert p * q == n, "p * q != N"

    n_hex = format(n, "x")
    n_dec = str(n)
    bit_length = n.bit_length()

    print(f"  N bit length: {bit_length}")
    print(f"  p bit length: {p.bit_length()}")
    print(f"  q bit length: {q.bit_length()}")
    print(f"  p * q == N: {p * q == n}")

    return {
        "public": {
            "level": 2,
            "name": "2048-bit RSA Factorization",
            "description": (
                "Factor this RSA modulus. N = p * q where p and q are "
                "each 1024-bit primes. This is equivalent in difficulty "
                "to breaking standard RSA-2048 encryption."
            ),
            "n_hex": n_hex,
            "n_decimal": n_dec,
            "bit_length": bit_length,
        },
        "private": {
            "level": 2,
            "name": "2048-bit RSA Factorization",
            "p_hex": format(p, "x"),
            "q_hex": format(q, "x"),
            "p_decimal": str(p),
            "q_decimal": str(q),
            "p_bits": p.bit_length(),
            "q_bits": q.bit_length(),
        },
    }


def generate_level_3():
    """Level 3: SHA-256 Preimage."""
    print("Generating Level 3: SHA-256 preimage challenge...")
    preimage = secrets.token_bytes(32)
    digest = hashlib.sha256(preimage).hexdigest()

    verify = hashlib.sha256(preimage).hexdigest()
    assert verify == digest, "SHA-256 verification failed"

    print(f"  Preimage length: {len(preimage)} bytes")
    print(f"  SHA-256 digest: {digest}")
    print(f"  Verification: {verify == digest}")

    return {
        "public": {
            "level": 3,
            "name": "SHA-256 Preimage",
            "description": (
                "Find the 32-byte input that produces this SHA-256 hash. "
                "This requires either brute force across 2^256 possibilities "
                "or a fundamental break in SHA-256."
            ),
            "hash_hex": digest,
        },
        "private": {
            "level": 3,
            "name": "SHA-256 Preimage",
            "preimage_hex": preimage.hex(),
        },
    }


def generate_level_4():
    """Level 4: Lattice SVP — marked as under construction."""
    return {
        "public": {
            "level": 4,
            "name": "Lattice Shortest Vector Problem",
            "description": (
                "This challenge is under construction. Lattice-based problems "
                "represent the frontier of post-quantum cryptography. "
                "A future version of this beacon will include a properly "
                "constructed SVP instance."
            ),
            "status": "under_construction",
        },
        "private": {
            "level": 4,
            "name": "Lattice Shortest Vector Problem",
            "status": "under_construction",
            "note": "No solution exists yet — challenge not generated.",
        },
    }


def main():
    print("=" * 60)
    print("Signal 1420 — Challenge Generator")
    print("=" * 60)
    print()

    challenges = [
        generate_level_0(),
        generate_level_1(),
        generate_level_2(),
        generate_level_3(),
        generate_level_4(),
    ]

    public_data = [c["public"] for c in challenges]
    private_data = [c["private"] for c in challenges]

    with open("challenge_data.json", "w", encoding="utf-8") as f:
        json.dump(public_data, f, indent=2)
    print("\nWrote challenge_data.json (public data)")

    with open("PRIVATE_SOLUTIONS.txt", "w", encoding="utf-8") as f:
        f.write("=" * 60 + "\n")
        f.write("SIGNAL 1420 — PRIVATE SOLUTIONS\n")
        f.write("DO NOT COMMIT THIS FILE\n")
        f.write("=" * 60 + "\n\n")
        for entry in private_data:
            f.write(f"--- Level {entry['level']}: {entry['name']} ---\n")
            for key, value in entry.items():
                if key not in ("level", "name"):
                    f.write(f"  {key}: {value}\n")
            f.write("\n")
    print("Wrote PRIVATE_SOLUTIONS.txt (private solutions)")

    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)
    print(f"  Level 0: Base64 plaintext length = {len(challenges[0]['private']['plaintext'])} chars")
    lvl1 = challenges[1]
    p1 = int(lvl1["private"]["p_decimal"])
    q1 = int(lvl1["private"]["q_decimal"])
    n1 = int(lvl1["public"]["n_decimal"])
    print(f"  Level 1: p * q == N: {p1 * q1 == n1}, bits: {n1.bit_length()}")
    lvl2 = challenges[2]
    p2 = int(lvl2["private"]["p_decimal"])
    q2 = int(lvl2["private"]["q_decimal"])
    n2 = int(lvl2["public"]["n_decimal"])
    print(f"  Level 2: p * q == N: {p2 * q2 == n2}, bits: {n2.bit_length()}")
    lvl3 = challenges[3]
    preimage = bytes.fromhex(lvl3["private"]["preimage_hex"])
    digest = hashlib.sha256(preimage).hexdigest()
    print(f"  Level 3: SHA-256 verified: {digest == lvl3['public']['hash_hex']}")
    print(f"  Level 4: Status: {challenges[4]['public']['status']}")
    print("\nAll challenges generated successfully.")


if __name__ == "__main__":
    main()
