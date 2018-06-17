# XSS Finder

Some simple tools which I'm using frequently to find XSS. Keep in mind: __Do not trust scripts only__! Sometimes the vulnerability is more complex and needs special treatment ;) Those scripts won't find dom bases/dynamic XSS!

## Why another XSS Find Tool?

Because most tools I tested did not find simple reflected XSS - that's why I hacked this script together. And it works... if you know how to use it.

## checkGivenParameters.py

__How to execute:__


```
python3 checkGivenParameters.py -url "http://victim/?param1=test&param2=test2&foo=bar" -payload '[XSS"]'
```

This script...
- searches for inputs, textareas, selects, buttons and uses their name/id values as additional get parameters
- replaces every get value with the given payload and checks if its reflected in the http body

Optional parameters:
- payload

### Hints
Using the default payload may result in a lot of false results.

### Screenshots

XSS on a starbucks subdomain

![s](https://i.imgur.com/hrIep5K.png)

XSS on a General Motors subdomain

![v](https://i.imgur.com/eanQkRk.png)


## parameterSearchSingleRequestMultiThread.py

__How to execute:__

```
python3 parameterSearchSingleRequestMultiThread.py -url "http://victim/" -payload '[XSS"]' -paramlist /path/to/params.txt -threads 10 -timeout 3600 --verbose --extended
```

This scripts...
- searches for inputs, textareas, selects, buttons and uses their name/id as additional get parameters
- takes every parameter (custom + wordlist) and appents it with the payload as value to the url and then checks, if the payload is reflected

Optional parameters:
- payload
- paramlist
- threads
- timeout
- verbose
- extended

__Extended mode__
Using the "--extended" flag will result in aditional checks if a parameter is found to be reflected.


### Hints
Some websites reflect the requested url this results in a lot false results WHEN the payload is something very simple like "abcdefg27sjs93" - see netflix.com or uber.com for instance. Thats why I'm not using the standard alphanumerical payload and instead choosing something like 'XSS">' or 'XSS"'. In that case I wouldnt also use the extended mode (because you basically doing extended search). If you have a victim where the request url is not reflected you should use the extended flag with a simple playload like the default one.

### Screenshots

Script bruteforces parameters and finds "year" parameter which is reflected (basic check) and then validated using extended checks (with special characters...)

![d](https://i.imgur.com/AmIxJnV.png)

I didnt pass a parameter wordlist, this forces the script to search for input fields and use the name/id as get parameters.

![ds](https://i.imgur.com/n8AN7u3.png)


## parameterSearchInChunksSingleThread.py

__How to execute:__

```
python3 parameterSearchInChunksSingleThread.py -url "http://victim/" -paramlist params.txt --extended -extendedchar "<" -chunksize 100 --verbose
```

This scripts...
- searches for inputs, textareas, selects, buttons and uses their name/id as additional get parameters
- adds also the current urls get parameters (if the exist)
- Creates for every parameter a custom payload, creates then even sized chunks
- a param-value query string based on every chunk is generated and then requested, response is checked for every payload

Optional parameters:
- paramlist
- verbose
- extended
- chunksize
- extendedchar

### Screenshots

Checking Brute Logic XSS Page with parameter wordlist...
![ds](https://i.imgur.com/smuy2yJ.png)

Checking Brute Logic XSS Page without parameter wordlist...
![ds](https://i.imgur.com/Ee4iolo.png)

Checking Starbucks subdomain (with xss):
![ds](https://i.imgur.com/un63HKZ.png)

## Wordlist

Thanks to Daniel Miessler for the parameter wordlist: https://github.com/danielmiessler/SecLists
I added some custom parameters ;)