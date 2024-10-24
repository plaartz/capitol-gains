from datetime import datetime, timedelta
from django.db.models import Exists

from core.models import Transaction, Stock, Profile, Politician

def upload_transactions(transactions: list) -> int:
    """
    Controller to upload transactions scraped from government website to database

    @param transactions     a list of transactions reports
    @return                 status code representing if the upload was successful or not
    """
    for transaction in transactions:
        # Profile Information
        first_name = transaction['first_name']
        last_name = transaction['last_name']
        middle_initial = transaction['middle_initial']
        profile = Profile(first_name=first_name, middle_initial=middle_initial, last_name=last_name)
        
        # TODO: Politician Information

        # TODO: Stock Information
    pass
