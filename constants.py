
n = 7
# Top Level states
(REGISTRATION,
 MAIN_MENU,
 I_HAVE_A_QUESTION,
 I_WANT_TO_GET_INFO,
 I_WANT_TO_WATCH,
 I_WANT_A_TEST,
 CONFIGURATIONS_PLEASE) = range(n)

# Second level states
(LANGUAGE,
 PHONE_CONFIRMATION,
 PHONE_CODE,
 NAME_INPUT,
 REG_END,
 TEST_AUTH,
 TEST_READY_STATE,
 TEST_PROCESS,
 TEST_OVERVIEW_STATE
 ) = range(n, n + 9)


# States of the user defined below
NEW_USER, LANGUAGE_GOT, CODE_SENT, PHONE_CONFIRMED, ACTIVE_USER = (
    'NewUser', 'LanguageGot', 'CodeSent', 'PhoneConfirmed', 'ActiveUser'
)
