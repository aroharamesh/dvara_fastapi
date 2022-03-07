from operator import itemgetter


# Function to prepare user data
async def create_user_data(data):
    sm_user_id = data.get('smUserId', "SM000001250")

    first_name = data.get('firstName', "")
    middle_name = data.get('middleName', "")
    last_name = data.get('lastName', "")
    first_name = (first_name if first_name else "")
    last_name = (last_name if last_name else "")
    middle_name = (middle_name if middle_name else "")
    full_name = first_name + middle_name + last_name

    gender = data.get('gender', "")
    gender = ('M' if gender == "MALE" else "F")

    father_first_name = data.get('fatherFirstName', "")
    father_middle_name = data.get('fatherMiddleName', "")
    father_last_name = data.get('fatherLastName', "")
    father_first_name = (father_first_name if father_first_name else "")
    father_last_name = (father_last_name if father_last_name else "")
    father_middle_name = (father_middle_name if father_middle_name else "")
    father_full_name = father_first_name + father_middle_name + father_last_name

    dob_info = data.get('dateOfBirth', "")
    year, month, day = itemgetter('year', 'monthValue', 'dayOfMonth')(dob_info)
    # date_of_birth = str(year) + '-' + str(month) + '-' + str(day)
    date_of_birth = "1990-01-21"
    marital_status = data.get('maritalStatus', "")
    marital_status = marital_status.lower()

    mobile_number = data.get('mobilePhone', "9862590000")
    email_id = data.get('email', "testsm1@gmail.com")
    email_id = (email_id if email_id else "testsm1@gmail.com")
    door_no = data.get('doorNo', "")
    street = data.get('street', "")
    locality = data.get('locality', "")
    district = data.get('district', "")
    state = data.get('state', "")
    pincode = data.get('pincode', "")
    res_address = door_no + street + locality
    shop_name = data.get('shopName', "xyz shop")
    shop_type = data.get('shopType', "Manufacturers")
    shop_address = data.get('shopAddress', "kolkata")

    family_info = data['familyMembers']
    monthly_income = family_info[0]['incomes'][0]['incomeEarned']

    udhyog_aadhar = data.get('udhyog_aadhar', "Yes")
    uan_number = data.get('uan_number', "123456987")
    poa_type = data.get('poa_type', "1")
    poa_number = data.get('poa_number', "123456")
    bureau_score = data.get('bureau_score', "650")
    sm_score = data.get('sm_score', "3")
    sm_loan_eligibility = data.get('sm_loan_eligibility', 25000.00)
    pan_no = data.get('panNo', "ALWPG5909L")
    pan_no = (pan_no if pan_no else "ALWPG5909L")
    res_type = data.get('res_type', "Rent")
    bank_accounts_info = data['customerBankAccounts'][0]
    customer_bank_name = bank_accounts_info.get('customerBankName', "")
    ifsc_code = bank_accounts_info.get('ifscCode', "")
    account_type = bank_accounts_info.get('accountType', 'savings')
    account_type = (account_type if account_type else "savings")
    account_number = bank_accounts_info.get('accountNumber', "")
    bank_statements = bank_accounts_info.get('bankStatements', "")
    bank_statement_availability = ("Yes" if (len(bank_statements) > 0) else "No")

    user_data = {
        "sm_user_id": sm_user_id,
        "name": full_name,
        "date_of_birth": str(date_of_birth),
        "gender": gender,
        "father_name": father_full_name,
        "marital_status": marital_status,
        "mobile_number": mobile_number,
        "email_id": email_id,
        "res_address": res_address,
        "res_city": district,
        "res_state": state,
        "res_pin_code": pincode,
        "res_type": res_type,
        "shop_name": shop_name,
        "shop_type": shop_type,
        "shop_address": shop_address,
        "monthly_income": monthly_income,
        "udhyog_aadhar": udhyog_aadhar,
        "uan_number": uan_number,
        "pan_number": pan_no,
        "poa_type": poa_type,
        "poa_number": poa_number,
        "bank_name": customer_bank_name,
        "account_number": account_number,
        "ifsc_code": ifsc_code,
        "account_type": account_type,
        "bureau_score": bureau_score,
        "sm_score": sm_score,
        "sm_loan_eligibility": sm_loan_eligibility,
        "bank_statement_availability": bank_statement_availability,
    }
    return user_data


# Function to prepare loan data
async def create_loan_request_data(data, sm_user_id, am_user_token):
    sm_loan_id = data.get("smLoanID", "SML00253011")
    loan_amount = data.get("loanAmount", "10000")
    interest_rate = data.get("interestRate", "12")
    disbursement_schedules = data.get("repaymentSchedule", [
        {
            "int_amount": 91.0,
            "prin": 607.0,
            "emi_no": 1,
            "due_date": "2021-11-19",
            "emi_amount": 773.0
        },
        {
            "int_amount": 91.0,
            "prin": 608.0,
            "emi_no": 2,
            "due_date": "2021-12-20",
            "emi_amount": 743.0
        }
    ])
    disbursement_amount = data.get("disbursementAmount", "9000")
    tenure = data.get("tenure", "")
    processing_fee_in_paisa = data.get("processingFeeInPaisa", "500")
    insurance_fee = data.get("insuranceFee", "250")
    insurance_fee = (insurance_fee if insurance_fee else "250")
    additional_charges = data.get("additionalCharges", "250")
    number_of_edis = data.get("noOfEdits", "5")
    loan_data = {
        "loan_amount": str(loan_amount),
        "interest_rate": str(interest_rate),
        "disbursement_amount": str(disbursement_amount),
        "tenure": str(tenure),
        "repayment_schedule_json": disbursement_schedules,
        "am_user_token": str(am_user_token),
        "sm_user_id": str(sm_user_id),
        "sm_loan_id": str(sm_loan_id),
        "processing_fee": str(processing_fee_in_paisa),
        "additional_charges": str(additional_charges),
        "insurance_charges": str(insurance_fee),
        "number_of_edis": str(number_of_edis)
    }
    return loan_data


# Function to prepare loan repayment data
async def create_loan_repayment_data(data, am_loan_id, am_user_token):
    am_user_token = am_user_token
    sm_loan_id = data.get('smLoanID', 'SML00258994')
    am_loan_id = am_loan_id
    repayment_due_amount = data.get('repaymentDueAmount', 10.00)
    principal_due_amount = data.get('principalDueAmount', 70.00)
    interest_due_amount = data.get('interestDueAmount', 50.00)
    repayment_due_date = data.get('repaymentDueDate', '2022-01-01')
    transfer_amount = data.get('transferAmount', 20.00)
    principal_transfer_amount = data.get('principalTransferAmount', 10.00)
    interest_transfer_amount = data.get('interestTransferAmount', 50.00)
    additional_charges_transfer_amount = data.get('additionalChargesTransferAmount', 10.00)
    transfer_transaction_number = data.get('transferTransactionNumber', 'TN0000001')
    transfer_transaction_date = data.get('transferTransactionDate', '2022-02-17')
    repayment_data = {
        "am_user_token": am_user_token,
        "sm_loan_id": str(sm_loan_id),
        "am_loan_id": str(am_loan_id),
        "repayment_due_amount": repayment_due_amount,
        "principal_due_amount": principal_due_amount,
        "interest_due_amount": interest_due_amount,
        "repayment_due_date": repayment_due_date,
        "transfer_amount": transfer_amount,
        "principal_transfer_amount": principal_transfer_amount,
        "interest_transfer_amount": interest_transfer_amount,
        "additional_charges_transfer_amount": additional_charges_transfer_amount,
        "transfer_transaction_number": transfer_transaction_number,
        "transfer_transaction_date": transfer_transaction_date
    }
    return repayment_data


# Function to prepare user document upload data
async def create_user_document_upload_data(data, sm_user_id, uuid):
    sm_user_id = sm_user_id
    uuid = uuid
    document_type = data.get('documentType', '4')
    user_document_data = {
        "sm_user_id": sm_user_id,
        "uuid": uuid,
        "document_type": document_type
    }
    return user_document_data


# Function to prepare loan document upload data
async def create_loan_document_upload_data(data, uuid, aml_id):
    sm_loan_id = data.get('smLoanId', 'SML00258994')
    uuid = uuid
    aml_id = aml_id
    time_stamp = data.get('timeStamp', '2022-02-17')
    ip_stamp = data.get('ipStamp', '127.0.0.1')
    document_type = data.get('documentType', '6')
    loan_document_data = {
        "uuid": uuid,
        "sm_loan_id": sm_loan_id,
        "aml_id": aml_id,
        "time_stamp": time_stamp,
        "ip_stamp": ip_stamp,
        "document_type": document_type
    }
    return loan_document_data

