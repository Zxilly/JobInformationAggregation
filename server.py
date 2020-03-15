import requests
from flask import Flask, make_response, request

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

    course_list = get_course_list(main_session)

    course_work_list = get_course_work(main_session, course_list)

    all_work_info_tag_list = get_work_info(main_session, course_work_list)

    all_work_info_dict_list = parse_work(all_work_info_tag_list)

    print(all_work_info_dict_list)

    template = """
<div class="mdui-col-xs-12 mdui-col-sm-6 mdui-col-md-4 row_distant">
    <div class="mdui-card mdui-typo">
        <div class="mdui-card-media">
            <img src="img/card.jpg"/>
            <div class="mdui-card-media-covered">
                <div class="mdui-card-primary">
                    <div class="mdui-card-primary-title">{}</div>
                    <div class="mdui-card-primary-subtitle">{}</div>
                </div>
            </div>
        </div>
        <div class="mdui-card-content">
            <div class="mdui-chip">
                <span class="mdui-chip-title"><strong>开始时间:</strong></span>
            </div>
            <div class="mdui-chip left-set">
                <span class="mdui-chip-title">{}</span>
            </div>
            <br>
            <div class="mdui-chip">
                <span class="mdui-chip-title"><strong>截止时间:</strong></span>
            </div>
            <div class="mdui-chip left-set">
                <span class="mdui-chip-title">{}</span>
            </div>
        </div>
    </div>
</div>
    """
    return_content = ''
    for one in all_work_info_dict_list:
        render_one = template.format(one['workname'], one['coursename'], one['start'], one['end'])
        return_content += render_one
    return make_response(return_content)


if __name__ == '__main__':
    server.run(debug=False)
