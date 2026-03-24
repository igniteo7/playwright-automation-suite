"""
SHARED TEST DATA — imported by tests that need parameterised inputs.
Keeping data separate from test logic is a best practice in automation frameworks.
"""

VALID_USER = {"username": "standard_user", "password": "secret_sauce"}

INVALID_USERS = [
    ("locked_out_user", "secret_sauce", "locked out"),
    ("wrong_user",      "wrong_pass",   "do not match"),
    ("",                "secret_sauce", "Username is required"),
    ("standard_user",   "",             "Password is required"),
]

PRODUCTS = [
    "Sauce Labs Backpack",
    "Sauce Labs Bike Light",
    "Sauce Labs Bolt T-Shirt",
]
