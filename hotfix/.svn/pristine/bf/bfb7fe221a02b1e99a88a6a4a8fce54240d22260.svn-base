from django import template
register=template.Library()  
def cut(value):
    return value.split("-")[1]
register.filter('cut',cut)

def cutStrNN(value,n):
    cc=cutStr()
    return cc.trunc_word(value,n)
register.filter('cutStrNN',cutStrNN)

class cutStr:

    def is_chinese(self,uchar):
        if uchar >= u'\u4e00' and uchar<=u'\u9fa5':
            return True
        return False
    def is_number2(self,uchar):
        if uchar >= u'\u0030' and uchar<=u'\u0039':
            return True
        return False
    def is_alphabet(self,uchar):
        if (uchar >= u'\u0041' and uchar<=u'\u005a') or (uchar >= u'\u0061' and uchar<=u'\u007a'):
            return True
        return False
    def is_other(self,uchar):
        if not (self.is_chinese(uchar) or self.is_number2(uchar) or self.is_alphabet(uchar)):
            return True
        return False

    def gbkwordlen(self,u):
        f1=self.is_number2(u)
        f2=self.is_alphabet(u)
        if self.is_number2(u) or self.is_alphabet(u):
            return 1
        return 2

    def gbkwordslen(self,uw):
        i = 0
        for u in uw:
            i += self.gbkwordlen(u)
        return i

    def trunc_word(self,uw, len):
        l = 0
        i = 1
        if uw is None:
            return ''
        for u in uw:
            l += self.gbkwordlen(u)
            if l > len:
                return uw[:i-1]+"..."
            i += 1
        return uw

