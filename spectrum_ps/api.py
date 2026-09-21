from urllib.parse import urlparse

import frappe
from frappe.utils.oauth import get_oauth2_authorize_url


ALLOWED_PROVIDERS = {"google", "facebook"}


@frappe.whitelist(allow_guest=True)
def get_social_login_url(provider: str):
    provider = (provider or "").strip().lower()

    if provider not in ALLOWED_PROVIDERS:
        frappe.throw("Unsupported social login provider")

    redirect_to = frappe.conf.get("social_login_redirect_url")

    if not redirect_to:
        frappe.throw("Social login redirect URL is not configured")

    parsed_redirect = urlparse(redirect_to)

    if parsed_redirect.scheme not in {"http", "https"} or not parsed_redirect.netloc:
        frappe.throw("Invalid social login redirect URL")

    return get_oauth2_authorize_url(provider, redirect_to)
