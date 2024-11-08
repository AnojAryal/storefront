import random
from django.core.management.base import BaseCommand
from faker import Faker
from store.models import (
    Promotion,
    Collection,
    Product,
    Customer,
    Order,
    OrderItem,
    Address,
    Cart,
    CartItem,
)


class Command(BaseCommand):
    help = "Generate seed data for the database"

    def handle(self, *args, **options):
        fake = Faker()

        # Create Promotions
        promotions = [
            Promotion.objects.create(
                description=fake.text(max_nb_chars=50), discount=random.uniform(5, 50)
            )
            for _ in range(10)
        ]

        # Create Collections
        collections = [Collection.objects.create(title=fake.word()) for _ in range(10)]

        # Create Products
        products = [
            Product.objects.create(
                title=fake.word(),
                slug=fake.slug(),
                description=fake.text(),
                price=random.uniform(10, 100),
                inventory=random.randint(1, 100),
                collection=random.choice(collections),
            )
            for _ in range(100)
        ]

        # Assign promotions to products
        for product in products:
            product.promotions.set(random.sample(promotions, k=random.randint(0, 3)))
            product.save()

        # Create Customers
        customers = [
            Customer.objects.create(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email(),
                phone=fake.phone_number()[:11],
                birth_date=fake.date_of_birth(),
                membership=random.choice(
                    [
                        Customer.MEMBERSHIP_BRONZE,
                        Customer.MEMBERSHIP_SILVER,
                        Customer.MEMBERSHIP_GOLD,
                    ]
                ),
            )
            for _ in range(100)
        ]

        # Create Orders
        orders = [
            Order.objects.create(
                placed_at=fake.date_time_this_year(),
                payment_status=random.choice(
                    [
                        Order.PAYMENT_STATUS_PENDING,
                        Order.PAYMENT_STATUS_COMPLETE,
                        Order.PAYMENT_STATUS_FAILED,
                    ]
                ),
                customer=random.choice(customers),
            )
            for _ in range(100)
        ]

        # Create OrderItems
        for order in orders:
            order_items = [
                OrderItem.objects.create(
                    order=order,
                    product=random.choice(products),
                    quantity=random.randint(1, 10),
                    unit_price=product.price,
                )
                for _ in range(random.randint(1, 5))
            ]

        # Create Addresses
        addresses = [
            Address.objects.create(
                street=fake.street_address(),
                city=fake.city(),
                customer=customer,
            )
            for customer in customers
        ]

        # Create Carts
        carts = [
            Cart.objects.create(created_at=fake.date_time_this_year())
            for _ in range(100)
        ]

        # Create CartItems
        for cart in carts:
            cart_items = [
                CartItem.objects.create(
                    cart=cart,
                    product=random.choice(products),
                    quantity=random.randint(1, 5),
                )
                for _ in range(random.randint(1, 5))
            ]

        self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))
