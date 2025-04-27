from odoo import models

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    def action_quick_validate(self):
        for order in self:
            if order.state not in ['progress', 'to_close']:
                continue
            moves = order.move_raw_ids
            lines = moves.mapped('move_line_ids').filtered(lambda l: l.lot_id and not l.qty_done)
            for line in lines:
                line.qty_done = line.reserved_uom_qty
            order.button_mark_done()