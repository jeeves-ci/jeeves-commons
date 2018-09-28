
class BaseStorage(object):

    def __init__(self, session):
        self.db_session = session

    def build_query(self, type, **kwargs):
        query_fields = {}
        query = self.db_session.query(type)
        for field, field_val in kwargs.iteritems():
            if field_val:
                query_fields[field] = field_val

        return query.filter_by(**query_fields)

    def _get(self, cls_type, **kwargs):
        query = self.build_query(cls_type, **kwargs)
        item = query.first()
        # refresh item to allow polling
        if item:
            self.db_session.refresh(item)
        return item

    def _list(self,
              cls_type,
              page=1,
              size=10,
              order_by=None,
              pattern=None,
              **kwargs):
        query = self.build_query(cls_type, **kwargs)
        total = query.count()
        if order_by:
            query = query.order_by(order_by.replace(',', ' '))
        if pattern:
            query = query.filter(cls_type.name.like('%{}%'.format(pattern)))
        query = query.offset(page).limit(size)
        items = query.all()
        return items, total

    def _create(self, cls_type, **kwargs):
        item = cls_type(**kwargs)
        self.db_session.add(item)
        self.db_session.flush()
        return item
