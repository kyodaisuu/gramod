#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Calculate G mod N, where G is the Graham's number
# http://gyafun.jp/ln/gramod.cgi
# written by Fish http://googology.wikia.com/wiki/User:Kyodaisuu
# MIT License
# Last update: 2018-01-08
# Language: Python 2 or 3
#
# When environmental variable SCRIPT_NAME is set, it runs as a CGI program.
# Otherwise it runs as a commandline program.


def main():
    """Calculate G mod N, where G is the Graham's number

    Determine if it is commandline or CGI.
    """
    import os
    if os.getenv('SCRIPT_NAME') is None:
        maincl()
    else:
        maincgi()
    return


def maincl():
    """Calculate G mod N, where G is the Graham's number

    Invoked from command line.
    """
    showprocess = True  # When it is False process is not shown.
    p = 3  # Graham's number is the tower of 3
    # Test some values
    assert towermod(3, 1000, False) == 387
    assert towermod(3, 2018, False) == 1557
    assert towermod(3, 108, False) == 27
    assert towermod(3, 109, False) == 1
    assert towermod(3, 127, False) == 119
    # Input the base of mod
    base = int(input('I will calculate G mod N.\nN = '))
    assert base > 1, "N should be larger than 1"
    # Calculate G mod N and show the result
    print("G mod {0} = {1}".format(base, towermod(p, base, showprocess)))
    return


def maincgi():
    """Calculate G mod N, where G is the Graham's number

    Running as a CGI program.
    """
    import cgi
    # Comment out for debugging
    # import cgitb
    # cgitb.enable()
    maxbase = 100000
    p = 3  # Graham's number is the tower of 3
    # Write html
    print(r'''Content-Type: text/html

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Graham's number mod N</title>
  <link rel="stylesheet" type="text/css" href="fish.css">
</head>
<body>
<h1>Graham's number mod N</h1>

<p>G = Graham's number</p>
<form action="gramod.cgi" method="post">
  Calculate G mod <input type="text" name="text" />
  <input type="submit" />
</form>
''')
    # Get form input
    f = cgi.FieldStorage()
    base = f.getfirst('text', '')
    # Calculate G mod N and show the result
    if base.isdigit() and int(base) > 1:
        base = int(base)
        if base > maxbase:
            base = maxbase
        print('<p>Calculation process of G mod {0}</p>\n<pre>'.format(base))
        result = towermod(p, base, True)
        print("</pre>\n<h2>Result</h2>")
        print("<strong>G mod {0} = {1}</strong>".format(base, result))
    else:
        print("<p>Input N &le; {0} and press the button.</p>".format(maxbase))
    print(r'''<hr>
<p style="text-align: right;"><a
href="http://gyafun.jp/ln/gramod.cgi">Graham's number mod N</a>
(<a href="gramod.txt">Source code</a>)
by <a href="http://googology.wikia.com/wiki/User:Kyodaisuu">Fish</a></p>
</body>
</html>
''')
    return


def towermod(p, base, showprocess):
    """Calculate convergence of(p ^^ n) mod base

    When showprocess = True, calculation process is shown.
    """
    import math
    if p**int(math.log(base, p)) == base:
        return 0  # when p ^ integer = base
    oldlist = range(base)
    equation = 'n mod ' + str(base) + ' = '
    while True:
        list = []  # p^p^...^p^n mod base (n=0,1,2,...)
        n = 1
        equation = str(p) + '^' + equation
        while True:
            list.append(oldlist[n])  # append p^p^...^p^n
            n = (n * p) % len(oldlist)
            if oldlist[n] in list:  # rotation
                if n != 1:
                    i = list.index(oldlist[n])
                    le = len(list)
                    if showprocess:
                        print(equation + str(list) + ' => ' + str(oldlist[n]))
                        print('Rotation is')
                    if i > le - i:
                        list = list[i - le % (le - i):le]
                        i = list.index(oldlist[n])
                        le = len(list)
                    list = list[le - i:le] + list[i:le - i]
                if showprocess:
                    print('{0} {1} (cycle length = {2})'.format(
                        equation, str(list), len(list)))
                break
        oldlist = list
        if len(list) == 1:  # converged
            break
    return list[0]


if __name__ == '__main__':
    main()
