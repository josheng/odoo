from dataclasses import field
from odoo import models, fields
from datetime import datetime, timedelta
from dateutil.relativedelta import *


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
