import re


class SetStateMixin(object):
    def set_state(self, state, path, value, base_name=None):
        if base_name is not None:
            prefix = "{}.".format(base_name)

            if path.startswith(prefix):
                path = re.sub(r"^{}".format(prefix), "", path)

        bits = path.split(".")
        key = bits.pop()

        obj = state
        for bit in bits:
            if bit not in obj:
                obj[bit] = {}
            obj = obj[bit]
        obj[key] = value

        return obj
