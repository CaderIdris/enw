from hashlib import sha256

def get_hash(string: str) -> str:
    """Convert a string into a SHA256 hash.

    Parameters
    ----------
    string : str
        String to hash

    Returns
    -------
    SHA256 string, encoded in utf-8, 64 characters long

    """
    return sha256(string.encode()).hexdigest()
