import argparse
import math


def get_month_quantity(principal, payment, loan_interest):

    interest = loan_interest / 12 / 100
    month_quantity = math.ceil(math.log(payment / (payment - interest * principal), 1 + interest))

    years = month_quantity // 12
    months = month_quantity % 12

    result = ''
    if years:
        result += f'{years} year'
        if years % 10 != 1 or years == 11:
            result += 's'

    if years and months:
        result += ' and '

    if months:
        result += f'{months} month'
        if months > 1:
            result += 's'

    print(f"It will take {result} to repay the loan!")
    print(f"Overpayment = {round(payment * month_quantity - principal)}")


def get_annuity_amount(principal, periods, loan_interest):

    interest = loan_interest / 12 / 100
    x = math.pow(1 + interest, periods)
    annuity_payment = principal * interest * x / (x - 1)

    print(f"Your monthly payment = {math.ceil(annuity_payment)}!")
    print(f"Overpayment = {math.ceil(annuity_payment) * periods - math.ceil(principal)}")


def get_loan_principal(payment, periods, loan_interest):

    interest = loan_interest / 12 / 100
    x = math.pow(1 + interest, periods)
    loan_principal = payment / (interest * x / (x - 1))

    print(f"Your loan principal = {round(loan_principal)}!")
    print(f"Overpayment = {round(payment * periods - loan_principal)}")


def get_differentiate_payment(principal, periods, loan_interest):
    payments = 0
    interest = loan_interest / 12 / 100
    for m in range(1, periods + 1):
        d = (principal / periods) + interest * (principal - ((principal * (m - 1)) / periods))
        payments += math.ceil(d)
        print(f"Month {m}: payment is {math.ceil(d)}")
    print(f"Overpayment = {round(payments - principal)}")


def main():
    parser = argparse.ArgumentParser(description="loan calculator CLI")
    parser.add_argument(
        "--type",
        default=0,
        choices=["annuity", "diff"],
        help="type indicates the type of payment: 'annuity' or 'diff' (differentiated)",
    )
    parser.add_argument(
        "--payment",
        default=0,
        type=float,
        help="payment is the monthly payment amount",
    )
    parser.add_argument(
        "--principal",
        default=0,
        type=float,
        help="principal is used for calculations of both types of payment",
    )
    parser.add_argument(
        "--periods",
        default=0,
        type=int,
        help="periods denotes the number of months needed to repay the loan",
    )
    parser.add_argument(
        "--interest",
        type=float,
        default=0,
        help="interest is specified without a percent sign",
    )

    args = parser.parse_args()

    if args.type == 0:
        print("Incorrect parameters")
        return
    if args.interest == 0:
        print("Incorrect parameters")
        return
    if args.type == "diff" and args.payment:
        print("Incorrect parameters")
        return
    if len(vars(args)) <= 4:
        print("Incorrect parameters")
        return
    calc_type = args.type
    payment = args.payment
    principal = args.principal
    periods = args.periods
    interest = args.interest

    if calc_type == "diff":
        get_differentiate_payment(principal, periods, interest)
    elif calc_type == "annuity":
        if principal == 0:
            get_loan_principal(payment, periods, interest)
        elif periods == 0:
            get_month_quantity(principal, payment, interest)
        elif payment == 0:
            get_annuity_amount(principal, periods, interest)


if __name__ == '__main__':
    main()
