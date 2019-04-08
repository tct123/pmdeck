
import netifaces
import hashlib
from baseconv import base16
from baseconv import BaseConverter


def get_uid():
    interfaces = netifaces.interfaces()
    interfaces.sort()
    i = interfaces[0]
    s = "abcdefghijklmnopqrstuvwxyz"
    u = "ABCDEFGHJKLMNPQRSTUVWXYZ"
    d = "0123456789"
    bc = BaseConverter(d+s+u)
    hashid = hashlib.sha1(i.encode("utf-8")).hexdigest()
    hashid = hashid.upper()
    raw = base16.decode(hashid)
    uid = bc.encode(raw)
    return uid


def get_short_uid():
    return get_uid()[:9]


if __name__ == "__main__":
    print(get_uid())
