#Advisorbot
Advisorbot is a chat bot with slack integration designed to provide information about the CS curriculum at Southern Illinois
University Edwardsville.

## Dependencies
Advisorbot uses python3 and [python-slackclient](https://github.com/slackapi/python-slackclient) to communicate with a slack bot.
Installation can be done with [PyIP](https://pypi.python.org/pypi). See the slackclient page for more details

    pip install slackclient

## API token
Advisorbot also requires an API token to connect to the team. This token can be found on the custom bot integration
page and must be saved as `api.token` in the same directory as `advisorbot.py`. Anyone that knows this token can
control the slack bot without further authentication, so it should not be pushed to the repository or shared with
anyone.

### Running without the API token
For testing purposes advisorbot can be run without the slack integration by running `advisorbot_console.py`. Any
text on the standard input will be feed through the same procedure as if it had been said to advisorbot by a user,
and the final response will be written to standard out.

## Adding Responses
Responses can be added by changing `data/responses.json`. `responses.json` is a list
of objects containing lists of regular expressions that trigger the responses, and a list of appropriate
responses, of which one will be selected at random to be used as the reply. Responses are matched from the top down, the
first match supersedes any other matches (though all will be captured). Responses may have substitution
targets indicated by prefixing a word with `$`, e.g. `$target()`. Substitution targets will be replaced by
the return value of the function with the same name in `substitutions.py`. Any class numbers found
in the arguments to a substitution target will be replaced by a reference to the object containing
that class' information. The `m[n]` argument will be replaced by the nth class mentioned in the
original message. All other arguments will be passed through to the function in `substitutions.py`.

