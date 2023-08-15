# -*- coding: utf-8 -*-
''' My AWS Tools '''
import csv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from uuid import uuid4

import setting

import arrow
import boto3
import requests
from jinja2 import Environment
from jinja2 import FileSystemLoader


TPLENV = Environment(loader=FileSystemLoader('./tpl'))


class AwsSESTools(object):
    ''' AWS SES tools

        :param str aws_access_key_id: aws_access_key_id
        :param str aws_secret_access_key: aws_secret_access_key

        .. todo::
           - Add integrated with jinja2 template.

    '''
    def __init__(self, aws_access_key_id, aws_secret_access_key):
        ''' Make a connect '''
        self.client = boto3.client(
                'ses',
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                region_name='us-east-1')

    @staticmethod
    def mail_header(name, mail):
        ''' Encode header to base64

            :param str name: user name
            :param str mail: user mail
            :rtype: string
            :returns: a string of "name <mail>" in base64.
        '''
        return formataddr((name, mail))

    def send_email(self, *args, **kwargs):
        ''' Send email

            seealso `send_email` in :class:`boto.ses.connection.SESConnection`
        '''
        return self.client.send_email(*args, **kwargs)

    def send_raw_email(self, **kwargs):
        ''' still in dev

        :param str source: from
        :param str to_addresses: to
        :param str subject: subject
        :param str body: body

        '''
        msg_all = MIMEMultipart()
        msg_all['From'] = kwargs['source']
        msg_all['To'] = kwargs['to_addresses']
        msg_all['Subject'] = kwargs['subject']
        msg_all['X-Github'] = 'toomore/COSCUP2013Secretary-Toolkit'

        msg_all.attach(MIMEText(kwargs['body'], 'html', 'utf-8'))

        #return self.client.send_raw_email(
        #        RawMessage={'Data': msg_all.as_string()})
        return msg_all.as_string()

MAIL_SOURCE = AwsSESTools.mail_header(u'OSCVPass 開源貢獻者快速通關', 'oscvpass@ocf.tw')
SENDER = AwsSESTools(setting.AWSID, setting.AWSKEY)

def make_raw_email(nickname, mail, subject, body, dry_run=True):
    if dry_run:
        mail = setting.TESTMAIL

    raw = SENDER.send_raw_email(
        source=MAIL_SOURCE,
        to_addresses=AwsSESTools.mail_header(nickname, mail),
        subject=subject,
        body=body,
    )
    return raw


def process_csv(path, _all=False):
    data = {
        'deny': [],
        'insufficient_for': [],
        'pass': [],
    }

    with open(path, 'r+') as files:
        csv_reader = csv.DictReader(files)
        for r in csv_reader:
            if not _all:
                if r['send'] != '':
                    continue

            if r['status'] == '拒絕':
                data['deny'].append(r)
            elif r['status'] == '補件':
                data['insufficient_for'].append(r)
            elif r['status'] == '通過':
                if r['start_date']:
                    r['expiration_date'] = arrow.get(r['start_date']).shift(years=1).format('YYYY-MM-DD')

                data['pass'].append(r)

    _fields = {
        'c_01': u'開放原始碼專案或活動名稱 / Open Source Project or Event Name',
        'c_02': u'開放原始碼專案 Repo 位置 / Open Source Project Repo',
        'c_03': u'其他有效證明 / Other Valid Proof ',
        'c_04': u'開放原始碼專案或活動說明 / Description of Open Source Project or Event ',
    }

    # ----- filter data ----- #
    for case in data:
        for r in data[case]:
            r['mail'] = r['mail'].strip()
            if len(r['nickname'].strip()) == 0:
                r['nickname'] = r['name'].strip()
            else:
                r['nickname'] = r['nickname'].strip()

            _doc = []
            for _f in ('c_01', 'c_02', 'c_03', 'c_04'):
                _doc.append('%s：' % _fields[_f])
                _doc.append('  %s' % r[_f])

            r['doc'] = '\r\n'.join(_doc)

    return data

def send(data, case, dry_run=True):
    ''' send mail

    :param dict data: include ``pass``, ``deny``, ``insufficient_for`` list data.
    :param tuple case: pass, deny, insufficient_for
    :param bool dry_run: Test mail

    '''
    if 'deny' in case:
        template = TPLENV.get_template('./deny.html')
        for r in data['deny']:
            r ['mail'] = r['mail'].strip().lower()
            if r['mail'] in setting.BLOCK:
                continue

            print('deny', r['mail'])
            body = template.render(**r)
            raw = make_raw_email(
                nickname=r['nickname'],
                mail=r['mail'],
                subject=u'[OSCVPass] Result: Deny (%s)' % r['nickname'],
                body=body,
                dry_run=dry_run,
            )
            if dry_run:
                continue

            SENDER.client.send_raw_email(RawMessage={'Data': raw})

    if 'insufficient_for' in case:
        template = TPLENV.get_template('./insufficient_for.html')
        for r in data['insufficient_for']:
            r ['mail'] = r['mail'].strip().lower()
            if r['mail'] in setting.BLOCK:
                continue

            print('insufficient_for', r['mail'])
            body = template.render(**r)
            raw = make_raw_email(
                nickname=r['nickname'],
                mail=r['mail'],
                subject=u'[OSCVPass] Result: Insufficient (%s)' % r['nickname'],
                body=body,
                dry_run=dry_run,
            )
            if dry_run:
                continue

            SENDER.client.send_raw_email(RawMessage={'Data': raw})

    if 'pass' in case:
        template = TPLENV.get_template('./pass.html')
        for r in data['pass']:
            r ['mail'] = r['mail'].strip().lower()
            if r['mail'] in setting.BLOCK:
                continue

            print('pass', r['mail'])
            body = template.render(**r)
            raw = make_raw_email(
                nickname=r['nickname'],
                mail=r['mail'],
                subject=u'[OSCVPass] Result: Pass (%s)' % r['nickname'],
                body=body,
                dry_run=dry_run,
            )
            if dry_run:
                continue

            SENDER.client.send_raw_email(RawMessage={'Data': raw})

def send_request_attendee(path, dry_run=True):
    with open(path, 'r') as files:
        csv_reader = csv.DictReader(files)

        template = TPLENV.get_template('./action_sitcon.html')
        for u in csv_reader:
            print(u)
            body = template.render(**u)
            raw = make_raw_email(
                nickname=u['name'],
                mail=u['mail'],
                subject=u'[OSCVPass] [提醒] 登記索取 SITCON (%s)' % u['name'],
                body=body,
                dry_run=dry_run,
            )
            SENDER.client.send_raw_email(RawMessage={'Data': raw})

def send_coscup_lpi(rows, dry_run=True):
    template = TPLENV.get_template('./lpi_token.html')
    _n = 1
    for u in rows:
        print(_n, u)
        _n += 1

        body = template.render(**u)
        raw = make_raw_email(
            nickname=u['name'],
            mail=u['mail'],
            subject=u'[OSCVPass] [提醒] 登記索取 LPI Exam 折扣券 (%s)' % u['name'],
            body=body,
            dry_run=dry_run,
        )
        SENDER.client.send_raw_email(RawMessage={'Data': raw})

        if dry_run:
            return

def send_mopcon_token(rows, dry_run=True):
    template = TPLENV.get_template('./mopcon_token.html')
    _n = 1
    for u in rows:
        if u['mail'] in setting.BLOCK:
            continue

        print(_n, u)
        _n += 1

        if dry_run:
            u['mail'] = setting.TESTMAIL

        body = template.render(**u)
        raw = make_raw_email(
            nickname=u['name'],
            mail=u['mail'],
            subject=u'[OSCVPass][提醒] MOPCON2022 開源貢獻票 免費券 (%s)' % u['name'],
            body=body,
            dry_run=dry_run,
        )
        SENDER.client.send_raw_email(RawMessage={'Data': raw})

        if dry_run:
            return

def send_g0v_token(rows, dry_run=True):
    template = TPLENV.get_template('./g0v_summit_token.html')
    _n = 1
    for u in rows:
        if u['mail'] in setting.BLOCK:
            continue

        print(_n, u)
        _n += 1

        if dry_run:
            u['mail'] = setting.TESTMAIL

        body = template.render(**u)
        raw = make_raw_email(
            nickname=u['name'],
            mail=u['mail'],
            subject=u'[OSCVPass][提醒] g0v Summit 2020 開源貢獻票 優惠券 (%s)' % u['name'],
            body=body,
            dry_run=dry_run,
        )
        SENDER.client.send_raw_email(RawMessage={'Data': raw})

        if dry_run:
            return

def send_sitcon_token(rows, dry_run=True):
    template = TPLENV.get_template('./sitcon_2022_token.html')
    _n = 1
    for u in rows:
        if u['mail'] in setting.BLOCK:
            continue

        print(_n, u)
        _n += 1

        if dry_run:
            u['mail'] = setting.TESTMAIL

        body = template.render(**u)
        raw = make_raw_email(
            nickname=u['name'],
            mail=u['mail'],
            subject=u'[OSCVPass][提醒] SITCON 2022 開源貢獻票 優惠券 (%s)' % u['name'],
            body=body,
            dry_run=dry_run,
        )
        SENDER.client.send_raw_email(RawMessage={'Data': raw})

        if dry_run:
            return

def send_pycon_token(rows, dry_run=True):
    template = TPLENV.get_template('./2023_coscup_pycon_hitcon.html')
    _n = 1
    for u in rows:
        if u['mail'] in setting.BLOCK:
            continue

        print(_n, u)
        _n += 1

        if dry_run:
            u['mail'] = setting.TESTMAIL

        body = template.render(**u)
        raw = make_raw_email(
            nickname=u['name'],
            mail=u['mail'],
            subject=u'[OSCVPass][提醒] PyConTW 2023 (%s)' % u['name'],
            body=body,
            dry_run=dry_run,
        )
        SENDER.client.send_raw_email(RawMessage={'Data': raw})

        if dry_run:
            return

def send_lv_token(rows, dry_run=True):
    template = TPLENV.get_template('./lv_2023_token.html')
    _n = 1
    for u in rows:
        if u['mail'] in setting.BLOCK:
            continue

        print(_n, u)
        _n += 1

        if dry_run:
            u['mail'] = setting.TESTMAIL

        body = template.render(**u)
        raw = make_raw_email(
            nickname=u['name'],
            mail=u['mail'],
            subject=u'[再提醒] [OSCVPass] Laravel x Vue Conf Taiwan 2023 優惠券 (%s)' % u['name'],
            body=body,
            dry_run=dry_run,
        )
        SENDER.client.send_raw_email(RawMessage={'Data': raw})

        if dry_run:
            return

def send_coscup_check(rows, dry_run=True):
    template = TPLENV.get_template('./coscup_2021.html')
    _n = 1
    for u in rows:
        if u['mail'] in setting.BLOCK:
            continue

        print(_n, u)
        _n += 1

        if dry_run:
            u['mail'] = setting.TESTMAIL

        body = template.render(**u)
        raw = make_raw_email(
            nickname=u['name'],
            mail=u['mail'],
            subject=u'[OSCVPass] COSCUP x RubyConfTW 2021 開源貢獻回饋調查 (%s)' % u['name'],
            body=body,
            dry_run=dry_run,
        )
        SENDER.client.send_raw_email(RawMessage={'Data': raw})

        if dry_run:
            return

def pickup_unique(data, cases):
    maillist = []
    unique = set()
    for case in cases:
        for row in data[case]:
            if row['mail'].strip() == '':
                row['mail'] = row['mail2']

            row['mail'] = ','.join(row['mail'].split(' '))
            row['mail'] = ','.join(row['mail'].split('/'))
            row['mail'] = [m.strip() for m in row['mail'].split(',') if m][0].lower()

            if row['mail'] in unique or '@' not in row['mail']:
                continue

            maillist.append({'name': row['name'], 'mail': row['mail']})
            unique.add(row['mail'])

            print(row['name'], row['mail'])

    return maillist

def add_uuid_export_csv(datas, path):
    with open(path, 'w+') as files:
        csv_writer = csv.DictWriter(files, fieldnames=('name', 'mail', 'uuid'))
        csv_writer.writeheader()
        for data in datas:
            data['uuid'] = ('%0.8x' % uuid4().fields[0]).upper()
            csv_writer.writerow(data)

def gen_token(nums, out_path):
    tokens = set()
    while len(tokens) < nums:
        tokens.add(('%0.8x' % uuid4().fields[0]).upper())

    with open(out_path, 'w+') as files:
        csv_writer = csv.writer(files, csv.QUOTE_ALL)
        csv_writer.writerow(('token', ))
        for token in tokens:
            csv_writer.writerow((token, ))

def merge_token(datas, token_path, out_path):
    with open(token_path, 'r+') as files:
        tokens = list(csv.DictReader(files))

    _n = 0
    for user in datas:
        tokens[_n].update(user)
        _n += 1

    with open(out_path, 'w+') as files:
        csv_writer = csv.DictWriter(files, fieldnames=list(tokens[0].keys()), quoting=csv.QUOTE_NONNUMERIC)
        csv_writer.writeheader()
        csv_writer.writerows(tokens)

def update_token(datas, org_path, out_path):
    with open(org_path, 'r+') as files:
        mails = list(csv.DictReader(files))

    added = {i['mail'] for i in mails}
    for data in datas:
        if data['mail'] in added:
            continue

        added.add(data['mail'])

        for mail in mails:
            if not mail['mail']:
                mail['name'] = data['name']
                mail['mail'] = data['mail']
                break

    with open(out_path, 'w+') as files:
        csv_writer = csv.DictWriter(files, fieldnames=('mail', 'name', 'token', 'check'), quoting=csv.QUOTE_NONNUMERIC)
        csv_writer.writeheader()
        csv_writer.writerows(mails)

    print(mails)

def send_expired(path, dry_run=True):
    ''' Send expired '''
    template = TPLENV.get_template('./expired.html')
    _n = 1

    with open(path) as files:
        for u in csv.DictReader(files):
            print(_n, u)
            _n += 1

            _date = arrow.get(u['date'])
            u['date'] = _date.format('YYYY-MM-DD')

            if _date >= arrow.now():
                u['say_expired'] = '即將'
            else:
                u['say_expired'] = '已'

            body = template.render(**u)

            if dry_run:
                u['mail'] = setting.TESTMAIL

            raw = make_raw_email(
                nickname=u['nickname'],
                mail=u['mail'],
                subject=f"[OSCVPass] [提醒] {u['say_expired']}到期！({u['nickname']})",
                body=body,
                dry_run=dry_run,
            )
            SENDER.client.send_raw_email(RawMessage={'Data': raw})

            if dry_run:
                return

def send_workshop(path, dry_run=True):
    ''' send workshop '''
    template = TPLENV.get_template('./2022_workshop.html')


    datas = {}
    with open(path) as files:
        for u in csv.DictReader(files):

            u['mail'] = u['mail'].strip().lower()
            if not u['mail']:
                u['mail'] = u['mail2'].strip().lower()

            if u['mail'] not in datas:
                datas[u['mail']] = {'nickname': u['nickname'], 'mail': u['mail']}

    _n = 1
    for mail in datas:
        u = datas[mail]
        body = template.render(**u)

        if dry_run:
            u['mail'] = setting.TESTMAIL

        raw = make_raw_email(
            nickname=u['nickname'].strip(),
            mail=u['mail'].strip().lower(),
            subject='[OSCVPass] WorkShop 活動：OSCVPass x SITCON Workshop 開源專案及貢獻者招募，截止日期 2022/8/22',
            body=body,
            dry_run=dry_run,
        )
        print(SENDER.client.send_raw_email(RawMessage={'Data': raw}))
        print(_n, u['nickname'], u['mail'])
        _n += 1

        if dry_run:
            return

def send_2022_report(path, dry_run=True):
    ''' send 2022 report '''
    template = TPLENV.get_template('./2022_year_end.html')


    datas = []
    with open(path) as files:
        for u in csv.DictReader(files):
            datas.append(u)

    _n = 1
    for u in datas:
        body = template.render(**u)

        if dry_run:
            u['mail'] = setting.TESTMAIL

        raw = make_raw_email(
            nickname=u['name'].strip(),
            mail=u['mail'].strip().lower(),
            subject='[OSCVPass] 2022 年度總結',
            body=body,
            dry_run=dry_run,
        )
        print(SENDER.client.send_raw_email(RawMessage={'Data': raw}))
        print(_n, u['name'], u['mail'])
        _n += 1

        if dry_run:
            return

def read_all_mails(path):
    ''' Read all mails '''
    data = process_csv(path, _all=True)
    mails = {}
    for case in data:
        print(case, len(data[case]))
        for row in data[case]:
            print(row['name'], row['mail'], row['mail2'])

            if row['mail2']:
                _mail = format_mail(row['mail2'])
                if _mail:
                    if _mail not in mails:
                        mails[_mail] = set()

                    mails[_mail].add(row['name'].strip())

            elif row['mail']:
                _mail = format_mail(row['mail'])
                if _mail:
                    if _mail not in mails:
                        mails[_mail] = set()

                mails[_mail].add(row['name'].strip())

    with open('./all_users_221215.csv', 'w+', encoding='UTF8') as files:
        csv_writer = csv.DictWriter(files, fieldnames=('name', 'mail'))
        csv_writer.writeheader()

        for key, value in mails.items():
            csv_writer.writerow({'name': ', '.join(value), 'mail': key})


def format_mail(mail):
    ''' format_mail '''
    mail = mail.strip()

    if ',' in mail:
        mail = mail.split(',')[0].strip()

    if ' ' in mail:
        mail = mail.split(' ')[0].strip()

    if '@' not in mail:
        return ''

    return mail

if __name__ == '__main__':
    # ----- send Pass/deny ----- #
    #from pprint import pprint
    #data = process_csv('./oscvpass_230807_sendpass.csv', _all=False)
    #for case in data:
    #    print(case, len(data[case]))
    #    for row in data[case]:
    #        print(row['name'], row['c_01'], row['mail'], row['mail2'])

    #pprint(data['deny'])
    #send(data=data, case=('deny', 'insufficient_for', 'pass'), dry_run=False)
    #send_request_attendee('/run/shm/hash_b0466044.csv', dry_run=True)

    # ----- send get token ----- #
    #data = process_csv('./oscvpass_210714_only_w_date.csv', _all=True)
    #maillist = pickup_unique(data=data, cases=('pass', ))
    #        datas=maillist, token_path='./mopcon_2020_token.csv', out_path='./mopcon_2020_token_mails.csv')
    #send_coscup_lpi(rows=maillist, dry_run=False)

    # ----- export uuid csv ----- #
    #add_uuid_export_csv(maillist, './pycon2021_tokens.csv')

    # ----- send mopcon token ----- #
    #with open('./mopcon_2022_tokens_mails_221007.csv', 'r+') as files:
    #    rows = []
    #    for user in csv.DictReader(files):
    #        if not user['mail']:
    #            continue
    #        rows.append(user)

    #    send_mopcon_token(rows=rows, dry_run=False)

    # ----- g0v Summit ----- #
    #data = process_csv('./oscvpass_200930.csv', _all=True)
    #maillist = pickup_unique(data=data, cases=('pass', ))
    #print(maillist, len(maillist))
    #merge_token(
    #        datas=maillist, token_path='./g0v_summit_token.csv', out_path='./g0v_summit_token_mails.csv')

    # ----- send g0v token ----- #
    #with open('./g0v_summit_token_mails_201124_min.csv', 'r+') as files:
    #    rows = []
    #    for user in csv.DictReader(files):
    #        if not user['mail']:
    #            continue
    #        rows.append(user)

    #    send_g0v_token(rows=rows, dry_run=False)

    # ----- update token ----- #
    #data = process_csv('./oscvpass_230807.csv', _all=True)
    #maillist = pickup_unique(data=data, cases=('pass', ))
    #print(maillist, len(maillist))

    #update_token(datas=maillist,
    #        org_path='./lv_taiwan_2023_token_mails_230725.csv',
    #        out_path='./lv_taiwan_2023_token_mails_230807.csv')

    #send_expired(path='./oscvpass_expired_220512.csv', dry_run=True)

    # ----- Gen tokens ----- #
    #gen_token(nums=300, out_path="./pycon_2023_tokens.csv")
    #data = process_csv('./oscvpass_221101_w.csv', _all=True)
    #data = {'pass': []}
    #maillist = pickup_unique(data=data, cases=('pass', ))
    #print(maillist, len(maillist))
    #merge_token(
    #        datas=maillist,
    #        token_path='./lv_taiwan_2022_token.csv',
    #        out_path='./lv_taiwan_2022_tokens_mails.csv')

    # ----- send SITCON2022 token ----- #
    #with open('./sitcon_2022_tokens_mails_220725_append.csv', 'r+') as files:
    #    rows = []
    #    for user in csv.DictReader(files):
    #        if not user['mail']:
    #            continue
    #        rows.append(user)

    #    send_sitcon_token(rows=rows, dry_run=True)

    # ----- send PyConTaiwan2023 token ----- #
    #with open('./pycon_2023_tokens_mails_230807.csv', 'r+') as files:
    #    rows = []
    #    for user in csv.DictReader(files):
    #        if not user['mail']:
    #            continue

    #        rows.append(user)

    #    send_pycon_token(rows=rows, dry_run=True)

    # ----- send Laravel x Vue Taiwan 2023 token ----- #
    #with open('./lv_taiwan_2023_token_mails_230807.csv', 'r+') as files:
    #    rows = []
    #    for user in csv.DictReader(files):
    #        if not user['mail']:
    #            continue
    #        rows.append(user)

    #    send_lv_token(rows=rows, dry_run=True)

    # ----- send COSCUP2021 check ----- #
    #with open('./oscvpass-check_yker8xb2.csv', 'r+') as files:
    #    rows = []
    #    for user in csv.DictReader(files):
    #        rows.append(user)

    #    send_coscup_check(rows=rows, dry_run=False)

    # ----- send 2022 workshop ----- #
    #send_workshop('./oscvpass_220811_valid.csv', dry_run=True)

    #read_all_mails(path='./oscvpass_all_221215.csv')
    #send_2022_report(path='all_users_221215.csv', dry_run=True)

    pass

