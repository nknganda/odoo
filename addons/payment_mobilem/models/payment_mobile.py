# -*- coding: utf-8 -*-
from passlib.context import CryptContext
from openerp import models, fields, api
import re
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

mes = "DZ22ZD653 Confirmed. You have received Ksh5,500.00 from ALEX NDUNG'U 254723784491 on 31/7/13 at 3:08 PM New M-PESA balance is Ksh5,844.00.Save & get a loan on Mshwari"
pat = "^\s*(\w+)\s*Confirmed[.\s]*You\s*have\s*received\s*Ksh\s*([\d,]+.00)\s*from\s*([\w\W]+)\s+(\d+)\s*on\s*([\d/]+)\s*at\s*([\d:\sAP]+M)\s*New\s*m-pesa\s*balance\s*is\s*Ksh\s*([\d,]+.00)[\s\W\w]*(?i)"
		

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
	provider_id = fields.Many2one('mobile.providers', 'Service Provider', select=True, required=True)

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
	origin = fields.Char('Authorised Sender', required=True, help="This is the authorised sender/origin of the SMS. Normally mobile payments SMS have a unique origin/sender which is used to verify that the payment message trully originates from the service provider")
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
	 incoming transaction messages from the SMS Gateway')
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
	def check_credentials(self, secret=None, msg_from=None, acc_id=None):
	    """ checks username and password and returns True or False and also the mobilem account_id for the SMS"""
	    authenticated = False; replacement = None; account_id=None; authorized=False;
	    account = self.env['mobile.accounts'].search([('name', '=', acc_id)], limit=1, order='id desc')
	    if msg_from and msg_from == account.origin:
		authorized=True
	    if account and secret:
	       authenticated, replacement = self._crypt_context().verify_and_update(secret, account.secret)
	       account_id = account.id
	    return authenticated, authorized, account_id 
	
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
	timestamp = fields.Datetime('Time Sent', readonly=True, help="This is the time the message was sent by the Mobile Network Service provider")
	sent_from = fields.Char('From', readonly=True, help="This is the message Origin Number or Name as set by the Mobile Network Service provider")
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


	_sql_constraints = {
		('unique_messages', 'unique(message_id, account_id)', 'Duplicate message ID found!')
	}

	@api.multi
	def mobile_message_process(self):
	   """ Function to be called by odoo workflow to process mobile SMS messages as soon as they arrive into odoo database """
	   for rec in self:
	      reg_exp = rec.account_id.regex_id.regex
	      data = re.findall(reg_exp, rec.message) # for test, substitute rec.message with mes 
	      if data:
	   	vals = {}
		data = data.pop()
	        field_ids = rec.account_id.regex_id.msg_fields
	        field_ids = re.sub("([^,_a-zA-Z]*)", "", field_ids) #remove anything else except A-Za-z,_
  	        db_fields = re.sub("(^[,_]*|[,_]*$)", "", field_ids).split(",") #remove any _ or , at start or end of string and split the string into a list
	        for field in db_fields:
		  vals[field] = data[db_fields.index(field)]    
	        rec.write(vals)

	      #start checking for matching transaction for every message received
	        if rec.code and rec.amount:
	   	   txn_obj = self.env['payment.transaction']
	           tx = txn_obj.search([('mobilem_cust_code', '=', rec.code), 
					('state', '=', 'pending'), 
					('acquirer_id.mobilem_account_id', '=', rec.account_id.id)],
					limit=1)
		   if tx:
		      txn_obj.mobilem_message_validate(tx, rec)
	   return True

