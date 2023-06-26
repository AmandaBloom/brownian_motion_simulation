import numpy as np
import time
from threading import Lock

FREQUENCY = 50  # Hertz
MOLE_MASS = 1
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700


class LevyPhysics:
    def __init__(self) -> None:
        self.iter = 0
        self.LevyPositions = [(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)]
        self.alpha = 1.5
        self.stepSize = 5

        self.fps = 0
        self.fps_iter = 0
        self.start_time = time.time()

    def doIter(self) -> None:
        self.iter += 1
        self.fps_iter += 1

        # calculate position
        step = self.stepSize * (
            np.random.randn(2) * np.abs(np.random.normal(0, 1)) ** (-1 / self.alpha)
        )
        self.LevyPositions = np.append(
            self.LevyPositions, self.LevyPositions[len(self.LevyPositions) - 1] + step
        )
        self.calcFPS()

    def calcFPS(self):
        if (time.time() - self.start_time) > 1:
            self.fps = self.fps_iter / (time.time() - self.start_time)
            self.fps_iter = 0
            self.start_time = time.time()

    def getFPS(self) -> float:
        return int(self.fps)

    def getAlpha(self) -> float:
        return self.alpha

    def setAlpha(self, a: int) -> None:
        self.alpha = a

    def getStepSize(self) -> float:
        return self.stepSize

    def setStepSize(self, ss: int) -> None:
        self.stepSize = ss

    def getLevyPositions(self):
        return np.reshape(self.LevyPositions, (len(self.LevyPositions) // 2, 2))

    def clearLevyPositions(self):
        self.LevyPositions = np.array([(350, 350)])
