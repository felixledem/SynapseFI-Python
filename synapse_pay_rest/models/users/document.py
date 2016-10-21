

class Document():
    """Ancestor of PhysicalDocument, SocialDocument, and VirtualDocument.

    Stores common functionality of child classes, but should not be
    instantiated.
    """

    def __init__(self, **kwargs):
        for arg, value in kwargs.items():
            setattr(self, arg, value)

    @classmethod
    def payload_for_create(cls, type, value):
        """Convert the Document into its dict representation for API payload.
        """
        return {'document_value': value, 'document_type': type}

    @classmethod
    def from_response(cls, response):
        """Construct a Document from a response dict."""
        return cls(type=response['document_type'],
                   id=response['id'],
                   status=response['status'],
                   last_updated=response['last_updated'])

    @classmethod
    def multiple_from_response(cls, response):
        """Construct multiple Documents from a response dict."""
        base_docs = [cls.from_response(doc_data) for doc_data in response]
        return base_docs
