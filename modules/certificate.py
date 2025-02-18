from dataclasses import dataclass
from datetime import datetime, timedelta
import uuid

@dataclass
class Certificate:
    subject: str
    issuer: str
    valid_from: datetime
    valid_to: datetime
    is_root: bool
    serial_number: str

    @classmethod
    def create_root_ca(cls, name="Root CA"):
        now = datetime.now()
        return cls(
            subject=name,
            issuer=name,
            valid_from=now,
            valid_to=now + timedelta(days=3650),
            is_root=True,
            serial_number=str(uuid.uuid4())
        )

    @classmethod
    def create_intermediate(cls, issuer, name="Intermediate CA"):
        now = datetime.now()
        return cls(
            subject=name,
            issuer=issuer.subject,
            valid_from=now,
            valid_to=now + timedelta(days=730),
            is_root=False,
            serial_number=str(uuid.uuid4())
        )

    @classmethod
    def create_leaf(cls, issuer, name="example.com"):
        now = datetime.now()
        return cls(
            subject=name,
            issuer=issuer.subject,
            valid_from=now,
            valid_to=now + timedelta(days=365),
            is_root=False,
            serial_number=str(uuid.uuid4())
        )

class CertificateChain:
    def __init__(self):
        self.certificates = []

    def add_certificate(self, cert):
        self.certificates.append(cert)

    def validate(self, trust_server_certificate=False):
        if not self.certificates:
            return False, "Empty chain"

        now = datetime.now()

        # Check certificate dates first
        for cert in self.certificates:
            if now < cert.valid_from:
                return False, f"Certificate for {cert.subject} is not yet valid"
            if now > cert.valid_to:
                return False, f"Certificate for {cert.subject} has expired"

        # If trustServerCertificate is True, we only validate dates, not the chain
        if trust_server_certificate:
            return True, "Valid (Trust Server Certificate enabled - chain validation skipped)"

        # Validate the certificate chain
        for i in range(len(self.certificates) - 1):
            current = self.certificates[i]
            issuer = self.certificates[i + 1]

            if current.issuer != issuer.subject:
                return False, f"Invalid issuer: {current.subject} not issued by {issuer.subject}"

        # Check if the last certificate is a root CA
        if not self.certificates[-1].is_root:
            return False, "Chain doesn't end with a trusted root certificate"

        # If we got here, the chain is valid
        return True, "Valid certificate chain"