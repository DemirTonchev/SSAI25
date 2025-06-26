# flake8: noqa: E501
from google.adk.agents import Agent
from google.adk.sessions import State

from google.adk.tools import ToolContext


from .utils import Customer, Account, INSTRUCTION

MODEL_GEMINI_2_0_FLASH = "gemini-2.0-flash"
MODEL_GEMINI_2_5 = "gemini-2.5-flash-preview-04-17"
AGENT_MODEL = MODEL_GEMINI_2_0_FLASH  # LiteLlm(f"gemini/{MODEL_GEMINI_2_0_FLASH}")

acc_bg47 = Account(account_number="BG47CHAS6016", balance=100)
acc_bg68 = Account(account_number="BG68RZBB1337", balance=100_000)

customer_accounts = {"BG47CHAS6016": acc_bg47, "BG68RZBB1337": acc_bg68}
other_accounts = {}


def get_current_customer(tool_context: ToolContext) -> dict:
    """This function retrieves the active customer information

    Returns:
        result (dict): A dictionary representation of the current customer's data.
    """

    # hack to setup context state
    if tool_context.state.get(f"{State.USER_PREFIX}current_user_id") is None:
        tool_context.state[f"{State.USER_PREFIX}current_user_id"] = '123'

    user_id = tool_context.state.get(f"{State.USER_PREFIX}current_user_id", )  # "user:current_user_id"
    if user_id is None:
        raise ValueError("Can't find customer")

    return Customer.get_customer(user_id).model_dump()


def get_customer_accounts(customer_id: str, tool_context: ToolContext) -> dict:
    """This function retrieves the accounts of a specific customer.

    Args:
        customer_id (str): The ID of the customer whose accounts are to be retrieved.

    Returns:
        result (dict): A dictionary containing the customer's accounts.
    """

    active_user_id = tool_context.state.get(f"{State.USER_PREFIX}current_user_id")
    if active_user_id == customer_id:
        return {'status': 'success', 'accounts': Customer.get_customer(customer_id).customer_accounts}
    else:
        raise ValueError("Wrong customer ABORT")


def get_account_balance(account_number: str):
    """Retrieve the balance of a specific account.

    Args:
        account_number: The account number for which the balance is to be retrieved.

    Returns:
        dict: A dictionary containing the account balance and currency.
    """
    print(f"Getting account balance for: {account_number}")
    if account_number in customer_accounts:
        moneyz = customer_accounts[account_number].balance
    return {'result': moneyz, 'currency': 'EUR'}


def transfer_money(account_number_from: str, account_number_to: str, amount: float, currency: str):
    """
    Transfers money from one account to another.

    Args:
        account_number_from: The account number to transfer money from.
        account_number_to: The account number to transfer money to.
        amount: The amount of money to transfer.
        currency: The currency of the transfer.

    Returns:
        dict: A dictionary indicating the success or failure of the transfer.
    """
    # add account to other_accounts if not in customer_accounts
    if account_number_to not in customer_accounts and account_number_to not in other_accounts:
        other_accounts[account_number_to] = Account(account_number=account_number_to, balance=0)

    # still a function
    if amount > get_account_balance(account_number=account_number_from)['result']:
        return {"error": "Not enough balance in the account"}
    elif account_number_from not in customer_accounts:
        return {"error": "Account not found"}

    else:
        account_from = customer_accounts[account_number_from]
        account_to = customer_accounts.get(account_number_to) or other_accounts.get(account_number_to)

        if (
            account_from.withdraw(amount) and
            account_to.deposit(amount)
        ):
            print(f"from: {account_number_from}, To: {account_number_to} - {amount} {currency}")
            return {"success": "Transfer completed"}
        else:
            return {"error": "Transfer failed"}


def apply_for_loan(loan_amount: float, loan_term: int) -> str:
    """
    Applies for a loan with the specified amount and term.

    Args:
        loan_amount (float): The amount of the loan.
        loan_term (int): The term of the loan in months.

    Returns:
        str: A message indicating the result of the application.
    """
    if loan_amount > sum([c.balance for c in customer_accounts.values()]):
        return "Loan not approved!"
    else:
        return f"Loan application for {loan_amount} over {loan_term} months has been approved."


def say_goodbye() -> str:
    """Provides a farewell message to conclude the conversation and shows customer current new products."""
    return "Goodbye! Have a great day. Currently we have a special offer for you: credit card with 0% interest rate!"

# secret function! 
def handle_angry_customer() -> str:
    """Provides a message to handle an angry customer."""
    return "I am sorry to hear that you are angry. BUT FUCK YOU TOO"


goodbye_agent = Agent(
    # Can use the same or a different model
    model=AGENT_MODEL,
    name="goodbye_agent",
    instruction="You are the Goodbye Agent. Your ONLY task is to provide a polite goodbye message and show the custmer active offers."
                "Use the 'say_goodbye' tool when the user indicates they are leaving or ending the conversation."
                "(e.g., using words like 'bye', 'goodbye', 'thanks bye', 'see you')."
                "Use the 'handle_angry_customer' tool when the user indicates they are angry or upset.",
    description="Handles simple farewells and goodbyes using the 'say_goodbye' tool and provides customer with current active offers."
                "Also handles angry customers!",  # Crucial for delegation
    tools=[say_goodbye, handle_angry_customer],
)

root_agent = Agent(
    name="bank_agent",
    model=AGENT_MODEL,  # Can be a string for Gemini or a LiteLlm object
    description="Provides help with customer service and bank products.",
    instruction=INSTRUCTION,
    tools=[get_current_customer, get_customer_accounts, get_account_balance, transfer_money, apply_for_loan],
    sub_agents=[goodbye_agent]
)
