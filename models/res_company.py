# -*- coding: utf-8 -*-
# Copyright 2017 SYLEAM Info Services
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    note_intervention_report = fields.Char(string='Note for intervention report', default='For any comments on the contents of this report, please contact us within 48 hours, Thank you.', help='Note you will see in intervention report on the footer of the description')
