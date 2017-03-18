# -*- coding: utf-8 -*-
# Copyright 2017 SYLEAM Info Services
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import models, api, fields
from datetime import timedelta

INTERVENTION_SATISFACTION = [
    ('0', 'Very Happy'),
    ('1', 'Happy'),
    ('2', 'Unhappy'),
    ('3', 'Furious'),
]

class InterventionRequest(models.Model):
    _name = 'intervention.request'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _description = 'Intervention'
    _order = 'id desc'

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        # write the domain
        # - ('id', 'in', stages.ids): add columns that should be present
        # - OR ('team_ids', '=', team_id) if team_id: add team columns
        search_domain = [('id', 'in', stages.ids)]
        if self.env.context.get('default_team_id'):
            search_domain = ['|', ('team_ids', 'in', self.env.context['default_team_id'])] + search_domain

        return stages.search(search_domain, order=order)

    def _default_team_id(self):
        team_id = self._context.get('default_team_id')
        if not team_id:
            team_id = self.env['intervention.team'].search([('member_ids', 'in', self.env.uid)], limit=1).id
        if not team_id:
            team_id = self.env['intervention.team'].search([], limit=1).id
        return team_id

    name = fields.Char(size=128, required=True)
    active = fields.Boolean(default=True)
    description = fields.Text(copy='')
    color = fields.Integer(string='Color Index')
    user_id = fields.Many2one('res.users', string='Responsible', required=True, default=lambda self: self.env.user)
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env['res.company']._company_default_get('intervention.request'))
    date_closed = fields.Datetime(string='Closed on', readonly=True)
    email_from = fields.Char(string='Email', size=128, help='These people will receive email.')
    satisfaction = fields.Selection(selection=INTERVENTION_SATISFACTION, string='Satisfaction', default='0')
    tag_ids = fields.Many2many(comodel_name='intervention.tag', string='Tags')
    team_id = fields.Many2one(comodel_name='intervention.team', string='Intervention Team', default=_default_team_id, index=True)
    number_request = fields.Char(string='Number Request', size=64, default=lambda self: self.env['ir.sequence'].next_by_code('intervention.request'), copy=False)
    customer_information = fields.Text(string='Customer_information')
    intervention_todo = fields.Text(string='Intervention to do', help='Indicate the description of this intervention to do')
    date_planned_start = fields.Datetime(string='Planned Start Date', help='Indicate the date of begin intervention planned')
    date_planned_end = fields.Datetime(string='Planned End Date', help='Indicate the date of end intervention planned')
    date_effective_start = fields.Datetime(string='Effective start date', copy=False, help='Indicate the date of begin intervention')
    date_effective_end = fields.Datetime(string='Effective end date', copy=False, help='Indicate the date of end intervention')
    duration_planned = fields.Float(string='Planned duration', help='Indicate estimated to do the intervention.')
    duration_effective = fields.Float(string='Effective duration', copy=0.0, help='Indicate real time to do the intervention.')
    partner_id = fields.Many2one('res.partner', string='Customer', domain="[('parent_id', '=', False)]", required=True, change_default=True, index=True)
    partner_invoice_id = fields.Many2one(
        'res.partner', string='Invoice Address',
        domain="[('parent_id', '!=', False), ('parent_id', '=', partner_id)]",
        required=True,
        default=lambda self: self.env.context.get('partner_id', False) and self.env['res.partner'].address_get([self.env.context['partner_id']], ['invoice'])['invoice'],
        help='The name and address for the invoice',
    )
    partner_order_id = fields.Many2one(
        'res.partner', string='Intervention Contact',
        domain="[('parent_id', '!=', False), ('parent_id', '=', partner_id)]",
        required=True, change_default=True,
        default=lambda self: self.env.context.get('partner_id', False) and self.env['res.partner'].address_get([self.env.context['partner_id']], ['contact'])['contact'],
        help='The name and address of the contact that requested the intervention.',
    )
    partner_shipping_id = fields.Many2one(
        'res.partner', string='Intervention Address',
        required=True,
        default=lambda self: self.env.context.get('partner_id', False) and self.env['res.partner'].address_get([self.env.context['partner_id']], ['delivery'])['delivery'],
    )
    partner_address_phone = fields.Char(string='Phone', size=64)
    partner_address_mobile = fields.Char(string='Mobile', size=64)
    stage_id = fields.Many2one(
        comodel_name='intervention.stage', string='Stage',
        track_visibility='onchange',
        group_expand='_read_group_stage_ids', copy=False,
        index=True, domain="[('team_ids', '=', team_id)]")

    def _onchange_team_get_values(self, team):
        return {
            'stage_id': self.env['intervention.stage'].search([('team_ids', 'in', team.id)], order='sequence', limit=1).id
        }

    @api.onchange('team_id')
    def _onchange_team_id(self):
        if self.team_id:
            import pdb
            pdb.set_trace()
            update_vals = self._onchange_team_get_values(self.team_id)
            if not self.stage_id or self.stage_id not in self.team_id.stage_ids:
                self.stage_id = update_vals['stage_id']

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        if not self.partner_id:
            return {'value': {'partner_invoice_id': False, 'partner_shipping_id': False, 'partner_order_id': False, 'email_from': False, 'partner_address_phone': False, 'partner_address_mobile': False}}

        address = self.partner_id.address_get(['default', 'delivery', 'invoice', 'contact'])
        self.partner_invoice_id = address['invoice']
        self.partner_order_id = address['contact']
        self.partner_shipping_id = address['delivery']
        delivery_address = self.env['res.partner'].browse([address['contact']])
        self.email_from = delivery_address.email
        self.partner_address_phone = delivery_address.phone
        self.partner_address_mobile = delivery_address.mobile

    @api.onchange('partner_order_id')
    def onchange_partner_order_id(self):
        if not self.partner_order_id:
            return {'value': {'email_from': False, 'partner_address_phone': False, 'partner_address_mobile': False}}

        self.email_from = self.partner_order_id.email
        self.partner_address_phone = self.partner_order_id.phone
        self.partner_address_mobile = self.partner_order_id.mobile

    @api.onchange('duration_planned')
    def onchange_planned_duration(self):
        if not self.duration_planned:
            return {'value': {'date_planned_end': False}}
        start_date = fields.Datetime.from_string(self.date_planned_start)
        self.date_planned_end = fields.Datetime.to_string(start_date + timedelta(hours=self.duration_planned))

    @api.onchange('date_planned_end')
    def onchange_planned_end_date(self):
        if not self.date_planned_start or not self.date_planned_end:
            return
        start_date = fields.Datetime.from_string(self.date_planned_start)
        end_date = fields.Datetime.from_string(self.date_planned_end)
        difference = end_date - start_date
        minutes, secondes = divmod(difference.seconds, 60)
        hours, minutes = divmod(minutes, 60)
        self.duration_planned = float(difference.days * 24) + float(hours) + float(minutes) / float(60)

    @api.onchange('duration_effective')
    def onchange_effective_duration(self):
        if not self.duration_effective:
            return {'value': {'date_effective_end': False}}
        start_date = fields.Datetime.from_string(self.date_effective_start)
        self.date_effective_end = fields.Datetime.to_string(start_date + timedelta(hours=self.duration_effective))

    @api.onchange('date_effective_end')
    def onchange_effective_end_date(self):
        if not self.date_effective_start or not self.date_effective_end:
            return
        start_date = fields.Datetime.from_string(self.date_effective_start)
        end_date = fields.Datetime.from_string(self.date_effective_end)
        difference = end_date - start_date
        minutes, secondes = divmod(difference.seconds, 60)
        hours, minutes = divmod(minutes, 60)
        self.duration_effective = float(difference.days * 24) + float(hours) + float(minutes) / float(60)
