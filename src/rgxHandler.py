import re

class rgxHandler:


	getrids = dict([("product/productId: ",''), ("product/title: ",''), ("product/price: ",''), ("review/userId: ",''), ("review/profileName: ",''), ("review/helpfulness: ",''), ("review/score: ",''), ("review/time: ",''), ("review/summary: ",''), ("review/text: ",'')])
	replace = {"\\":"\\\\", '"': "&quot;" }

	def __init__(self):

		def multiple_replace(self, text, adict):
			rx = re.compile('|'.join(map(re.escape, adict)))
	    	def one_xlat(match):
	    	    return adict[match.group(0)]
	    	return rx.sub(one_xlat, text)

		def line_rgx(self, text):
			rtnline = multiple_replace(text.strip('\n'), getrids)
			rtnline = multiple_replace(rtnline, replace)
			return rtnline
