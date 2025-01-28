class Solution:
    def isValid(self, s: str) -> bool:
        stack = []
        opening = ["(","[","{"]
        closing = [")", "]","}"]
        for parenthesis in s:
            if parenthesis in opening:
                stack.append(parenthesis)
            if parenthesis in closing:
                if len(stack) == 0:
                    return False
                elif stack[-1] == "(" and parenthesis == ")":
                    stack.pop(-1)
                    continue
                elif stack[-1] == "[" and parenthesis == "]":
                    stack.pop(-1)
                    continue
                elif stack[-1] == "{" and parenthesis == "}": 
                    stack.pop(-1)
                    continue
                else: 
                    return False
        if len(stack) == 0:
            return True
        else:
            return False

s = Solution()
s.isValid("")