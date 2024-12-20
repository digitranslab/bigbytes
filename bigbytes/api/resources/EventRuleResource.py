from bigbytes.api.resources.GenericResource import GenericResource
from bigbytes.orchestration.db import safe_db_query


class EventRuleResource(GenericResource):
    @classmethod
    @safe_db_query
    def member(self, pk, user, **kwargs):
        rules = []

        if 'aws' == pk:
            from bigbytes.services.aws.events.events import get_all_event_rules

            try:
                rules = get_all_event_rules()
            except Exception as err:
                print(f'[WARNING] EventRuleResource.member: {err}')

        return self(dict(rules=rules), user, **kwargs)
