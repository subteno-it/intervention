# -*- coding: utf-8 -*-
# Copyright 2017 SYLEAM Info Services
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class InterventionTag(models.Model):
    _name = 'intervention.tag'
    _description = 'Intervention Tag'

    name = fields.Char(string='Name', size=64)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
