# -*- coding: utf-8 -*-
#from passlib.context import CryptContext
from openerp import models, fields, api
from openerp.tools.float_utils import float_compare
import re
import datetime
import logging
import json
_logger = logging.getLogger(__name__)


class MobileMoneyAquirer(models.Model):
	_inherit = 'payment.acquirer'

	@api.model
	def _get_providers(self):
	    providers = super(MobileMoneyAquirer, self)._get_providers()
	    providers.append(['mobilem', 'Mobile Money'])
	    return providers

	@api.multi
	def mobilem_get_form_action_url(self):
	    return '/payment/mobilem/feedback'


	mobilem_currency_id = fields.Many2one('res.currency', 'Service Currency', select=True, 
	   help="Currency of the Mobile Money Service")
	mobilem_journal_id = fields.Many2one('account.journal', 'Accounting Journal', select=True, domain="[('type', 'in', ('bank','cash'))]",
	   help="This is the journal to record all successful Mobile Money payments in the accounting books")
	mobilem_account_id = fields.Many2one('mobile.accounts', 'Mobile Account', select=True, 
	   help="This is the unique mobile account id that has been configured to be used to receive payment from client using mobile money.This account\
	 contains service provider specific detaails such as account number, paybill number etc")
	mobilem_provider_id = fields.Many2one(related='mobilem_account_id.provider_id', string="Mobile Money Provider", 
	   help="This is the Mobile Money service provider associated with the Mobile Money Account ID selected above.This is to guide you in naming this\
	 payment aquirer according to the service provider")
	mobilem_service_type = fields.Char('Service Name', help="Enter the type of Payment Service name given by your Mobile payment service provider..e.g 'Paybill', 'Buy Goods', 'Send Money', This service Name will appear on your ecommerce website for your clients to see and use it")
	mobilem_service_number = fields.Char('Service Number', help="This is the unique number given by the Mobile Service Provider for the above service name. e.g 'Paybill Number', 'Till Number', 'MPESA Number'")


class TransactionMobilem(models.Model):
	_inherit = 'payment.transaction'

	mobilem_msg_id = fields.Many2one('payment.mobile','Mobile Message', readonly=True, 
		help="This is the Mobile Money payment message that is linked to this Transaction")
	mobilem_cust_code = fields.Char('Transaction Code', readonly=True, help="Transaction Code entered by customer during payment confirmation")
	mobilem_paid_amount = fields.Float('Amount Paid', digits=(32,2), readonly=True, help="Amount that the customer paid through Mobile Money")
	mobilem_bal_amount = fields.Float('Balance to Clear', digits=(32,2), compute='_compute_bal', help="Balance amount that the customer has to clear")
	
	@api.one
	@api.depends('mobilem_paid_amount', 'amount')
	def _compute_bal(self):
	    self.mobilem_bal_amount = self.amount - self.mobilem_paid_amount
	    return
	
	@api.model
	def _mobilem_form_get_tx_from_data(self,data):
            reference, amount, currency, acquirer = data.get('reference'), data.get('amount'), data.get('currency'), data.get('acquirer')
            tx = self.search([('reference', '=', reference), ('amount', '=', float(amount) ), ('acquirer_id', '=', int(acquirer)), ('currency_id', '=', int(currency))])
            if not tx or len(tx) > 1:
               error_msg = 'received data for Order reference %s' % reference
               if not tx:
                  error_msg += '; but no transaction found'
               else:
                  error_msg += '; but multiple transactions found'
               _logger.error(error_msg)
               #raise ValidationError(error_msg)
            return tx


	def _mobilem_form_get_invalid_parameters(self, cr, uid, tx, data, context=None):
            invalid_parameters = []
            if float_compare(float(data.get('amount', '0.0')), tx.amount, 2) != 0:
               invalid_parameters.append(('amount', data.get('amount'), '%.2f' % tx.amount))
            if int(data.get('currency')) != tx.currency_id.id:
               invalid_parameters.append(('currency', data.get('currency'), tx.currency_id.id))
            if int(data.get('acquirer')) != tx.acquirer_id.id:
               invalid_parameters.append(('acquirer', data.get('acquirer'), tx.acquirer_id.id))
            if str(data.get('reference')) != tx.reference:
               invalid_parameters.append(('reference', data.get('reference'), tx.reference))
            return invalid_parameters

	@api.model
	def mobilem_message_validate(self, tx, msg=None):
	    """ This method validates transaction and SMS for SMSes that arrive later than the time the  customer submits payment confirmation"""
	    vals ={}
	    if msg and msg.amount:
		vals.update(self.process_txn(tx, msg, vals))
	        vals['date_validate'] = datetime.datetime.now()
	    tx.write(vals)
	    #Now check if we need to confirm sale order at this point or not,Also create invoice (if set in config) after sale confirmation
	    if tx and tx.state == 'done' and tx.acquirer_id.auto_confirm == 'at_pay_confirm' and  tx.sale_order_id.state in ['draft', 'sent']:
		context=dict(self.env.context, send_email=True)
		tx.sale_order_id.with_context(context).action_confirm()
		self.create_invoice(tx)
	    elif tx and tx.state not in ['cancel'] and tx.sale_order_id.state in ['draft']:
                tx.sale_order_id.force_quotation_send()
 
			
	    	
	@api.model
	def _mobilem_form_validate(self, tx, data):
	    """ This method validates txn and SMS for SMSes that arrive earlier than the time the customer submits payment confirmation"""

	    #cust_tx_code = str(data.get('confirm_code'))
	    cust_tx_code = re.sub("([^0-9a-zA-Z]*)", "", data.get('confirm_code')) #remove anything else except Alphanumeric 
	    vals = {'mobilem_cust_code': cust_tx_code}

	    # check if confirmation code and txn exist or else order has error
	    if cust_tx_code and tx:
	       _logger.info('Validating Mobile Money payment for Order Ref: %s' % tx.reference)
	       #look for matching  unprocessed SMS message  
	       mobilem_rec = self.env['payment.mobile'].search(
			[	('code', '=', cust_tx_code ), 
				('account_id', '=', tx.acquirer_id.mobilem_account_id.id ), 
				('processed', '=', False)
			], 
				order="timestamp desc", limit=1)

	       vals['date_validate'] = datetime.datetime.now()
	       vals['acquirer_reference'] = tx.acquirer_id.mobilem_service_type + ': ' +  tx.acquirer_id.mobilem_service_number
	       # check if  matching message was found  and message has amount else txn goes to pending
	       if mobilem_rec and mobilem_rec.amount:
		  vals.update(self.process_txn(tx, mobilem_rec, vals))
	       else: #message has not arrived or no such message(wrong confirmation code) or message already processed or message is missing some data
	          vals['state'] = 'pending'
		  vals['state_message'] = "No matching message for confirmation code entered. Needs investigation"
	    else:
	       vals['state'] = 'error'
	       vals['state_message'] = "No transaction code or No mobilem payment acquirer data"
	    return tx.write(vals)

	@api.model
	def process_txn(self, tx, mobilem_rec, vals):
		  """Method called to process txn, when matching SMS exist; or SMS, when matching txn exist """

		  paid_amount = float(re.sub(',', '', mobilem_rec.amount))
	       	  mobilem_rec.write({'processed': True}) # Important to mark SMS as processed at this point!!

		  # Create a 'account.payment' entry, if set in config
            	  _logger.info('Create Payment for this order?  %s' % tx.partner_id.company_id.mobilem_create_payment)
		  if tx.partner_id.company_id.mobilem_create_payment:
		     res = self.create_payment(paid_amount, tx)
		     if res is None:
              	       _logger.error("Failed to create Payment entry for Order No: %s" % tx.sale_order_id.name )
		  vals['mobilem_msg_id'] = mobilem_rec.id
		  vals['mobilem_paid_amount'] = ((paid_amount / tx.acquirer_id.mobilem_currency_id.rate) * tx.currency_id.rate) #amount paid in order currency
		  vals['state'] = 'done'
		  vals['state_message'] = 'Customer has paid'
	    	  return vals

	@api.model
	def create_payment(self, paid_amount, tx):
	    """ Method called to create payment in account.payment if set in the config""" 
	    vals = {}
	    res = None
	    if paid_amount and tx:
	       vals = {
		 'communication': tx.reference,
		 'company_id': tx.partner_id.company_id.id,
		 'currency_id': tx.acquirer_id.mobilem_currency_id.id,
		 'partner_id': tx.partner_id.id,
		 'payment_method_id': self.env['account.payment.method'].search([('payment_type', '=', 'inbound'), ('code', '=', 'manual' )], limit=1).id,
		 'payment_date': datetime.datetime.now(),
		 'payment_difference_handling': 'open',
		 'journal_id': tx.acquirer_id.mobilem_journal_id.id,
		 'partner_type': 'customer',
		 'amount': paid_amount,
		 'payment_type': 'inbound',
		}
	       res = self.env['account.payment'].create(vals)
	       res.post()
	    return res
	
	@api.model
	def form_feedback(self, data, acquirer_name): 
		""" Override to create invoice  if mobilem_create_invoice is set and transaction is in 'done' state. """
	        tx = None
	        res = super(TransactionMobilem, self).form_feedback(data, acquirer_name)
	        tx_find_method_name = '_%s_form_get_tx_from_data' % acquirer_name
		
		# get txn before proceeding
	        if hasattr(self, tx_find_method_name):
        	    tx = getattr(self, tx_find_method_name)(data)
		if tx  and tx.partner_id.company_id.mobilem_create_invoice and data.get('return_url') == '/shop/payment/validate':
		    # payment made from from online shop
               	    _logger.info('{} is making payment from online shop'.format(tx.partner_id.name))
		    self.create_invoice(tx)
		elif tx and tx.partner_id.company_id.mobilem_register_payment and data.get('return_url') == '/website_payment/confirm':
		    #payment made from customer web portal
               	    _logger.info('{} is making payment from website portal'.format(tx.partner_id.name))
		    number = re.sub('-\d+$', '', data.get('reference'))#TODO  improvement needed, May not work witn invoices with '-' in their numbers
		    invoice = self.env['account.invoice'].search([('number', '=', number), ('state', '=', 'open'), 
				('partner_id', '=', tx.partner_id.id)], limit=1)
		    if invoice:
		       self.register_payment(invoice, tx)
		    else:
			_logger.info('Mobilem did not find invoice while reconciling payment from: %s' % tx.partner_id.name)
		    
		       
		    
		return res
	
	@api.model
	def create_invoice(self, tx):
		""" Method called to create invoice from txn and sale order if set in config"""

		# if txn has been validated then create invoice from txn and sale order
		if tx and tx.state == 'done' and tx.sale_order_id.state in ['sale', 'done']:
			invoice_id = tx.sale_order_id.action_invoice_create(final=True)
			#check if invoice was created
			if invoice_id:
			    invoice = self.env['account.invoice'].browse(invoice_id)
			    #confirm that invoice is not already validated by another user or process
			    if invoice and invoice.state == 'draft':
				invoice.signal_workflow('invoice_open') #validate invoice
				# reconcile invoice with payment if set in config
				if tx.partner_id.company_id.mobilem_register_payment:
				   self.register_payment(invoice, tx)
				else:
				    _logger.info('Payment  and Invoice registration/reconciliation not enabled')		
			    else:
				_logger.info('Invoice not found  or not in draft state in order to be validated')		
			else:
			    _logger.info('Invoice was not created for some reason -needs checking')		
			
		return


	@api.model
	def register_payment(self, invoice, tx):
	    """ Method called to register/reconcile a payment with an unpaid invoice for a given partner"""
	    #first, check if invoice is still open and there is outstanding payment for this invoice
	    if invoice.state == 'open' and invoice.has_outstanding and invoice.outstanding_credits_debits_widget:
               payments = json.loads(invoice.outstanding_credits_debits_widget)
               #look for payment that match this invoice origin(i.e using transaction reference number)
               for payment in payments['content']:
                   # we register/reconcile only those payments linked to the sale order
                   if payment['journal_name'] == tx.reference and payments['title'] == 'Outstanding credits':
                      _logger.info('Reconciling payment ref:{} with invoice no. {}'.format(payment['journal_name'], invoice.number))
                      pay_line = self.env['account.move.line'].browse([payment['id']])
                      invoice.register_payment(pay_line)
		      # now check of we need to send invoice to customer
		      if tx.partner_id.company_id.mobilem_send_invoice:
			 self.send_invoice(invoice) 
            else:
                _logger.info('No outstanding payment to assign this invoice %s' % invoice.number)

	    	    

	@api.model
	def send_invoice(self, invoice):
	    """ Method to send invoice via mail if activated in the configs"""
            email_act = invoice.action_invoice_sent()
            if email_act and email_act.get('context'):
		admin_email = self.env.ref('base.user_root').partner_id.email
                email_ctx = email_act['context']
                email_ctx.update(default_email_from = admin_email)
                invoice.with_context(email_ctx).message_post_with_template(email_ctx.get('default_template_id'))
            return True

