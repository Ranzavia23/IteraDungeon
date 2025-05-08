class SceneManager:
    def __init__(self, game):
        self.game = game
        self.scene_stack = []
        self.scene = None

    def go_to(self, scene):
        self.scene = scene

    def push(self, scene):
        if self.scene:
            self.scene_stack.append(self.scene)
        self.scene = scene

    def pop(self):
        if self.scene_stack:
            self.scene = self.scene_stack.pop()

    def handle_events(self):
        if self.scene:
            self.scene.handle_events()

    def update(self):
        if self.scene:
            self.scene.update()

    def render(self):
        if self.scene:
            self.scene.render()
