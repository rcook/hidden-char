{-|
Module      : HiddenCharSpec
Description : Tests for @System.IO.HiddenChar@ module
Copyright   : (C) Richard Cook, 2017
Licence     : MIT
Maintainer  : rcook@rcook.org
Stability   : stable
Portability : portable
-}

{-# LANGUAGE ScopedTypeVariables #-}

module HiddenCharSpec (spec) where

import           Control.Concurrent
import           Control.Exception
import           System.IO.HiddenChar
import           System.Timeout
import           Test.Hspec

spec :: Spec
spec = do
    describe "concurrent use of getHiddenChar" $
        it "doesn't block other threads" $ do
            -- Run getHiddenChar in a bound thread and swallow all exceptions
            _ <- forkOS $ do
                _ <- getHiddenChar `catch` (\(_ :: SomeException) -> return ' ')
                return ()

            -- On another bound thread, count up to a given value with a small
            -- delay at each step. runInBoundThread should terminate and return
            -- the expected value if getHiddenChar works correctly. In the presence
            -- of calls to functions via the "unsafe", then this thread will block.
            -- This is a behaviour we would like to avoid.
            -- https://github.com/rcook/hidden-char/issues/1
            let countUpTo :: Int -> IO Int
                countUpTo n = helper n n
                    where
                        helper n' i
                            | i == 0 = return n'
                            | otherwise = do
                                threadDelay 1
                                helper n' (i - 1)
            result <- timeout 1000000 $ runInBoundThread (countUpTo 5)
            result `shouldBe` Just 5