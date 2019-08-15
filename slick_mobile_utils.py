def is_localhost(url):
    if "localhost" in url or "127.0.0.1" in url:
        return True


def get_epoch_time():
    import time
    int(round(time.time() * 1000))


def run_local(command, detatch=False, shell=True, raise_assertion=False, value=False):
    from subprocess import call, check_output
    if detatch:
        command = "{} > /dev/null 2>&1 &".format(command)

    print(command)
    if not value:
        ret_code = call(command, shell=shell) == 0

        if raise_assertion and not ret_code:
            raise Exception("Command failed: {}".format(command))

        return ret_code

    else:
        return check_output(command, shell=shell)


def is_truthy(value):
    """
    If value is true then it returns a Boolean of True, else False
    If value is None, return False
    :param value: str
    :return:
    """
    if value is None:
        return False

    return value.lower() in ('yes', 'true', 't', 'y', '1')


def string_to_dict(extra_vars):
    """

    :return: dict[str, str] {'foo': 'bar', 'key2': 'value2'}
    """
    var_dict = {}
    if extra_vars:
        for var in extra_vars:
            items = var.split('=')
            if 1 < len(items) < 3:
                key = items[0].strip()
                value = items[1]
                var_dict[key] = value
    return var_dict