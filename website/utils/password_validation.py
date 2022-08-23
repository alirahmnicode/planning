def vlidate(password:str, password2:str=None) -> str:
    message = ''
    if password2 and password != password2:
        message+=('پسورد ها مطابقت ندار.')
        
    if len(password) < 8:
        message+=('طول پسورد نمیتواند کمتر از 8 رشته باشد.')

    return message