{-|
Module      : System.IO.HiddenChar.Posix
Description : Posix implementation of @getHiddenChar@
Copyright   : (C) Richard Cook, 2017
Licence     : MIT
Maintainer  : rcook@rcook.org
Stability   : stable
Portability : portable

Provides the Posix implementation of @getHiddenChar@
-}

module System.IO.HiddenChar.Posix (getHiddenChar) where

import           Control.Exception
import           System.IO

data HandleState = HandleState BufferMode Bool

hGetState :: Handle -> IO HandleState
hGetState h = do
    bufferMode <- hGetBuffering h
    isEcho <- hGetEcho h
    return $ HandleState bufferMode isEcho

hSetState :: Handle -> HandleState -> IO ()
hSetState h (HandleState mode isEcho) = do
    hSetEcho h isEcho
    hSetBuffering h mode

bracketHandle :: Handle -> (IO a -> IO a)
bracketHandle h action = bracket
    (hGetState h)
    (hSetState h)
    (const action)

-- | Read a character from the standard input device with buffering and echoing disabled
getHiddenChar ::
    IO Char -- ^ returned character
getHiddenChar = bracketHandle stdin $ do
    hSetBuffering stdin NoBuffering
    hSetEcho stdin False
    getChar
