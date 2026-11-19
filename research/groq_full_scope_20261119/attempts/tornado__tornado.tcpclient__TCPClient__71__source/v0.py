import asyncio
import socket
import ssl
import datetime
import pytest
from tornado.tcpclient import TCPClient
from tornado.gen import TimeoutError

@pytest.mark.asyncio
async def test_connect_timeout_raises():
    client = TCPClient()
    # Use a port that is unlikely to be open
    with pytest.raises(TimeoutError):
        await client.connect("127.0.0.1", 65535, timeout=0.01)

@pytest.mark.asyncio
async def test_source_ip_binding_error():
    client = TCPClient()
    # Use an invalid IP address to force bind to fail
    with pytest.raises(OSError):
        await client.connect(
            "127.0.0.1",
            80,
            source_ip="256.256.256.256",
            source_port=0,
            timeout=0.1,
        )

@pytest.mark.asyncio
async def test_ssl_connection_success(tmp_path):
    # Start a simple SSL echo server on a local port
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind(("127.0.0.1", 0))
    server_sock.listen(1)
    host, port = server_sock.getsockname()

    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    certfile = tmp_path / "cert.pem"
    keyfile = tmp_path / "key.pem"
    # Generate a self‑signed cert for testing
    from cryptography import x509
    from cryptography.x509.oid import NameOID
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import rsa
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    subject = issuer = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, u"localhost")])
    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.datetime.utcnow() - datetime.timedelta(days=1))
        .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=1))
        .add_extension(x509.SubjectAlternativeName([x509.DNSName(u"localhost")]), critical=False)
        .sign(key, hashes.SHA256())
    )
    certfile.write_bytes(cert.public_bytes(serialization.Encoding.PEM))
    keyfile.write_bytes(key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.TraditionalOpenSSL,
        serialization.NoEncryption(),
    ))
    ssl_context.load_cert_chain(certfile=str(certfile), keyfile=str(keyfile))

    async def handle_client():
        conn, _ = await asyncio.get_running_loop().sock_accept(server_sock)
        ssl_conn = ssl_context.wrap_socket(conn, server_side=True, do_handshake_on_connect=False)
        await asyncio.get_running_loop().sock_sendall(ssl_conn, b"hello")
        ssl_conn.close()

    asyncio.create_task(handle_client())

    client = TCPClient()
    stream = await client.connect(
        host,
        port,
        ssl_options=ssl_context,
        timeout=1,
    )
    data = await stream.read_until(b"hello")
    assert data == b"hello"
    stream.close()
    server_sock.close()
