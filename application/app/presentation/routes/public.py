"""
Public routes - accessible without authentication.

This blueprint handles all public-facing pages including the landing page
and subscription flow.
"""

from flask import Blueprint, redirect, render_template, request, url_for

from app.business.services.subscription_service import SubscriptionService

bp = Blueprint("public", __name__)


@bp.route("/")
def index():
    """Render the landing page."""
    return render_template("index.html")


@bp.route("/subscribe")
def subscribe():
    """Render the subscription form."""
    return render_template("subscribe.html")


@bp.route("/admin")
def admin():
    """Render the admin dashboard with real database data."""
    service = SubscriptionService()
    try:
        subscribers = service.get_all_subscribers()
    except Exception:
        # Fallback if database is not initialized
        subscribers = []
    return render_template("admin.html", subscribers=subscribers)


@bp.route("/admin/delete/<int:id>", methods=["POST"])
def delete_subscriber(id):
    """Handle subscriber deletion."""
    service = SubscriptionService()
    service.delete_subscriber(id)
    return redirect(url_for("public.admin"))


@bp.route("/subscribe/confirm", methods=["POST"])
def subscribe_confirm():
    """Handle subscription form submission."""
    email = request.form.get("email", "")
    name = request.form.get("name", "")

    # Use business layer for full subscription flow
    service = SubscriptionService()
    try:
        success, error = service.subscribe(email, name)
    except Exception as e:
        success = False
        error = f"Database error: {str(e)}"

    if not success:
        # Return to form with error message, preserving input
        return render_template(
            "subscribe.html",
            error=error,
            email=email,
            name=name,
        )

    # Subscription saved successfully - show thank you page
    # Use normalized values for display
    normalized_email = service.normalize_email(email)
    normalized_name = service.normalize_name(name)

    return render_template(
        "thank_you.html",
        email=normalized_email,
        name=normalized_name,
    )


@bp.route("/subscribers")
def subscribers_list():
    """Render a list of all subscribers from the database."""
    service = SubscriptionService()
    try:
        subscribers = service.get_all_subscribers()
    except Exception:
        # Fallback if database is not initialized
        subscribers = []
    return render_template("subscribers_list.html", subscribers=subscribers)
