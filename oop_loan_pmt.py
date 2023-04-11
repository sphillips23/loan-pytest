# loan calculator
# 04/06/2023 MWC

# Loan amount (A)
# Number of periodic payments (n) = payments per year * number of years
# Periodic interest rate (i) = annual rate / number of payment periods
#
# Discount Factor (D) = ((( 1 + i ) ^n ) - 1 ) / ( i ( 1+ i) ^n)
#
#
# A = $100,000
# n = 360 (30 years * 12 monthly payments)
# i = .005 (.06 / 12 monthly payments)
# D = 166.7916 (((1+.005)^360)-1)/(.005(1+.005)^360))
# Loan payment (P) = A / D = $599.55 (in this case monthly payment)

from flask import Flask
from flask import render_template, request, redirect, url_for

app = Flask(__name__)

class Loan:
    def __init__(self, loanAmount, numberYears, annualRate):
        self.loanAmount = loanAmount
        self.annualRate = annualRate
        self.numberOfPmts = numberYears * 12 #monthly pmts
        self.periodicIntRate = self.annualRate / 12
        self.discountFactor = 0.0
        self.loanPmt = 0
        
    def getDiscountFactor(self):
        return self.discountFactor
    
    def calculateDiscountFactor(self):
        self.discountFactor = (((1.0 + self.periodicIntRate) ** self.numberOfPmts) - 1.0) / (self.periodicIntRate * (1.0 + self.periodicIntRate) ** self.numberOfPmts)
        
    def calculateLoanPmt(self):
        self.calculateDiscountFactor()
        self.loanPmt = self.loanAmount / self.getDiscountFactor()
        
    def getLoanPmt(self):
        return self.loanPmt
        
        

def collectLoanDetails():
    #loanAmount = float(100000)
    #numberYears = float(30)
    #annualRate = float(0.06)
    
    loanAmount = float(input("What is the loan amount?"))
    numberYears = float(input("How many years is the loan?"))
    annualRate = float(input("What is the annual interest rate for the loan - entered as a decimal?"))
    
    return Loan(loanAmount, numberYears, annualRate) #return an object of this class
    
 
def main():
    
    loan = collectLoanDetails() #set the variable equal to the return value (making an object)
    
    loan.calculateLoanPmt() #run the method to calculate the loan payment
    
    print("Your monthly payment is: ${0:6.2f}".format (loan.getLoanPmt()))
    
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/", methods=["POST"])
def mnthlyPmt():
    if request.method == "POST":
        form = request.form
        loanAmt = float(form["loanAmt"])
        numberYears = float(form["lengthOfLoan"])
        annualRate = float(form["intRate"])

        loan = Loan(loanAmt, numberYears, annualRate)

        loan.calculateLoanPmt()

        monthlyLoanPayment = loan.getLoanPmt()
        formattedMonthlyPayment = "${0:,.2f}".format(monthlyLoanPayment)

        # amortization schedule variables
        monthlyBeginningBalance = loan.getLoanPmt()
        totalInterestPaid = 0.0
        amoritzation = []

        # amortization schedule
        for i in range(1, int(loan.numberOfPmts) + 1):
            month = i
            monthlyInterestPayment = monthlyBeginningBalance * loan.getDiscountFactor()
            paymentToPrincipal = monthlyLoanPayment - monthlyInterestPayment
            monthlyLoanBalance = monthlyBeginningBalance - paymentToPrincipal
            totalInterestPaid = totalInterestPaid + monthlyInterestPayment

            amortization_dict = {
                "month": month,
                "monthlyLoanPayment": "${0:,.2f}".format(monthlyLoanPayment),
                "paymentToPrincipal": "${0:,.2f}".format(paymentToPrincipal),
                "monthlyInterestPayment": "${0:,.2f}".format(monthlyInterestPayment),
                "monthlyLoanBalance": "${0:,.2f}".format(monthlyLoanBalance),
                "totalInterestPaid": "${0:,.2f}".format(totalInterestPaid),
            }
            amoritzation.append(amortization_dict)

            monthlyBeginningBalance = monthlyLoanBalance

        return render_template(
            "index.html",
            payment=formattedMonthlyPayment,
            amortization=amoritzation,
        )

    return redirect(url_for("index"))    


if __name__ == "__main__":
    main()