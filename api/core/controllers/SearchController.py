from core.serializers import TransactionSerializer
from core.models import Transaction

class SearchController:
    def __init__(self, first_name, last_name, politician_type, politician_house, start_date, end_date):
        self.first_name = first_name
        self.last_name = last_name
        self.politician_type = politician_type
        self.politician_house = politician_house
        self.start_date = start_date
        self.end_date = end_date

    
    def get_transactions(self):
        filter_criteria = {}
        if self.first_name:
            filter_criteria['politician__profile__first_name'] = self.first_name
        if self.last_name:
            filter_criteria['politician__profile__last_name'] = self.last_name
        if self.politician_type:
            filter_criteria['politician__politician_type'] = self.politician_type
        if self.politician_house:
            filter_criteria['politician__politician_house'] = self.politician_house
        if self.start_date:
            filter_criteria['transaction_date__gte'] = self.start_date.replace("/", "-")
        if self.end_date:
            filter_criteria['transaction_date__lte'] = self.end_date.replace("/", "-")
        
        # Get transactions
        transactions = Transaction.objects.filter(**filter_criteria)
        
        # Serialize the transactions 
        transaction_data = TransactionSerializer(transactions, many = True).data

        return transaction_data