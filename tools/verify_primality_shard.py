import sys
from hashlib import sha256
from pathlib import Path

path = Path(sys.argv[1])
expected = sys.argv[2].lower()
actual = sha256(path.read_bytes()).hexdigest()
if actual != expected:
    raise SystemExit("SHA-256 mismatch")

print(f"SHA-256 OK: {actual}")
