"""
A module for every constant of symmetric.
"""


# Logs
LOG_FILE_NAME = "symmetric.log"

# Docs
OPENAPI_ROUTE = "/openapi.json"
DOCUMENTATION_ROUTE = "/docs"

# API token authentication
API_CLIENT_TOKEN_NAME = "symmetric_api_key"
API_SERVER_TOKEN_NAME = "SYMMETRIC_API_KEY"
API_DEFAULT_TOKEN = "symmetric_token"

# Route parsing
ROUTE_PATTERN = (r"^\/$|^(?!.*[\/\-]{2,}.*)(?!.*[\-_]{2,}.*)(?!.*_{2,}.*)\/"
                 r"[a-zA-Z\_\-\/]*(?<!\-)(?<!_)(?<!\/)$")
# ^\/$  => Match a "/" string. (the "|" operator means or)
# ^(?!.*[\/\-]{2,}.*)  => Don't allow repetition of "/" or "-" characters or
#                         combinations of both, like "/-"
# (?!.*[\-_]{2,}.*)  => Don't allow repetition of "-" or "_" characters or
#                       combinations of both, like "-_"
# (?!.*_{2,}.*)  => Don't allow repetition of "_"
# \/  => The route must always start with a "/"
# [a-zA-Z\_\-\/]*  => Then, any amount of letters, hyphens, underscores and/or
#                     slashes can be allowed (as long as the don't conflict)
#                     with previous rules, namely, the lookaheads)
# (?<!\-)(?<!_)(?<!\/)$  => The final character can't be a hyphen, an
#                           underscore nor a slash
