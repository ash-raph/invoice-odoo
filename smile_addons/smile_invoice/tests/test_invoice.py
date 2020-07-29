from odoo.tests import TransactionCase
from odoo.exceptions import UserError


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
        self.quotation = self.env.ref('smile_invoice.order_1')
        self.invoice = self.env.ref('smile_invoice.invoice_1')

    def test_validate_quotation(self):
        self.assertRaises(UserError, self.quotation.with_user(self.user_1).action_confirm)
        self.assertTrue(self.quotation.with_user(self.user_2).action_confirm())
        self.assertTrue(self.quotation.state, 'sale')

    def test_validate_invoice(self):
        self.assertRaises(UserError, self.invoice.with_user(self.user_1).action_post)
        self.assertIsNone(self.invoice.with_user(self.user_2).action_post())
        self.assertTrue(self.invoice.state, 'post')
