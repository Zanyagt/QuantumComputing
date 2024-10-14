%run quantum.py
from random import randrange
from math import pi, sin, cos
from matplotlib.pyplot import arrow
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, execute, Aer


class SingleQubit:
    def __init__(self, theta=None):
        self.__qc = QuantumCircuit(1, 1)
        self.__states_done = []
        self.__countStates = 0
        if theta is None or theta == 0:
            print('qubit was not rotated')
            self.__theta = randrange(360) * pi / 180
            print('angle theta created in radians:', self.__theta)
        else:
            self.__qc.ry(2 * theta, 0)
            self.__theta = theta
            print('qubit was rotated with angle', theta)

    def read_state(self):
        job = execute(self.__qc, Aer.get_backend('statevector_simulator'), optimization_level=0)
        self.__current_state = job.result().get_statevector(self.__qc).data
        for i in range(1):
            self.__states_done.append([])
            self.__states_done[self.__countStates].append(self.__current_state[0].real)
            self.__states_done[self.__countStates].append(self.__current_state[1].real)
        print()
        print('current quantum state:', '(', round(self.__current_state[0].real, 3), ',',
              round(self.__current_state[1].real, 3), ')')
        self.__countStates = self.__countStates + 1
        return self.__current_state, self.__states_done

    def rotation(self, angle_rot):
        self.__qc.ry(2 * angle_rot, 0)
        print('quibit rotated with angle=', angle_rot)

    def reflection(self, angle_ref=None):
        # line of reflection
        x_line = -1.109
        slope = sin(angle_ref) / cos(angle_ref)
        y_line = x_line * slope
        arrow(x_line, y_line, x_line * -2, y_line * -2, linestyle='dotted', color='red')
        # Reflection matrix
        R = [[cos(2 * angle_ref), sin(2 * angle_ref)], [sin(2 * angle_ref), -cos(2 * angle_ref)]]
        # Reflected state
        self.__reflected_state = [self.__current_state[0].real * R[0][0] + self.__current_state[1].real * R[0][1],
                                  self.__current_state[0].real * R[1][0] + self.__current_state[1].real * R[1][1]]
        print("reflected state :", self.__reflected_state)
        return self.__reflected_state

    def draw_state(self):
        draw_qubit()
        draw_quantum_state(self.__current_state[0].real, self.__current_state[1].real, "|u>")

    def draw_all_states(self):
        draw_qubit()
        for i in range(len(self.__states_done)):
            draw_quantum_state(self.__states_done[i][0], self.__states_done[i][1], "$|u_%i>$" % (i))

    def reflect_and_draw(self, angle_input=None):
        draw_qubit()
        draw_quantum_state(self.__current_state[0].real, self.__current_state[1].real, "|u>")
        self.reflection(angle_input)
        draw_quantum_state(self.__reflected_state[0], self.__reflected_state[1], "|u'>")

    def prob(self):
        prob_0 = (self.__states_done[self.__countStates - 1][0]) ** 2
        prob_1 = (self.__states_done[self.__countStates - 1][1]) ** 2
        print('The probability of observing state 0 is:', round(prob_0, 4))
        print('The probability of observing state 1 is:', round(prob_1, 4))

    def measure(self, number_of_shots):
        expect_0s = number_of_shots * (self.__states_done[self.__countStates - 1][0]) ** 2
        expect_1s = number_of_shots * (self.__states_done[self.__countStates - 1][1]) ** 2
        print('The expected number of 0s is:', round(expect_0s, 4))
        print('The expected number of 1s is:', round(expect_1s, 4))
