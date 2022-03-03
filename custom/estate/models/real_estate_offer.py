from dataclasses import field
from odoo import api, models, fields
from datetime import datetime, timedelta
from dateutil.relativedelta import *


class RealEstateOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float()
    status = fields.Selection(string="Status", selection=[('accepted', 'Accepted'), ('refused', 'Refused')], copy=False)
    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute='_compute_date_deadline', inverse='_inverse_date_deadline')

    @api.depends('validity')
    def _compute_date_deadline(self):
        for x in self:
            if x.create_date:
                x.date_deadline = x.create_date + relativedelta(days=+x.validity)


    @api.depends('validity')
    def _inverse_date_deadline(self):
        for x in self:
            if x.create_date:
                x.validity = (x.date_deadline - x.create_date.date()).days
