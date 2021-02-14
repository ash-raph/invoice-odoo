from odoo import fields, models, _
from odoo.exceptions import UserError


class Purchase(models.Model):
    _inherit = 'purchase.order'

    validator_id = fields.Many2one('res.users', default=lambda self: self.env.user)

    def button_confirm(self):
        for row in self:
            if row.env.user.validation_threshold < row.amount_total:
                raise UserError(_(f"Sorry You don't have right to confirm this order {row.name}"))
            row.validator_id = row.env.user
        return super(Purchase, self).button_confirm()
