from dataclasses import field
from odoo import models, fields, api


class RealEstateType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "sequence"

    name = fields.Char(required=True)
    sequence = fields.Integer(default=1)
    property_ids = fields.One2many('estate.property', 'property_type_id')
    offer_ids = fields.One2many(related='property_ids.offer_ids')
    offer_count = fields.Integer(compute="_compute_offer")

    @api.depends("offer_ids")
    def _compute_offer(self):
        if self.ids:
            for x in self:
                x.offer_count = 0
                x.offer_count = self.env['estate.property.offer'].search_count(
                    [('property_type_id', '=', x.id)])
