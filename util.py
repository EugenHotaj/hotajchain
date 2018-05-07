"""Utilities useful for Hotajchain."""

import hashlib

def check_pow(hexdigest, difficulty):
  """Checks that the pow `hexdigest` starts wtih `difficulty` leading zeros.

  Note that each hex value corresponds to 4 bytes. The algorithm checks the
  following:
      * Hex has at least floor(difficulty/4) leading zeros.
      * If there is a remainder, we check that the next hex value has remainder
        leading zeros.
  """
  leading_zeros = difficulty // 4
  head = hexdigest[:leading_zeros]
  if not head == '0' * len(head):
    return False
  remaining_difficulty = 4 - (difficulty % 4)
  # If there is no remainder, use 0 here instead of having another conditional.
  critical_char = hexdigest[leading_zeros:leading_zeros + 1] or '0'
  return int(critical_char, 16) <= (2 ** remaining_difficulty +1) - 1

def hash(strings):
  """Hashes the given list of strings (and/or hexdigests) using sha256."""
  h = hashlib.sha256()
  for s in strings: 
    h.update(s)
  return h.hexdigest()

