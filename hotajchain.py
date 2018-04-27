"""A toy blockchain."""

import hashlib

from absl import app

def _check_pow(hexdigest, difficulty):
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


class Block(object):
  def __init__(self, data, prev_hash=''):
    self._prev_hash = prev_hash
    self._data = data
    self._nonce = 0

  def _hash(self):
    h = hashlib.sha256()
    h.update(self._prev_hash.encode())
    h.update(self._data.encode())
    h.update(str(self._nonce).encode())
    return h.hexdigest()

  def pow(self, difficulty): 
    hex_ = self._hash()
    while not _check_pow(hex_, difficulty):
      self._nonce += 1
      hex_ = self._hash()

    return hex_


def main(argv):
  del argv  # Unused.

  genesis = Block('hello hotajchain')
  print (genesis.pow(50))
  print (genesis._nonce)


if __name__ == '__main__':
  app.run(main)
