from flashtext.keyword import KeywordProcessor

# 提取关键字
# add_keyword（查找字符，替换字符），也就是先找到句子中的’你好’，然后显示出来的是add_keyword的替换字符
# 英文
keyword_processor = KeywordProcessor()
keyword_processor.add_keyword('Big Apple', 'New York')
keyword_processor.add_keyword('Bay Area')
keywords_found = keyword_processor.extract_keywords('I love Big Apple and Bay Area.')
print(keywords_found)
#中文
keyword_processor = KeywordProcessor()
keyword_processor.add_keyword('你好', '您好')  # 前面一个单词为住   后面一个单词为替换
keyword_processor.add_keyword('不要')
keywords_found = keyword_processor.extract_keywords('你好，请不要随便践踏草坪。')  #显示的单词为替换之后的
print(keywords_found)

# 替换关键字
keyword_processor = KeywordProcessor()
keyword_processor.add_keyword('你好', '您好')  # 前面一个单词为住   后面一个单词为替换
new_sentence = keyword_processor.replace_keywords('你好，请不要随便践踏草坪。')
print(new_sentence)