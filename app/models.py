import requests, json
import simplify
from app import app

class simplify():
    def __init__(self):

        simplify.public_key = app.config['simplify_public_key']
        simplify.private_key = app.config['simplify_private_key']

    def make_payment(self, cc_number, cc_exp_month, cc_exp_year, cc_cvc, amount, description):
        try:
            payment = simplify.Payment.create({
               "card" : {
                    "number": "%s" % cc_number,
                    "expMonth": cc_exp_month,
                    "expYear": cc_exp_year,
                    "cvc": "%s" % cc_cvc
                },
                "amount" : "%s" % amount,
                "description" : "%s" % description,
                "currency" : "USD"
            })
        except:
            return payment.paymentStatus


        if payment.paymentStatus == 'APPROVED':
            return True

    def create_user(self):
        user = simplify.Customer.create({
            "email" : "customer@mastercard.com",
            "name" : "Customer Customer",
            "card" : {
               "expMonth" : "11",
               "expYear" : "19",
               "cvc" : "123",
               "number" : "5555555555554444"
            },
            "reference" : "Ref1"})

        return user

    def find_user(self, info):
        user = simplify.Customer.find('%s') % info

        return user

    def delete_user(self, info):
        user = self.find_user(info)

        user.delete()

    def update_user(self, key, value, info):
        # @todo not needed for this hack
        return True




