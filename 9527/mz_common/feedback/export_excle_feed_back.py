# -*-coding:utf8-*-
from utils.excel_tool import ExcelExport


FEED_TYPE_NAME = (u"bug", u"功能建议", u"交互体验", u"吐个槽", u"表个扬", u"课程建议")
def draw_feed_back_data(feed_back_list):
    '''
    填充用户反馈表格的数据
    :param feed_back_list:
    :return:
    '''
    data = list()
    if feed_back_list:
        for feed in feed_back_list:
            row = [feed['id'], feed['nick_name'], FEED_TYPE_NAME[int(feed["feed_type"])], feed['content'], feed['publish_date'].strftime("%Y-%m-%d %H:%M:%S"),
                   feed['contact'], feed['current_url'], feed['record']]
            data.append(row)
    return data


def excle_export(feed_back_list):
    '''
    设置excel的标题和内容，并保存为字节流的方式
    :param feed_back_list:
    :return:
    '''
    ex = ExcelExport()
    title = (u'ID', u'用户昵称', u'反馈类型', u'内容描述', u'反馈时间', u'联系方式', u'反馈URL', u'反馈记录')
    ex.set_excel(titles=title, values=draw_feed_back_data(feed_back_list))
    return ex.write_bio()
