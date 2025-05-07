import os
import pickle
from abc import ABC, abstractmethod
from datetime import date, datetime
from enum import Enum
from typing import List, Optional


# Enum Types
class RaceCategory(Enum):
    PREMIUM = "Premium"
    STANDARD = "Standard"
    ECONOMY = "Economy"


class OrderStatus(Enum):
    PENDING = "Pending"
    CONFIRMED = "Confirmed"
    CANCELLED = "Cancelled"


class PaymentMethod(Enum):
    CREDIT_CARD = "Credit Card"
    DEBIT_CARD = "Debit Card"
    DIGITAL_WALLET = "Digital Wallet"


# Abstract Ticket Class
class Ticket(ABC):
    def __init__(self, ticket_id: str, price: float, event_date: date, venue_section: str):
        self.__ticket_id = ticket_id  # Private attribute
        self.__price = price  # Private attribute
        self.__event_date = event_date  # Private attribute
        self.__venue_section = venue_section  # Private attribute
        self.__is_used = False  # Private attribute
        self.__created_by = None  # Private attribute for admin reference

    # Getters and setters
    def get_ticket_id(self) -> str:
        return self.__ticket_id

    def set_ticket_id(self, ticket_id: str) -> None:
        self.__ticket_id = ticket_id

    def get_price(self) -> float:
        return self.__price

    def set_price(self, price: float) -> None:
        if price < 0:
            raise ValueError("Price cannot be negative")
        self.__price = price

    def get_event_date(self) -> date:
        return self.__event_date

    def set_event_date(self, event_date: date) -> None:
        self.__event_date = event_date

    def get_venue_section(self) -> str:
        return self.__venue_section

    def set_venue_section(self, venue_section: str) -> None:
        self.__venue_section = venue_section

    def is_used(self) -> bool:
        return self.__is_used

    def set_used(self, is_used: bool) -> None:
        self.__is_used = is_used

    def get_created_by(self):
        return self.__created_by

    def set_created_by(self, admin) -> None:
        self.__created_by = admin

    @abstractmethod
    def calculate_price(self) -> float:
        """Calculate the final price of the ticket, must be implemented by subclasses"""
        pass

    def __str__(self) -> str:
        return f"Ticket ID: {self.__ticket_id}, Price: ${self.__price}, Date: {self.__event_date}, Section: {self.__venue_section}"


# SingleRaceTicket Class
class SingleRaceTicket(Ticket):
    def __init__(self, ticket_id: str, price: float, event_date: date, venue_section: str,
                 race_name: str, race_category: RaceCategory):
        super().__init__(ticket_id, price, event_date, venue_section)
        self.__race_name = race_name  # Private attribute
        self.__race_category = race_category  # Private attribute using enum

    # Getters and setters
    def get_race_name(self) -> str:
        return self.__race_name

    def set_race_name(self, race_name: str) -> None:
        self.__race_name = race_name

    def get_race_category(self) -> RaceCategory:
        return self.__race_category

    def set_race_category(self, race_category: RaceCategory) -> None:
        self.__race_category = race_category

    def calculate_price(self) -> float:
        """Calculate final price based on race category"""
        base_price = self.get_price()
        if self.__race_category == RaceCategory.PREMIUM:
            return base_price * 1.2  # 20% premium
        elif self.__race_category == RaceCategory.STANDARD:
            return base_price
        else:  # ECONOMY
            return base_price * 0.9  # 10% discount

    def __str__(self) -> str:
        return f"{super().__str__()}, Race: {self.__race_name}, Category: {self.__race_category.value}"


# SeasonTicket Class
class SeasonTicket(Ticket):
    def __init__(self, ticket_id: str, price: float, event_date: date, venue_section: str,
                 season_year: int, included_races: List[str], race_dates: List[date] = None):
        # For SeasonTicket, event_date represents season start date
        super().__init__(ticket_id, price, event_date, venue_section)
        self.__season_year = season_year  # Private attribute
        self.__included_races = included_races  # Private attribute
        self.__race_dates = race_dates if race_dates else []  # Private attribute

    # Getters and setters
    def get_season_year(self) -> int:
        return self.__season_year

    def set_season_year(self, season_year: int) -> None:
        self.__season_year = season_year

    def get_included_races(self) -> List[str]:
        return self.__included_races

    def set_included_races(self, included_races: List[str]) -> None:
        self.__included_races = included_races

    def get_race_dates(self) -> List[date]:
        return self.__race_dates

    def set_race_dates(self, race_dates: List[date]) -> None:
        self.__race_dates = race_dates

    def calculate_price(self) -> float:
        """Calculate final price based on number of included races"""
        base_price = self.get_price()
        num_races = len(self.__included_races)

        if num_races >= 15:
            return base_price * 0.7  # 30% discount for 15+ races
        elif num_races >= 10:
            return base_price * 0.8  # 20% discount for 10-14 races
        elif num_races >= 5:
            return base_price * 0.9  # 10% discount for 5-9 races
        else:
            return base_price  # No discount for less than 5 races

    def __str__(self) -> str:
        races_str = ", ".join(self.__included_races) if self.__included_races else "None"
        return f"{super().__str__()}, Year: {self.__season_year}, Races: {races_str}"


# User Class
class User:
    def __init__(self, user_id: str, username: str, password: str, email: str, phone_number: str = None):
        self.__user_id = user_id  # Private attribute
        self.__username = username  # Private attribute
        self.__password = password  # Private attribute
        self.__email = email  # Private attribute
        self.__phone_number = phone_number  # Private attribute
        self.__orders = []  # Private attribute for bidirectional relationship

    # Getters and setters
    def get_user_id(self) -> str:
        return self.__user_id

    def set_user_id(self, user_id: str) -> None:
        self.__user_id = user_id

    def get_username(self) -> str:
        return self.__username

    def set_username(self, username: str) -> None:
        self.__username = username

    def get_password(self) -> str:
        return self.__password

    def set_password(self, password: str) -> None:
        if len(password) < 6:
            raise ValueError("Password must be at least 6 characters long")
        self.__password = password

    def get_email(self) -> str:
        return self.__email

    def set_email(self, email: str) -> None:
        if '@' not in email:
            raise ValueError("Invalid email format")
        self.__email = email

    def get_phone_number(self) -> Optional[str]:
        return self.__phone_number

    def set_phone_number(self, phone_number: str) -> None:
        self.__phone_number = phone_number

    def get_orders(self) -> List:
        return self.__orders

    def add_order(self, order) -> None:
        self.__orders.append(order)

    def verify_password(self, password: str) -> bool:
        return self.__password == password

    def __str__(self) -> str:
        return f"User: {self.__username} ({self.__email})"


# Admin Class
class Admin(User):
    def __init__(self, user_id: str, username: str, password: str, email: str,
                 admin_level: int, department: str, phone_number: str = None):
        super().__init__(user_id, username, password, email, phone_number)
        self.__admin_level = admin_level  # Private attribute
        self.__department = department  # Private attribute

    # Getters and setters
    def get_admin_level(self) -> int:
        return self.__admin_level

    def set_admin_level(self, admin_level: int) -> None:
        if admin_level < 1 or admin_level > 3:
            raise ValueError("Admin level must be between 1 and 3")
        self.__admin_level = admin_level

    def get_department(self) -> str:
        return self.__department

    def set_department(self, department: str) -> None:
        self.__department = department

    def create_ticket(self, ticket_type: str, ticket_id: str, price: float, event_date: date,
                      venue_section: str, **kwargs) -> Ticket:
        """Create a new ticket of the specified type"""
        ticket = None

        if ticket_type == "SingleRace":
            race_name = kwargs.get('race_name', '')
            if not race_name:
                raise ValueError("Race name is required for SingleRaceTicket")

            race_category = kwargs.get('race_category', RaceCategory.STANDARD)
            ticket = SingleRaceTicket(ticket_id, price, event_date, venue_section, race_name, race_category)

        elif ticket_type == "Season":
            season_year = kwargs.get('season_year', event_date.year)
            included_races = kwargs.get('included_races', [])
            race_dates = kwargs.get('race_dates', [])

            ticket = SeasonTicket(ticket_id, price, event_date, venue_section,
                                  season_year, included_races, race_dates)
        else:
            raise ValueError(f"Invalid ticket type: {ticket_type}")

        # Set the admin as creator
        ticket.set_created_by(self)

        return ticket

    def __str__(self) -> str:
        return f"Admin: {self.get_username()}, Level: {self.__admin_level}, Department: {self.__department}"


# Order Class
class Order:
    def __init__(self, order_id: str, order_date: date, status: OrderStatus = OrderStatus.PENDING,
                 total_amount: float = 0.0, payment_method: PaymentMethod = None):
        self.__order_id = order_id  # Private attribute
        self.__order_date = order_date  # Private attribute
        self.__status = status  # Private attribute using enum
        self.__total_amount = total_amount  # Private attribute
        self.__payment_method = payment_method  # Private attribute using enum
        self.__tickets = []  # Private attribute for composition relationship
        self.__user_id = None  # Private attribute to reference the user

    # Getters and setters
    def get_order_id(self) -> str:
        return self.__order_id

    def set_order_id(self, order_id: str) -> None:
        self.__order_id = order_id

    def get_order_date(self) -> date:
        return self.__order_date

    def set_order_date(self, order_date: date) -> None:
        self.__order_date = order_date

    def get_status(self) -> OrderStatus:
        return self.__status

    def set_status(self, status: OrderStatus) -> None:
        self.__status = status

    def get_total_amount(self) -> float:
        return self.__total_amount

    def set_total_amount(self, total_amount: float) -> None:
        if total_amount < 0:
            raise ValueError("Total amount cannot be negative")
        self.__total_amount = total_amount

    def get_payment_method(self) -> Optional[PaymentMethod]:
        return self.__payment_method

    def set_payment_method(self, payment_method: PaymentMethod) -> None:
        self.__payment_method = payment_method

    def get_user_id(self) -> str:
        return self.__user_id

    def set_user_id(self, user_id: str) -> None:
        self.__user_id = user_id

    # Methods to manage tickets
    def add_ticket(self, ticket: Ticket) -> None:
        """Add a ticket to the order"""
        if self.__status == OrderStatus.CONFIRMED:
            raise ValueError("Cannot add tickets to a confirmed order")

        self.__tickets.append(ticket)
        self.__total_amount = self.calculate_total()

    def remove_ticket(self, ticket_id: str) -> bool:
        """Remove a ticket from the order"""
        if self.__status == OrderStatus.CONFIRMED:
            return False

        for i, ticket in enumerate(self.__tickets):
            if ticket.get_ticket_id() == ticket_id:
                self.__tickets.pop(i)
                self.__total_amount = self.calculate_total()
                return True

        return False

    def get_tickets(self) -> List[Ticket]:
        """Get all tickets in the order"""
        return self.__tickets

    def calculate_total(self) -> float:
        """Calculate the total amount of the order"""
        return sum(ticket.calculate_price() for ticket in self.__tickets)

    def confirm_order(self) -> bool:
        """Confirm the order if conditions are met"""
        if not self.__tickets:
            return False

        if not self.__payment_method:
            return False

        self.__status = OrderStatus.CONFIRMED
        return True

    def cancel_order(self) -> bool:
        """Cancel the order if possible"""
        # Check if any tickets are already used
        for ticket in self.__tickets:
            if ticket.is_used():
                return False

        # Check if any event dates have passed
        today = date.today()
        for ticket in self.__tickets:
            if ticket.get_event_date() < today:
                return False

        self.__status = OrderStatus.CANCELLED
        return True

    def __str__(self) -> str:
        return (f"Order #{self.__order_id}, Status: {self.__status.value}, "
                f"Total: ${self.__total_amount:.2f}, Tickets: {len(self.__tickets)}")


# BookingSystem Class with Pickle Persistence
class BookingSystem:
    def __init__(self, name: str, version: str):
        self.__name = name  # Private attribute
        self.__version = version  # Private attribute
        self._database = None  # Protected attribute
        self._log_file = "booking_system.log"  # Protected attribute

        # Aggregation relationships
        self.__users = {}  # username -> User
        self.__admins = {}  # username -> Admin (also in users)
        self.__tickets = {}  # ticket_id -> Ticket
        self.__orders = {}  # order_id -> Order

        # Data directory
        self._data_dir = "data"
        if not os.path.exists(self._data_dir):
            os.makedirs(self._data_dir)

        # Load data from files if they exist
        self.load_data()

    # Getters and setters
    def get_name(self) -> str:
        return self.__name

    def set_name(self, name: str) -> None:
        self.__name = name

    def get_version(self) -> str:
        return self.__version

    def set_version(self, version: str) -> None:
        self.__version = version

    # File operations
    def save_data(self) -> bool:
        """Save all system data to pickle files"""
        try:
            # Save users
            with open(os.path.join(self._data_dir, 'users.pkl'), 'wb') as f:
                pickle.dump(self.__users, f)

            # Save admins
            with open(os.path.join(self._data_dir, 'admins.pkl'), 'wb') as f:
                pickle.dump(self.__admins, f)

            # Save tickets
            with open(os.path.join(self._data_dir, 'tickets.pkl'), 'wb') as f:
                pickle.dump(self.__tickets, f)

            # Save orders
            with open(os.path.join(self._data_dir, 'orders.pkl'), 'wb') as f:
                pickle.dump(self.__orders, f)

            self._write_log("All data saved successfully")
            return True
        except Exception as e:
            self._write_log(f"Error saving data: {e}")
            return False

    def load_data(self) -> bool:
        """Load all system data from pickle files"""
        try:
            # Load users
            users_path = os.path.join(self._data_dir, 'users.pkl')
            if os.path.exists(users_path):
                with open(users_path, 'rb') as f:
                    self.__users = pickle.load(f)
                self._write_log(f"Loaded {len(self.__users)} users")

            # Load admins
            admins_path = os.path.join(self._data_dir, 'admins.pkl')
            if os.path.exists(admins_path):
                with open(admins_path, 'rb') as f:
                    self.__admins = pickle.load(f)
                self._write_log(f"Loaded {len(self.__admins)} admins")
            else:
                # Create default admin if no admin data exists
                if not self.__admins:
                    self.create_admin(
                        "ADM-001",
                        "admin",
                        "admin123",
                        "admin@grandprix.com",
                        3,  # Highest level
                        "System Administration"
                    )
                    self._write_log("Created default admin account")

            # Load tickets
            tickets_path = os.path.join(self._data_dir, 'tickets.pkl')
            if os.path.exists(tickets_path):
                with open(tickets_path, 'rb') as f:
                    self.__tickets = pickle.load(f)
                self._write_log(f"Loaded {len(self.__tickets)} tickets")

            # Load orders
            orders_path = os.path.join(self._data_dir, 'orders.pkl')
            if os.path.exists(orders_path):
                with open(orders_path, 'rb') as f:
                    self.__orders = pickle.load(f)
                self._write_log(f"Loaded {len(self.__orders)} orders")

            return True
        except Exception as e:
            self._write_log(f"Error loading data: {e}")
            return False

    # Protected methods
    def _connect_database(self) -> bool:
        """Connect to the database (protected method)"""
        # Simulate database connection
        self._database = "connected"
        self._write_log("Database connected")
        return True

    def _write_log(self, message: str) -> None:
        """Write to the log file (protected method)"""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_message = f"[{timestamp}] {message}\n"

            with open(self._log_file, 'a') as f:
                f.write(log_message)

            # Print to console as well
            print(f"LOG: {message}")
        except Exception as e:
            print(f"Error writing to log file: {e}")
            print(f"LOG: {message}")

    # User management
    def create_user(self, user_id: str, username: str, password: str, email: str, phone_number: str = None) -> User:
        """Create a new user"""
        if username in self.__users:
            raise ValueError(f"Username '{username}' already exists")

        user = User(user_id, username, password, email, phone_number)
        self.__users[username] = user
        self._write_log(f"Created user: {username}")

        # Save changes to file
        self.save_data()

        return user

    def create_admin(self, user_id: str, username: str, password: str, email: str,
                     admin_level: int, department: str, phone_number: str = None) -> Admin:
        """Create a new admin"""
        if username in self.__users:
            raise ValueError(f"Username '{username}' already exists")

        admin = Admin(user_id, username, password, email, admin_level, department, phone_number)
        self.__users[username] = admin
        self.__admins[username] = admin
        self._write_log(f"Created admin: {username}")

        # Save changes to file
        self.save_data()

        return admin

    def get_user(self, username: str) -> Optional[User]:
        """Get a user by username"""
        return self.__users.get(username)

    def get_admin(self, username: str) -> Optional[Admin]:
        """Get an admin by username"""
        return self.__admins.get(username)

    # Ticket management
    def register_ticket(self, ticket: Ticket) -> None:
        """Register a ticket in the system"""
        ticket_id = ticket.get_ticket_id()
        if ticket_id in self.__tickets:
            raise ValueError(f"Ticket ID '{ticket_id}' already exists")

        self.__tickets[ticket_id] = ticket
        self._write_log(f"Registered ticket: {ticket_id}")

        # Save changes to file
        self.save_data()

    def get_ticket(self, ticket_id: str) -> Optional[Ticket]:
        """Get a ticket by ID"""
        return self.__tickets.get(ticket_id)

    # Order management
    def create_order(self, user: User) -> Order:
        """Create a new order for a user"""
        # Generate a unique order ID
        order_id = f"ORD-{len(self.__orders) + 1}"
        order = Order(order_id, date.today())
        order.set_user_id(user.get_username())

        # Add order to the system
        self.__orders[order_id] = order

        # Add order to user's order history (bidirectional relationship)
        user.add_order(order)

        self._write_log(f"Created order: {order_id} for user: {user.get_username()}")

        # Save changes to file
        self.save_data()

        return order

    def get_order(self, order_id: str) -> Optional[Order]:
        """Get an order by ID"""
        return self.__orders.get(order_id)

    def update_order(self, order: Order) -> None:
        """Update an existing order in the system"""
        order_id = order.get_order_id()
        if order_id not in self.__orders:
            raise ValueError(f"Order '{order_id}' does not exist")

        self.__orders[order_id] = order
        self._write_log(f"Updated order: {order_id}")

        # Save changes to file
        self.save_data()

    def __str__(self) -> str:
        return (f"BookingSystem: {self.__name} v{self.__version}, "
                f"Users: {len(self.__users)}, Orders: {len(self.__orders)}, "
                f"Tickets: {len(self.__tickets)}")


# Example usage
def main():
    # Create a booking system
    system = BookingSystem("Grand Prix Experience", "1.0")

    try:
        print("\n" + "=" * 80)
        print("GRAND PRIX EXPERIENCE TICKET BOOKING SYSTEM DEMO")
        print("=" * 80 + "\n")

        # 1. User Creation
        print("-" * 80)
        print("1. CREATING USERS")
        print("-" * 80)

        # Create a regular user
        user = system.create_user(
            "USR-001",
            "john_doe",
            "password123",
            "john@example.com",
            "555-1234"
        )
        print(f"Regular User Created: {user}")

        # Create an admin
        admin = system.create_admin(
            "ADM-002",
            "admin_user",
            "admin123",
            "admin@example.com",
            2,  # Admin level
            "Operations",  # Department
            "555-5678"
        )
        print(f"Admin User Created: {admin}")
        print()

        # 2. Ticket Creation
        print("-" * 80)
        print("2. CREATING TICKETS")
        print("-" * 80)

        # Admin creates tickets
        single_ticket = admin.create_ticket(
            "SingleRace",
            "TKT-001",
            200.0,
            date(2025, 6, 15),
            "Main Grandstand",
            race_name="Monaco Grand Prix",
            race_category=RaceCategory.PREMIUM
        )
        system.register_ticket(single_ticket)
        print(f"Single Race Ticket Created: {single_ticket}")
        print(f"Base Price: ${single_ticket.get_price():.2f}")
        print(f"Calculated Price: ${single_ticket.calculate_price():.2f}")
        print()

        season_ticket = admin.create_ticket(
            "Season",
            "TKT-002",
            1000.0,
            date(2025, 1, 1),  # Season start date
            "VIP Lounge",
            season_year=2025,
            included_races=["Monaco", "Silverstone", "Monza", "Singapore", "Abu Dhabi"],
            race_dates=[
                date(2025, 5, 25),  # Monaco
                date(2025, 7, 7),  # Silverstone
                date(2025, 9, 1),  # Monza
                date(2025, 9, 21),  # Singapore
                date(2025, 12, 1)  # Abu Dhabi
            ]
        )
        system.register_ticket(season_ticket)
        print(f"Season Ticket Created: {season_ticket}")
        print(f"Base Price: ${season_ticket.get_price():.2f}")
        print(f"Calculated Price (with discount): ${season_ticket.calculate_price():.2f}")
        print()

        # 3. Order Processing
        print("-" * 80)
        print("3. PROCESSING ORDERS")
        print("-" * 80)

        # Create an order
        order = system.create_order(user)
        print(f"New Order Created: {order}")

        # Add tickets to the order
        order.add_ticket(single_ticket)
        print(f"Added Single Race Ticket to order.")
        print(f"Order Status: {order}")
        system.update_order(order)  # Save the updated order

        order.add_ticket(season_ticket)
        print(f"Added Season Ticket to order.")
        print(f"Order Status: {order}")
        system.update_order(order)  # Save the updated order
        print()

        # Process payment and confirm order
        print("Setting payment method to Credit Card...")
        order.set_payment_method(PaymentMethod.CREDIT_CARD)

        print("Attempting to confirm order...")
        if order.confirm_order():
            print(f"SUCCESS: Order confirmed!")
            print(f"Final Order Status: {order}")
            system.update_order(order)  # Save the confirmed order
        else:
            print("ERROR: Could not confirm order.")
        print()

        # Try to cancel the order
        print("Attempting to cancel confirmed order...")
        if order.cancel_order():
            print("SUCCESS: Order cancelled.")
            system.update_order(order)  # Save the cancelled order
        else:
            print("NOTICE: Could not cancel order (already confirmed).")
        print()

        # 4. System Status and Data Persistence
        print("-" * 80)
        print("4. SYSTEM STATUS AND DATA PERSISTENCE")
        print("-" * 80)

        # Check user's orders
        print(f"User {user.get_username()} has {len(user.get_orders())} orders in their history.")

        # Print the booking system status
        print(f"System Status: {system}")

        # Show that data is saved
        print("\nAll data has been saved to the following files:")
        print(f"- {os.path.join(system._data_dir, 'users.pkl')}")
        print(f"- {os.path.join(system._data_dir, 'admins.pkl')}")
        print(f"- {os.path.join(system._data_dir, 'tickets.pkl')}")
        print(f"- {os.path.join(system._data_dir, 'orders.pkl')}")
        print(f"- {system._log_file}")

        print("\nYou can restart the application and the data will be loaded from these files.")
        print("\n" + "=" * 80)
        print("DEMONSTRATION COMPLETED SUCCESSFULLY")
        print("=" * 80)

    except ValueError as e:
        print(f"\nERROR: {e}")
        print("\nDemonstration terminated due to an error.")


if __name__ == "__main__":
    main()