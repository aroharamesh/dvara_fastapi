from operator import itemgetter

async def create_user_data(data):
    customer_info = data['enrollmentDTO']['customer']
    sm_user_id, firstName, lastName, middleName, gender, \
    fatherFirstName, fatherLastName, fatherMiddleName, maritalStatus, \
    mobilePhone, email, doorNo, street, locality, district, state, pincode, \
    panNo = itemgetter('id', 'firstName', 'lastName', 'middleName', 'gender', 'fatherFirstName', 'fatherLastName', 'fatherMiddleName', 'maritalStatus', 'mobilePhone', 'email', 'doorNo', 'street', 'locality', 'district', 'state', 'pincode', 'panNo')(customer_info)
    
    firstName = (firstName if firstName else "")
    lastName = (lastName if lastName else "")
    middleName = (middleName if middleName else "")
    full_name = firstName + middleName + lastName
    
    gender = ('M' if gender=="MALE" else "F")

    fatherFirstName = (fatherFirstName if fatherFirstName else "")
    fatherLastName = (fatherLastName if fatherLastName else "")
    fatherMiddleName = (fatherMiddleName if fatherMiddleName else "")
    father_full_name = fatherFirstName + fatherMiddleName + fatherLastName

    doorNo = (doorNo if doorNo else "")
    street = (street if street else "")
    locality = (locality if locality else "")
    res_address = doorNo + street + locality


    dob_info = data['enrollmentDTO']['customer']['dateOfBirth']
    year, monthValue, dayofMonth = itemgetter('year', 'monthValue', 'dayOfMonth')(dob_info)
    date_of_birth = str(year)+'-'+str(monthValue)+'-'+str(dayofMonth)

    bank_accounts_info = data['enrollmentDTO']['customer']['customerBankAccounts']
    account_info = bank_accounts_info[0]
    customerBankName, ifscCode, accountType, accountNumber, bankStatements = itemgetter('customerBankName', 'ifscCode', 'accountType', "accountNumber", "bankStatements")(account_info)
    bank_statement_availability = ("Yes" if(len(bankStatements)>0) else "No")

    family_info = data['enrollmentDTO']['customer']['familyMembers']
    income_info = family_info[0]['incomes'][0]['incomeEarned']

    print(income_info)
    user_data = {
        "sm_user_id": sm_user_id,
        "name": full_name,
        "date_of_birth": date_of_birth,
        "gender": gender,
        "father_name": father_full_name,
        "marital_status": maritalStatus,
        "mobile_number": mobilePhone,
        "email_id": email,
        "res_address": res_address,
        "res_city": district,
        "res_state": state,
        "res_pin_code": pincode,
        "shop_name": "Not Found",
        "shop_type": "Not Found",
        "shop_address": "Not Found",
        "monthly_income": income_info,
        "udhyog_aadhar": "Not Found",
        "uan_number": "Not Found",
        "pan_number": panNo,
        "poa_type": "Not Found",
        "poa_number": "Not Found",
        "bank_name": customerBankName,
        "account_number": accountNumber,
        "ifsc_code": ifscCode,
        "account_type": accountType,
        "bureau_score": "Not Found",
        "sm_score": "Not Found",
        "sm_loan_eligibility": "Not Found",
        "bank_statement_availability": bank_statement_availability,
    }
    return user_data


async def create_loan_data(data):
    loan_info = data['loanDTO']['loanAccount']
    loanAmount, interestRate, disbursementSchedules, tenure, processingFeeInPaisa, insuranceFee = itemgetter('loanAmount', 'interestRate', 'disbursementSchedules', 'tenure', 'processingFeeInPaisa', 'insuranceFee')(loan_info)
    disbursement_amount = disbursementSchedules[0]['disbursementAmount']
    print(loanAmount, interestRate, disbursement_amount, processingFeeInPaisa)
    response = {
        "loan_amount": loanAmount,
        "interest_rate": interestRate,
        "disbursement_amount": disbursement_amount,
        "tenure": tenure,
        "repayment_schedule_json":"Not Found",
        "am_user_token": "Not Found",
        "sm_user_id": "Not Found",
        "sm_loan_id": "Not Found",
        "processing_fee": processingFeeInPaisa,
        "additional_charges": "Not Found",
        "insurance_charges": insuranceFee,
        "number_of_edis": "Not Found"
    }
    return response