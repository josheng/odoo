from dataclasses import field
from odoo import models, fields


class RealEstateTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer()

    _sql_constraints = [
        ('check_tag', 'UNIQUE(name)',
         'The tag name must be unique!'),
    ]
