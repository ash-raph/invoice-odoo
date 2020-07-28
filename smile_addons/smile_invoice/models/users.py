from odoo import fields, models


class User(models.Model):
    _inherit = 'res.users'

    validation_threshold = fields.Integer(default=0)
