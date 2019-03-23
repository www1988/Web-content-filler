import xmlrpc.client

class MetaWeblog():
    def __init__(self, username, password, verbose=False):
        self.un = username
        self.pw = password
        self.sp = xmlrpc.client.ServerProxy(
            'https://你的地址/action/xmlrpc', verbose=verbose)

 
    def newPost(self, title, content, keywords, category, date):
        return self.sp.metaWeblog.newPost(0, self.un, self.pw, {
            'title' : title,
            'description' : content,
            'mt_allow_comments' : '0', # 1 to allow comments
            'mt_allow_pings' : '0',  # 1 to allow trackbacks
            'post_type' : 'post',
            'mt_keywords' : keywords,
            'categories' : category,
            'date' : date
            }, True)