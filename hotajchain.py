"""A toy blockchain."""

import hashlib

import ecdsa
from ecdsa import util
from absl import app

_BITCOIN_CURVE = ecdsa.SECP256k1

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


class Wallet(object):
  def __init__(self, seed=None):
    if seed:
      sec_exp = util.randrange_from_seed__X(seed, _BITCOIN_CURVE.order)
      self._sk = ecdsa.SigningKey.from_secret_exponent(sec_exp, 
                                                        curve=_BITCOIN_CURVE)
    else: 
      self._sk = ecdsa.SigningKey.generate(curve=_BITCOIN_CURVE)
    self._vk = self._sk.get_verifying_key()

  def sign(self, hexdigest):
    return self._sk.sign_digest(hexdigest)

  
  def verify(self, signature, hexdigest):
    self._vk.verify_digest(signature, hexdigest)



# TODO(ehotaj): actually implement
class Transaction(object):
  def __init__(self, signed_transfer, receiver_public_key):
    self.hexdigest = self._hash() 

  def _hash(self):
    h = hashlib.sha256()
    h.update('deadbeef'.encode())
    return h.hexdigest()

class Block(object):
  def __init__(self, txns, prev_block_hash=''):
    self._prev_block_hash = prev_block_hash
    self._txns = txns
    self._salt = 0

  def _hash(self):
    h = hashlib.sha256()
    h.update(self._prev_block_hash.encode())
    for txn in self._txns:
      h.update(txn.hexdigest.encode())
    h.update(str(self._salt).encode())
    return h.hexdigest()

  def pow(self, difficulty): 
    hex_ = self._hash()
    while not _check_pow(hex_, difficulty):
      self._salt += 1
      hex_ = self._hash()

    return hex_

def main():
  print('hello')

if __name__ == '__main__':
  app.run(main)
