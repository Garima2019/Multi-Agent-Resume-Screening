class StreamlitCallback:
    def __init__(self, container):
        self.container = container
        self.logs = ""

    def __call__(self, message):
        if not self.container:
            return
        self.logs += f"\n{message}"
        self.container.markdown(self.logs)
