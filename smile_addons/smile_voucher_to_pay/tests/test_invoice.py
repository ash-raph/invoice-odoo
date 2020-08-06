from odoo.tests import TransactionCase
from odoo.exceptions import UserError
from datetime import datetime


class TestInvoice(TransactionCase):
    def setUp(self):
        super(TestInvoice, self).setUp()
        user_kwargs = {
            'login': 'user_1',
            'name': "user_1",
            'email': 'user_1@email.com',
            'groups_id': [(6, 0, [self.env.ref('base.group_system').id])],
        }
        self.user_1 = self.env['res.users'].create(user_kwargs)
        user_kwargs.update({
            'login': 'user_2',
            'name': "user_2",
            'email': 'user_2@email.com',
            'validation_threshold': 5500,
        })
        self.user_2 = self.env['res.users'].create(user_kwargs)

        self.product_1 = self.env['product.product'].create({
            'name': 'P1',
            'type': 'consu',
            'list_price': 20,
            'categ_id': self.env.ref('product.product_category_1').id
        })
        self.product_2 = self.env['product.product'].create({
            'name': 'P2',
            'list_price': 50,
            'type': 'consu',
            'categ_id': self.env.ref('product.product_category_1').id
        })
        self.purchase = self.env['purchase.order'].create(
            {
                'partner_id': self.env.ref('base.public_partner').id,
                'date_order': datetime.now(),
            }
        )
        self.purchase_order_line_1 = self.env['purchase.order.line'].create({
            'product_id': self.product_1.id,
            'price_unit': 79.80,
            'product_qty': 5,
            'name': 'order_1',
            'product_uom': self.env.ref('uom.product_uom_unit').id,
            'date_planned': datetime.now(),
            'order_id': self.purchase.id
        })
        self.purchase_order_line_2 = self.env['purchase.order.line'].create({
            'product_id': self.product_2.id,
            'price_unit': 170.50,
            'product_qty': 2,
            'name': 'order_2',
            'product_uom': self.env.ref('uom.product_uom_unit').id,
            'date_planned': datetime.now(),
            'order_id': self.purchase.id
        })

        default_account_revenue = self.env['account.account'].search([('company_id', '=', self.env.company.id)], limit=1)
        self.invoice = self.env['account.move'].create({
            'type': 'in_invoice',
            'date': datetime.now(),
            'amount_total': 100,
            'partner_id': self.env.ref('base.public_partner').id,
            'line_ids': [
                (0, None, {
                    'name': 'revenue line 1',
                    'account_id': default_account_revenue.id,
                    'product_id': self.product_1.id,
                    'quantity': 2,
                    'price_unit': 100,
                    'currency_id': self.env.company.currency_id.id,
                    'company_currency_id': None,
                    'amount_currency': 3
                }),
                (0, None, {
                    'name': 'revenue line 2',
                    'account_id': default_account_revenue.id,
                    'product_id': self.product_2.id,
                    'quantity': 3,
                    'price_unit': 30,
                    'currency_id': self.env.company.currency_id.id,
                    'company_currency_id': None,
                    'amount_currency': 1
                })
            ]
        })

    def test_validate_quotation(self):
        self.assertRaises(UserError, self.purchase.with_user(self.user_1).button_confirm)
        self.assertTrue(self.purchase.with_user(self.user_2).button_confirm())
        self.assertTrue(self.purchase.state, 'purchase')

    def test_validate_invoice(self):
        self.assertRaises(UserError, self.invoice.with_user(self.user_1).action_post)
        self.assertIsNone(self.invoice.with_user(self.user_2).action_post())
        self.assertTrue(self.invoice.state, 'post')
