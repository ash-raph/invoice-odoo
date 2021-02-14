from odoo import fields, models
from odoo.exceptions import UserError


class Move(models.Model):
    _inherit = 'account.move'

    validator_id = fields.Many2one('res.users', default=lambda self: self.env.user)
    state = fields.Selection(selection_add=[('wait_for_validation', 'Wait for validation'), ('posted', )])

    def action_post(self):
        for row in self:
            if row.env.user.validation_threshold < row.amount_total:
                raise UserError(f"Sorry You don't have right to confirm this invoice")
            row.validator_id = row.env.user
        return super(Move, self).action_post()

    def action_wait_validation(self):
        self.write(
            {'state': 'wait_for_validation'}
        )
