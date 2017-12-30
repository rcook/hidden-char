# `hidden-char`

[![Travis branch](https://img.shields.io/travis/rcook/hidden-char/master.svg)](https://travis-ci.org/rcook/hidden-char)
[![Hackage](https://img.shields.io/hackage/v/hidden-char.svg)](http://hackage.haskell.org/package/hidden-char)
[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/rcook/hidden-char/master/LICENSE)

This package provides a `getHiddenChar` function which works reasonably consistently across the Windows, Linux and macOS platforms. `getHiddenChar` yields a single character from the standard input device with buffering and echoing to standard output disabled.

## Dev guide

This project can be built using the [Stack][stack] build tool.

### Build

```
stack build
```

### Test

```
stack test
```

### Upload package

```
stack upload .
```

### Upload documentation

I use my [`upload-haddocks`][upload-haddocks] tool which requires a functioning installation of Python and pip:

```
pip install --user upload-haddocks
upload-haddocks
```

## Releases

[View change log for more information][change-log]

## Licence

[MIT License][licence]

Copyright &copy; 2017, Richard Cook.

[change-log]: CHANGELOG.md
[licence]: LICENSE
[stack]: http://haskellstack.org/
[upload-haddocks]: https://github.com/rcook/upload-haddocks