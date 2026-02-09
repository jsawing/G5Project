"""
News Flash - Application Factory

This module creates and configures the Flask application using the
application factory pattern. This pattern enables:
- Multiple instances with different configurations
- Easy testing with test configurations
- Delayed configuration loading
"""

import os
from typing import Optional

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from .config import config

# Create extensions at module level (initialized in create_app)
db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name: Optional[str] = None) -> Flask:
    """
    Create and configure the Flask application.

    Args:
        config_name: Configuration to use ('development', 'testing', 'production').
                    Defaults to FLASK_ENV environment variable or 'development'.

    Returns:
        Configured Flask application instance.
    """
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "development")

    app = Flask(
        __name__,
        template_folder="presentation/templates",
        static_folder="presentation/static",
    )

    # Load configuration
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Import models for migration detection
    from .data.models.subscriber import Subscriber  # noqa: F401

    # Create database tables if they don't exist (ensures local file is created)
    with app.app_context():
        db.create_all()

    # Register blueprints
    from .presentation.routes.public import bp as public_bp

    app.register_blueprint(public_bp)

    @app.cli.command("subscribers")
    def list_subscribers():
        """List all subscribers from the database."""
        from app.business.services.subscription_service import SubscriptionService

        service = SubscriptionService()
        try:
            subscribers = service.get_all_subscribers()
            print(f"\n{'ID':<5} {'Name':<20} {'Email':<30} {'Joined':<12}")
            print("-" * 70)
            for sub in subscribers:
                joined = sub.subscribed_at.strftime('%Y-%m-%d')
                print(f"{sub.id:<5} {sub.name:<20} {sub.email:<30} {joined:<12}")
            print("-" * 70)
            print(f"Total: {len(subscribers)}\n")
        except Exception as e:
            print(f"\nError accessing database: {e}")
            print("Make sure to run: flask db upgrade\n")

    return app
