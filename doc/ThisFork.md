About This Fork
===============

Several goals:
  * Learning :)
  * Fix issues
  * Contribute to upgrading the kit with new releases of libraries
  * Possibly extend it using other popular extensions.

I'm starting on June 3,2014 
with commit `25b8d1ac2376daed2e3cef8253ef1f48bbd4718d` 
from Feb 22, 2013.

Issues
------

### 20140604-1930 - TypeError: decoding Unicode is not supported
http://stackoverflow.com/questions/17092849/flask-login-typeerror-decoding-unicode-is-not-supported

SOLVED by specifying an older version of werzeug
at the top of requirements, and re-running `pip install -r`

More info:
    * https://github.com/maxcountryman/flask-login/issues/78
    
### 20140604-1950 - Nosetest misses libraries
    * lxml
    * requests
    * cssselect

SOLVED - I added them in reqs.pip, without version number.
