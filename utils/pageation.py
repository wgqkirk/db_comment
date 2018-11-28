#__Author__："汪国强"
#__Date__: 2017/12/17


class page_help():
    def __init__(self,base_url,current_page,total,pagesize):
        self.base_url=base_url
        self.current_page=current_page
        self.total=total
        self.pagesize=pagesize
    def pagenum(self):
        a,v=divmod(self.total,self.pagesize)
        if v==0:
            return a
        else:
            return a+1
    def db_start(self):
        return (self.current_page-1)*self.pagesize
    def db_end(self):
        return self.current_page*self.pagesize

    def page_tackle(self):
        pagenum=self.pagenum()
        page_list = []
        pre_page = self.current_page - 1
        after_page = self.current_page + 1
        if self.current_page == 1:
            page_list.append('''<nav aria-label="Page navigation" class="pull-right">
                                <ul class="pagination">
                                <li>
                                  <a href="%s?pagenum=1" aria-label="Previous">
                                <span aria-hidden="true">&laquo;</span>
                                  </a>
                                </li>'''%self.base_url)
        else:
            page_list.append('''<nav aria-label="Page navigation" class="pull-right">
                        <ul class="pagination">
                        <li>
                          <a href="%s?pagenum=%d" aria-label="Previous">
                        <span aria-hidden="true">&laquo;</span>
                          </a>
                        </li>''' % (self.base_url,pre_page))
        page_list.append('<li><a href="%s?pagenum=1">首页</a></li>'%self.base_url)
        if self.current_page <= 6:
            x = 1
            y = 12
        elif self.current_page >= pagenum - 5:
            x = pagenum - 10
            y = pagenum + 1
        else:
            x = self.current_page - 5
            y = self.current_page + 6
        for i in range(x, y):
            if i == self.current_page:
                page_list.append('<li class="active"><a href="%s?pagenum=%d">%d</a></li>' % (self.base_url,i, i))
            else:
                page_list.append('<li><a href="%s?pagenum=%d">%d</a></li>' % (self.base_url,i, i))
        page_list.append('<li><a href="%s?pagenum=%d">尾页</a></li>' % (self.base_url,pagenum))
        if self.current_page == pagenum:
            page_list.append('''<li>
                          <a href="%s?pagenum=%d" aria-label="Next">
                        <span aria-hidden="true">&raquo;</span>
                          </a>
                        </li>
                          </ul>
                        </nav>''' % (self.base_url,pagenum))
        else:
            page_list.append('''<li>
                          <a href="%s?pagenum=%d" aria-label="Next">
                        <span aria-hidden="true">&raquo;</span>
                          </a>
                        </li>
                          </ul>
                        </nav>''' % (self.base_url,after_page))

        return ''.join(page_list)
    def page_str(self):
        return self.page_tackle()

