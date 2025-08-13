from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError



class CelluleSolidaire(models.Model):
    _name = 'cellule.solidaire'
    _description = 'Suivis des activités de la cellule solidaire de l\'ong Ujadi'
    _inherit = ['mail.thread', 'mail.activity.mixin']


    name = fields.Char(string='Dénomination de la CS', required=True, tracking=True,)
    province_id = fields.Many2one('res.province', string="Province")
    ville = fields.Many2one(
        'res.ville.territoire',
        domain="[('province_id', '=', province_id)]",
        string="Ville/Territoire")
    entity = fields.Char(string='Entité')
    responsable_id = fields.Many2one('responsable.cs', string="Responsable", tracking=True)
    membre_ids = fields.One2many('membre.cs', 'cellule_id', string="Membres",tracking=True)
    description = fields.Text(string='Description')
    active = fields.Boolean(string='Active', default=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed')
    ], string="State", default="draft")
    


    @api.constrains('membre_ids')  # ✅ 'constrains' avec un S, sans T
    def _check_membre_count(self):
        for rec in self:
            if len(rec.membre_ids) > 30:
                raise ValidationError("Une cellule solidaire ne peut pas avoir plus de 30 membres.")

    
    def action_confirm(self):
        for record in self:
            if not record.responsable_id:
                raise UserError("Impossible de confirmer : veuillez définir un responsable pour cette cellule.")
            record.state = "confirmed"

    def action_open_set_draft_wizard(self):
        return {
            'name': 'Remettre en Draft',
            'type': 'ir.actions.act_window',
            'res_model': 'cellule.set.draft.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'active_id': self.id,
            }   
        }
