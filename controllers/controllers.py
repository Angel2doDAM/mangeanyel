# -*- coding: utf-8 -*-
# from odoo import http


# class Manageanyel(http.Controller):
#     @http.route('/manageanyel/manageanyel', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/manageanyel/manageanyel/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('manageanyel.listing', {
#             'root': '/manageanyel/manageanyel',
#             'objects': http.request.env['manageanyel.manageanyel'].search([]),
#         })

#     @http.route('/manageanyel/manageanyel/objects/<model("manageanyel.manageanyel"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('manageanyel.object', {
#             'object': obj
#         })
