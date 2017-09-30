from datetime import date, datetime

class BaseRule:
    # Test to see if the tx matches this rule
    # Only one rule will apply to each tx -- the last one in the array
    # This way we have Cascading Rules, and can write generic ones up top and override them with specifics below
    def matches(self, tx) -> bool:
        pass



class MiningIncome(BaseRule):
    def matches(self, tx) -> bool:
        # Date format: "created_at": "2017-06-02T15:13:58Z",
        dateStrFormat = "%Y-%m-%dT%H:%M:%SZ"
        minDate = datetime.strptime("2013-09-05T01:35:56Z", dateStrFormat)
        maxDate = datetime.strptime("2014-11-03T18:41:58Z", dateStrFormat)
        created = datetime.strptime(tx['created_at'], dateStrFormat)
        return tx["type"] == "send" and created >= minDate and created < maxDate

    def evaluate(self, tx):
        pass