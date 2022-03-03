from dataclasses import field
from odoo import api, models, fields
from datetime import datetime, timedelta
from dateutil.relativedelta import *
from odoo.exceptions import UserError, ValidationError


class RealEstate(models.Model):
    _name = "estate.property"
    _description = "Real Estate Demo"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False, default=fields.Date.today() + relativedelta(months=+6))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True,copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(string='Garden Orientation',
                                          selection=[
                                              ('north', 'North'),('south', 'South'),('east', 'East'),('west', 'West')])
    active = fields.Boolean(default=True)
    state = fields.Selection(string='State', selection=[
        ('new', 'New'), ('offer received', 'Offer Recevied'), ('offer accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')],
        required=True,
        copy=False,
        default='new')
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    property_seller_id = fields.Many2one(
        "res.users", string="Salesperson", default=lambda self: self.env.user)
    property_buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many(
        "estate.property.offer", "property_id")
    total_area = fields.Integer(compute='_compute_total_area', readonly=True)
    best_price = fields.Float(compute='_compute_best_price', readonly=True)


    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for area in self:
            area.total_area = area.living_area + area.garden_area


    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for x in self:
            max_price = 0
            for y in x.offer_ids:
                if y.price > max_price:
                    max_price = y.price

            x.best_price = max_price


    @api.onchange('garden')
    def _onchange_garnde(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = ''


    def action_sold(self):
        for x in self:
            if x.state == 'cancelled':
                raise UserError("Cancelled property cannot be sold.")
            else:
                x.state = 'sold'
        return True

    def action_cancelled(self):
        for x in self:
            if x.state == 'sold':
                raise UserError("Sold property cannot be cancelled.")
            else:
                x.state = 'cancelled'
        return True
