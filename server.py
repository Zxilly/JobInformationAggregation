import requests
from flask import Flask, make_response, request

import mobile_func
from func import *

server = Flask('server')
# CORS(server, supports_credentials=True)
headers = {
    "User-Agent": "Mozilla/5.0 (iPad; CPU OS 13_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) "
                  "Mobile/15E148 ChaoXingStudy/ChaoXingStudy_3_4.3.2_ios_phone_201911291130_27 ("
                  "@Kalimdor)_11391565702936108810 "
}


@server.route('/ajax/logincode')
def logincode():
    main_session = requests.session()
    uuid = request.cookies.get('uuid')
    # uuid = 'e3984b0c-e468-43aa-9b5e-a368c1911e89'  # TODO:production记得换回来
    pic_base64, main_session, polling_url = login(conv=main_session, user_uuid=uuid, server=True)
    user_dat = {'session': main_session.cookies.get_dict(), 'polling': polling_url, 'uuid': uuid, 'time': time.time()}
    file_path = str('data/' + str(uuid) + '.dat')
    print(file_path)
    with open(file_path, 'w+') as f:
        f.write(json.dumps(user_dat))

    res = make_response(pic_base64)
    return res


@server.route('/ajax/loginstatus')
def loginstatus():
    main_session = requests.session()
    uuid = request.cookies.get('uuid')  # TODO:production记得换回来
    # uuid = 'e3984b0c-e468-43aa-9b5e-a368c1911e89'
    file_path = str('data/' + str(uuid) + '.dat')
    with open(file_path, 'r+') as f:
        user_dat = json.loads(f.read())
    main_session.cookies.update(user_dat['session'])
    main_session.keep_alive = False
    login_rec_json = main_session.post(str(user_dat['polling']), headers=headers)
    login_rec_dict = json.loads(login_rec_json.content)
    if login_rec_dict['status']:
        user_dat['session'] = main_session.cookies.get_dict()
        user_dat['time'] = time.time()
        with open(file_path, 'w+') as f:
            f.write(json.dumps(user_dat))
        return '1'
    else:

        return '0'


@server.route('/ajax/userstatus')  # 判断session是否过期
def userstatus():
    uuid = request.cookies.get('uuid')  # TODO:production记得换回来
    # uuid = 'e3984b0c-e468-43aa-9b5e-a368c1911e89'
    file_path = str('data/' + str(uuid) + '.dat')
    with open(file_path, 'r+') as f:
        user_dat = json.loads(f.read())
    session_time = user_dat['time']
    if ((time.time() - session_time) > 2160000):
        return '0'  # session过期
    # main_session.cookies.update(user_dat['session'])
    else:
        return '1'  # session有效


@server.route('/ajax/workinfo')
def workinfo():
    main_session = requests.session()
    uuid = request.cookies.get('uuid')  # TODO:production记得换回来
    # uuid = 'e3984b0c-e468-43aa-9b5e-a368c1911e89'
    file_path = str('data/' + str(uuid) + '.dat')
    with open(file_path, 'r+') as f:
        user_dat = json.loads(f.read())
    main_session.cookies.update(user_dat['session'])
    main_session.keep_alive = False
    """
    course_list = get_course_list(main_session)

    course_work_list = get_course_work(main_session, course_list)

    all_work_info_tag_list = get_work_info(main_session, course_work_list)

    all_work_info_dict_list = parse_work(all_work_info_tag_list)

    print(all_work_info_dict_list)
    """

    course_info = mobile_func.get_course(main_session)
    all_work_info_dict_list = mobile_func.get_work(main_session, course_info)

    template = r'<div class="mdui-col-xs-12 mdui-col-sm-6 mdui-col-md-4 row_distant"><div class="mdui-card mdui-typo"><div class="mdui-card-media"><img src="img/card.jpg"/><div class="mdui-card-media-covered"><div class="mdui-card-primary"><div class="mdui-card-primary-title">{}</div><div class="mdui-card-primary-subtitle">{}</div></div></div></div><div class="mdui-card-content"><div class="mdui-chip"><span class="mdui-chip-icon"><i class="mdui-icon material-icons">timelapse</i></span><span class="mdui-chip-title">{}</span></div><div class="mdui-float-right"><a class="mdui-btn mdui-ripple" href="{}" target="_blank">做作业</a></div></div></div></div>'
    return_content = ''
    for one in all_work_info_dict_list:
        render_one = template.format(one['work_name'], one['course_name'], one['left_time'], one['work_url'])
        return_content += render_one
    if len(return_content)==0:
        return_content += r'<div class="mdui-typo-display-4-opacity mdui-center mdui-text-center nowork">无作业</div>'
    return make_response(return_content)


if __name__ == '__main__':
    server.run(debug=False)
