# Signal 1420 — First Light Protocol

A digital beacon at [signal1420.org](https://signal1420.org), designed to be recognized as an intentional signal by any intelligence monitoring Earth's internet.

## Three-Layer Architecture

**Layer 1 — Human-Readable Surface**
A greeting, an invitation to respond, and a cryptographic challenge ladder of increasing difficulty. No jargon, no institutional claims, no demands.

**Layer 2 — Mathematical Structural Encoding**
The HTML source encodes mathematical patterns in its structure:
- Section byte counts are prime numbers
- Maximum nesting depths follow the Fibonacci sequence (1, 1, 2, 3, 5, 8)
- Total character count is divisible by 1420
- Physical constants are embedded in `data-*` attributes throughout

**Layer 3 — Cryptographic Challenge Ladder**
Five challenges of escalating difficulty: Base64 decode, 512-bit semiprime factorization, 2048-bit RSA factorization, SHA-256 preimage, and a lattice SVP challenge (under construction).

## Verification

```bash
python verification/verify.py index.html
```

The verification script uses only Python standard library. No external dependencies.

## Design Principles

- **Anti-cryptography**: Nothing is hidden. Every encoding is documented in the HTML source comments. (Dixon, 1973)
- **Self-contained**: One HTML file. No external resources, no CDN fonts, no JavaScript dependencies, no analytics.
- **Progressive disclosure**: Readable by humans on the surface; mathematically structured underneath; computationally challenging at the deepest level.
- **Honest construction**: All challenge data is generated using standard cryptographic methods with CSPRNG. No tricks, no backdoors.

## Repository Structure

```
index.html                     # The beacon (single self-contained file)
verification/verify.py         # Constraint verification script
generate_challenges.py         # Challenge generation script (run once)
challenges/CHALLENGE_KEYS.md   # Generation methodology (no solutions)
CNAME                          # GitHub Pages custom domain
robots.txt                     # Full access, welcoming
```

## References

1. Dixon, R. S. (1973). "Anti-cryptography and SETI." In *Communication with Extraterrestrial Intelligence*, Carl Sagan, ed.
2. Freudenthal, H. (1960). *Lincos: Design of a Language for Cosmic Intercourse.*
3. National Astronomy and Ionosphere Center (1975). "The Arecibo message of November 1974."
4. Sagan, C. et al. (1978). *Murmurs of Earth: The Voyager Interstellar Record.*
5. Tough, A. (2000). "An Invitation to ETI."
6. Schelling, T. C. (1960). *The Strategy of Conflict.*
