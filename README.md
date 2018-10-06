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

## parameterSearchInChunksSingleThread.py

__How to execute:__

```
python3 parameterSearchInChunksSingleThread.py -u "http://victim/" --paramlist wordlists/params.txt --extended --extendedchar "<" --chunksize 75 --verbose --wait 5
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
- chunksize (default: 75, using a bigger value may result in server errors due small client buffer settings!!)
- extendedchar
- wait (default: 0, wait time in seconds between requests)

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
