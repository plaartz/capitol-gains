from django.db.utils import IntegrityError, DatabaseError
from core.models import Transaction, Stock, Profile, Politician

def upload_transactions(transactions: list) -> int:
    """
    Controller to upload transactions scraped from government website to database

    @param transactions     a list of transactions reports
    @return                 status code representing if the upload was successful or not
    """
    try:
        for transaction in transactions:
            # Profile Information
            first_name = transaction['first_name']
            last_name = transaction['last_name']
            middle_initial = transaction['middle_initial']
            profile = Profile(
                first_name=first_name,
                middle_initial=middle_initial,
                last_name=last_name
            )
            try:
                profile_copy = Profile.objects.get(
                    first_name=first_name,
                    middle_initial=middle_initial,
                    last_name=last_name
                )
            except Profile.DoesNotExist:
                profile.save()

            # TODO: Politician Information, ask about politician_house
            politician_type = transaction['filer_type']
            politician = Politician(profile=profile, politician_type=politician_type)
            try:
                politician_copy = Politician.objects.get(
                    profile=profile,
                    politician_type=politician_type
                )
            except Politician.DoesNotExist:
                politician.save()

            disclosure_date = transaction['date_received']
            for trade in transaction['transactions']:
                # TODO: Stock Information
                ticker = trade['ticker']
                stock_name = trade['stock_name']
                stock_description = trade['comment']
                stock = Stock(ticker=ticker, name=stock_name, description_short=stock_description)
                try:
                    stock_copy = Stock.objects.get(
                        ticker=ticker,
                        name=stock_name,
                        description_short=stock_description
                    )
                except Stock.DoesNotExist:
                    stock.save()

                # TODO: Transaction Information
                transaction_amount = trade['transaction_amount']
                transaction_date = trade['transaction_date']
                transaction_type = trade['transaction_type']
                transaction_object = Transaction(
                    politician=politician,
                    stock=stock,
                    transaction_amount=transaction_amount,
                    transaction_date=transaction_date,
                    disclosure_date=disclosure_date,
                    transaction_type=transaction_type
                )
                try:
                    transaction_copy = Transaction.objects.get(
                        politician=politician,
                        stock=stock,
                        transaction_amount=transaction_amount,
                        transaction_date=transaction_date,
                        discolsure_date=disclosure_date,
                        transaction_type=transaction_type
                    )
                except Transaction.DoesNotExist:
                    transaction_object.save()
        return 200
    except (KeyError, TypeError, ValueError):
        return 400
    except IntegrityError:
        return 409
    except DatabaseError:
        return 500
