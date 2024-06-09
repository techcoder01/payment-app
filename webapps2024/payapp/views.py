
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate
from .forms import BankAccountForm, SignUpForm
from .models import BankAccount, UserProfile  # Import UserProfile model
import logging
from .models import Card
from .forms import CardForm
from django.db.models import Min
from django.contrib.auth.hashers import check_password
logger = logging.getLogger(__name__)
from django.contrib.auth.decorators import login_required



def index(request):
    return render(request, 'index.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Get form data
            username = form.cleaned_data['username']  # Assuming 'username' field is for first name
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            phone_number = form.cleaned_data['phone_number']
            # Create user
            user = User.objects.create_user(username=email, email=email, password=password)
            user.first_name = username
            user.save()
            # Create UserProfile
            profile = UserProfile.objects.create(user=user, phone_number=phone_number)
            # Authenticate user and log in
            user = authenticate(request, username=email, password=password)
            if user:
                login(request, user)
                return redirect('login')  # Redirect to login success page
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.filter(email=email).first()  # Fetch user by email
        if user is not None and check_password(password, user.password):
            login(request, user)
            logger.info("User logged in successfully")
            return redirect('dashboard')
        else:
            logger.error("Invalid login credentials")
            error_message = "Invalid email or password. Please try again."
            return render(request, 'login.html', {'error': error_message})
    return render(request, 'login.html')


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def transactions(request):
    return render(request, 'transactions.html')

@login_required
def send_money(request):
    return render(request, 'send-money.html')

@login_required
def request_money(request):
    return render(request, 'request-money.html')

@login_required
def send_money_success(request):
    return render(request, 'send-money-success.html')

@login_required
def request_money_success(request):
    return render(request, 'request-money-success.html')

@login_required
def send_money_confirm(request):
    return render(request, 'send-money-confirm.html')

@login_required
def request_money_confirm(request):
    return render(request, 'request-money-confirm.html')

@login_required
def profile(request):
    return render(request, 'profile.html')

# @login_required
# def payment_methods(request):
#     if request.method == 'POST':
#         # Update card details
#         if 'card_id' in request.POST:
#             card_id = request.POST.get('card_id')
#             card = Card.objects.get(id=card_id, user=request.user)
#             form = CardForm(request.POST, instance=card)
#             if form.is_valid():
#                 form.save()
#                 return redirect('payment-methods')
#         # Add new card
#         else:
#             form = CardForm(request.POST)
#             if form.is_valid():
#                 form.instance.user = request.user
#                 form.save()
#                 return redirect('payment-methods')
            
#     else:
#         form = CardForm()
    
#     user_cards = Card.objects.filter(user=request.user)
#     return render(request, 'payment-methods.html', {'form': form, 'user_cards': user_cards})


@login_required
def payment_methods(request):
    if request.method == 'POST':
        if 'card_id' in request.POST:
            card_id = request.POST.get('card_id')
            card = Card.objects.get(id=card_id, user=request.user)
            form = CardForm(request.POST, instance=card)
        elif 'bank_account_id' in request.POST:
            bank_account_id = request.POST.get('bank_account_id')
            bank_account = BankAccount.objects.get(id=bank_account_id, user=request.user)
            form = BankAccountForm(request.POST, instance=bank_account)
        else:
            if 'account_type' in request.POST:
                form = BankAccountForm(request.POST)
            else:
                form = CardForm(request.POST)
        
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('payment-methods')
    else:
        # Reinitialize forms inside the conditional block
        card_form = CardForm()
        bank_account_form = BankAccountForm()

        user_cards = Card.objects.filter(user=request.user)
        user_bank_accounts = BankAccount.objects.filter(user=request.user)
        
                # Check if there are any existing cards or bank accounts
        # Check if there are any existing cards or bank accounts
        if user_cards.exists():
            # Assign primary to the earliest card by id
            primary_card_id = user_cards.aggregate(Min('id'))['id__min']
            Card.objects.filter(id=primary_card_id).update(is_primary=True)
            # Get the primary card's balance
            primary_card_balance = Card.objects.get(id=primary_card_id).account_balance
        else:
            primary_card_balance = None

        if user_bank_accounts.exists():
            # Assign primary to the earliest bank account by id
            primary_bank_account_id = user_bank_accounts.aggregate(Min('id'))['id__min']
            BankAccount.objects.filter(id=primary_bank_account_id).update(is_primary=True)
        
        

        payment_methods = {
        'COUNTRY_CHOICES' : [
        ("", "--- Please Select ---"),
        ("244", "Aaland Islands"),
        ("1", "Afghanistan"),
        ("2", "Albania"),
        ("3", "Algeria"),
        ("4", "American Samoa"),
        ("5", "Andorra"),
        ("6", "Angola"),
        ("7", "Anguilla"),
        ("8", "Antarctica"),
        ("9", "Antigua and Barbuda"),
        ("10", "Argentina"),
        ("11", "Armenia"),
        ("12", "Aruba"),
        ("252", "Ascension Island (British)"),
        ("13", "Australia"),
        ("14", "Austria"),
        ("15", "Azerbaijan"),
        ("16", "Bahamas"),
        ("17", "Bahrain"),
        ("18", "Bangladesh"),
        ("19", "Barbados"),
        ("20", "Belarus"),
        ("21", "Belgium"),
        ("22", "Belize"),
        ("23", "Benin"),
        ("24", "Bermuda"),
        ("25", "Bhutan"),
        ("26", "Bolivia"),
        ("245", "Bonaire, Sint Eustatius and Saba"),
        ("27", "Bosnia and Herzegovina"),
        ("28", "Botswana"),
        ("29", "Bouvet Island"),
        ("30", "Brazil"),
        ("31", "British Indian Ocean Territory"),
        ("32", "Brunei Darussalam"),
        ("33", "Bulgaria"),
        ("34", "Burkina Faso"),
        ("35", "Burundi"),
        ("36", "Cambodia"),
        ("37", "Cameroon"),
        ("38", "Canada"),
        ("251", "Canary Islands"),
        ("39", "Cape Verde"),
        ("40", "Cayman Islands"),
        ("41", "Central African Republic"),
        ("42", "Chad"),
        ("43", "Chile"),
        ("44", "China"),
        ("45", "Christmas Island"),
        ("46", "Cocos (Keeling) Islands"),
        ("47", "Colombia"),
        ("48", "Comoros"),
        ("49", "Congo"),
        ("50", "Cook Islands"),
        ("51", "Costa Rica"),
        ("52", "Cote D'Ivoire"),
        ("53", "Croatia"),
        ("54", "Cuba"),
        ("246", "Curacao"),
        ("55", "Cyprus"),
        ("56", "Czech Republic"),
        ("237", "Democratic Republic of Congo"),
        ("57", "Denmark"),
        ("58", "Djibouti"),
        ("59", "Dominica"),
        ("60", "Dominican Republic"),
        ("61", "East Timor"),
        ("62", "Ecuador"),
        ("63", "Egypt"),
        ("64", "El Salvador"),
        ("65", "Equatorial Guinea"),
        ("66", "Eritrea"),
        ("67", "Estonia"),
        ("68", "Ethiopia"),
        ("69", "Falkland Islands (Malvinas)"),
        ("70", "Faroe Islands"),
        ("71", "Fiji"),
        ("72", "Finland"),
        ("74", "France, Metropolitan"),
        ("75", "French Guiana"),
        ("76", "French Polynesia"),
        ("77", "French Southern Territories"),
        ("126", "FYROM"),
        ("78", "Gabon"),
        ("79", "Gambia"),
        ("80", "Georgia"),
        ("81", "Germany"),
        ("82", "Ghana"),
        ("83", "Gibraltar"),
        ("84", "Greece"),
        ("85", "Greenland"),
        ("86", "Grenada"),
        ("87", "Guadeloupe"),
        ("88", "Guam"),
        ("89", "Guatemala"),
        ("256", "Guernsey"),
        ("90", "Guinea"),
        ("91", "Guinea-Bissau"),
        ("92", "Guyana"),
        ("93", "Haiti"),
        ("94", "Heard and Mc Donald Islands"),
        ("95", "Honduras"),
        ("96", "Hong Kong"),
        ("97", "Hungary"),
        ("98", "Iceland"),
        ("99", "India"),
        ("100", "Indonesia"),
        ("101", "Iran (Islamic Republic of)"),
        ("102", "Iraq"),
        ("103", "Ireland"),
        ("254", "Isle of Man"),
        ("104", "Israel"),
        ("105", "Italy"),
        ("106", "Jamaica"),
        ("107", "Japan"),
        ("257", "Jersey"),
        ("108", "Jordan"),
        ("109", "Kazakhstan"),
        ("110", "Kenya"),
        ("111", "Kiribati"),
        ("113", "Korea, Republic of"),
        ("253", "Kosovo, Republic of"),
        ("114", "Kuwait"),
        ("115", "Kyrgyzstan"),
        ("116", "Lao People's Democratic Republic"),
        ("117", "Latvia"),
        ("118", "Lebanon"),
        ("119", "Lesotho"),
        ("120", "Liberia"),
        ("121", "Libyan Arab Jamahiriya"),
        ("122", "Liechtenstein"),
        ("123", "Lithuania"),
        ("124", "Luxembourg"),
        ("125", "Macau"),
        ("127", "Madagascar"),
        ("128", "Malawi"),
        ("129", "Malaysia"),
        ("130", "Maldives"),
        ("131", "Mali"),
        ("132", "Malta"),
        ("133", "Marshall Islands"),
        ("134", "Martinique"),
        ("135", "Mauritania"),
        ("136", "Mauritius"),
        ("137", "Mayotte"),
        ("138", "Mexico"),
        ("139", "Micronesia, Federated States of"),
        ("140", "Moldova, Republic of"),
        ("141", "Monaco"),
        ("142", "Mongolia"),
        ("242", "Montenegro"),
        ("143", "Montserrat"),
        ("144", "Morocco"),
        ("145", "Mozambique"),
        ("146", "Myanmar"),
        ("147", "Namibia"),
        ("148", "Nauru"),
        ("149", "Nepal"),
        ("150", "Netherlands"),
        ("151", "Netherlands Antilles"),
        ("152", "New Caledonia"),
        ("153", "New Zealand"),
        ("154", "Nicaragua"),
        ("155", "Niger"),
        ("156", "Nigeria"),
        ("157", "Niue"),
        ("158", "Norfolk Island"),
        ("112", "North Korea"),
        ("159", "Northern Mariana Islands"),
        ("160", "Norway"),
        ("161", "Oman"),
        ("162", "Pakistan"),
        ("163", "Palau"),
        ("247", "Palestinian Territory, Occupied"),
        ("164", "Panama"),
        ("165", "Papua New Guinea"),
        ("166", "Paraguay"),
        ("167", "Peru"),
        ("168", "Philippines"),
        ("169", "Pitcairn"),
        ("170", "Poland"),
        ("171", "Portugal"),
        ("172", "Puerto Rico"),
        ("173", "Qatar"),
        ("174", "Reunion"),
        ("175", "Romania"),
        ("176", "Russian Federation"),
        ("177", "Rwanda"),
        ("178", "Saint Kitts and Nevis"),
        ("179", "Saint Lucia"),
        ("180", "Saint Vincent and the Grenadines"),
        ("181", "Samoa"),
        ("182", "San Marino"),
        ("183", "Sao Tome and Principe"),
        ("184", "Saudi Arabia"),
        ("185", "Senegal"),
        ("243", "Serbia"),
        ("186", "Seychelles"),
        ("187", "Sierra Leone"),
        ("188", "Singapore"),
        ("189", "Slovak Republic"),
        ("190", "Slovenia"),
        ("191", "Solomon Islands"),
        ("192", "Somalia"),
        ("193", "South Africa"),
        ("194", "South Georgia & South Sandwich Islands"),
        ("248", "South Sudan"),
        ("195", "Spain"),
        ("196", "Sri Lanka"),
        ("249", "St. Barthelemy"),
        ("197", "St. Helena"),
        ("250", "St. Martin (French part)"),
        ("198", "St. Pierre and Miquelon"),
        ("199", "Sudan"),
        ("200", "Suriname"),
        ("201", "Svalbard and Jan Mayen Islands"),
        ("202", "Swaziland"),
        ("203", "Sweden"),
        ("204", "Switzerland"),
        ("205", "Syrian Arab Republic"),
        ("206", "Taiwan"),
        ("207", "Tajikistan"),
        ("208", "Tanzania, United Republic of"),
        ("209", "Thailand"),
        ("210", "Togo"),
        ("211", "Tokelau"),
        ("212", "Tonga"),
        ("213", "Trinidad and Tobago"),
        ("255", "Tristan da Cunha"),
        ("214", "Tunisia"),
        ("215", "Turkey"),
        ("216", "Turkmenistan"),
        ("217", "Turks and Caicos Islands"),
        ("218", "Tuvalu"),
        ("219", "Uganda"),
        ("220", "Ukraine"),
        ("221", "United Arab Emirates"),
        ("222", "United Kingdom"),
        ("223", "United States"),
        ("224", "United States Minor Outlying Islands"),
        ("225", "Uruguay"),
        ("226", "Uzbekistan"),
        ("227", "Vanuatu"),
        ("228", "Vatican City State (Holy See)"),
        ("229", "Venezuela"),
        ("230", "Viet Nam"),
        ("231", "Virgin Islands (British)"),
        ("232", "Virgin Islands (U.S.)"),
        ("233", "Wallis and Futuna Islands"),
        ("234", "Western Sahara"),
        ("235", "Yemen"),
        ("238", "Zambia"),
        ("239", "Zimbabwe")
    ],
    'BANKS': [
        ("", "--- Please Select ---"),
        ("1", "Bank 1"),
        ("2", "Bank 2"),
        ("3", "Bank 3"),
        ("4", "Bank 4"),
        ("5", "Bank 5"),
        ("6", "Bank 6"),
        ("7", "Bank 7")
    ]
        }
        return render(request, 'payment-methods.html', {
            'user_cards': user_cards,
            'user_bank_accounts': user_bank_accounts,
            'card_form': card_form,
            'bank_account_form': bank_account_form,
            'payment_methods': payment_methods,
            'primary_card_balance': primary_card_balance  # Pass primary card balance to template context
        })


@login_required
def delete_card(request):
    if request.method == 'POST':
        card_id = request.POST.get('card_id')
        try:
            card = Card.objects.get(id=card_id, user=request.user)
            card.delete()
            logger.info('Card deleted successfully')
            return redirect('payment-methods')  # Redirect to payment_methods view
        except Card.DoesNotExist:
            logger.error('Card not found')
            return JsonResponse({'success': False, 'error': 'Card not found.'})
    logger.error('Invalid request method')
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})


@login_required
def delete_bank_account(request):
    if request.method == 'POST':
        bank_account_id = request.POST.get('bank_account_id')
        try:
            bank_account = BankAccount.objects.get(id=bank_account_id, user=request.user)
            bank_account.delete()
            logger.info('Bank account deleted successfully')
            return redirect('payment-methods')  # Redirect to payment_methods view
        except BankAccount.DoesNotExist:
            logger.error('Bank account not found')
            return JsonResponse({'success': False, 'error': 'Bank account not found.'})
    logger.error('Invalid request method')
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})
