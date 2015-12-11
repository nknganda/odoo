# -*- coding: utf-8 -*-
from openerp import http
import logging
import json
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
	 authenticated = False
	 authorized = False
	 account = None
	 reply = {'payload': {'success': None, 'error': None}}
	 _logger.info('MOBILEM is receiving message from SMS gateway ID: %s', kw.get('id'))  # debug

	 authenticated, authorized, account = http.request.env['mobile.accounts'].check_credentials(kw.get('secret'), kw.get('from'), kw.get('id'))
	 
	 if authenticated and authorized: #successful authentication and authorization
	    vals = {
	     'timestamp': datetime.utcfromtimestamp(float(re.findall("^[0-9]{10}",kw.get('sent_timestamp'))[0])),
	     'sent_from': kw.get('from'),
	     'sent_to': kw.get('sent_to'),
	     'device_id': kw.get('device_id'),
	     'message_id': kw.get('message_id'),
	     'message': kw.get('message'),
	     'account_id': account,
	    }
	    res = http.request.env['payment.mobile'].create(vals)
	    if res:
	       	_logger.info('Successfully stored message with ID:{}'.format(res.message_id))  # debug
	       	reply['payload']['success'] = True
	    	_logger.info(json.dumps(reply))  # debug
	       	return json.dumps(reply)
	    else:
		m = 'Failure to store message from SMS Gateway Account: {}'.format(kw.get('id'))
	       	_logger.info(m)  # debug
		reply['payload']['success'] = False
		reply['payload']['error'] = m
	    	_logger.info(json.dumps(reply))  # debug
	       	return json.dumps(reply)
	 elif not authenticated:#unsuccessful authentication
		m = 'Authentication Failure for SMS Gateway Account: {}, please check your ID and password'.format(kw.get('id'))
	    	_logger.info(m)  # debug
		reply['payload']['success'] = False
		reply['payload']['error'] = m
	    	_logger.info(json.dumps(reply))  # debug
	    	return json.dumps(reply)
	 elif not authorized:#unsuccessful authorization
		m = 'Authorization Failure for sender: {}'.format(kw.get('from'))
	    	_logger.info(m)  # debug
		reply['payload']['success'] = False
		reply['payload']['error'] = m
	    	_logger.info(json.dumps(reply))  # debug
	    	return json.dumps(reply)

