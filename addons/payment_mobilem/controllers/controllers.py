# -*- coding: utf-8 -*-
from openerp import http
import logging
import re
from openerp import SUPERUSER_ID
from datetime import datetime, timedelta, tzinfo
#import pprint
_logger = logging.getLogger(__name__)


class MobileMoneyFeedback(http.Controller):
    _accept_url = '/payment/mobilem/feedback'
    @http.route('/payment/mobilem/feedback', type='http', auth='public', methods=['POST'], website=True, csrf=False)
    def mobilem_form_feedback(self, **post):
        http.request.uid = SUPERUSER_ID
        _logger.info('Beginning form_feedback with post data %s', post)
        #if len(post.get('confirm_code')) < 9:
         #  order_obj = request.registry.get('sale.order')
          # order_obj._set_mpesa_data(post)
           #_logger.info('SSSSSSSSSSSSSSSSSSSSSSSSS REDIRECTING COZ OF ERRORR with POST  as: %s', pprint.pformat(post))
           #return request.redirect("/shop/payment")

        http.request.registry['payment.transaction'].form_feedback(http.request.cr, http.request.uid, post, 'mobilem', http.request.context)
        #return werkzeug.utils.redirect(post.pop('return_url', '/'))
        return http.request.redirect(post.pop('return_url', '/'))

class PaymentMobile(http.Controller):
     @http.route('/payment_mobilem', type='http', auth='none', methods=['POST'], csrf=False)
     def index(self, **kw):
	 http.request.uid = SUPERUSER_ID
	 verdict = False
	 account = None
	 #_logger.info('Beginning of post data %s', pprint.pformat(kw))  # debug
	 #cr, uid, context = http.request.cr, http.request.uid, http.request.context
	 _logger.info('Beginning of post data %s', kw)  # debug

	 #account = http.request.env['mobile.accounts'].search([('name', '=', kw.get('id'))], limit=1, order="id desc")
	 #secret = kw.get('secret')
	 #acc_id = kw.get('id')
	 verdict, account = http.request.env['mobile.accounts'].check_credentials(kw.get('secret'), kw.get('id'))
         _logger.info("HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHh %s", verdict)
	 #if secret and account and (secret == account.secret):
	 if verdict: #successful authentication
	    vals = {
	     'timestamp': datetime.utcfromtimestamp(float(re.findall("^[0-9]{10}",kw.get('sent_timestamp'))[0])),
	     'sent_from': kw.get('from'),
	     'sent_to': kw.get('sent_to'),
	     'device_id': kw.get('device_id'),
	     'message_id': kw.get('message_id'),
	     'message': kw.get('message'),
	     'account_id': account,
	    }
	    if http.request.env['payment.mobile'].create(vals):
	       _logger.info('Successfully stored message: [%s]', kw.get('message'))  # debug
	       return '{ payload: { success: "true" } }'
	    else:
	       _logger.info('Failure to store payment message: [%s]', kw.get('message'))  # debug
	       return '{ payload: { success: "false" } }'
	 else:
	    _logger.info('Authentication Failure for account: %s', kw.get('id'))  # debug
	    return '{ payload: { success: "false" } }'
	 #_logger.info('3333333333333333333333 current context is %s', http.request.context)  # debug

#     @http.route('/payment_mobile/payment_mobile/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('payment_mobile.listing', {
#             'root': '/payment_mobile/payment_mobile',
#             'objects': http.request.env['payment_mobile.payment_mobile'].search([]),
#         })

#     @http.route('/payment_mobile/payment_mobile/objects/<model("payment_mobile.payment_mobile"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('payment_mobile.object', {
#             'object': obj
#         })
