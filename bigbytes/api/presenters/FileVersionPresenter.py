from bigbytes.api.presenters.BasePresenter import BasePresenter


class FileVersionPresenter(BasePresenter):
    default_attributes = [
        'modified_timestamp',
        'name',
        'path',
        'size',
    ]

    def present(self, **kwargs):
        return self.model.to_dict()
