# Change log

## Version 0.1.0.2

* Use `_getch` instead of deprecated `getch` function (https://github.com/rcook/hidden-char/pull/2)

## Version 0.1.0.1

* Fix for concurrency issue on Windows (https://github.com/rcook/hidden-char/issues/1): the underlying "unsafe" FFI calls to `getch` would previously suspend _all_ threads in the running program while `getch` was blocking on keyboard input; with this fix, the call to `getch` is now marked "safe" and can be pre-empted

## Version 0.1.0.0

* Initial release
