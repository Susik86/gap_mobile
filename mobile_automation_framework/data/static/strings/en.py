class StringsEn:

    class LoginPage:
        subtitle = 'Sign in with your company email'
        email_placeholder = 'Email'
        password_placeholder = 'Password'
        reset_your_password = 'Reset your password'
        show_btn = "Show"
        sign_in_btn = "Sign In"
        bottom_txt = "Don’t have an account? Learn more about Genius"
        invalid_login_pop_up = "Username or password is invalid"
        invalid_email_message = "Invalid email address"
        empty_email = "Please enter your email."
        empty_password = "Please enter your password"


    class DashboardPage:
        title = 'Swipe for Genius'
        subtitle = ''
        email_placeholder = 'Email'
        password_placeholder = 'Password'
        redet_your_password = 'Reset your password'
        bottom_txt = ""

    class GMPage:
        title = ''
        subtitle = ''


    class General:
        login_button = 'Sign In'


    class Errors:
        required_field = 'This field is required'
        invalid_email = 'Invalid email'
        invalid_company_url = 'Invalid company URL'
        invalid_password = 'Password must contain at least 8 characters including numbers, special symbols, upper and lower cased characters'
        input_minimum_length = 'Minimum length of this field is %s characters.'
        input_maximum_length = 'Maximum length of this field is %s characters'
        input_expiration_period_length = 'Expiration period cannot exceed 10000 months'
        passwords_dont_match = 'Passwords don\'t match'
        already_existing_name = 'Name already exists'
        invalid_value = 'Entered Invalid value'
        existing_model = 'Model already exists'
        existing_email = 'User already exists'
        invalid_number = 'Invalid number'
        price_valid_range = 'Please enter a valid price between 0 and 1,000,000,000'

    class ApiErrors:
        invalid_amount_characters = 'Ensure this field has no more than %s characters.'






    class ToastMessages:
        company_id_already_exist = 'Company identifier already exists'
        email_successfully_resent = 'The email has been successfully resent'
        booked_company_is_not_found = 'Booked company is not found'
        invalid_verification_code = 'Invalid verification code'
        something_went_wrong = 'Something went wrong'
        company_id = 'Company id already exists'
        invalid_email_password_message = 'You have entered an invalid e-mail or password'
        title_error = 'Error'
        title_success = 'Success'
        recovery_link_has_resent = 'Password recovery link has resent'
        invalid_token = 'Token is invalid'
        user_not_exist = 'User does not exist'
        user_created = 'User successfully created.'
        user_edited = 'User successfully updated.'
        asset_type_created = 'Asset type successfully created.'
        asset_type_deleted = 'Asset type successfully deleted.'
        asset_type_updated = 'Asset type successfully updated.'
        asset_created = 'Asset successfully created.'

    class DialogSubTitles:
        delete_location = 'This location is used on %s assets. If you delete it, it will be removed from all that assets.'
        delete_brand = 'This brand is used on %s assets. If you delete it, it will be removed from all that assets.'
        delete_tag = 'This tag is used on %s assets. If you delete it, it will be removed from all that assets.'
        delete_custom_field = 'This field is used on %s assets. If you delete it, you will loose those values and their history.'
        leave_form = 'There are unsaved changes. After clicking the "leave" button these changes will not be saved.'

    class DialogTitles:
        leave_form = 'Are you sure you want to leave?'  #TODO maybe should be dynamic as it is same for Users too?
        delete_asset_type_model = 'Are you sure you want to delete this model?'
        delete_asset_type = 'Are you sure you want to delete this type?'
        delete_asset_field = 'Are you sure you want to delete this field?'
