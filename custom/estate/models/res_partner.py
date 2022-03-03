from dataclasses import field
from email.policy import default
from odoo import models, fields


class Partner(models.Model):
    _name = "res.partner"
    _inherit = 'res.partner'
    _description = "Estate Property Partner"

    name = fields.Char(required=True)
