# -*- coding: utf-8 -*-
#判断网站来自mobile还是pc
import re
from django.http.response import Http404
import math
import datetime

def checkMobile(request):
    """
    demo :
        @app.route('/m')
        def is_from_mobile():
            if checkMobile(request):
                return 'mobile'
            else:
                return 'pc'
    :param request:
    :return:
    """
    try:
        userAgent = request.META["HTTP_USER_AGENT"]
        # userAgent = env.get('HTTP_USER_AGENT')

        _long_matches = r'googlebot-mobile|android|avantgo|blackberry|blazer|elaine|hiptop|ip(hone|od)|kindle|midp|mmp|mobile|o2|opera mini|palm( os)?|pda|plucker|pocket|psp|smartphone|symbian|treo|up\.(browser|link)|vodafone|wap|windows ce; (iemobile|ppc)|xiino|maemo|fennec'
        _long_matches = re.compile(_long_matches, re.IGNORECASE)
        _short_matches = r'1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|e\-|e\/|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(di|rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|xda(\-|2|g)|yas\-|your|zeto|zte\-'
        _short_matches = re.compile(_short_matches, re.IGNORECASE)

        if _long_matches.search(userAgent) != None:
            return True
        user_agent = userAgent[0:4]
        if _short_matches.search(user_agent) != None:
            return True
        return False
    except:
        return False


def safe_int(n, default=None):
    if n:
        try:
            n = int(n)
        except ValueError:
            n = default
    else:
        n = default
    return n

def paginater(page_index, page_size, rows_count, page_aroud):
    """
    分页器
    :param page_index: 当前页码(int)
    :param page_size: 每页条数(int)
    :param rows_count: 总条数(int)
    :param page_aroud: 页数处于中间时,前后分别围绕的页数(int)
    :return:
        page_count_list([str, ...], 页码list)
        page_index(str, 当前页面)
        start_index(int, 开始条数)
        end_index(int, 结束条数+1)
    """
    try:
        page_index, page_size, rows_count, page_aroud = \
            map(abs, map(int, [page_index, page_size, rows_count, page_aroud]))
    except ValueError:
        raise Http404
    page_count = int(math.ceil(rows_count / float(page_size)))
    start_index = (page_index - 1) * page_size
    end_index = start_index + page_size
    page_count_list = range(1, page_count + 1)

    if (page_index != 1) and (page_index not in page_count_list):
        raise Http404

    page_arouds = page_aroud * 2

    if page_count == 1:
        page_count_list = []
    elif page_count > page_arouds + 2:
        front_pages_list = [1, '...']
        back_pages_list = ['...', page_count]
        if page_index < page_arouds:
            page_count_list = range(1, page_arouds + 2) + back_pages_list
        elif page_index > page_count - (page_arouds - 1):
            page_count_list = front_pages_list + range(page_count - page_arouds, page_count + 1)
        else:
            if page_index == page_arouds:
                front_pages_list = [1]
            elif page_index == page_count - (page_arouds - 1):
                back_pages_list = [page_count]
            page_count_list = \
                front_pages_list + range(page_index - page_aroud, page_index + page_aroud + 1) + back_pages_list
    page_count_list = map(str, page_count_list)
    page_index = str(page_index)

    return page_count_list, page_index, start_index, end_index

def reformat_datetime_from_cache(date_str):
    """
    @brief 格式化从缓存取出的datetime字符串到datetime类型
    :param date_str:
    :return:
    """
    if isinstance(date_str, datetime.datetime):
        return date_str
    assert isinstance(date_str, (str, unicode))  # 如果不是datetime.datetime类型,则必须是字符串
    return datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
