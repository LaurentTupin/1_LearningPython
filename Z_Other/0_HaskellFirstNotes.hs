--https://www.youtube.com/watch?v=02_H3LjqMr8&list=PLYIxT-vN4kRpGt0F4j5PL5ggFtYYnoxdn&index=7&t=27s

-- Init Terminal to compile everything
gsci
:l haskell-tut
:r


-- Import
import Data.List
import System.IO


--DATA Type

--INt
maxInt = maxBound :: Int	--  -2^63
minInt = minBound :: Int	--   2^63

--Integer: No Bound
--Float
--Double
bigFloat = 3.99999999999 + 0.0000000005

--Bool
--Char
--Tuple


--CONST variable
always5 :: Int
always5 = 5

--SUM
sumOfNums = sum[1..1000]

--function mod
modEx = mod 5 4
modEx2 = 5 `mod` 4
--Result is 1

--SQRT
num = 9 :: Int
sqrt_num = sqrt(fromIntegral num)  --fromIntegral to transform Int into float for sqrt function
	-- > 3

-- Math
piVal = pi
expNum = exp 9
logNum = log 9
square = 9 **2
truncate = truncate 9.9999  -- > 9
roundVal = round 9.99
ceil = ceiling 9.999
flo = floor 9.999

--type on Console:
	:t sqrt
	--  sqrt :: Floating a => a -> a
	:t truncate
	--  truncate :: (RealFrac a, Integral b) => a -> b
	
-- List
l_zeroToTen = [0..10]
l_evenList = [2, 4..20]
	-- > [2,4,6,8,10,12,14,16,18,20]
l_infintieList = [10, 20..]
	-- > List infini : 10, 20, 30... n'est pas vreiment cree jusqua que lon demande l'element X de la liste
l_num = [3,5,7,11]
l_num2 = l_num ++ [13,17,19,23,29]
l_num3 = 2 : 7 : 21 : 66 : []
	-- > [2, 7, 21, 66]
l_num4 = 1 : l_num3
	-- > [1, 2, 7, 21, 66]
int_len = length l_num4
	-- > 5
l_reverse = reverse l_num4
bl_isListempty = null l_num4
bl_is7InList = 7 `elem`	l_num4
	-- > True
int_max = maximum l_num	
int_sum = sum l_num	
int_product = product l_num

	
-- Access list by index
int_SecondNumber = l_num4 !! 1
int_fistNum = head l_num4
int_lastNum = last l_num4
l_allExceptLastVal = init l_num4
l_3firstValues = take 3 l_num4
	-- > [1, 2, 7]


























