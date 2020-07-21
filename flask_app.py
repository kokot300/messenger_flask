#!/usr/bin/python

from flask import Flask, render_template, request
import users as u
import messages as m

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def talk_to_me():
    if request.method == 'GET':
        return render_template('talk_to_me.html')
    else:
        msg = ''
        m_user = request.form.get('m_user')
        m_secret = request.form.get('m_secret')
        guy = request.form.get('guy')
        message = request.form.get('message')
        m_list = request.form.get('m_list')

        user = request.form.get('user')
        secret = request.form.get('secret')
        new_password = request.form.get('new_password')
        listing = request.form.get('list')
        delete = request.form.get('deletion')

        print(m_user, m_secret, guy, message, m_list)
        print(user, secret, new_password, listing, delete)

        if delete == 'yes':
            u.delete_user(user, secret)
        if listing == 'yes':
            u.list_users()
        if m_list == 'yes':
            m.list_messages(m_user, m_secret)
        if message is not None:
            m.send_message(m_user, m_secret, guy, message)
        if user is not None:
            u.create_user(user, secret)
        if new_password is not None:
            u.edit_user(user, secret, new_password)

        return render_template('talk_to_me.html', msg=msg)


if __name__ == '__main__':
    app.run(debug=True)
