from dataclasses import field
from email.policy import default
from odoo import models, fields


class Users(models.Model):
    _inherit = 'res.users'
    _description = "Estate Property User"

    name = fields.Char(required=True)
