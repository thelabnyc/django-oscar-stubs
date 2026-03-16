from oscar.forms.widgets import MultipleRemoteSelect, RemoteSelect

class ProductSelect(RemoteSelect):
    lookup_url: str

class ProductSelectMultiple(MultipleRemoteSelect):
    lookup_url: str
