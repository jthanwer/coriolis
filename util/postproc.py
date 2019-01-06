def exit_app(mw):
    print('Closing the application')
    clear_all()


def clear_all():
    all_vars = [var for var in globals() if var[0] != '_']
    for var in all_vars:
        del globals()[var]
    print('Cache memory erased')
