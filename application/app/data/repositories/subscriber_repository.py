"""
Subscriber repository - handles database operations for subscribers.

This repository encapsulates all SQLAlchemy queries for the Subscriber model,
keeping the business layer free from database-specific code.
"""

from app import db
from app.data.models.subscriber import Subscriber


class SubscriberRepository:
    """
    Data access layer for Subscriber operations.

    Provides CRUD operations and queries for the Subscriber model.
    All database interactions for subscribers should go through this class.
    """

    def find_by_email(self, email: str) -> Subscriber | None:
        """
        Find a subscriber by email address.

        Args:
            email: The email address to search for (case-insensitive)

        Returns:
            Subscriber if found, None otherwise
        """
        return Subscriber.query.filter_by(email=email.lower()).first()

    def exists(self, email: str) -> bool:
        """
        Check if a subscriber with the given email exists.

        Args:
            email: The email address to check

        Returns:
            True if subscriber exists, False otherwise
        """
        return self.find_by_email(email) is not None

    def create(self, email: str, name: str) -> Subscriber:
        """
        Create a new subscriber.

        Args:
            email: The subscriber's email address
            name: The subscriber's display name

        Returns:
            The newly created Subscriber instance

        Raises:
            IntegrityError: If email already exists (unique constraint violation)
        """
        subscriber = Subscriber(email=email, name=name)
        db.session.add(subscriber)
        db.session.commit()
        return subscriber

        

