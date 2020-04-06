class AutoComp:
    def __init__(self, starters: list):
        """
        The env could be one (1) or more.
        Our job would be to watch and update the automcomplete KEYWORDS
        """

        self.keywords = starters

    def updateEnv(self, env: object):
        envs = [env.values, env.statics]
        for env in envs:
            self.update(env)

    def update(self, env):
        for word in env:
            self.keywords.append(word)

    def completer(self, text, state):
        options = [x for x in self.keywords if x.startswith(text)]

        try:
            return options[state]

        except IndexError:
            return None


def completer(text, state):
    options = [x for x in Keywords if x.startswith(text)]

    try:
        return options[state]

    except IndexError:
        return None
