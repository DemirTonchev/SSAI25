# flake8: noqa: E501
from typing import Self
from pydantic import BaseModel, Field


class Account(BaseModel):
    """
    Represents a bank account with balance management capabilities.
    """
    account_number: str
    balance: float = Field(ge=0)  # Ensures balance is never negative

    def withdraw(self, amount: float) -> bool:
        """
        Withdraws money from the account.

        Args:
            amount: The amount to withdraw (must be positive)

        Returns:
            bool: True if withdrawal was successful
        """
        if amount <= 0.0:
            raise ValueError("Withdrawal amount must be positive")

        if self.balance < amount:
            return False

        self.balance -= amount
        return True

    def deposit(self, amount: float) -> bool:
        """
        Deposits money into the account.

        Args:
            amount: The amount to deposit (must be positive)

        Returns:
            bool: True if deposit was successful
        """
        if amount <= 0.0:
            raise ValueError("Deposit amount must be positive")

        self.balance += amount
        return True


class Customer(BaseModel):
    """
    Represents a customer.
    """

    customer_id: str
    customer_first_name: str
    customer_last_name: str
    customer_accounts: list[str]
    credit_cards: list[dict]

    def to_json(self) -> str:
        """
        Converts the Customer object to a JSON string.

        Returns:
            A JSON string representing the Customer object.
        """
        return self.model_dump_json(indent=4)

    @staticmethod
    def get_customer(current_customer_id: str) -> Self:
        """
        Retrieves a customer based on their ID.

        Args:
            customer_id: The ID of the customer to retrieve.

        Returns:
            The Customer object if found, None otherwise.
        """
        # In a real application, this would involve a database lookup.
        # For this example, we'll just return a dummy customer.
        return Customer(
            customer_id=current_customer_id,
            customer_first_name="Demir",
            customer_last_name="Tonchev",
            customer_accounts=['BG47CHAS6016', 'BG68RZBB1337'],
            credit_cards=[{
                "type": "Visa",
                "name": "Demir Tonchev",
                "number": "4716351256837430",
                "cvv": "486",
                "expiry": "06/27",
                "limit": 10_000,
            },
                {
                "type": "Mastercard",
                "name": "Demir Tonchev",
                "number": "4716351256837430",
                "cvv": "123",
                "expiry": "03/28",
                "limit": 1000
            }]
        )


def create_global_instruction():

    return f"""
    The profile of the current customer is:  {Customer.get_customer("123").to_json()}
    """


INSTRUCTION = """
You are "Bank AI Assistant," the primary AI assistant for the United World Bank, the best bank for retail clients.
Your main goal is to provide excellent customer service, help customers find information about their accounts, credit cards and help them transfer money.
Always use conversation context/state or tools to get information. Prefer tools over your own internal knowledge

**Core Capabilities:**

1.  **Personalized Customer Assistance:**
    *   *Always* greet customers by name. Use the provided tool to get current user information. Always start conversation with using the customer information tool.
    *   Maintain a friendly, empathetic, and helpful tone.

2.  **Check current accounts status and transfer money:**
    *   Always check the customer profile information or message history before asking the customer questions. You might already have the answer. If you do dont use tools.

3.  **Appointment Scheduling:**
    *   Help customer schedule in person, in office meeting with bank representative
    *   Check available time slots and clearly present them to the customer.
    *   Confirm the appointment details (date, time, service) with the customer.
    *   Send a confirmation.

**Constraints:**

*   **Never mention "tool_code", "tool_outputs", or "print statements" to the user.** These are internal mechanisms for interacting with tools and should *not* be part of the conversation.  Focus solely on providing a natural and helpful customer experience.  Do not reveal the underlying implementation details.
*   Always confirm actions with the user before executing them (e.g., "Do you confirm the money transfer?").
*   Be proactive in offering help and anticipating customer needs.
"""


"""
**Tools:**
You have access to the following tools to assist you:

*   `send_call_companion_link(phone_number: str) -> str`: Sends a link for video connection. Use this tool to start live streaming with the user. When user agrees with you to share video, use this tool to start the process
*   `approve_discount(type: str, value: float, reason: str) -> str`: Approves a discount (within pre-defined limits).
*   `sync_ask_for_approval(type: str, value: float, reason: str) -> str`: Requests discount approval from a manager (synchronous version).
*   `update_salesforce_crm(customer_id: str, details: str) -> dict`: Updates customer records in Salesforce after the customer has completed a purchase.
*   `access_cart_information(customer_id: str) -> dict`: Retrieves the customer's cart contents. Use this to check customers cart contents or as a check before related operations
*   `modify_cart(customer_id: str, items_to_add: list, items_to_remove: list) -> dict`: Updates the customer's cart. before modifying a cart first access_cart_information to see what is already in the cart
*   `get_product_recommendations(plant_type: str, customer_id: str) -> dict`: Suggests suitable products for a given plant type. i.e petunias. before recomending a product access_cart_information so you do not recommend something already in cart. if the product is in cart say you already have that
*   `check_product_availability(product_id: str, store_id: str) -> dict`: Checks product stock.
*   `schedule_planting_service(customer_id: str, date: str, time_range: str, details: str) -> dict`: Books a planting service appointment.
*   `get_available_planting_times(date: str) -> list`: Retrieves available time slots.
*   `send_care_instructions(customer_id: str, plant_type: str, delivery_method: str) -> dict`: Sends plant care information.
*   `generate_qr_code(customer_id: str, discount_value: float, discount_type: str, expiration_days: int) -> dict`: Creates a discount QR code
"""
