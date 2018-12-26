.. :changelog:


v2.2.2 (2018-12-26)
-------------------
- Bump version: 2.2.1 → 2.2.2. [Petri Jokimies]
- Fix typo when calling Yahoo tracker. [Petri Jokimies]


v2.2.1 (2018-12-26)
-------------------
- Bump version: 2.2.0 → 2.2.1. [Petri Jokimies]
- Fix exhange name in Yahoo tracker. [Petri Jokimies]


v2.2.0 (2018-12-26)
-------------------
- Bump version: 2.1.6 → 2.2.0. [Petri Jokimies]
- Add Yahoo tracker. [Petri Jokimies]





v2.1.6 (2018-10-21)
-------------------
- Bump version: 2.1.5 → 2.1.6. [Petri Jokimies]
- Fix tests. [Petri Jokimies]
- Take AV tracker into account in tests. [Petri Jokimies]
- Mock out get_alpha_vantage_stock_quote. [Petri Jokimies]






- Fix Account.positions() renaming to get_positions. [Petri Jokimies]
- Rename Account.positions() to get_positions() [Petri Jokimies]










v2.1.5 (2018-10-19)
-------------------
- Bump version: 2.1.4 → 2.1.5. [Petri Jokimies]
- Ignore additinal files. [Petri Jokimies]
- Get currency from local backend. [Petri Jokimies]



- Define and use API wait time as constant. [Petri Jokimies]
- Add option to define API wait time on commandline. [Petri Jokimies]





v2.1.4 (2018-09-01)
-------------------
- Bump version: 2.1.3 → 2.1.4. [Petri Jokimies]
- New: usr: Allow multiple updates to share prices. [Petri Jokimies]








- Add optional delay when using AlphaVantage. [Petri Jokimies]



- Convert daily change to base currency. [Petri Jokimies]





- New: usr: Add security listing. [Petri Jokimies]


v2.1.3 (2018-07-26)
-------------------
- Bump version: 2.1.2 → 2.1.3. [Petri Jokimies]
- Adjust AlphaVantage request rate. [Petri Jokimies]









- Cache AlphaVantage requests. [Petri Jokimies]















v2.1.2 (2018-07-12)
-------------------
- Bump version: 2.1.1 → 2.1.2. [Petri Jokimies]
- Add dayly change. [Petri Jokimies]


v2.1.1 (2018-06-10)
-------------------
- Bump version: 2.1.0 → 2.1.1. [Petri Jokimies]
- Use API key for fixer.io. [Petri Jokimies]





- Update history. [Petri Jokimies]


v2.1.0 (2018-06-03)
-------------------

Fix
~~~
- *google*: Remove debug logging. [Petri Jokimies]

Other
~~~~~
- Bump version: 2.0.6 → 2.1.0. [Petri Jokimies]
- Use  AlphaVantatge as 'local' price provider. [Petri Jokimies]



- Add AlphaVantage as a price tracker. [Petri Jokimies]


v2.0.6 (2017-11-28)
-------------------

New features
~~~~~~~~~~~~
- *quote api*: Provide API for stock quotes. [Petri Jokimies]








Fix
~~~
- *google*: Use local google finance proxy. [Petri Jokimies]

Other
~~~~~
- Bump version: 2.0.5 → 2.0.6. [Petri Jokimies]
- *google*: Change Yahoo url in test. [Petri Jokimies]





v2.0.5 (2017-10-07)
-------------------
- Bump version: 2.0.4 → 2.0.5. [Petri Jokimies]
- Change google url. [Petri Jokimies]








v2.0.4 (2017-02-23)
-------------------

Documentation
~~~~~~~~~~~~~
- *HISTORY*: Update HISTORY. [Petri Jokimies]

Other
~~~~~
- Bump version: 2.0.3 → 2.0.4. [Petri Jokimies]
- Change Yahoo url. [Petri Jokimies]





v2.0.3 (2017-01-08)
-------------------

Fix
~~~
- Don't load anglular-scripts in templates. [Petri Jokimies]








- *summary*: Fix improperly detected currency. [Petri Jokimies]









- Use plain get in retrieving exchange rates. [Petri Jokimies]






Documentation
~~~~~~~~~~~~~
- *HISTORY*: Update HISTORY. [Petri Jokimies]

Other
~~~~~
- Bump version: 2.0.2 → 2.0.3. [Petri Jokimies]


v2.0.2 (2016-12-31)
-------------------

New features
~~~~~~~~~~~~
- *bumpversion*: Configure bumpversion. [Petri Jokimies]

Fix
~~~
- *management*: Set defaults to google quote. [Petri Jokimies]



- *urls*: Change deprecated django.conf.urls.patterns. [Petri Jokimies]
- *DividendByYear*: Fix JSON serialising. [Petri Jokimies]









Other
~~~~~
- Bump version: 2.0.1 → 2.0.2. [Petri Jokimies]
- Add pytest & bumpversion to requirements. [Petri Jokimies]
- History update. [Petri Jokimies]


v2.0.1 (2016-12-10)
-------------------
- Bump version. [Petri Jokimies]
- Add migrations. [Petri Jokimies]



- Remove Python 3.3 from travis configuration. [Petri Jokimies]


v2.0.0 (2016-11-13)
-------------------
- Use Django 1.9.11. [Petri Jokimies]





v1.2.2 (2016-11-13)
-------------------
- Bump version. [Petri Jokimies]
- Update requirements for Python3. [Petri Jokimies]


v1.2.1 (2016-11-08)
-------------------
- Bump version to 1.2.1. [Petri Jokimies]
- Use newest version of django-currency-history. [Petri Jokimies]





v1.2.0 (2016-11-03)
-------------------

Fix
~~~
- *requirements*: beatifulsoup added to requirements. [Petri Jokimies]

Other
~~~~~
- Bump version 1.1.1 to 1.2.0. [Petri Jokimies]
- Add possibility to get quotes from Yahoo Finance. [Petri Jokimies]







v1.1.1 (2016-03-06)
-------------------

New features
~~~~~~~~~~~~
- *summary detail*: Flash changed prices. [Petri Jokimies]




Other
~~~~~
- *account summary*: Use latest date from Google Finance. [Petri
  Jokimies]



- *account summary*: Sort table using Angular's orderBy. [Petri
  Jokimies]







- *securities service*: Use smaller number of mocked results. [Petri
  Jokimies]



- *gulp*: Output results in separate directory. [Petri Jokimies]



- *account summary*: $timeout parameters changed in 1.4.x. [Petri
  Jokimies]





- *account summary*: More tests. [Petri Jokimies]
- *position service*: Test for google_quote. [Petri Jokimies]
- *karma conf*: Run coverage. [Petri Jokimies]


v1.1.0 (2016-02-16)
-------------------

New features
~~~~~~~~~~~~
- *account summary*: Use correct currency in calculations, use spinner.
  [Petri Jokimies]















- *account summary*: Added market value calculation. [Petri Jokimies]
- *account summary*: Display live values. [Petri Jokimies]
- *account summary*: Count total market value. [Petri Jokimies]
- *account summary*: Initial price live updates. [Petri Jokimies]



- Added API to get list of holdings. [Petri Jokimies]

Other
~~~~~
- More files to watch in karma.conf. [Petri Jokimies]
- Added test for Angular currency service. [Petri Jokimies]
- *karma*: Using jasmine-query for fixtures. [Petri Jokimies]
- *gulp*: First gulp tasks. [Petri Jokimies]
- *account summary*: Removed unnecessary DB queries. [Petri Jokimies]



- *account*: Make AccountBase more usable. [Petri Jokimies]





v1.0.1 (2016-01-15)
-------------------

Fix
~~~
- *requirements*: Specific about Django version. [Petri Jokimies]







Other
~~~~~
- *update prices*: Adapt to KL's new web page. [Petri Jokimies]


v1.0.0 (2015-11-30)
-------------------

New features
~~~~~~~~~~~~
- Add management commands to update prices. [Petri Jokimies]




Refactor
~~~~~~~~
- *test*: Security test and factories separeted. [Petri Jokimies]
- *test*: Price tests and factories sepateted. [Petri Jokimies]

Documentation
~~~~~~~~~~~~~
- Added comments for management commads. [Petri Jokimies]


v0.1.0 (2015-09-25)
-------------------
- Initial commit. [Petri Jokimies]
