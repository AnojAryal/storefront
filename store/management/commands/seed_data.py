import random
from django.core.management.base import BaseCommand
from faker import Faker
from uuid import uuid4
from django.contrib.auth import get_user_model
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
    Review,
)

User = get_user_model()


class Command(BaseCommand):
    help = "Generate seed data for the database"

    def handle(self, *args, **options):
        fake = Faker()

        # Create Promotions
        promotions = [
            Promotion.objects.create(
                description=fake.text(max_nb_chars=50),
                discount=round(random.uniform(5, 50), 2),
            )
            for _ in range(10)
        ]

        # Create Collections
        collections = [
            Collection.objects.create(
                title=fake.word(),
                featured_product=None,
            )
            for _ in range(5)
        ]

        # Create Products
        products = []
        for _ in range(20):
            product = Product.objects.create(
                title=fake.word(),
                slug=fake.slug(),
                description=fake.text(),
                price=round(random.uniform(10, 500), 2),
                inventory=random.randint(10, 100),
                collection=random.choice(collections),
            )
            product.promotions.set(random.sample(promotions, random.randint(0, 3)))
            product.save()
            products.append(product)

        # Assign featured products to collections
        for collection in collections:
            collection.featured_product = random.choice(products)
            collection.save()

        # Create Users and Customers
        customers = []
        for _ in range(10):
            user = User.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password="password123",
                first_name=fake.first_name(),
                last_name=fake.last_name(),
            )
            customer = Customer.objects.create(
                user=user,
                phone=fake.phone_number()[:11],
                birth_date=fake.date_of_birth(minimum_age=18, maximum_age=70),
                membership=random.choice(
                    [
                        Customer.MEMBERSHIP_BRONZE,
                        Customer.MEMBERSHIP_SILVER,
                        Customer.MEMBERSHIP_GOLD,
                    ]
                ),
            )
            customers.append(customer)

        # Create Orders and OrderItems
        for _ in range(15):
            order = Order.objects.create(
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
            for _ in range(random.randint(1, 5)):
                product = random.choice(products)
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=random.randint(1, 10),
                    unit_price=product.price,
                )

        # Create Addresses
        for customer in customers:
            Address.objects.create(
                street=fake.street_address(),
                city=fake.city(),
                customer=customer,
            )

        # Create Carts and CartItems
        for _ in range(5):
            cart = Cart.objects.create()
            for _ in range(random.randint(1, 5)):
                CartItem.objects.create(
                    cart=cart,
                    product=random.choice(products),
                    quantity=random.randint(1, 10),
                )

        # Create Reviews
        for _ in range(30):
            product = random.choice(products)
            Review.objects.create(
                product=product,
                name=fake.name(),
                description=fake.text(),
                date=fake.date_this_year(),
            )

        self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))
