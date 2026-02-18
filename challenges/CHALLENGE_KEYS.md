# Signal 1420 — Challenge Generation Methodology

This document describes how each cryptographic challenge was generated.
It does NOT contain solutions.

---

## Level 0: Base64 Decode

- **Algorithm**: Standard Base64 encoding (RFC 4648)
- **Library**: Python `base64.b64encode()`
- **Input**: A plaintext greeting message (UTF-8 encoded)
- **Purpose**: Not a real challenge — a handshake to confirm the solver understands
  basic Earth encoding conventions

## Level 1: 512-bit Semiprime Factorization

- **Algorithm**: Generate two random 256-bit primes, multiply to produce N
- **Library**: `Crypto.Util.number.getPrime(256)` from pycryptodome
- **Validation**: Cross-validated with `sympy.isprime()` to confirm both factors
  are prime; asserted `p * q == N` and verified bit lengths
- **Difficulty**: Within reach of modern classical computing (GNFS), but requires
  non-trivial computational effort
- **Output format**: N provided in both hexadecimal and decimal

## Level 2: 2048-bit RSA Factorization

- **Algorithm**: Generate two random 1024-bit primes, multiply to produce N
- **Library**: `Crypto.Util.number.getPrime(1024)` from pycryptodome
- **Validation**: Cross-validated with `sympy.isprime()` to confirm both factors
  are prime; asserted `p * q == N` and verified bit lengths
- **Difficulty**: Equivalent to breaking RSA-2048 — currently considered infeasible
  for classical computing. Estimated to require thousands of years with best
  known algorithms
- **Output format**: N provided in both hexadecimal and decimal

## Level 3: SHA-256 Preimage

- **Algorithm**: Generate 32 cryptographically random bytes, compute SHA-256 hash
- **Library**: `secrets.token_bytes(32)` for random generation,
  `hashlib.sha256()` for hashing
- **Validation**: Verified `SHA-256(preimage) == published_hash`
- **Difficulty**: Requires either brute force over 2^256 possibilities or a
  fundamental break in SHA-256. No known approach exists
- **Output format**: SHA-256 hash as 64-character hex string

## Level 4: Lattice Shortest Vector Problem

- **Status**: Under construction
- **Rationale**: Lattice-based problems (SVP, LWE) are the foundation of
  post-quantum cryptography. A properly constructed instance requires careful
  parameterization to be both meaningful and verifiable
- **Plan**: A future version of this beacon will include a lattice challenge
  once the construction methodology has been thoroughly validated

---

## Security Notes

- All random values were generated using cryptographically secure RNGs
  (`Crypto.Util.number.getPrime` uses system entropy; `secrets.token_bytes`
  uses the OS CSPRNG)
- Primality was validated using two independent libraries (pycryptodome and sympy)
- Private solutions are stored in `PRIVATE_SOLUTIONS.txt` which is gitignored
  and must never be committed to the repository

## Reproducibility

These challenges are NOT reproducible — they use true random generation.
The `challenge_data.json` file contains the definitive public challenge data.
Regenerating will produce entirely new challenges and invalidate any existing
solutions.
