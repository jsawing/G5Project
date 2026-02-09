"""
Admin routes for managing subscribers.

Initially unprotected - authentication will be added later.
"""

from flask import Blueprint, render_template

from app.business.services.subscription_service import SubscriptionService

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/subscribers")
def subscribers():
    """Display list of all newsletter subscribers."""
    service = SubscriptionService()
    all_subscribers = service.get_all_subscribers()
    return render_template(
        "admin/subscribers.html",
        subscribers=all_subscribers,
        count=len(all_subscribers),
    )
