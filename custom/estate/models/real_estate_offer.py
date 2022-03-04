from dataclasses import field
from odoo import api, models, fields
from datetime import datetime, timedelta
from dateutil.relativedelta import *
from odoo.exceptions import UserError, ValidationError


class RealEstateOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price"

    price = fields.Float()
    status = fields.Selection(string="Status", selection=[('accepted', 'Accepted'), ('refused', 'Refused')], copy=False)
    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute='_compute_date_deadline', inverse='_inverse_date_deadline')

    _sql_constraints = [
        ('check_price', 'CHECK(price >= 0)',
         'The price cannot be negative!'),
    ]

    @api.depends('validity')
    def _compute_date_deadline(self):
        for x in self:
            if x.create_date:
                x.date_deadline = x.create_date + relativedelta(days=+x.validity)
            else:
                x.date_deadline = fields.Date.today() + relativedelta(days=+x.validity)

            x.property_id.state = 'offer received'


    @api.depends('validity')
    def _inverse_date_deadline(self):
        for x in self:
            if x.create_date:
                x.validity = (x.date_deadline - x.create_date.date()).days
            else:
                x.validity = (fields.Date.today() - x.create_date.date()).days

    def action_accept(self):
        for x in self:
            if x.status == 'refused':
                raise UserError("You cannot accept a refused offer.")
            else:
                x.status = 'accepted'
                x.property_id.state = 'offer accepted'
                x.property_id.selling_price = x.price
                x.property_id.property_buyer_id = x.partner_id
        return True

    def action_refuse(self):
        for x in self:
            x.status = 'refused'
        return True
