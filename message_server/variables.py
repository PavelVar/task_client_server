"""
Module contains names and message for MessengerServer class.
"""

database_name = 'DataBase_for_task_3.db'

table_name = 'clients_logs_and_passwords'

port_num = 11111

arg_for_socket_listen = 10

proper_incoming_data = ('-reg', '-log')

start_message = 'Server message:\n' \
                'Input "-reg" to start registration.\n' \
                'Input "-log" to start login.\n' \
                'Input "-exit" to close session. >>>'

enter_login_message = 'Please input your login >>>'

enter_password_message = 'Please input your password >>>'

error_log_message = 'This login is used by somebody else or wrong. Please try to input another one >>>'

success_register_message = 'Congratulations! You have registered. Now input "-log" to login >>>'

error_password_message = 'Wrong password. Please try to input one more time. >>>'

success_login_message = 'Congratulations! You have logged in. >>>'

messages_option = 'There are next possibilities for you here: \n' \
                  'input "-2all <text>" - to send message to all clients online;\n' \
                  'input "-show" - to see who is online;\n'\
                  'input "-username <text>" - to send message to special client. >>>'

mistake = f'Wrong input. Try one more time. {messages_option}. >>>'

close_message = ''
