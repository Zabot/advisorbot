# Adding Responses
Responses can be added by changing `data/responses.json`. `responses.json` is a list
of objects containing lists of keywords that trigger the responses, and a list of appropriate
responses, of which one will be selected at random to be used as the reply. Responses may have substitution
targets indicated by prefixing a word with `$`, e.g. `$target()`. Substitution targets will be replaced by
the return value of the function with the same name in `substitutions.py`. Any class numbers found
in the arguments to a substitution target will be replaced by a reference to the object containing
that class' information. The `m[n]` argument will be replaced by the nth class mentioned in the
original message. All other arguments will be passed through to the function in `substitutions.py`.

