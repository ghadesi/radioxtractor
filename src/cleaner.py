import re
import unicodedata


norm_accents = re.compile(r'[\u0610\u0611\u0612\u0613\u0614\u0615\u0616\u0617\u0618\u0619\u061a\u064b\u064c\u064d\u064e\u064f\u0650\u0651\u0652\u0653\u0654\u0655\u0656\u0657\u0658\u0659\u065a\u065b\u065c\u065d\u065e\u065f\u0670\u06d6\u06d7\u06d8\u06d9\u06da\u06db\u06dc\u06df\u06e0\u06e1\u06e2\u06e3\u06e4\u06e7\u06e8\u06ea\u06eb\u06ec\u06ed]',flags=re.U)
numerals = {r'\u0660':r'0',r'\u0661':r'1',r'\u0662':r'2',r'\u0663':r'3',r'\u0664':r'4',r'\u0665':r'5',r'\u0666':r'6',r'\u0667':r'7',r'\u0668':r'8',r'\u0669':r'9',
			r'\u06f0':r'0',r'\u06f1':r'1',r'\u06f2':r'2',r'\u06f3':r'3',r'\u06f4':r'4',r'\u06f5':r'5',r'\u06f6':r'6',r'\u06f7':r'7',r'\u06f8':r'8',r'\u06f9':r'9'} 

norm_other = re.compile(r'[\u0621]')
unknown = re.compile(r'[\x08\u200e\u200f\u202b\u202c]')
delete_marks = re.compile(r'[#&<=>?@|*\xd7\u0301\u2022\U0001f539\u2019]')

norm_marks = { r'\u066a':r'%',r'\u066c':r',',r'\u2013':r'-',r'_':r'-',r'\u2014':r'-',r'\u0640':r'-',r'\u201c':r'"',
r'\u201d':r'"',r';':r'\u061b',

}



nim_fasele = re.compile(r'[\u200b\u200d\u200c\xad]')
_ascii_letters = re.compile(r'[a-zA-Z]', flags=re.UNICODE)

ya = re.compile(r'[\u064a\u0649]')


def normalize(text):

	text = text.strip(u'\xa0\u200c \t\n\r\f\v')
	text = unicodedata.normalize('NFKD',text)
	text = _ascii_letters.sub("A", text)
	text = norm_accents.sub(r'',text)
	
	
	text = ya.sub(r'\u06cc\\',text)
	
	text = delete_marks.sub(r'',text)
	text = re.sub(r'\u0643',r'\u06a9',text,flags=re.U)
	text = re.sub(r'\u06c6',r'\u0648',text,flags=re.U)
	text = re.sub(r'\u0629',r'\u0647',text,flags=re.U) #ARABIC LETTER TEH MARBUTA
	text = re.sub(r'\u06d5',r'\u0647',text,flags=re.U)
	text = re.sub(r'\u0671',r'\u0627',text,flags=re.U) #ARABIC LETTER ALEF WASLA
	text = re.sub(r'\{',r'(',text,flags=re.U)
	text = re.sub(r'\}',r')',text,flags=re.U)
	text = re.sub(r'\[',r'(',text,flags=re.U)
	text = re.sub(r'\]',r')',text,flags=re.U)
	text = re.sub(u'\xab',r'(',text,flags=re.U)
	text = re.sub(u'\xbb',r')',text,flags=re.U)
	text = re.sub(r'\u060c',r',',text,flags=re.U) #virgool
	text = nim_fasele.sub(r'\u200c',text)

	for mark in norm_marks:
		text = re.sub(mark,norm_marks[mark],text,flags=re.U)
	
	for num in numerals:
		text = re.sub(num,numerals[num],text,flags=re.U)


	text = norm_other.sub(r'',text)
	text = unknown.sub(r'',text)
	return text
