from dataclasses import field
from odoo import models, fields


class RealEstateType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"

    name = fields.Char(required=True)
