from .certificate import Certificate, CertificateChain
from datetime import datetime, timedelta

class Scenarios:
    @staticmethod
    def get_basic_chain():
        root = Certificate.create_root_ca()
        intermediate = Certificate.create_intermediate(root)
        leaf = Certificate.create_leaf(intermediate)

        chain = CertificateChain()
        chain.add_certificate(leaf)
        chain.add_certificate(intermediate)
        chain.add_certificate(root)

        return chain

    @staticmethod
    def get_expired_cert_chain():
        root = Certificate.create_root_ca()
        intermediate = Certificate.create_intermediate(root)

        # Create expired leaf certificate
        now = datetime.now()
        leaf = Certificate(
            subject="expired.example.com",
            issuer=intermediate.subject,
            valid_from=now - timedelta(days=730),
            valid_to=now - timedelta(days=365),
            is_root=False,
            serial_number="expired123"
        )

        chain = CertificateChain()
        chain.add_certificate(leaf)
        chain.add_certificate(intermediate)
        chain.add_certificate(root)

        return chain

    @staticmethod
    def get_broken_chain():
        root = Certificate.create_root_ca()
        intermediate = Certificate.create_intermediate(root)

        # Create leaf with wrong issuer
        leaf = Certificate(
            subject="wrong.example.com",
            issuer="Wrong Issuer",
            valid_from=datetime.now(),
            valid_to=datetime.now() + timedelta(days=365),
            is_root=False,
            serial_number="wrong123"
        )

        chain = CertificateChain()
        chain.add_certificate(leaf)
        chain.add_certificate(intermediate)
        chain.add_certificate(root)

        return chain

    @staticmethod
    def get_untrusted_chain():
        # Create a standalone certificate without proper chain
        now = datetime.now()
        standalone = Certificate(
            subject="untrusted.example.com",
            issuer="Unknown CA",
            valid_from=now,
            valid_to=now + timedelta(days=365),
            is_root=False,
            serial_number="untrusted123"
        )

        chain = CertificateChain()
        chain.add_certificate(standalone)
        return chain

    @staticmethod
    def get_mitm_attack_chain():
        # Create malicious certificates
        malicious_root = Certificate(
            subject="Malicious Root CA",
            issuer="Malicious Root CA",
            valid_from=datetime.now(),
            valid_to=datetime.now() + timedelta(days=365),
            is_root=True,
            serial_number="malicious_root_123"
        )

        malicious_leaf = Certificate(
            subject="bank.example.com",  # Impersonating legitimate site
            issuer=malicious_root.subject,
            valid_from=datetime.now(),
            valid_to=datetime.now() + timedelta(days=365),
            is_root=False,
            serial_number="malicious_leaf_123"
        )

        chain = CertificateChain()
        chain.add_certificate(malicious_leaf)
        chain.add_certificate(malicious_root)
        return chain