import re

class rgxHandler:

    # Taken from https://www.safaribooksonline.com/library/view/python-cookbook-2nd/0596007973/ch01s19.html
    linetitles = ["product/productId: ", "product/title: ", "product/price: ", "review/userId: ", "review/profileName: ", "review/helpfulness: ", "review/score: ", "review/time: ", "review/summary: ", "review/text: "]
    getrids = dict([(linetitles[0],''), (linetitles[1],''), (linetitles[2],''), (linetitles[3],''), (linetitles[4],''), (linetitles[5],''), (linetitles[6],''), (linetitles[7],''), (linetitles[8],''), (linetitles[9],'')])
    replace = {"\\":"\\\\", '"':"&quot;" }
    unreplace = {"\\\\":"\\", "&quot;":'"'}

    def __init__(self):
        pass

    def multiple_replace(self, text, adict):
        rx = re.compile('|'.join(map(re.escape, adict)))
        def one_xlat(match):
            return adict[match.group(0)]
        return rx.sub(one_xlat, text)

    def line_rgx(self, text):
        text = text.strip('\n')
        text = self.multiple_replace(text, self.getrids)
        text = self.multiple_replace(text, self.replace)
        return text

    def find3OrMore(self, line):
        #line = re.sub("&quot;", ' ', line)
        line = re.sub(r'([^\s\w]|_)+', ' ', line)
        words = line.split()
        rtnwords = []

        for word in words:
            if len(word.strip()) >= 3:
               rtnwords.append(word.strip().lower())
        return rtnwords

    def putLineTitlesBack(self, review):
        rtnlines = []

        iter = re.finditer('"', review)
        quotes = [m.start(0) for m in iter] 

        iter = re.finditer(',', review)
        commas = [m.start(0) for m in iter]     
        
        q = 0
        c = 0

        while(True):

            if commas[c] < quotes[q]:
                if c == 0:
                    rtnlines.append(review[0:commas[c]] + '\n')
                else:
                    if quotes[q-1] > commas[c-1]:
                        pass
                    else:
                        rtnlines.append(review[commas[c-1]+1:commas[c]] + '\n')
                c += 1
            elif commas[c] > quotes[q] and commas[c] < quotes[q+1]:
                rtnlines.append(review[quotes[q]+1:quotes[q+1]] + '\n')
                if q+1 == len(quotes)-1:
                    break
                while commas[c] < quotes[q+1]:
                    c += 1
                q+=2
            else:
                rtnlines.append(review[quotes[q]+1:quotes[q+1]] + '\n')
                q+=2    
            if q == len(quotes):
                break
         
        i = 0     
        for line in rtnlines:
            line = self.multiple_replace(line.strip('"'), self.unreplace)
            rtnlines[i] = self.linetitles[i] + line + '\n'
            i += 1
        return rtnlines
        

