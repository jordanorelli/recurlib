from recurly.models import BaseModel

class Payment(BaseModel):
    item_tag = 'payment'
    collection_tag = 'payments'
    known_attributes = (
        'id',
        'date',
        'amount_in_cents',
        'currency',
        'message',
        'reference',
    )

class LineItem(BaseModel):
    item_tag = 'line_item'
    collection_tag = 'line_items'
    known_attributes = (
        'id',
        'type',
        'amount_in_cents',
        'currency',
        'start_date',
        'end_date',
        'description',
        'created_at',
        'applied_coupon_code',
    )


class Invoice(BaseModel):
    item_tag = 'invoice'
    collection_tag = 'invoices'
    known_attributes = (
        'id',
        'account_code',
        'date',
        'invoice_number',
        'vat_number',
        'status',
        'subtotal_in_cents',
        'total_in_cents',
        'vat_amount_in_cents',
        'paid_in_cents',
        'total_due_in_cents',
        'discount_in_cents',
        'currency',
        'line_items',
        'payments',
    )
