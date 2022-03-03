from dataclasses import field
from odoo import models, fields


class RealEstateTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"

    name = fields.Char(required=True)
