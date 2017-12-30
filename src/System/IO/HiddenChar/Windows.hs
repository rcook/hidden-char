{-|
Module      : System.IO.HiddenChar.Windows
Description : Windows implementation of @getHiddenChar@
Copyright   : (C) Richard Cook, 2017
Licence     : MIT
Maintainer  : rcook@rcook.org
Stability   : stable
Portability : portable

Provides the Windows implementation of @getHiddenChar@
-}

{-# LANGUAGE ForeignFunctionInterface #-}

module System.IO.HiddenChar.Windows (getHiddenChar) where

import           Data.Char
import           Foreign.C.Types

-- Must import as "safe" in order to prevent FFI call from blocking other threads
-- https://github.com/rcook/hidden-char/issues/1
foreign import ccall safe "conio.h _getch" c_getch :: IO CInt

-- | Read a character from the standard input device with buffering and echoing disabled
-- Hack based on http://stackoverflow.com/questions/2983974/haskell-read-input-character-from-console-immediately-not-after-newline
getHiddenChar ::
    IO Char -- ^ returned character
getHiddenChar = fmap (chr . fromEnum) c_getch
