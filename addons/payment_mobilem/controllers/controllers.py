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
        _logger.info('MOBILEM is validating session variable for %s' % (http.request.session.get('login') or 'New Customer'))

	# Check that  sale order exist especially for customer who logout and then login and the cart is not empty	
	if not http.request.session.get('sale_order_id') and http.request.session.get('sale_last_order_id'):
	    http.request.session.update(sale_order_id = http.request.session.get('sale_last_order_id'))

        http.request.registry['payment.transaction'].form_feedback(http.request.cr, http.request.uid, post, 'mobilem', http.request.context)

        _logger.info('MOBILEM is redirecting back to odoo ecommerce')
        return http.request.redirect(post.pop('return_url', '/'))

class PaymentMobile(http.Controller):
     @http.route('/payment_mobilem', type='http', auth='none', methods=['POST'], csrf=False)
     def index(self, **kw):
	 http.request.uid = SUPERUSER_ID
	 verdict = False
	 account = None
	 _logger.info('MOBILEM is receiving message from SMS gateway ID: %s', kw.get('id'))  # debug

	 verdict, account = http.request.env['mobile.accounts'].check_credentials(kw.get('secret'), kw.get('id'))
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
	       _logger.info('Successfully stored message from SMS Gateway ID: [%s]', kw.get('id'))  # debug
	       return '{ payload: { success: "true" } }'
	    else:
	       _logger.info('Failure to store  message from SMS Gateway ID: [%s]', kw.get('id'))  # debug
	       return '{ payload: { success: "false" } }'
	 else:#unsuccessful authentication
	    _logger.info('Authentication Failure for SMS Gateway ID: %s', kw.get('id'))  # debug
	    return '{ payload: { success: "false" } }'

