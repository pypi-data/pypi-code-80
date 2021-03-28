

import geant_tcs_client
import ssl_certificates

client = geant_tcs_client.GEANTTCSClient.connect()

config = {"username": "admin_customer14378", "password": "password123", "custom_uri": "test"}
ssl_certs = ssl_certificates.SSLCertificates(config)

print(ssl_certs.listing_ssl_types())
