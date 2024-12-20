from bigbytes.api.presenters.BasePresenter import BasePresenter


class GitFilePresenter(BasePresenter):
    default_attributes = [
        'content',
        'content_from_base',
        'content_from_compare',
        'error',
        'filename',
        'modified',
    ]
