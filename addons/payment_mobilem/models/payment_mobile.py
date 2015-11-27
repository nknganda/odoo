# -*- coding: utf-8 -*-
from passlib.context import CryptContext
from openerp import models, fields, api
from openerp.tools.float_utils import float_compare
import re
import datetime
import logging
_logger = logging.getLogger(__name__)

default_crypt_context = CryptContext(
    # kdf which can be verified by the context. The default encryption kdf is
    # the first of the list
    ['pbkdf2_sha512', 'md5_crypt'],
    # deprecated algorithms are still verified as usual, but ``needs_update``
    # will indicate that the stored hash should be replaced by a more recent
    # algorithm. Passlib 1.6 supports an `auto` value which deprecates any
    # algorithm but the default, but Ubuntu LTS only provides 1.5 so far.
    deprecated=['md5_crypt'],
)

mes = "DZ22ZD655 Confirmed. You have received Ksh5,500.00 from ALEX NDUNG'U 254723784491 on 31/7/13 at 3:08 PM New M-PESA balance is Ksh5,844.00.Save & get a loan on Mshwari"
pat = "^\s*(\w+)\s*Confirmed[.\s]*You\s*have\s*received\s*Ksh\s*([\d,]+.00)\s*from\s*([\w\W]+)\s+(\d+)\s*on\s*([\d/]+)\s*at\s*([\d:\sAP]+M)\s*New\s*m-pesa\s*balance\s*is\s*Ksh\s*([\d,]+.00)[\s\W\w]*(?i)"

#class mobile_fields(models.Model):
#	_name = 'mobile.fields'
#	_description = 'Mobile Message Field'
#	
#	name = fields.Char('Name of Field', required=True)
#	db_name = fields.Char('Real name in DB', required=True)
#	
#	_sql_constraints = {
#                ('unique_field', 'unique(name)', 'The field name must be unique!')
#        }
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
            reference, amount, currency_name = data.get('reference'), data.get('amount'), data.get('currency_name')
            tx = self.search([('reference', '=', reference)])
            if not tx or len(tx) > 1:
               error_msg = 'received data for Order reference %s' % (pprint.pformat(reference))
               if not tx:
                  error_msg += '; no order found'
               else:
                  error_msg += '; multiple order found'
               _logger.error(error_msg)
               raise ValidationError(error_msg)
            return tx


	def _mobilem_form_get_invalid_parameters(self, cr, uid, tx, data, context=None):
            invalid_parameters = []
            if float_compare(float(data.get('amount', '0.0')), tx.amount, 2) != 0:
               invalid_parameters.append(('amount', data.get('amount'), '%.2f' % tx.amount))
            if data.get('currency') != tx.currency_id.name:
               invalid_parameters.append(('currency', data.get('currency'), tx.currency_id.name))
            return invalid_parameters

	@api.model
	def _mobilem_form_validate(self, tx, data):
	    _logger.info('Validating Mobile Money payment for Order %s:' % tx.reference)
	    account_id = None
	    #cust_tx_code = str.upper(str(data.get('confirm_code')))
	    cust_tx_code = str(data.get('confirm_code'))
	    if data.get('acquirer'):
		account_id = self.env['payment.acquirer'].browse([int(data.get('acquirer'))]).mobilem_account_id.id
	    vals = {'mobilem_cust_code': cust_tx_code}
	    if cust_tx_code and account_id:
	       mobilem_rec = self.env['payment.mobile'].search(
			[
				('code', '=', cust_tx_code ), 
				('account_id', '=', account_id ), 
				('processed', '=', False)
			], 
				order="timestamp desc")
	       if mobilem_rec and mobilem_rec.amount:
		  paid_amount = float(re.sub(',', '', mobilem_rec.amount))
		  order_amount = float(data.get('amount'))
		  vals['acquirer_reference'] = mobilem_rec.account_id.name
		  vals['mobilem_msg_id'] = mobilem_rec.id
		  vals['mobilem_paid_amount'] = paid_amount 
		  if paid_amount >= order_amount:
		     vals['state'] = 'done'
		     vals['state_message'] = 'OK - Customer has paid in full'
		     vals['date_validate'] = datetime.datetime.now()
		     #mobilem_rec.write({'processed': True})
		  else:
		     vals['state_message'] = "Customer paid less than order value"
		     vals['state'] = 'pending'
		     #mobilem_rec.write({'processed': True})
	       else: ##message has not arrived or no such message(wrong confirmation code) or message already processed or message is missing some data
	          vals['state'] = 'pending'
		  vals['state_message'] = "message has not arrived or no such message(wrong confirmation code)"
	    else:
	       vals['state'] = 'error'
	       vals['state_message'] = "Empty transaction code or empty  mobilem payment account"
	    return tx.write(vals)

 
class RegularExp(models.Model):
	_name = 'mobile.regex'
	_description = 'Regular Expression'
	_order = 'name asc'

	name = fields.Char('Name', required=True)
	msg_fields = fields.Char('List of DB Fields', required=True, default="code,amount,sender_name,sender_number,date,time,balance", help="The list of\
	 fields to store the payment data extracted from transaction SMS.\
	Valid database fields to use are as follows:\n 1. code\n2. amount\n3. sender_name\n4. receiver_name\n5. sender_number\n6. receiver_number\n7. date\n\
	8. time\n9. balance\n Please note the following:\n1. The fields MUST be separated by comma e.g (code,amount,balance etc...)\n 2.The fields are case\
	 sensitive\n3. put the fields in the order of matching regular Expression i.e if 'amount' is the first match in the Regular expression then the first\
	 field in the list  must also be 'amount'")
	regex = fields.Text('Regular Expression', default=pat, required=True, help="The REGULAR EXPRESSION Syntax to use to match and extract payment\
	 information from the transaction SMS..\n Python regular expression (re) synthax and flags are supported")
	#account_id = fields.Many2one('mobile.accounts', select=True, required=True)
	provider_id = fields.Many2one('mobile.providers', 'Service Provider', select=True, required=True)
	#field_ids = fields.Many2many('mobile.fields', string="Fields", help="These are the fields in the database to be used to store matched data from sms")

class MobileProviders(models.Model):
	_name = 'mobile.providers'
	_description = 'Mobile Payment Service Providers'
	_order = 'name asc'

	name = fields.Char('Provider Name', required=True, help="Name of the service provider")
	code = fields.Char('Code', help="optinal code to identify this provider")	
	logo = fields.Binary('Logo', attachment=True, help="This is the logo image to display in the payment window. limited to 1024x1024px.")	
	regex_ids = fields.One2many('mobile.regex', 'provider_id', string='Regular Expressionsi', help="list of regular expressions associated with a service\
	 provider. Regular expression vary from message to message and from one service provider to another")	

	_sql_constraints = {
		('unique_provider', 'unique(name)', 'The Provider Name must be unique!')
	}

class MobileAccounts(models.Model):
	_name = 'mobile.accounts'
	_description = 'Mobile Payment Accounts'
	_order = 'name asc'
	
	name = fields.Char('Username', required=True, help="This is a UNIQUE username for this mobile payment account. This MUST be exactly the same as the id/username configured in your SMSsync URL in your phone. It is used by the system to identify and authenticate the SMSsync gateway that is sending in the SMS texts.")
	provider_id = fields.Many2one(related='regex_id.provider_id', string='Service Provider', readonly=True, select=True, help="The Mobile Service Provider e.g safaricom,\
	 Airtel")
	regex_id = fields.Many2one('mobile.regex', 'Regula Expression', required=True, select=True, help="This is the Regular Expression that will be used to\
		to extract payment data from the transaction SMS. Choose the correct one matching the purpose of this account. failure to use the right\
		 regular expression can lead to inconsistent or incorret payment data")
	password = fields.Char('Password', size=64, required=True, help="This is the password for operating this account. The same password set\
	 here MUST be the same as the one set in the SMSsync app as 'secret' or on any other SMS gateway used")
	secret = fields.Char('Secret', invisible=True, required=True)
	logo = fields.Binary('Logo', attachment=True, help="This is the logo image to display in the payment window. limited to 1024x1024px.")	

	_sql_constraints = {
		('unique_name', 'unique(name)', 'Similar account ID is already configured, this field must be unique since it is used to authenticate\
	 incoming transaction messages from the SMSsync Gateway')
	}

	@api.multi
	def write(self, vals):
	   for rec in self:
	     if vals.get('password'):
	        vals.update({'secret': rec._crypt_context().encrypt(vals.get('password'))})
	     vals.update({'password': '********'})
	     super(MobileAccounts, rec).write(vals)
	   return True
	
	@api.model
	def create(self, vals):
	   if vals.get('password'):
		#encrypted = self._crypt_context().encrypt(vals.get('secret'))
		vals.update({'secret': self._crypt_context().encrypt(vals.get('password'))})
	   vals.update({'password': '********'})
	   res = super(MobileAccounts, self).create(vals)
	   return res

	@api.model
	def _crypt_context(self):
        	""" Passlib CryptContext instance used to encrypt and verify
        	passwords. Can be overridden if technical, legal or political matters
        	require different kdfs than the provided default.

        	Requires a CryptContext as deprecation and upgrade notices are used
        	internally
        	"""
        	return default_crypt_context

	@api.model
	def check_credentials(self, secret=None, acc_id=None):
	    valid_pass = False; replacement = None; account_id=None;
	    account = self.env['mobile.accounts'].search([('name', '=', acc_id)], limit=1, order='id desc')
	    if account and secret:
	       valid_pass, replacement = self._crypt_context().verify_and_update(secret, account.secret)
	       account_id = account.id
	    return valid_pass, account_id 
	
class PaymentMobile(models.Model):
	_name = 'payment.mobile'
	_description = 'Mobile Payment'
	_order = 'timestamp desc'

	@api.one
	@api.depends('write_date')
	def _compute_name(self):
	    self.name = str(self.id) if self.id else ''
	
	name = fields.Char(compute='_compute_name', string="ID", store=True)
	message = fields.Text('Message', readonly=True)
	timestamp = fields.Datetime('Time Sent', readonly=True, help="This is the time the message was sent by the Service provider such as airtel,\
	 Tigo, Safaricom, MTN etc")
	sent_from = fields.Char('From', readonly=True, help="This is the message Origin Number or Name as set by the service provider.. e.g MPESA, SAFARICOM,\
	 2255 etc")
	message_id = fields.Char('Message ID', readonly=True, help="This is a unique message ID set by service provider")
	sent_to = fields.Char('To', readonly=True, help="This is the Message destination Number as set in the Gateway")
	device_id = fields.Char('Device ID', readonly=True, help="Device ID as set in the SMS Gateway, may be similar to message destination number")
	account_id = fields.Many2one('mobile.accounts', 'Mobile Account', readonly=True, help="This is the account ID/number used to send this message.\
	 ID is configured in the SMS gateway URL settings and must match the mobile Accont ID configured in this system ")
	provider_id = fields.Many2one(related='account_id.provider_id', readonly=True, help="The Mobile payment service provider sending this message")
	processed = fields.Boolean('Processed?', default=False, readonly=True)

	## msg data fields 
	code = fields.Char('Transaction Code', readonly=True, help="Transaction code found in the SMS. Also know as confirmation code by other\
	 service providers like safaricom")
	amount = fields.Char('Amount', readonly=True, help="Amount of money transacted. shown in local currency")
	sender_name = fields.Char('Customer Name', readonly=True, help="The name of person or entity making the payment. Also known as sender name")
	receiver_name = fields.Char('Receiver Name', readonly=True, help="The name of person or entity receiving the payment. Also known as payee name" )
	sender_number = fields.Char('Customer Number', readonly=True, help="The number of person or entity making the payment. Also known as sender number")
	receiver_number = fields.Char('Receiver Number', readonly=True, help="The number of person or entity receiving the payment. Also known as payee\
	 number")
	date = fields.Char('Date', readonly=True, help="The date of transaction as shown in the SMS")
	time = fields.Char('Time', readonly=True, help="The time of transaction as shown in the SMS")
	balance = fields.Char('Balance', readonly=True, help="The mobile money account balance  after the transaction.This is in local currency as shown\
	 in the message")

	@api.multi
	def mobile_message_process(self):
	   """ Function to be called by odoo workflow to process mobile SMS messages as soon as they arrive into odoo database """
	   vals = {}
	   for rec in self:
	      reg_exp = rec.account_id.regex_id.regex
	      field_ids = rec.account_id.regex_id.msg_fields
              _logger.info("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXx field_ids %s", field_ids)
	      field_ids = re.sub("([^,_a-zA-Z]*)", "", field_ids) #remove anything else except A-Za-z,_
  	      db_fields = re.sub("(^[,_]*|[,_]*$)", "", field_ids).split(",") #remove any _ or , at start or end of string and split the string into a list
              _logger.info("JJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJ db_fields %s", db_fields)
	      data = re.findall(reg_exp, mes).pop() # data is in tuple
              _logger.info("DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDddddddd data %s", data)
	      for field in db_fields:
		  vals[field] = data[db_fields.index(field)]    
              _logger.info("VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV vals %s", vals)
	      rec.write(vals)
	   return True

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#     self.value2 = float(self.value) / 100
