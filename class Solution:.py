class Solution(object):
    def romanToInt(self, s):
        """
        :type s: str
        :rtype: int
        """
        values = {'I':1, 'V':5, 'X':10,'L':50,"C":100,"D":500,"M":1000}
        i = 0
        total = 0
        for alphabets in s:
            currentval = values[alphabets]
            if i+1 != len(s):
                nextval = values[s[i+1]]
                if currentval < nextval:
                    remainder = nextval - currentval
                    total = total - nextval
                    total = total + remainder
                else:
                    total = total + currentval
            else:
                total = total + currentval
            i = i +1
        return total
        
if __name__ == "__main__":
    game = Solution()  
    print(game.romanToInt("III")) # 3
    print(game.romanToInt("IV")) # 4
    print(game.romanToInt("IX")) # 9
    print(game.romanToInt("LVIII")) # 58
    print(game.romanToInt("MCMXCIV")) # 199 