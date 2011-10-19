from recurly.models.base import BaseModel

class Charge(BaseModel):
    """
    Whenever a subscription is billed, a charge is recorded for the service /
    period. Charges allow Recurly to track paid service. Charges can also be /
    used for one-time fees. For example, if you want to charge a customer a one /
    time $200 for a support incident, you may submit a charge to Recurly for /
    this item.

    Unlike transactions, charges are not immediately invoiced. When a /
    subscription renews, Recurly will automatically invoice for any non-invoiced /
    charges on the account. Alternatively, you may collect any outstanding /
    charges on an account by posting an invoice.
    """
    item_tag = 'charge'
    collection_tag = 'charges'
    known_attributes = (
        'id',
        'account_code',
        'amount_in_cents',
        'start_date',
        'end_date',
        'description',
        'created_at',
    )
