"""A toy blockchain."""

import hashlib

import ecdsa
from absl import app

# TODO(ehotaj): figure out packages. 
import util 

_BITCOIN_CURVE = ecdsa.SECP256k1

class Wallet(object):
  def __init__(self, seed=None):
    if seed:
      sec_exp = ecdsa.util.randrange_from_seed__X(seed, _BITCOIN_CURVE.order)
      self._sk = ecdsa.SigningKey.from_secret_exponent(sec_exp, 
                                                        curve=_BITCOIN_CURVE)
    else: 
      self._sk = ecdsa.SigningKey.generate(curve=_BITCOIN_CURVE)
    self._vk = self._sk.get_verifying_key()

  @property
  def public_key(self):
    return self._vk

  def sign(self, hexdigest):
    return self._sk.sign_digest(hexdigest)

  def verify(self, signature, hexdigest):
    self._vk.verify_digest(signature, hexdigest)


class Coin(object):
  def __init__(self):
    self.txn_chain_hexdigest = None
    self.signature = None

class Transaction(object):
  def __init__(self, coin, wallet_sender, wallet_receiver):
    self._coin = coin
    self._wallet_sender = wallet_sender
    self._wallet_receiver = wallet_receiver
  
  def commit(self):
    _verify_sender_owns_coin()
    _transfer_coin()
    pass

  def _verify_sender_owns_coin(self):
    signature = coin.signature
    hexdigest = coin.tnx_chain_hexdigest
    self._wallet_sender.verify(signature, hexdigest)

  def _transfer_coin(self):
    receiver_pk = wallet_receiver.public_key
    tnx_chain_hexdigest = _hash([self._coin.signature.encode(), 
                            self._coin.tnx_chain_hexdigest])



class Block(object):
  def __init__(self, transactions, prev_block_hash=''):
    assert len(transactions) > 0

    self._prev_block_hash = prev_block_hash
    self._transactions = transactions
    self._salt = 0

  def _hash(self):
    strs = [str(self._salt).encode(), self._prev_block_hash.encode()]
    tnxs = [tnx.encode() for tnx in self._transactions]
    return util.hash(strs + tnxs)

  def pow(self, difficulty): 
    hex_ = self._hash()
    while not util.check_pow(hex_, difficulty):
      self._salt += 1
      hex_ = self._hash()

    return hex_

def main(argv):
  del argv  # Unused
  genesis = Block(['fake', 'transactions', 'here'])
  genesis.pow(20)
  print(genesis._salt)

if __name__ == '__main__':
  app.run(main)
