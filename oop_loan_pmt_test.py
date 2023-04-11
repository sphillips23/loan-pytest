# test_friend.py

# assert expression
## if true nothing happens
## if false raises AssertionError

# create virtual environment and activate
# pip install pytest
# pip install pytest-cov

# run tests with python -m pytest -s
# compare -s and -v when running the tests
# run coverage tests with python -m pytest --cov
import pytest
import oop_loan_pmt
from oop_loan_pmt import app, Loan

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

# Unit Tests
def test_loan_creation():
    loan = oop_loan_pmt.Loan(100000, 30, 0.06)
    print("\r")  
    print(" -- test_loan_creation unit test")
    assert loan.loanAmount == 100000
    assert loan.annualRate == 0.06
    assert loan.numberOfPmts == 360
    assert loan.periodicIntRate == 0.005
    assert loan.discountFactor == 0.0
    assert loan.loanPmt == 0

def test_discount_factor_calculation():
    loan = oop_loan_pmt.Loan(100000, 30, 0.06)
    loan.calculateDiscountFactor()
    print("\r") 
    print(" -- test_discount_factor_calculation unit test")
    assert round(loan.getDiscountFactor(), 4) == 166.7916

def test_loan_payment_calculation():
    loan = oop_loan_pmt.Loan(100000, 30, 0.06)
    loan.calculateLoanPmt()
    print("\r")  
    print(" -- test_loan_payment_calculation unit test")
    assert round(loan.getLoanPmt(), 2) == 599.55


# Functional Tests
def test_home_page(client):
    """
    GIVEN a user visits the home page
    WHEN the page loads
    THEN the user sees "Loan Calculator" in the page body
    """
    response = client.get("/")
    assert response.status_code == 200
    print("\r")
    print(" -- home page loads functional test")
    assert b"Loan Calculator" in response.data


def test_calculate_loan_payment(client):
    """
    GIVEN a user enters their loan details
    WHEN the user clicks the calculate button
    THEN the user sees the monthly payment for their loan
    """
    response = client.post(
        "/", data={"loanAmt": "100000", "lengthOfLoan": "30", "intRate": "0.06"}
    )
    print("\r")
    print(" -- calculate loan functional test")
    assert response.status_code == 200
    assert b"$599.55" in response.data