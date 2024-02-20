from ek_loop_py.device.ek import BUFFER_SIZE


def build_request(header: bytes, payload: bytes) -> bytearray:
    """Builds a request with a fixed size of 63 bytes.

    Args:
        header (bytes): The header bytes for the request.
        payload (bytes): The payload bytes for the request.
    """
    request = bytearray(header) + payload
    padding_size = BUFFER_SIZE - len(request)
    request += bytes([0] * max(0, padding_size))
    return request[:BUFFER_SIZE]
