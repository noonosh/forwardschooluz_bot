
# Top Level states
REGISTRATION, MAIN_MENU = range(2)
# Second level states
LANGUAGE, PHONE_CONFIRMATION, PHONE_CODE, REG_END = map(chr, range(4))


# States of the user defined below
NEW_USER, LANGUAGE_GOT, CODE_SENT, PHONE_CONFIRMED, ACTIVE_USER = (
    'NewUser', 'LanguageGot', 'CodeSent', 'PhoneConfirmed', 'ActiveUser'
)
