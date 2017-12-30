{-|
Module      : System.IO.HiddenChar
Description : Umbrella module for @System.IO.HiddenChar@
Copyright   : (C) Richard Cook, 2017
Licence     : MIT
Maintainer  : rcook@rcook.org
Stability   : stable
Portability : portable

This module provides a @getHiddenChar@ function which works reasonably
consistently across the Windows, Linux and macOS platforms. @getHiddenChar@
yields a single character from the standard input device with buffering and
echoing to standard output disabled.
-}

{-# LANGUAGE CPP #-}

module System.IO.HiddenChar (getHiddenChar) where

#if defined(OS_LINUX) || defined(OS_MACOS)
import           System.IO.HiddenChar.Posix
#elif defined(OS_WINDOWS)
import           System.IO.HiddenChar.Windows
#else
#error Unsupported platform
#endif
