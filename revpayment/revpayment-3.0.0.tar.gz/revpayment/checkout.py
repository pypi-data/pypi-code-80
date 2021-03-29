import json
import urllib.request
from base64 import b64decode

import jwt
import requests
from django.conf import settings
from django.shortcuts import redirect
from jwcrypto.jwt import JWK
from M2Crypto import X509
from M2Crypto.Err import M2CryptoError
from rest_framework import response

from revpayment.models import RedirectState
from revpayment.settings import api_settings

SNS_MESSAGE_TYPE_SUB_NOTIFICATION = "SubscriptionConfirmation"
SNS_MESSAGE_TYPE_NOTIFICATION = "Notification"
SNS_MESSAGE_TYPE_UNSUB_NOTIFICATION = "UnsubscribeConfirmation"


class CheckoutSDK:
    payment_classes = (
        ("neweb", api_settings.DEFAULT_NEWEB_CLASS),
        ("ecpay", api_settings.DEFAULT_ECPAY_CLASS),
        ("credit", api_settings.DEFAULT_CREDIT_CLASS),
    )
    handler_class = api_settings.HANDLER_CLASS
    fail_url = api_settings.DEFAULT_CHECKOUTFAIL_URL
    redirect_url = api_settings.DEFAULT_REDIRECT_URL
    redirect_query = api_settings.DEFAULT_REDIRECT_QUERY

    def __init__(self, state):
        self.state = state
        if type(state.cart) is str:
            self.cart = json.loads(state.cart)
        elif type(state.cart) is dict:
            self.cart = state.cart
        else:
            raise TypeError
        self.payment_type = state.payment_type
        self.payment_subtype = state.payment_subtype
        self.buyer = state.buyer

    def get_payment_class(self):
        try:
            payment_class = [
                c[1] for c in self.payment_classes if c[0] == self.payment_type
            ][0]
            return payment_class
        except IndexError:
            valids = [payment[0] for payment in self.payment_classes]
            raise exceptions.InvalidPaymentType(
                valids=valids, invalid=self.payment_type
            )

    def get_payment(self):
        payment_class = self.get_payment_class()
        return payment_class(
            buyer=self.buyer,
            payment_subtype=self.payment_subtype,
            cart=self.cart,
            order_id=self.state.order_id,
            order_type=self.state.order_type,
        )

    def checkout(self):
        try:
            payment = self.get_payment()
            result = payment.checkout()
            return redirect(result["url"])
        except exceptions.PaymentException as e:
            return redirect(
                f"{self.fail_url}?error={e.error}&error_detail={e.error_detail}"
            )

    def callback(self, data):
        payment = self.get_payment()
        payment.callback(data)
        return response.Response({}, 200)

    def customer_redirect(self, data):
        payment = self.get_payment()
        order = payment.customer_redirect(data)
        return redirect(f"{self.redirect_url}?{self.redirect_query}={order.id}")


def canonical_message_builder(content, format):
    """Builds the canonical message to be verified.
    Sorts the fields as a requirement from AWS
    Args:
        content (dict): Parsed body of the response
        format (list): List of the fields that need to go into the message
    Returns (str):
        canonical message
    """
    m = ""

    for field in sorted(format):
        try:
            m += field + "\n" + content[field] + "\n"
        except KeyError:
            # Build with what you have
            pass

    return str(m)


def verify_sns_notification(request):
    """Takes a notification request from Amazon push service SNS and verifies the origin of the notification.
    Kudos to Artur Rodrigues for suggesting M2Crypto: http://goo.gl/KAgPPc
    Args:
        request (HTTPRequest): The request object that is passed to the view function
    Returns (bool):
        True if he message passes the verification, False otherwise
    Raises:
        ValueError: If the body of the response couldn't be parsed
        M2CryptoError: If an error raises during the verification process
        URLError: If the SigningCertURL couldn't be opened
    """
    cert = None
    pubkey = None
    canonical_message = None
    canonical_sub_unsub_format = [
        "Message",
        "MessageId",
        "SubscribeURL",
        "Timestamp",
        "Token",
        "TopicArn",
        "Type",
    ]
    canonical_notification_format = [
        "Message",
        "MessageId",
        "Subject",
        "Timestamp",
        "TopicArn",
        "Type",
    ]

    content = json.loads(request.body)
    decoded_signature = b64decode(content["Signature"])

    # Depending on the message type, canonical message format varies: http://goo.gl/oSrJl8
    if (
        request.META.get("HTTP_X_AMZ_SNS_MESSAGE_TYPE", None)
        == SNS_MESSAGE_TYPE_SUB_NOTIFICATION
        or request.META.get("HTTP_X_AMZ_SNS_MESSAGE_TYPE", None)
        == SNS_MESSAGE_TYPE_UNSUB_NOTIFICATION
    ):

        canonical_message = canonical_message_builder(
            content, canonical_sub_unsub_format
        )

    elif (
        request.META.get("HTTP_X_AMZ_SNS_MESSAGE_TYPE", None)
        == SNS_MESSAGE_TYPE_NOTIFICATION
    ):

        canonical_message = canonical_message_builder(
            content, canonical_notification_format
        )

    else:
        raise ValueError(
            "Message Type (%s) is not recognized"
            % request.META.get("HTTP_X_AMZ_SNS_MESSAGE_TYPE", None)
        )

    # Load the certificate and extract the public key
    cert = X509.load_cert_string(str(urllib.request(content["SigningCertURL"]).read()))
    pubkey = cert.get_pubkey()
    pubkey.reset_context(md="sha1")
    pubkey.verify_init()

    # Feed the canonical message to sign it with the public key from the certificate
    pubkey.verify_update(canonical_message)

    # M2Crypto uses EVP_VerifyFinal() from openssl as the underlying verification function.
    # http://goo.gl/Bk2G36: "EVP_VerifyFinal() returns 1 for a correct signature, 0 for failure and -1
    # if some other error occurred."
    verification_result = pubkey.verify_final(decoded_signature)

    if verification_result == 1:
        return True
    elif verification_result == 0:
        return False
    else:
        raise M2CryptoError("Some error occured while verifying the signature.")
