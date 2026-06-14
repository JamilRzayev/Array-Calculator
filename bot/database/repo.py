from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from bot.database.models import User, Subscription, Transaction

class UserRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_or_create_user(self, telegram_id: int, username: str | None = None):
        stmt = select(User).where(User.telegram_id == telegram_id)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            user = User(telegram_id=telegram_id, username=username)
            self.session.add(user)
            await self.session.flush()
        return user

    async def update_balance(self, telegram_id: int, amount: float):
        stmt = update(User).where(User.telegram_id == telegram_id).values(
            balance=User.balance + amount
        ).returning(User)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

class TransactionRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_transaction(self, user_id: int, amount: float, tx_type: str, status: str = "completed"):
        tx = Transaction(user_id=user_id, amount=amount, type=tx_type, status=status)
        self.session.add(tx)
        return tx

class SubscriptionRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_subscription(self, user_id: int, marzban_username: str, expiry_date):
        sub = Subscription(user_id=user_id, marzban_username=marzban_username, expiry_date=expiry_date)
        self.session.add(sub)
        return sub

    async def get_user_subscriptions(self, user_id: int):
        stmt = select(Subscription).where(Subscription.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()
