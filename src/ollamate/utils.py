import os


def set_proxy(http=None, https=None, socks5=None):
    os.environ['HTTP_PROXY'] = http
    os.environ['HTTPS_PROXY'] = https
    os.environ['SOCKS5_PROXY'] = socks5