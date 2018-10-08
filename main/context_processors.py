from django.contrib.auth.models import User
from models.models import AccountDetails

def add_variable_to_context(request):
    if request.user.is_authenticated:
        accountDetails = AccountDetails.objects.filter(user=request.user).first()
        level = accountDetails.level
        levels = range(1, level + 1)
        exp_bar = (accountDetails.current_exp * 100) / accountDetails.exp_max
        hp_bar = (accountDetails.current_hp * 100) / accountDetails.hp_max
        return {
            "player": request.user.get_full_name(), 
            "levels": levels, 
            "account": accountDetails,
            "exp_bar": exp_bar,
            "hp_bar": hp_bar,
            }
    return {
        
    }