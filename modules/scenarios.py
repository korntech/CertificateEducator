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