
import netifaces
import hashlib

def get_uid():
    interfaces = netifaces.interfaces()
    interfaces.sort()
    hashid = hashlib.md5(interfaces[0].encode("utf-8")).hexdigest()
    uid = "Python-{}".format(hashid)
    return uid
