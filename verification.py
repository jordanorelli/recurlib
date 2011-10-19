from hashlib import sha1
import hmac
import re
import time
import functools

def digest_data(data):
    """
    Generates a Recurly "message" string from arbitrary input data, where
    the "message" format is decribed here:

        http://docs.recurly.com/recurlyjs/signatures/spec/

    This is based on the reference implementation found here:

        https://github.com/recurly/recurly-client-ruby

    Specifically in lib/recurly/verification.rb
    """

    def _escape(data):
        """ Escapes syntax characters in an input string. """
        return re.sub(r'([\[\]\,\:\\])', r'\\\1', str(data))

    def _digest_list(data):
        """ Given a list, generates a comma-separated string of values """
        if not data:
            return None
        stringy_data = [str(digest_data(x)) for x in data if x]
        return '[%s]' % ','.join(stringy_data)

    def _digest_dict(data):
        """
        Encodes a dictionary into a '[key0:value0,key1:value1,...,keyN:valueN]'
        string.  There are a few quirks here:

            - all keys are converted to ascii.

            - key-value pairs are always ascii sorted by key.

            - keys are NOT escaped, but values are.

            - a None key is represented by an empty string, not the string
              "None".

            - all positive integer keys are destroyed, but only *after* being
              used to ascii sort the dictionary by key (i.e. integer keys set
              dictionary order but are thrown away). Negative numeric keys or
              non-decimal numeric keys (e.g. -1, 1.9 or 1.0) are retained.

            - values that digest to None (i.e. None, an empty list, or an empty
              dictionary) are destroyed, as are their associated keys.

            - empty dictionaries digest to None, but dictionaries containing
              only values that digest to None digest to '[]', so {None:None}
              digests to '[]', but {} digests to None.
        """
        if not data:
            return None
        kv_pairs = [('' if k == None else str(k), digest_data(v))
                    for k, v in data.items()
                    if v != None]
        kv_pairs.sort()
        prefix = lambda x: '' if re.match(r'^\d+$', x) else '%s:' % x
        kv_strings = ['%s%s' % (prefix(k), v) for k, v in kv_pairs]
        return '[%s]' % ','.join(kv_strings)

    return {
        str: _escape,
        unicode: _escape,
        list: _digest_list,
        dict: _digest_dict,
    }.get(type(data), lambda x: x)(data)


def generate_signature(claim, args, private_key, timestamp=None):
    """
    Generates an HMAC signature.  Expects the following:

        - claim: a string describing some event.  Known claim strings:
            - billinginfoupdate: for signing a request to Recurly to update
              the billing info on an account.

            - billinginfoupdated: used by Recurly to sign a response
              confirming that billing info was updated.

            - transactioncreate: for signing a request to Recurly to create
              a transaction.

            - transactioncreated: used by Recurly to sign a response
              confirming that a transaction was created.

            - subscriptioncreated: used by Recurly to sign a response
              confirming that a subscription was created.

        - args: the body of a request or response object, as a dictionary.

        - private_key: duh.

        - timestamp: time of signature generation, represented as Unix epoch
          time in seconds.

    """
    if not timestamp:
        timestamp = int(time.time())
    timestamp = str(timestamp)
    input_data = [timestamp, claim, args]
    input_string = digest_data(input_data)

    digest_key = sha1(private_key).digest()
    signature = hmac.new(digest_key, str(input_string), sha1)
    return '%s-%s' % (signature.hexdigest(), timestamp)


def verify_params(claim, args, private_key):
    """
    Checks the validity of a signature sent from the user's browser to the
    server.  See the usage notes for generate_signature for details about
    input parameters.
    """
    args = dict([(str(k), v) for k, v in args.items()])
    signature = args.pop('signature')
    hmac, timestamp = signature.split('-')
    age = int(time.time()) - int(timestamp)

    if age > 3600 or age < -3600:
        raise ValueError("signature is too old or too new")

    print 'signature: ' + signature
    print repr(args)
    expected_signature = generate_signature(claim, args, private_key, timestamp)
    print 'expected signature: ' + expected_signature
    return signature == expected_signature
