from datetime import datetime
from peewee import Model, IdentityField, CharField, IntegerField, TextField, DateTimeField
from data.database import financialForms

class FinancialFormsModel(Model):
	class Meta:
		database = financialForms

class AuditedFinancialFormsModel(FinancialFormsModel):
	createdBy = CharField()
	createdAt = DateTimeField(default=datetime.now)
	lastEditedBy = CharField()
	lastEditedAt = DateTimeField(default=datetime.now)

class User(FinancialFormsModel):
	id = IdentityField()
	user_id = CharField()
	user_name = CharField()
	email_address = CharField()
	class Meta:
		table_name = 'users'

class ExternalInterfaceLogging(AuditedFinancialFormsModel):
	id = IdentityField()
	version = IntegerField(default=0)
	transactionId = CharField()
	serviceProvider = CharField()
	serviceType = CharField()
	referenceId = CharField()
	enquiryRequestString = TextField()
	module = CharField()
	moduleRefId = IntegerField()
	enquiryResponseString = TextField()
	status = CharField()
	errorCode = CharField()
	httpsStatusCode = CharField()
	errorDescription = TextField()
	processingStatus = CharField()