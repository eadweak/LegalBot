import stripe
from bot.config import TOKEN

stripe.api_key = "YOUR_STRIPE_API_KEY"

def process_payment(amount, currency="RUB", description="Подписка"):
    try:
        payment_intent = stripe.PaymentIntent.create(
            amount=int(amount * 100),  # Stripe принимает суммы в копейках
            currency=currency,
            description=description,
        )
        return payment_intent
    except Exception as e:
        return f"Ошибка при обработке оплаты: {e}"
